import time
import serial

f = open("log.csv", "w")
f.write("time_ms,volts,pressure_kpa,compressor\n")

def write_log(time_ms, volts, pressure_kpa, mode):
    line = "%d,%f,%.3f,%s" % (time_ms, volts, pressure_kpa, mode)
    f.write(line + "\n")
    f.flush()
    print(line)