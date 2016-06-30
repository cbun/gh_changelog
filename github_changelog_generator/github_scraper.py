import sys
import markdown as md
from github import Github

class GithubScraper():
    def __init__(self, api_token, organization_name):
        self.organization = Github(api_token).get_organization(organization_name)

    def compare_branch_between(self, repo_name, branch, date_str,
                               title=None, latest_date_str=None):
        repo = self.organization.get_repo(repo_name)
        try:
            old_branch = '{}@{{{}}}'.format(branch, date_str)
            if latest_date_str:
                target = '{}@{{{}}}'.format(branch, latest_date_str)
            else:
                target = branch
            compare_branches(repo, old_branch, target)
        except Exception as e:
            print e
            pass #Branch doesnt exist

def compare_branches(repo, base, target, title=None, trello_links=None):
    changes = repo.compare(base, target).commits
    if not title:
        title = '{} to {}'.format(base, target)
    if changes:
        print md.h4(title)
        print_commits(parse_commits(changes, trello_links))

def describe_pr(repo, pr_num):
    parse_commits(repo.get_pull(pr_num).get_commits())

def commit_type(commit):
    tag_map = {
        'b': 'BUGFIX',
        'u': 'UI',
        'r': 'REFACTOR',
        'f': 'FEATURE',
        'p': 'PRODUCTION'
    }
    try:
        msg = commit.commit.message
        tag_bracket = msg[msg.find("{")+1:msg.find("}")][0].lower()
        return tag_map.get(tag)
    except:
        print "Could not get commit type: {}".format(commit)

def parse_commits(commits_list, trello_links=None):

    def is_true_commit(commit):
        return commit.commit.message[:5] != 'Merge'

    def filter_message(msg):
        return '\n'.join([l.encode('utf-8') for l in msg.split('\n')
                          if len(l) > 0 and l[0] != '#'])

    commits_data = []
    for commit in filter(is_true_commit, commits_list):
        commit_info = {'obj': commit.commit}
        commit_info['commit_type'] = commit_type(commit)
        commit_info['message'] = filter_message(commit.commit.message)
        commit_info['git_url'] = commit_info['obj'].html_url
        if trello_links:
            commit_info['trello_url'] = trello_links.get(find_tag(commit_info['message']))
        commits_data.append(commit_info)
    return commits_data

def print_commits(commits_data):
    sections = [
        {'commit_type': 'FEATURE', 'section_title': 'New Features' },
        {'commit_type': 'BUGFIX', 'section_title': 'Bugfixes' },
        {'commit_type': 'REFACTOR', 'section_title': 'Code Refactor' },
        {'commit_type': 'PRODUCTION', 'section_title': 'Production Support' },
        {'commit_type': 'UI', 'section_title': 'User Interface' },
        {'commit_type': None, 'section_title': 'Unlabeled' },
    ]

    def is_valid_section_member(commit_info, section):
        return commit_info['commit_type'] == section['commit_type'] and commit['message']

    def format_commits(commits, title, trello_links=None):
        if commits:
            print '\n**{}**\n'.format(title)
            for commit in commits:
                msg = '- {}'.format(commit['message']).strip()
                if commit.get('trello_url'):
                    msg += ' ' + md_link('[Trello]', commit['trello_url'])
                msg += md.link(' [git-{}]'.format(commit['obj'].sha[:6]), commit['git_url'])
                print msg
            print '\n'

    for section in sections:
        section_commits = [commit for commit in commits_data
                           if is_valid_section_member(commit, section)]
        format_commits(section_commits, section['section_title'])
