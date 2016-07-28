# Description:
#   Generates help commands for Hubot.
#
# Commands:
#   bender zbx-maint set <host_group>,<host> <minutes> <description>
#   bender zbx-maint del <maintenance_uuid>
#
# URLS:
#   /hubot/help
#
# Configuration:
#   HUBOT_HELP_REPLY_IN_PRIVATE
#
# Notes:
#   These commands are grabbed from comment blocks at the top of each file.

zbxUsername   = process.env.HUBOT_ZBX_USER
zbxPassword   = process.env.HUBOT_ZBX_PW
zbxUrl        = process.env.HUBOT_ZBX_URL
zbxscriptpath = process.env.HUBOT_ZBX_PYMAINT


module.exports = (robot) ->
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
