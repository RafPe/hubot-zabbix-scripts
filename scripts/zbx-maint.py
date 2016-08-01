#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import argparse
import json
import uuid

try:
    from zabbix_api import ZabbixAPI
    HAS_ZABBIX_API = True
except ImportError:
    HAS_ZABBIX_API = False


__author__ = 'RafPe'

parser = argparse.ArgumentParser(description='This is a demo script by RafPe.')
parser.add_argument('-u','--user', help='Zabbix user name',required=True)
parser.add_argument('-p','--password',help='Zabbix user password', required=True)
parser.add_argument('-t','--target',help='Zabbix target host/group', required=False)
parser.add_argument('-s','--server',help='Zabbix server', required=False)
parser.add_argument('-a','--action',help='Action to be taken', required=True)
parser.add_argument('-l','--length',help='Maintanance length', required=False)
parser.add_argument('-d','--desc',help='Maintanance description', required=False)
parser.add_argument('-r','--requestor',help='Maintanance requested by', required=False)
parser.add_argument('-i','--id',help='Maintanance uuid', required=False)
args = parser.parse_args()


def create_maintenance(zbx, group_ids, host_ids, start_time, maintenance_type, period, name, desc):
    end_time = start_time + period
    try:
        res = zbx.maintenance.create(
            {
                "groupids": group_ids,
                "hostids": host_ids,
                "name": name,
                "maintenance_type": maintenance_type,
                "active_since": str(start_time),
                "active_till": str(end_time),
                "description": desc,
                "timeperiods":  [{
                    "timeperiod_type": "0",
                    "start_date": str(start_time),
                    "period": str(period),
                }]
            }
        )
    except BaseException as e:
        print e
        return None

    referenceids = ', '.join(str(x) for x in res['maintenanceids'])

    print "Success! Created maintanance for %s groups/%s hosts with name *%s*" %(len(group_ids) if group_ids else "0", len(host_ids) if host_ids else "0" ,name )
    print "Reference IDs: *%s* "%referenceids

    return "So now :) go and have fun!"


def get_maintenance_id_by_id(zbx, name):
    try:
        result = zbx.maintenance.get(
            {
                "filter":
                {
                    "name": name
                }
            }
        )
    except BaseException as e:
        return None

    maintenance_ids = []

    for res in result:
        maintenance_ids.append(res["maintenanceid"])


    return maintenance_ids


def delete_maintenance(zbx, maintenance_id):
    try:
        zbx.maintenance.delete(maintenance_id)
        # print "nothing to watch here - would delete %s" % maintenance_id
        print "Maintanance %s has been deleted" % maintenance_id
    except BaseException as e:
        return None
    return "Done!"


def get_group_id(zbx, host_group):
    try:

        if '\"' in host_group:
            host_group = host_group.replace("\"","")

        result = zbx.hostgroup.get(
            {
                "output": "extend",
                "filter":
                {
                    "name": host_group
                }
            }
        )

    except BaseException as e:
        print "[ DEBUG ] Printing exception"
        print e
        return None

    if not result:
        return None

    return result[0]["groupid"]


def get_host_id(zbx, host_names):
    try:

        if '\"' in host_names:
            host_name = host_names.replace("\"","")

            result = zbx.host.get(
                {
                    "output": "extend",
                    "filter":
                    {
                        "name": host_name
                    }
                }
            )

    except BaseException as e:
        print "[ DEBUG ] Printing exception"
        print e
        return None

    if not result:
        return None

    return result[0]["hostid"]

def main():

    if not HAS_ZABBIX_API:
        print("Missing requried zabbix-api module ")

    # host_names          = args.target
    # host_groups         = args.target
    target              = args.target
    state               = args.action
    login_user          = args.user
    login_password      = args.password
    http_login_user     = args.user
    http_login_password = args.password
    requestor           = args.requestor
    minutes             = args.length
    _name_uuid          = uuid.uuid4()
    name                = "bender:%s" % _name_uuid
    if args.id is not None:
            name = args.id
    desc                = args.desc
    server_url          = args.server
    collect_data        = 1                         # Need to variableize this :)
    timeout             = 5


    # Havent yet created param for this
    if collect_data:
        maintenance_type = 0
    else:
        maintenance_type = 1

    try:
        zbx = ZabbixAPI(args.server, timeout=5, user=login_user, passwd=login_password)
        zbx.login(login_user, login_password)

    except BaseException:
        print("ERROR: Failed to connect to Zabbix server")


    if state == "set":

            now         = datetime.datetime.now()
            start_time  = time.mktime(now.timetuple())
            period      = 60 * int(args.length)  # N * 60 seconds

            # Defined our array for group IDs
            group_ids     = []
            host_ids      = []

            # Query for groups
            if ',' in target:
                for group in target.strip().split(","):
                    result = get_group_id(zbx, group)
                    if result:
                        group_ids.append(result)
            else:
                result = get_group_id(zbx, target)
                if result:
                    group_ids.append(result)

            # Query for hosts
            if ',' in target:
                for host in target.strip().split(","):
                    result = get_host_id(zbx, host)
                    if result:
                        host_ids.append(result)
            else:
                result = get_host_id(zbx, target)
                if result:
                    host_ids.append(result)

             ## info
            print("Helping out *@%s* to be quiet as ninja when working :) " % requestor)
            # print("host_names          = %s" % host_names)
            # print("host_groups         = %s" % host_groups)
            print("state               = %s" % state)
            # print("login_user          = %s" % http_login_user)
            # print("login_password      = %s" % args.password)
            # print("http_login_user     = %s" % http_login_user)
            # print("http_login_password = %s" % args.password)
            print("minutes             = %s" % minutes)
            print("name/id             = %s" % name)
            print("desc                = %s" % desc)
            # print("server_url          = %s" % server_url)
            print("collect_data        = %s" % collect_data)
            print("timeout             = %s" % timeout)
            print("requestor           = %s" % requestor)
            print("Found %s groups(s) / %s host(s) "% (len(group_ids),len(host_ids)) )


            # if host_groups:
            #     group_ids = get_group_ids(zbx, host_groups)
            #     if not group_ids:
            #         print("Groups: 0")
            # else:
            #     group_ids = []
            #
            # if host_names:
            #     host_ids = get_host_ids(zbx, host_names)
            #     if not host_ids:
            #         print("Hosts: 0")
            # else:
            #     host_ids = []
            #
            #
            #
            maintenance = get_maintenance_id_by_id(zbx, name)
            #
            if not maintenance:
                if not host_ids and not group_ids:
                    print("At least one host/host group must be defined/found to create maintenance.")
                    return

                outcome = create_maintenance(zbx, group_ids, host_ids, start_time, maintenance_type, period, name, desc)
                if not outcome:
                    print("Failed to create maintenance")
                else:
                    print outcome

            else:
                print "Maintanance already exists : %s" % maintenance

    elif state == "del":

            maintenance = get_maintenance_id_by_id(zbx, name)

            if not maintenance:
                print("No maintanance(s) have been found with name %s" % name )
                return
            else:
                delete_maintenance(zbx, maintenance)




    else:
        print "Not implemented in this version yet :/ "

if __name__ == '__main__':
    main()
