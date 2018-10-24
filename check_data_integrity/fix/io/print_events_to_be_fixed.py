def print_events_to_be_fixed(events_to_be_fixed, progress_printer, level):
    """
    Print events to be fixed.

    :param events_to_be_fixed: IDs of events that can be fixed
    :type events_to_be_fixed: list
    :param progress_printer: Object to print progress messages
    :type progress_printer: ProgressPrinter
    :param level: The level of indentation
    :type level: int
    """

    progress_printer.print_message("Media package", level)
    progress_printer.print_message("------------------------------------", level)
    for event in events_to_be_fixed:
        progress_printer.print_message(event, level)
    print()
