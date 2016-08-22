# hubot-zabbix-maintanance

Hubot script allowing to create/delete zabbix maintanance

## Requirements:
In order to run properly the script you will need to zabbix api installed

```shell
pip install zabbix-api
```

Make sure your python does support **argparse** as that is being used to parse input for python script


## Installing and configuring:

### With npm
In hubot project repo, run:

`npm install hubot-zabbix-maintanance --save`

Then add **hubot-zabbix-maintanance** to your `external-scripts.json`:

```json
[
  "hubot-zabbix-maintanance"
]
```

### Manually
Installing is easy as having 2 scripts in your hubot scripts folder. Those scripts are:
* zbx-maint.py
* zbx-maint.coffee
You can get them directly from git repo.


Once this is done set the following environment variables
```shell
HUBOT_ZBX_USER      : user accessing zabbix
HUBOT_ZBX_PW        : password for the user
HUBOT_ZBX_URL       : zabbix server URL
```

## Sample Interaction

### Creating:
```shell
user1>> @bender zbx-maint set host-01.dummy,host-02.dummy 1 SomeCommentXYZ
hubot>>
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
user1>>@bender zbx-maint del name:uuid
```


## NPM Module

https://www.npmjs.com/package/hubot-zabbix-maintanance


## Thanks for help and code goes to:
* [sanderv32](https://github.com/sanderv32) for mentoring and patience :)
* Alexander Bulimov <lazywolf0@gmail.com> for original work on Ansible python module

## Future development
Planned to include listing of maintanance being active / scheduling
