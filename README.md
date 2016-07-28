# Hubot Zabbix maintanance script
This scripts provide functionality to use zabbix maintanance directly from your Slack/Rocket chat

![s](https://github.com/RafPe/hubot-zabbix-scripts/blob/master/screenshots/hubot_zbx_maint_v1.png?raw=true)

## Info:
This is running already in production solution. It has been tested however I believe it can always be made better.For sure certain things can be done better - if you find thos - let me know

## Implemented actions
The basic actions implemented by the scrip include creation and deletion of maintanance on zabbix server

### Creating:
```shell
@bender zbx-maint set host-01.dummy,host-02.dummy 1 SomeCommentXYZ
```
In return you will receive information which will contain the following:
```shell
Success! Created maintanance for 0 groups/1 hosts with name bender:d7b29a45-f94c-46e6-8008-e8f9b1434f5a
Reference IDs: *1842*
So now 🙂 go and have fun!
```

### Deleting:
Deleting is easy as providing ID from the results we have received creating maintanance
```shell
@bender zbx-maint del name:uuid
```

## Requirements:
In order to run properly the script you will need to zabbix api installed

```shell
pip install zabbix-api
```

Make sure your python does support **argparse** as that is being used to parse input for python script


## Installing and configuring:
Installing is easy as having 2 scripts in your hubot scripts folder. Those scripts are:
* zbx-maint.py
* zbx-maint.coffee

Once this is done set the following environment variables
```shell
HUBOT_ZBX_USER      : user accessing zabbix
HUBOT_ZBX_PW        : password for the user
HUBOT_ZBX_URL       : zabbix server URL
HUBOT_ZBX_PYMAINT   : full path to zbx-maint.py script (used by coffee script)
```

## Usage from command line
The whole functionality is hidden behind python script which is side by side to coffee script in hubots' script folder.

```shell

python zbx-maint.py

usage: zbx-maint.py [-h] -u USER -p PASSWORD [-t TARGET] [-s SERVER] -a ACTION
                    [-l LENGTH] [-d DESC] [-r REQUESTOR] [-i ID]

 -u USER      : used to connect to zabbix - needs perm to create/delete maintanance
 -p PASSWORD  : password for the user above
 -t TARGET    : host/groups to create maintanance on
 -s SERVER    : URL of the zabbix server
 -a ACTION    : del or set
 -l LENGTH    : Number of minutes to have maintanance for
 -d DESC      : Additonal description added to maintanance
 -r REQUESTOR : Used to pass who has requested action
 -i ID        : Name of maintanance - used for deletion
```

## Thanks for help and code goes to:
* [sanderv32](https://github.com/sanderv32) for mentoring and patience :)
* Alexander Bulimov <lazywolf0@gmail.com> for original work on Ansible python module
