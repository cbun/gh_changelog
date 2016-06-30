## Description

Goes through a list of repositories and prints a Markdown formatted changelog to STDOUT

## Setup

You need to generate a Github token:

https://github.com/settings/tokens

### Install dependencies

    pip install -r requirements.txt
    
## Usage

    python generate.py --config MYCONFIG.yml BRANCH PRIOR_DATE_TO_COMPARE
    
e.g 

    python generate.py --config config.yml master 2016-02-05
    
or to compare between dates

    python generate.py --config config.yml master 2016-02-05 --latest-date 2016-03-05
