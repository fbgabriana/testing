#!/usr/bin/python3

import sys
from datetime import datetime
from math import sin, cos, tan, acos, asin, atan, atan2
from math import degrees as deg, radians as rad, pi

#=== Edit the following values according to your requirements ===#

start_time = "2022-01-01"  # Entire 2022
final_time = "2022-12-31"
increments = 1  ## hour

#=== The calculations start here, based on values entered above ===#

t0 = datetime.strptime(start_time, "%Y-%m-%d").timestamp()
tf = datetime.strptime(final_time, "%Y-%m-%d").timestamp()
ti = increments * 60 * 60

print("Date_Time,EOT")
for t in range(int(t0), int(tf) + ti, ti):
	T = (t - 946684800) / 86400 / 36525
	L0 = 280.4664567 + 36000.76982779 * T + 0.0003032028 * T**2 - 0.0056924035
	M = 357.52911 + 35999.05029 * T - 0.0001559 * T**2 - 0.00000048 * T**3
	E = 23.439291 - 0.013004167 * T - 0.000000164 * T**2 + 0.0000005036 * T**3
	C = (1.914602 - 0.004817 * T - 0.000014 * T**2) * sin(rad(M)) + (0.019993 - 0.000101 * T) * sin(2 * rad(M)) + 0.000289 * sin(3 * rad(M))
	L = L0 + C

	sun_ra_deg = deg(atan2( sin(rad(L)) * cos(rad(E)), cos(rad(L)) )) % 360
	sun_dec_deg = deg(asin( sin(rad(L)) * sin(rad(E)) ))
	eot_deg = (L0 - sun_ra_deg + 180) % 360 - 180
	eot_min = eot_deg / 15 * 60
	timestring = datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")
	print( f"{timestring},{eot_min:+010.6f}" )
