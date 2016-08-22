# Description
#   Hubot script allowing to create/delete zabbix maintanance
#
# Configuration:
#   LIST_OF_ENV_VARS_TO_SET
#
# Commands:
#   bender zbx-maint set <host_group>,<host> <minutes> <description>
#   bender zbx-maint del <maintenance_uuid>#
#
# Configuration:
#   HUBOT_ZBX_USER
#   HUBOT_ZBX_PW
#   HUBOT_ZBX_URL
#
# Notes:
#   <optional notes required for the script>
#
# Author:
#   RafPe <rafal@pieniazek.nl>

zbxUsername   = process.env.HUBOT_ZBX_USER
zbxPassword   = process.env.HUBOT_ZBX_PW
zbxUrl        = process.env.HUBOT_ZBX_URL



module.exports = (robot) ->

  zbxscriptpath = __dirname

  robot.respond /zbx-maint\s(set)\s(["]?\w.*)\s(\d+)\s(["]?\w.*)/i, (msg) ->

    zbxhostgroup  = msg.match[2]
    zbxlength     = msg.match[3]
    zbxaction     = msg.match[1]
    zbxdesc       = "Created by #{msg.message.user.name} : " + msg.match[4]

    data = ''
    spawn = require('child_process').spawn
    proc = spawn 'python', ['-u', "#{zbxscriptpath}", "-d#{zbxdesc}","-u#{zbxUsername}","-r#{msg.message.user.name}","-t#{zbxhostgroup}","-l#{zbxlength}","-a#{zbxaction}","-p#{zbxPassword}","-s#{zbxUrl}"]
    me = this
    proc.stdout.on 'data', (chunk) ->
      data += chunk.toString()
    proc.stderr.on 'data', (chunk) ->
      msg.send chunk.toString()
    proc.stdout.on 'end', () ->
      msg.send data.toString()

  robot.respond /zbx-maint\s(del)\s(.*)/i, (msg) ->

    zbxuuid      = msg.match[2]
    zbxaction    = msg.match[1]
    zbxdesc      = "n/a"

    data = ''
    spawn = require('child_process').spawn
    proc = spawn 'python', ['-u', "#{zbxscriptpath}","-u#{zbxUsername}","-r#{msg.message.user.name}","-a#{zbxaction}","-p#{zbxPassword}","-i#{zbxuuid}","-s#{zbxUrl}"]
    me = this
    proc.stdout.on 'data', (chunk) ->
      data += chunk.toString()
    proc.stderr.on 'data', (chunk) ->
      msg.send chunk.toString()
    proc.stdout.on 'end', () ->
      msg.send data.toString()

