import re


def __normal_pretty_print(title, pr_number, pr_link, legacy):
    legacy_str = '\\*' if legacy else ''
    title = __pretty_print_title(title, legacy_str)
    print('- [[#%s](%s)] -\n  %s' % (pr_number, pr_link, title))


def __bot_pretty_print(title, pr_number, pr_link, legacy):
    legacy_str = '*' if legacy else ''
    title = __pretty_print_title(title, legacy_str)
    print('<li>[<a href="%s">%s</a>] - \n  %s</li>' % (pr_link, pr_number, title))


def __pretty_print_title(title, legacy_str):
    return re.sub(r'^\S*[mM][hH]-\d{3,5}[,: ]*', '', title) + legacy_str


def filter_and_sort_prs(pull_requests):
    # filter by type
    normal_pull_requests = [pr for pr in pull_requests if pr.get('user').get('type') != 'Bot']
    bot_pull_requests = [pr for pr in pull_requests if pr.get('user').get('type') == 'Bot']

    # sort by merged date
    normal_pull_requests.sort(key=lambda p: p.get('merged_date'), reverse=True)
    bot_pull_requests.sort(key=lambda p: p.get('merged_date'), reverse=True)
    return normal_pull_requests, bot_pull_requests


def print_pull_requests(normal_pull_requests, bot_pull_requests):
    # print results
    for pr in normal_pull_requests:
        __normal_pretty_print(pr.get('title').strip(), pr.get('number'), pr.get('html_url'), pr.get('legacy'))

    if len(bot_pull_requests) > 0:
        print('<details><summary>Dependency updates</summary>\n')
        print('<ul>')
        for bot_pr in bot_pull_requests:
            __bot_pretty_print(bot_pr.get('title').strip(), bot_pr.get('number'), bot_pr.get('html_url'),
                               bot_pr.get('legacy'))
        print('</ul>')
        print('</details>')
