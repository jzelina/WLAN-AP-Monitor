echo "####### start ######" > /tmp/wmon_out
echo "generated: $(date)" >> /tmp/wmon_out
echo "host: $(hostname)" >> /tmp/wmon_out
echo "####### iw wlan0 info ######" >> /tmp/wmon_out
/usr/sbin/iw wlan0 info >> /tmp/wmon_out
echo "####### iw wlan0 station dump ######" >> /tmp/wmon_out
/usr/sbin/iw wlan0 station dump >> /tmp/wmon_out
echo "####### iw wlan0 survey dump ######" >> /tmp/wmon_out
/usr/sbin/iw wlan0 survey dump >> /tmp/wmon_out
echo "####### iw wlan1 info ######" >> /tmp/wmon_out
/usr/sbin/iw wlan1 info >> /tmp/wmon_out
echo "####### iw wlan1 station dump ######" >> /tmp/wmon_out
/usr/sbin/iw wlan1 station dump >> /tmp/wmon_out
echo "####### iw wlan2 info ######" >> /tmp/wmon_out
/usr/sbin/iw wlan2 info >> /tmp/wmon_out
echo "####### iw wlan2 station dump ######" >> /tmp/wmon_out
/usr/sbin/iw wlan2 station dump >> /tmp/wmon_out
echo "####### iw wlan3 info ######" >> /tmp/wmon_out
/usr/sbin/iw wlan3 info >> /tmp/wmon_out
echo "####### iw wlan3 station dump ######" >> /tmp/wmon_out
/usr/sbin/iw wlan3 station dump >> /tmp/wmon_out
