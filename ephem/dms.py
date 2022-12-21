#!/usr/bin/python3

import sys
sys.tracebacklimit = 0

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

def main():
	if len(sys.argv) > 4:
		num = float(sys.argv[1])
		unit = sys.argv[2]
		signed = sys.argv[3]
		frac = int(sys.argv[4])
	elif len(sys.argv) > 3:
		num = float(sys.argv[1])
		unit = sys.argv[2]
		signed = sys.argv[3]
		frac = 0
	elif len(sys.argv) > 2:
		num = float(sys.argv[1])
		unit = sys.argv[2]
		signed = ""
		frac = 0
	elif len(sys.argv) > 1:
		num = float(sys.argv[1])
		unit = ""
		signed = ""
		frac = 0
	d,m,s = dms(num, unit, signed, frac)
	print(d,m,s)
	if signed == "sec":
		print(f"{d:02.0f} {m:02.0f} {s:+03.0f}")
	elif signed == "min":
		print(f"{d:02.0f} {m:+03.0f} {s:02.0f}")
	else:
		print(f"{d:+03.0f} {m:02.0f} {s:02.0f}")
main()

