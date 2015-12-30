#!/usr/bin/python

"""
Title: WLAN-AP-Monitor
----------------------
WLAN Access Point Monitor - poll information script

About:
------
This program connects to single or multiple WLAN Access Point(s) by SSH.
Once connected instructions to download AP status information are executed
and the collected result is received by this tool.

The result is written to an output file per AP, or a common file.

For more information read the readme.txt
or see: https://github.com/jzelina/WLAN-AP-Monitor
"""
__author__ = "jzelina"
__license__ = "GPL"
__version__ = "0.1"

#requirements

import paramiko
import time
import select
from ConfigParser import SafeConfigParser

#enable debug
debug = False

############################
#function
def echo_debug(text,debug):
    if debug == True:
        print(text)

############################

#title
echo_debug("\nWelcome to WLAN AP Monitor - poll script\n------------------------",debug)

#configure environment
scan_result={}

#import configuration (or ask for cli input)
echo_debug("import configuration",debug)
config = SafeConfigParser()
config.read('config/config.cfg')

#config file values
debug = bool(int(config.get('config', 'debug')))
config_agentfile = str.strip((config.get('config', 'agentfile')))
ip = str.strip((config.get('config', 'ip')))
port = int(config.get('config', 'port'))
username = str(config.get('config', 'username'))
password = str(config.get('config', 'password'))
outdir = str.strip((config.get('config', 'outdir')))

#check for 2nd login (su)
try:
    if config.get('config', 'su_username') and config.get('config', 'su_password'):
        echo_debug("SU: user + password configured",debug)
        su = True
        su_username = str(config.get('config', 'su_username'))
        su_password = str(config.get('config', 'su_password'))    
except:
    echo_debug("SU: no second login defined",debug)
    su = False

try:
    if config.get('config', 'su_postlogin'):
        echo_debug("SU: post login script configured",debug)
        su_postlogin = True
        su_postscript = str(config.get('config', 'su_postlogin')) 
except:
    echo_debug("SU: no post login defined",debug)
    su_postlogin = False

#########
# start #
#########

echo_debug("begin poll per access point",debug)

#get IP / IP range and poll per target
targets = []
if "-" in ip:
    #split ip range into list
    tmp_target = ip.split('.')
    tmp_range = tmp_target[3].split('-')
    for i in range(int(tmp_range[0]),int(tmp_range[1])+1):
        targets.append(str(tmp_target[0] + '.' + tmp_target[1] + '.' + tmp_target[2] + '.' + str(i)))
    echo_debug("Number of targets: " + str(len(targets)),debug)
else:  
    targets.append(ip)

#for each IP in list
for ip in targets:

    if __name__ == "__main__":
      
        echo_debug("connect to AP: " + ip,debug)
        result = []
        
        try:  
            ### configure ssh client
            paramiko.util.log_to_file('log/paramiko_' + ip +'.log')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, username, password, timeout=2)
                    
            #2nd level login (su, sudo)
            if su == True:
                echo_debug("login to root (2nd level)",debug)
                
                stdin, stdout, stderr = ssh.exec_command('help', get_pty=False)
                stdin.write('su ' + su_username + '\n')
                stdin.flush()
                stdin.write(su_password + '\n')
                stdin.flush()
                time.sleep(1)
            
            # pre process script - TODO
    
            # upload instructions to target
            echo_debug("upload instructions to " + ip,debug)
            
            f = open(config_agentfile)
            line = f.readline()
            
            while line:
                
                stdin, stdout, stderr = ssh.exec_command( line, get_pty=True)
                exit_status = stdout.channel.recv_exit_status()
                line = f.readline()
            f.close()  
            
            # download result
            echo_debug("download result on " + ip,debug)
            
            stdin, stdout, stderr = ssh.exec_command("cat /tmp/wmon_out", get_pty=False)
                    
            while not stdout.channel.exit_status_ready():
                # Only print data if there is data to read in the channel
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    if len(rl) > 0:
                        # Print data from stdout
                        result.append(stdout.channel.recv(1024))
            
            #remove output file
            stdin, stdout, stderr = ssh.exec_command("rm /tmp/wmon_out", get_pty=False)
            
            #close connection
            echo_debug("close ssh connection with " + ip,debug)
            ssh.close()
            
            #store result
            #todo: check if result is empty
            echo_debug(result,debug)
            
            result = ''.join(result)
            scan_result[ip] = result
            target = open(outdir + '/out_' + ip, 'w')
            target.write(result)
            target.close()
            
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % ip
        except:
            print "ERROR could not connect to " + ip

echo_debug("Poll completed " + "(" + str(len(scan_result)) + " of " + str(len(targets)) + " successful)",debug)
##########################

#print scan_result
target = open(outdir + '/scan_' + str(int(time.time())), 'w')
for item in scan_result:
  target.write("%s\n" % '###IP###' + item + '\n')
  target.write("%s\n" % scan_result[item])
target.close()
