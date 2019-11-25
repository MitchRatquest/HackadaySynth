#!/bin/sh

getd () {
        USER=raul
        SERVER=192.168.100.2
        MOUNTPOINT=/home/raul/projects/
        rsync -avP $USER@$SERVER:$MOUNTPOINT/$1/ ./$1
}
getf () {
        USER=raul
        SERVER=192.168.100.2
        MOUNTPOINT=/home/raul/projects/
        rsync -avP $USER@$SERVER:$MOUNTPOINT/$1 ./$1
}

xferd () {
        USER=raul
        SERVER=192.168.100.2
        MOUNTPOINT=/home/raul/projects/SYNTHINPROGRESS
        rsync -avP $1/ $USER@$SERVER:$MOUNTPOINT/$1/ 
}
xferf () {
        USER=raul
        SERVER=192.168.100.2
        MOUNTPOINT=/home/raul/projects/SYNTHINPROGRESS
        rsync -avP $1 $USER@$SERVER:$MOUNTPOINT/$1 
}
if ! screen -list | grep chamble
then
	screen -dmS chamble
fi

