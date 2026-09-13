import time
import serial

f = open("log.csv", "w")
f.write("time,volts\n")

def write_log(volts):
    f.write("%s,%s\n" % (time.strftime("%H:%M:%S"), volts))
    f.flush()