#!/bin/sh
###########################################################
#
# update oct 27
# kt0803l clicks hideously when it changes stations
# makes sense but is annoying, might mute, switch, unmute
#
# this script just focuses on changing the frequency
#
###########################################################

I2C_BUS=0
I2C_ADDRESS=0X3E
FREQ=$1
FREQ_MIN=70000
FREQ_MAX=108000

#computes frequency from human readable to MHz
FREQ=$(echo "$FREQ * 1000" | bc | awk -F'.' '{print $1}')
#echo $FREQ

if [ "$FREQ" -gt $(($FREQ_MIN-1)) -a "$FREQ" -lt $(($FREQ_MAX+1)) ]
    then
# Divide desired frequency by 50
   FREQ_WORD=$(($FREQ/50))
# Split off bits 11 to 9 and store
   FREQ_REG_01=`printf "%x\n" $(echo "$FREQ_WORD/512" | bc)`
# Store bits 8 to 0
   FREQ_REG_00=$((FREQ_WORD-($FREQ_REG_01*512)))
# Strip off bit 1 to 7 and store
   FREQ_REG_02=$(($FREQ_REG_00 & 0x01))
# Shift bit to bit position 7
   FREQ_REG_02=$(($FREQ_REG_02 << 7))
# Convert registers to 2 characters
   FREQ_REG_00=`printf "%02x\n" $(echo "$FREQ_REG_00/2" | bc)`
   FREQ_REG_01=`printf "%02x\n" $FREQ_REG_01`
   FREQ_REG_02=`printf "%x\n" $FREQ_REG_02`
# Read registers' current values
# Register 0x02
   READ_REG_01=`i2cget -y $I2C_BUS $I2C_ADDRESS 0x01`
# Register 0x00 
#    No need to read register 0x00, all 8 bits to be written
   READ_REG_00=`i2cget -y $I2C_BUS $I2C_ADDRESS 0x00`
# Register 0x02
   READ_REG_02=`i2cget -y $I2C_BUS $I2C_ADDRESS 0x02`
# Clear bits to be changed,
# store new value 
# and format to two characters to prevent dropping leading zeros
# Register 0x01
   WRITE_REG_01=$((0xf8 & $READ_REG_01))
   WRITE_REG_01=$(($WRITE_REG_01 | $FREQ_REG_01))
   WRITE_REG_01=`printf "%02x\n" $WRITE_REG_01`
# Register 0x00
   WRITE_REG_00=$FREQ_REG_00
# Register 0x02
   WRITE_REG_02=$((0x7f & $READ_REG_02))
   WRITE_REG_02=$(($WRITE_REG_02 | $FREQ_REG_02))
   i2cset -y $I2C_BUS $I2C_ADDRESS 0x01 0x$WRITE_REG_01
   i2cset -y $I2C_BUS $I2C_ADDRESS 0x00 0x$WRITE_REG_00
   i2cset -y $I2C_BUS $I2C_ADDRESS 0x02 0x$WRITE_REG_02
    else
# Invalid or no value set
        echo Frequency value not set or invalid - skipping
fi

