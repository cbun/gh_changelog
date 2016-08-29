## Description

Goes through a list of repositories and prints a Markdown formatted changelog to STDOUT

## Setup

```
git clone git@github.com:cbun/gh_changelog.git
```

You need to generate a Github token:

https://github.com/settings/tokens

### Create your configuration file

```
$ cd gh_changelog

$ cp config/config.yml.template myconfig.yml

$ vi myconfig.yml
```

### Install dependencies

    pip2.7 install -r requirements.txt
    
## Usage

    python2.7 generate.py --config MYCONFIG.yml BRANCH PRIOR_DATE_TO_COMPARE
    
e.g 

    python2.7 generate.py --config config.yml master 2016-02-05
    
or to compare between dates

    python2.7 generate.py --config config.yml master 2016-02-05 --latest-date 2016-03-05
