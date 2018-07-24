#!/bin/bash
INCOLOUR="#FF0000"
OUTCOLOUR="#0000FF"
TRENDCOLOUR="#000000"

CRIMSON="#B0171F"
PINK="#FFC0CB"
PURPLE="#9B30FF"
BLUE="#0000FF"
CYAN="#00EEEE"
GREEN="#00C957"
LIME="#00FF00"
YELLOW="#FFFF00"
ORANGE="#FFA500"
RED="#FF0000"
BLACK="#000000"

#plot graphs for the 6 sensors in the example
# export TZ="CET-1CEST"

#hour
rrdtool graph graph/mhour.png -A --start -24h \
--width 800 --height 600 --right-axis 1:0 --right-axis-format "%.1lf" \
DEF:a0=moisture.rrd:A0:AVERAGE \
DEF:a1=moisture.rrd:A1:AVERAGE \
DEF:a2=moisture.rrd:A2:AVERAGE \
CDEF:a10=0.9,a1,*,0.1,a0,*,+ \
CDEF:a12=0.9,a1,*,0.1,a2,*,+ \
AREA:a2$YELLOW:"avg(R) ± sigma" \
AREA:a12$RED:"avg(R) ± sigma/10" \
AREA:a10$YELLOW:"" \
AREA:a0#FFFFFF:"" \
LINE2:a1$BLUE:"avg(R)"
