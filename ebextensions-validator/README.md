# ebextensions-validator

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
  - [Command line tool](#command-line-tool)
  - [Python package](#python-package)
- [Validation rule](#validation-rule)
- [allowlist format](#allowlist-format)
  - [.ebextensions-like YAML files with Regex](#ebextensions-like-yaml-files-with-regex)
  - [Non-.ebextensions YAML files with Regex](#non-ebextensions-yaml-files-with-regex)
- [Examples](#examples)
  - [allowlist all](#allowlist-all)
  - [Empty file](#empty-file)
- [Tips and Remarks](#tips-and-remarks)

## About

ebextensions-validator is a tool which validates ebextensions configuration files against a provided allowlist.  
See https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions.html for more information on the .ebextensions file format.  
Currently only YAML configuration files are supported.

## Installation

ebextensions-validator can be installed using pip:

```
git clone <URL_TO_EBEXTENSIONS_VALIDATOR> ebextensions-validator
pip install ./ebextenstions-validator
```

## Usage

ebextensions-validator is both a command line tool and a python library.  
Note that the command line tool is spelled `ebextensions-validator` with a hyphen, while the python package is `ebextensions_validator` with an underscore.

### Command line tool

```
usage: ebextensions-validator [-h] [-v] config_file allowlist_file

Validate a config file from the .ebextensions directory against a allowlist of dictionaries

positional arguments:
  config_file     Config file from .ebextensions directory
  allowlist_file  File which defines a allowlist of dictionaries. Regex can be
                  used

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   Print information about not allowlisted configuration
```

ebextensions-validator parses the provided `config_file` and `allowlist_file`. It then validates the `config_file` against the `allowlist_file`

Examples:

* Validating a config file against a allowlist *successfully*:
```
ebextensions-validator path/to/.ebextensions/config_file.config path/to/allowlist.list
Configuration is in allowlist
```
* Validating a config file against a allowlist *unsuccessfully*:
```
ebextensions-validator path/to/.ebextensions/config_file.config path/to/allowlist.list
Configuration NOT in allowlist
```

* Validating a config file against a allowlist *unsuccessfully* with the *verbose* option:
```
ebextensions-validator path/to/.ebextensions/config_file.config path/to/allowlist.list -v
* Dictionary ODict([('command1', ODict([('command', 'git commit -am "Comment"'), ('cwd', '/home/user/working/')]))]) is not in allowlist
* Dictionary ODict([('command2', ODict([('command', 'ls'), ('cwd', '/home/user/working/')]))]) is not in allowlist
Configuration NOT in allowlist
```

### Python package

To use ebextensions-validator from your own python projects, import the function `validate`:

```
from ebextensions_validator.validator import validate

"""
The function expects the path to a configuration file in yaml and the path to a allowlist file as described below.
It returns True if the configuration is in the allowlist.
It return False if the configuration is not in the allowlist.
"""

if validate("path/to/.ebextensions/config_file.config", "path/to/allowlist.list"):
    push_application_code()
else:
    print("Configuration File not valid.")
    return
```

## Validation rule

Each dictionary in the validated configuration file must match a dictionary in the provided allowlist file. See the following section for some examples.

## allowlist format

allowlists are defined as YAML files.  
Python-style regular expressions can be used in the allowlist files as well: Any key or value in the allowlist can be replaced by a regular expression. For more information on regular expressions in Python see https://docs.python.org/3/library/re.html  
**Note**: Regular expressions cannot be used in the
* top level of the allowlist and
* second level of the allowlist if the first level is `services`.  

See the "allowlist all" example below.

### .ebextensions-like YAML files with Regex

.ebextensions configuration files (with regular expressions in the keys and values) can be used as allowlists.

Let's see this example:
```
commands:
  .*:
    command: 'git commit .*'
```

This allowlist allows following configuration files:

```
commands:
  any_command_name:
    command: git commit -m "Any comment."
```

```
commands:
  another_command_name:
    command:
      - git
      - commit
      - -m
      - This is another comment.
```
```
commands:
  command_name_2:
    command: |
      git commit -m "This is a comment."
      git push
```

Since the linebreak and `git push` are all part of the `command` value, the `git commit .*`  matches the whole block.


Another example:
```
option_settings:
  - namespace:  aws:elasticbeanstalk:container:tomcat:jvmoptions
    option_name:  Xmx
    value:  "[0-9]*m"
  - option_name: MYPARAMETER
    value: parametervalue
```

This allowlist allows following configuration files (see https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions-optionsettings.html)

```
option_settings:
  - namespace:  aws:elasticbeanstalk:container:tomcat:jvmoptions
    option_name:  Xmx
    value:  256m
```
```
option_settings:
  aws:elasticbeanstalk:container:tomcat:jvmoptions:
    Xmx: 256m
  aws:elasticbeanstalk:application:environment:
    MYPARAMETER: parametervalue
```

### Non-.ebextensions YAML files with Regex

Sometimes it is necessary to allow multiple different sets of configurations. Therefore, you can create a *list* *of dictionaries* in the allowlist.  
For example you want to allowlist multiple different command definitions:

```
commands:
  - .*:
    command: 'git commit -m .*$'
    cwd: /home/user/.*
  - .*:
    command: 'ls'
    cwd: /etc/.*
```

This allowlist allows following configuration files:

```
commands:
  git_in_working:
    command: 'git commit -m "This is a comment"'
    cwd: /home/user/working/
  - ls_etc:
    command: 'ls'
    cwd: /etc/
```
```
commands:
  git_in_working:
    command: 'git commit -m "This is a comment"'
    cwd: /home/user/working/
```
```
commands:
  ls_etc:
    command: 'ls'
    cwd: /etc/
```

The allowlist does ***not*** allow the following configuration file:

```
commands:
  git_in_working:
    command: 'git commit -m "This is a comment"'
    cwd: /home/user/working/
  ls_etc:
    command: 'ls'
    cwd: /home/user/working/
```

The dictionary `ls_etc` is not in any of the list of dictionaries in the allowlist under `commands`

## Examples

See the files in `test_files/allowlist_files` for more examples.

### allowlist all
This allowlist allows any valid .ebextensions configuration file
```
option_settings:
  .*
packages:
  .*
groups:
  .*
users:
  .*
sources:
  .*
files:
  .*
commands:
  .*
services:
  sysvinit:
    .*
container_commands:
  .*
Resources:
  .*
Outputs:
  .*
```

### Empty file
If you specify an empty file as allowlist, the validation will always return a non-valid configuration.

## Tips and Remarks

* Be careful with wildcards! The following allowlist allows commands such as `git commit -m "Any comment." & execute_another_command`
```
commands:
  .*:
    command: 'git commit .*$'
```

This allowlist is better:

```
commands:
  .*:
    command: 'git commit ".*"$'
```
