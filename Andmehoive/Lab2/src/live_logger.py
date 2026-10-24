import os
import sys

# last argument ending with .csv = log file name, otherwise log.csv
NAME = sys.argv[-1] if sys.argv[-1].endswith(".csv") else "log.csv"
if NAME != "log.csv" and os.path.exists(NAME):
    sys.exit(NAME + " already exists, choose another name")
f = open(NAME, "w")
print("logging to", NAME)
f.write("t_ms,config,adc,volts,p_kpa,pump\n")

rows = 0


def write_log(*values):
    global rows
    line = ",".join(str(v) for v in values)
    f.write(line + "\n")
    f.flush()
    rows += 1
    if rows % 20 in (1, 2):  # 2 rows x 100 Hz is too fast for the console, print one raw + opamp pair every 10th sample
        print(line)
