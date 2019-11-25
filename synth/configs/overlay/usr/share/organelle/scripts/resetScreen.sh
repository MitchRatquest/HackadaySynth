#!/bin/sh
#if ! screen -list | grep chamble >/dev/null #if you dont have a screen up named chamble
#then
	killall screen >/dev/null  #could be a dead screen session
	screen -dmS chamble >/dev/null
	oscsend 127.0.0.1 4000 /oled/aux/3 s "SUCCESSFULLY RESET THE SCREEN"
	oscsend 127.0.0.1 4000 /oled/setscreen i 1
#fi
exit 0
