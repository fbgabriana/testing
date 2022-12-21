#!/usr/bin/python3

################################################################################
#                                                                              #
# Julian Day Calendar                                                          #
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

from datetime import datetime

#=== Edit the following values according to your requirements ===#

# Enter the start and final dates to calculate, in YYYY-MM-DD format
start_date = "2022-01-01"
final_date = "2022-12-31"

#=== The calculations start here, based on values entered above ===#

def main():
	t0 = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
	tf = datetime.strptime(final_date, "%Y-%m-%d").timestamp()
	ti = 24 * 60 * 60  ## seconds per day

	tzoffset = datetime.now().astimezone().utcoffset().seconds

	print("Date, Day_of_Week, Day_of_Year, Fraction_of_Year, JDN")
	for t in range(int(t0), int(tf) + ti, ti):
		datestring = datetime.fromtimestamp(t).strftime("%Y-%m-%d")

		##=== Values to print out ===##

		# Day of Week
		Day_of_Week = ("Sun","Mon","Tue","Wed","Thu","Fri","Sat")[ int( 5 + t/86400 ) % 7 ]

		# Day of Year
		y_this_year = int(datetime.fromtimestamp(t).strftime("%Y"))
		t_this_year = datetime.strptime(str(y_this_year), "%Y").timestamp()
		Day_of_Year = int(1 + (t - t_this_year) / 86400)

		# Fraction of Year
		y_next_year = y_this_year + 1
		t_next_year = datetime.strptime(str(y_next_year), "%Y").timestamp()
		Fraction_of_Year = (t - t_this_year) / (t_next_year - t_this_year)

		# Julian Day Number
		JDN = 2440587.5 + (t + tzoffset) / 86400

		print( f"{datestring}, {Day_of_Week}, {Day_of_Year:3d}, {Fraction_of_Year:0.4f}, {JDN}" )

main()
