#!/bin/sh
#mutes kt0803 using the standby bit
#and the power amplifier power down bit
i2cset -y 0 0x3e 0x0b 0xa0
