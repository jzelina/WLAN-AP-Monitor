Title: WLAN-AP-Monitor
----------------------
WLAN Access Point Monitor - poll information script

URL:
---- 
https://github.com/jzelina/WLAN-AP-Monitor

About:
------
This program connects to single or multiple WLAN Access Point(s) by SSH.
Once connected instructions to download AP status information are executed
and the collected result is received by this tool.

The result is written to an output file.

Access Points requirement:
--------------------------
This tool match to linux based AP's providing SSH access.
Sample scripts are matching with hostapd environments.

Requirements:
-------------
- python
-- paramiko (sudo pip install paramiko)

Configuration: (config/)
--------------
config.cfg: 	general settings
wmon_agent.sh:	instruction to execute on AP 

Usage:
----------
python wlanmon.py 
(or sh start_poll.sh)

License:
--------
GPL
