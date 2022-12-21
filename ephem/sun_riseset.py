#!/usr/bin/python3

################################################################################
#                                                                              #
# Sun Rise/Set                                                                 #
# Version 1.0                                                                  #
#                                                                              #
# Originally written by Bamm Gabriana. Feel free to use and modify.            #
# If you have improvements, send them back to me so I can incorporate them.    #
#                                                                              #
# This program is free software; you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation; either version 2 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but without any warranty; without even the implied warranty of               #
# merchantability or fitness for a particular purpose.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# A copy of the GNU General Public License can be found here:                  #
# <http://www.gnu.org/licenses/>                                               #
#                                                                              #
################################################################################

import math
from datetime import datetime

#=== Edit the following values according to your requirements ===#

# Enter the start and final dates to calculate, in YYYY-MM-DD format
start_date = "2022-01-01"
final_date = "2022-12-31"

# Enter the latitude and longitude to use, in degrees including decimals
lat =  14.60
lon = 120.97

# Enter the altitude to use for the sun's rise and set, in degrees. This is
# typically a negative number to account for atmospheric refraction and sun
# disk size. If set to None, it will be automatically calculated.
sun_alt = -0.833

#=== The calculations start here, based on values entered above ===#

def main():
	t0 = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
	tf = datetime.strptime(final_date, "%Y-%m-%d").timestamp()
	ti = 24 * 60 * 60  ## seconds per day

	tzoffset = datetime.now().astimezone().utcoffset().seconds / 3600
	lon_corr = lon - tzoffset * 15
	tt_tai_deg = 32.184 / 3600 * 15

	print("Date, Rise, Transit, Set, RA_Transit, Dec_Transit, NPD_08h, Hrly_Var, NPD_14h, Hrly_Var, EOT_12h, GST_00h_UT")
	for t in range(int(t0), int(tf) + ti, ti):
		datestring = datetime.fromtimestamp(t).strftime("%Y-%m-%d")

		##=== Values to print out ===##

		# Sunrise
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 6*3600)
		sun_r_deg = sun_ha_r - eot_deg - lon_corr + tt_tai_deg + 180
		h,m,s = dms(sun_r_deg, unit="hms"); sun_r_hms = f"{h:02.0f}:{m:02.0f}:{s:02.0f}"

		# Transit
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 12*3600)
		sun_t_deg = sun_ha_t - eot_deg - lon_corr + tt_tai_deg + 180
		h,m,s = dms(sun_t_deg, unit="hms"); sun_t_hms = f"{h:02.0f}:{m:02.0f}:{s:02.0f}"

		# Sunset
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 18*3600)
		sun_s_deg = sun_ha_s - eot_deg - lon_corr + tt_tai_deg + 180
		h,m,s = dms(sun_s_deg, unit="hms"); sun_s_hms = f"{h:02.0f}:{m:02.0f}:{s:02.0f}"

		# RA at Transit
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 12*3600)
		h,m,s = dms(sun_ra_deg, unit="hms"); sun_ra_hms = f"{h:02.0f} {m:02.0f} {s:02.0f}"

		# Dec at Transit
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 12*3600)
		d,m,s = dms(sun_dec_deg, unit="dms"); sun_dec_dms = f"{d:+03.0f} {m:02.0f} {s:02.0f}"

		# NPD at 8AM
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 8*3600)
		sun_npd_deg = 90 - sun_dec_deg
		d,m,s = dms(sun_npd_deg, unit="dms"); sun_npd08 = f"{d:3.0f} {m:02.0f} {s:02.0f}"

		# Hourly Variation
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + (8+6)*3600)
		hrly_var = ((90 - sun_dec_deg) - sun_npd_deg) / 6
		d,m,s = dms(hrly_var, unit="dms", signed="sec", frac=3); hrly_var08 = f"{s:+06.2f}"

		# NPD at 2PM
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 14*3600)
		sun_npd_deg = 90 - sun_dec_deg
		d,m,s = dms(sun_npd_deg, unit="dms"); sun_npd14 = f"{d:3.0f} {m:02.0f} {s:02.0f}"

		# Hourly Variation
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + (14+6)*3600)
		hrly_var = ((90 - sun_dec_deg) - sun_npd_deg) / 6
		d,m,s = dms(hrly_var, unit="dms", signed="sec", frac=3); hrly_var14 = f"{s:+06.2f}"

		# EOT at 12NN
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 12*3600)
		h,m,s = dms(eot_deg, unit="hms", signed="min", frac=1); eot_hms = f"{m:+03.0f} {s:04.1f}"

		# Greenwich Sidereal Time
		sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg = sun_position(t + 8*3600)
		h,m,s = dms(gst_deg, unit="hms", frac=1); gst_hms = f"{h:02.0f} {m:02.0f} {s:04.1f}"

		print( f"{datestring}, {sun_r_hms}, {sun_t_hms}, {sun_s_hms}, {sun_ra_hms}, {sun_dec_dms}, {sun_npd08}, {hrly_var08}, {sun_npd14}, {hrly_var14}, {eot_hms}, {gst_hms}" )

def sun_position(t):

	# Julian Centuries from Epoch 2000.0, defined as 2000 Jan 1 at 12 noon UT1
	T = (t - 946728000) / 86400 / 36525  ## UnixTime of Epoch = 946728000
	T2,T3,T4,T5=T**2,T**3,T**4,T**5

	# Semimajor Axis
	a = 1.0000010178 * 149597870700 + 1.5 * T

	# Eccentricity
	e = 0.0167086342 - 0.00004203654 * T - 0.000000126734 * T2 + 0.0000000001444 * T3 - 0.00000000000002 * T4 + 0.000000000000003 * T5

	# Mean Anomaly of Sun
	M = ( 1287104.793048 + 129596581.0481 * T - 0.5532 * T2 + 0.000136 * T3 - 0.00001149 * T4 ) / 3600  # (IERS Conventions, 2003)

	# Equation of the Center
	C = ( 1.914602 - 0.004817 * T - 0.000014 * T2 ) * sin(M) + ( 0.019993 - 0.000101 * T ) * sin(2 * M) + 0.000289 * sin(3 * M)

	# True Anomaly of Sun
	ν = M + C

	# Mean Longitude of Sun
	L = 280.46645683 + 36000.76982779 * T + 0.0003032028 * T2 + (1/49931) * T3 - (1/15299) * T4 - (1/1988000) * T5  # (VSOP 87)

	# Solar Aberration
	v = 2 * π * a * (129597742.283429 - 2 * 0.204411 * T - 3 * 0.0000523 * T2) / (3600 * 360 * 36525 * 86400)
	κ = atan(v * ( 1 + e * cos(ν) ) / ( 1 - e**2 ) / 299792458)

	# Mean Longitude of Sun, Corrected for Solar Aberration
	L = L - κ

	# True Longitude of Sun
	λ = L + C

	# Mean Obliquity of the Ecliptic
	ε = ( 84381.4119 - 46.84024 * T - 0.00059 * T2 + 0.001813 * T3 ) / 3600  # (N. Capitaine, P. T. Wallace, and J. Chapront, 2003)

	# Equatorial Coordinates of the Sun
	α = sun_ra_deg = atan2( sin(λ) * cos(ε), cos(λ) )
	δ = sun_dec_deg = asin( sin(λ) * sin(ε) )

	# Distance of Sun
	D = a * ( 1 - e**2 ) / ( 1 + e * cos(ν) )

	# Equation of Time
	eot_deg = ( L - α + 180 ) % 360 - 180

	# Hour Angle of Rise/Transit/Set
	a = sun_riseset_alt (default=sun_alt, sun_distance=D); l = lat
	sun_ha_r = -acos( ( sin(a) - sin(δ) * sin(l) ) / ( cos(δ) * cos(l) ) )
	sun_ha_s = -sun_ha_r; sun_ha_t = 0

	# Greenwich Mean Sidereal Time
	gst_deg = ((24110.54841 + 8640184.812866 * T + 0.093104 * T2 + 0.0000062 * T3) / 3600 * 15) % 360

	# Local Mean Sidereal Time
	lst_deg = gst_deg + lon

	return sun_ra_deg,sun_dec_deg,eot_deg,sun_ha_r,sun_ha_t,sun_ha_s,gst_deg,lst_deg

def sun_riseset_alt(default=None, sun_radius=696342000, sun_distance=149598022960.7127984600, atm_refraction=0.56080572916666666666):

	# Default values:
	#   sun_radius     =  696342000 based on SOHO 2006 Mercury Transit observation
	#   sun_distance   =  1.0000010178 * 149597870700 is semimajor axis at J000.0
	#   atm_refraction =  33.648343750 / 60 at horizon at STP (15 °C and 1013.25 millibars)

	if default is None:
		sun_disk_radius = atan( sun_radius / sun_distance )
		return -( atm_refraction + sun_disk_radius )
	else:
		return default

def dms(num, unit="", signed="", frac=0):
	num = num / 15 if unit == "hms" else num
	sgn = 1 if num >= 0 else -1;
	mul = 10**frac
	num_int = float(int(abs(num)))
	num_min = float(int(abs(num * 60) % 60))
	num_sec = float(int(abs(num * 3600) % 60) + int(abs(num * 3600 * mul) % mul) / mul)
	if signed == "sec":
		return num_int,num_min,sgn * num_sec
	elif signed == "min":
		return num_int,sgn * num_min,num_sec
	else:
		return sgn * num_int,num_min,num_sec

def sin(x):
	return math.sin(math.radians(x))
def cos(x):
	return math.cos(math.radians(x))
def tan(x):
	return math.tan(math.radians(x))
def asin(x):
	return math.degrees(math.asin(x))
def acos(x):
	return math.degrees(math.acos(x))
def atan(x):
	return math.degrees(math.atan(x))
def atan2(y,x):
	return math.degrees(math.atan2(y,x)) % 360
π = math.pi

main()
