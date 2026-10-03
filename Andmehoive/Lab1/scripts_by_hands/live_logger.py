import time
import serial

f = open("log.csv", "w")
f.write("time_ms,volts,pressure_kpa,compressor\n")

def write_log(time_ms, volts, pressure_kpa, mode):
    f.write("%d,%f,%.3f,%s\n" % (time_ms, volts, pressure_kpa, mode))
    f.flush()