#!/usr/bin/env python3

from fix.fixer.series_dc_of_event_fixer import SeriesDCOfEventFixer
from fix.io.input import FixAnswer, fix_question
from fix.io.parse_args import parse_args
from fix.io.results_parser import ResultsParser
from shared.args.url_builder import URLBuilder
from shared.rest_requests.request_error import RequestError
from shared.util.progress_printer import ProgressPrinter
from fix.io.log_writer import LogWriter


def __filter_tenants(chosen_tenants, excluded_tenants, tenants_in_results, progress_printer):
    """
    Filter tenants by either excluding or choosing them (both is not possible).

    :param chosen_tenants: The chosen tenants
    :type chosen_tenants: list
    :param excluded_tenants: The excluded tenants
    :type excluded_tenants: list
    :param tenants_in_results: The tenants for which results exist
    :type tenants_in_results: list
    :param progress_printer: The progress printer
    :type progress_printer: ProgressPrinter
    :return: A sorted list with tenants to fix
    :rtype list:
    """
    if not chosen_tenants and not excluded_tenants:
        # get tenants
        tenants = tenants_in_results
        progress_printer.print_message("{} tenant(s) were found in results: {}\n"
                                       .format(len(tenants), ", ".join(tenants)))

    elif chosen_tenants:
        tenants = [tenant for tenant in chosen_tenants if tenant in tenants_in_results]
        tenants_not_found = [tenant for tenant in chosen_tenants if tenant not in tenants_in_results]
        if tenants_not_found:
            progress_printer.print_message("{} tenant(s) were chosen, but {} of those were not found in the results,"
                                           " {} remain: {}\n"
                                           .format(len(chosen_tenants), len(tenants_not_found), len(tenants),
                                                   ", ".join(tenants)))
        else:
            progress_printer.print_message("{} tenant(s) were chosen: {}\n".format(len(tenants), ", ".join(tenants)))

    elif excluded_tenants:
        tenants = [tenant for tenant in tenants_in_results if tenant not in excluded_tenants]
        progress_printer.print_message("{} tenant(s) were found in results, {} remain after filtering: {}\n"
                                       .format(len(tenants_in_results), len(tenants), ", ".join(tenants)))
    else:
        raise ValueError("chosen_tenants and excluded_tenants can't be both defined")

    tenants.sort()
    return tenants


def main():
    """
    Iterate over each tenant, each fixer, each error that fixer can fix, each event belonging to that event with that
    error and fix them if possible, log results.
    """

    # parse args
    opencast, https, chosen_tenants, excluded_tenants, digest_login, waiting_period, batch_size, silent, \
    no_fancy_output, results_dir = parse_args()

    url_builder = URLBuilder(opencast, https)
    progress_printer = ProgressPrinter(silent, no_fancy_output)
    log_writer = LogWriter()

    try:
        # parse results
        progress_printer.print_message("Parsing results... ", 0, False, True)
        results_parser = ResultsParser(results_dir)
        progress_printer.print_message("finished.\n", 0, True, False)

        # which tenants to fix?
        tenants_in_results = results_parser.get_tenants()
        tenants = __filter_tenants(chosen_tenants, excluded_tenants, tenants_in_results, progress_printer)

        fixers = [SeriesDCOfEventFixer()]  # TODO make choosable once more errors can be fixed
        state = FixAnswer.NEXT
        workflows_started = 0

        for tenant in tenants:

            progress_printer.print_message("Starting with tenant {}...\n".format(tenant), 0)
            base_url = url_builder.get_base_url(tenant)

            for fixer in fixers:

                errors = fixer.get_errors()

                for error in errors:

                    if state == FixAnswer.SKIP or state == FixAnswer.REST:
                        state = FixAnswer.NEXT

                    # get events
                    progress_printer.print_message("Looking for {}...".format(error), 1, False, True)
                    events_to_be_fixed = results_parser.get_events_with_error(tenant, error)
                    progress_printer.print_message(" {} found.\n".format(len(events_to_be_fixed)), 1, True, False)

                    if len(events_to_be_fixed) == 0:
                        continue

                    fixed_events = 0

                    for event_id in events_to_be_fixed:

                        # wait?
                        if waiting_period != 0 and workflows_started != 0 and workflows_started % batch_size == 0:
                            progress_printer.print_time(waiting_period,
                                                        "Waiting for {} second(s) to not overflow the system...")

                        try:
                            # fix?
                            if state == FixAnswer.NEXT:
                                state = fix_question(no_fancy_output, 2)
                                progress_printer.print_empty_line()

                                if state == FixAnswer.SKIP:
                                    break
                                elif state == FixAnswer.QUIT:
                                    progress_printer.print_message("...aborted.")
                                    return

                            # fix
                            progress_printer.print_message("Fixing event {}... ".format(event_id), 2, False, True)
                            fixer.fix(base_url, digest_login, event_id)
                            log_writer.write_to_log(event_id, tenant, error, fixer.get_fix_description())
                            progress_printer.print_message("fixed.\n", 2, True, False)
                            fixed_events = fixed_events + 1
                            workflows_started = workflows_started + 1

                        except RequestError as e:
                            progress_printer.print_message("could not be fixed: {}\n".format(e.error), 2, True, False)
                            log_writer.write_to_log(event_id, tenant, error, "could not be fixed: {}".format(e.error))

                    progress_printer.print_message("{} of {} {} fixed for tenant {}.\n"
                                                   .format(fixed_events, len(events_to_be_fixed), error, tenant), 1)

            progress_printer.print_message("...finished.\n".format(tenant))

    finally:
        log_writer.close_log()


if __name__ == '__main__':
    main()
