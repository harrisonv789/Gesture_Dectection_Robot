#!/bin/sh

### BEGIN INIT INFO
# Provides:          start.sh
# Required-Start:    $network $local_fs $remote_fs $syslog
# Required-Stop:     $local_fs $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Starts the initial scripts
# Descriptipon:      Enable service provided by daemon
### END INIT INFO

# Start the initial script after some time
sleep 10s
. /home/pi/Desktop/Sign_Language_Neural/sh/pi.sh &
