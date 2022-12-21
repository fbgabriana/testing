#!/usr/bin/python3

# Moon and Sun altitude and distance using Astropy
# For use in calculating tidal force and tidal height
# Written by Bamm Gabriana (2022 Apr 05-18)
# Feel free to use and share.

import sys
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import get_body, solar_system_ephemeris
from astropy.coordinates import EarthLocation, AltAz, SkyCoord as pos
from astropy import units as u

sys.tracebacklimit = 0

#=== Edit the following values according to your requirements ===#

lat = 14.635942   # WL 11104201 (Marikina Sto. Nino Bridge Station)
lon = 121.093122  #

start_time = "2022-05-16 12:14"  # First entry of KOICA WL
final_time = "2022-05-16 12:24"
increments = 10   ## minutes

#=== The calculations start here, based on values entered above ===#

t0 = datetime.strptime(start_time, "%Y-%m-%d %H:%M").timestamp()
tf = datetime.strptime(final_time, "%Y-%m-%d %H:%M").timestamp()
ti = increments * 60  ## seconds per minute

loc = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m, ellipsoid="WGS84")
solar_system_ephemeris.set("DE440s")

print("Date_Time,Moon_Dist")
for t in range(int(t0), int(tf), ti):

	time = Time(t, format="unix", scale="utc")

	moon = get_body("moon", time)

	moon_dist = moon.distance.m

	timestring = datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")
	print( "{},{:0.0f}".format(timestring, moon_dist) )

