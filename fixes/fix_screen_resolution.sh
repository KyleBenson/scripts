#!/bin/bash
RESOLUTION=1920x1080
xrandr --newmode "$RESOLUTION""_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
#xrandr --addmode VGA1 "$RESOLUTION""_60.00"
xrandr --addmode HDMI1 "$RESOLUTION""_60.00"
