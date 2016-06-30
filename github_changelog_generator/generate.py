#! /usr/bin/env python
from cStringIO import StringIO
import sys
import argparse
import os
import yaml
import markdown as md
import markdown2
from github_scraper import GithubScraper

parser = argparse.ArgumentParser(prog='generate_changelog',
                                 epilog='Use "generate_changelog command -h" for more information about a command.')
parser.add_argument('-c', '--config', action='store', required=True)
parser.add_argument('branch', type=str, action='store')
parser.add_argument('last_date', type=str, action='store')
parser.add_argument('-l', '--latest-date', action='store')
parser.add_argument('-o', '--output', action='store')
parser.add_argument('-H', '--html', action='store')

args = parser.parse_args()
config_yml = yaml.load(file(args.config, 'r'))

# Hack to redirect output to file
if args.output:
    with open(args.output, 'w') as outfile:
        sys.stdout = outfile
if args.html:
    # Capture prints to string
    old_stdout = sys.stdout
    sys.stdout = md_string = StringIO()

gh_client = GithubScraper(config_yml['github_api_token'], config_yml['organization'])
repos = config_yml['repositories']
for repo in repos:
    print md.h1(repo)
    gh_client.compare_branch_between(repo, args.branch,
                                     args.last_date,
                                     latest_date_str=args.latest_date)

if args.html:
    sys.stdout = old_stdout
    print 'Creating html file'
    with open(args.html, 'w') as htmlfile:
        htmlfile.write(markdown2.markdown(md_string.getvalue()))
