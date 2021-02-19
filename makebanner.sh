#!/bin/bash

case $1 in
	--help | -h | -help)
		echo "Usage: $0 <imagefile>"
		exit
		;;
esac

width=$(identify -format "%w" $1)
percentage=$((100 * 580 / $width))
mogrify -resize $percentage% -auto-orient $1
mogrify -crop 580x150+0+0 -gravity center $1
