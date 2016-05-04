## Description

Goes through a list of repositories and prints a Markdown formatted changelog to STDOUT

## Setup

    git clone git@github.com:cbun/gh_changelog.git

    cp config.yml.template config.yml

    vi config.yml

Sample Config.yml file for us:

    organization: CancerIQ
    repositories:
      - CIQ
      - CIQ-Specialist
      - survey_service
      - SurveyClient
      - cas-server
    github_api_token: '123957897putgithubtokenhere'

You need to generate a Github token:

https://github.com/settings/tokens

For Select Scopes choose only "repo" scope.

    pip2.7 install pyyaml

    pip2.7 install pygithub

## Usage

    python generate.py --config MYCONFIG.yml BRANCH PRIOR_DATE_TO_COMPARE
    
e.g 

    python generate.py --config config.yml master 2016-02-05
    
or to compare between dates

    python generate.py --config config.yml master 2016-02-05 --latest-date 2016-03-05

