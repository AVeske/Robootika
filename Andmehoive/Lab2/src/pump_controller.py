import sys
import time
import serial
import compressor_client
import live_logger
import keyboard

# usage: python pump_controller.py suck opamp   (suction, control from op-amp signal)
#        python pump_controller.py suck raw     (suction, control from raw sensor)
#        python pump_controller.py blow opamp   (blowing)
#        python pump_controller.py off raw      (only log, pump never starts)
#        last word ending with .csv = log file name
#        t=30 stop after 30 s, n=10 stop after 10 pump starts
#        keys while running: 1 suck, 2 blow, 0 off, Esc quit
MODE = sys.argv[1] if len(sys.argv) > 1 else "suck"
ARGS = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
RUN_S = float(ARGS.get("t", 0))     # t=30 -> stop after 30 s (0 = until Esc)
RUN_STARTS = int(ARGS.get("n", 0))  # n=10 -> stop after 10 pump starts, when the 10th cycle is over
CONFIG = "raw" if "raw" in sys.argv[1:] else "opamp"

PORT = "COM5"
SUPPLY_V = 5.0           # MPX5700AP supply voltage, measure it with a multimeter
ATM_KPA = 96.2           # atmosphere, kPa absolute (raw sensor in open air, 0.819 V, l1_noise_off.csv 24.10)
GAIN = 5.24              # op-amp: V_out = GAIN * V_sensor + OFFSET  (from plot_result.py)
OFFSET = -1.27
ON_KPA = 15              # pump on when pressure is weaker than this (kPa vs atmosphere)
OFF_KPA = 30             # pump off when pressure reaches this
MIN_OFF_S = 1.0          # minimum off time before the next start
MAX_STARTS_PER_MIN = 10  # more starts than this -> pump stays off
TIMEOUT_S = 0.5          # no line from Atom for this long -> pump off
LIMIT_KPA = 130          # reading outside the pump range -> pump off

atom = serial.Serial()
atom.port, atom.baudrate, atom.timeout = PORT, 115200, 0.1
atom.dtr = atom.rts = False  # do not reset the Atom on connect
atom.open()
atom.write(b"\x03\x03\x01")  # Ctrl-C: stop running script, Ctrl-A: raw REPL
time.sleep(0.5)
atom.write(open("controller.py", "rb").read() + b"\x04")  # send controller.py, Ctrl-D: run
atom.read_until(b"OK")


def kpa(v_sensor):
    return (v_sensor / SUPPLY_V - 0.04) / 0.0012858  # MPX5700AP datasheet formula, kPa absolute


used_api = MODE != "off"           # off mode never talks to the pump
if used_api:
    compressor_client.set_compressor("off")
sign = -1 if MODE == "suck" else 1  # suction = negative pressure
pump = 0
last_off = time.time()
last_line = time.time()
starts = []                         # start times in the last minute
total_starts = 0                    # all starts in this run


def switch(on, reason):
    global pump, last_off, used_api, total_starts
    used_api = True
    pump = on
    if on:
        starts.append(time.time())
        total_starts += 1
    else:
        last_off = time.time()
    answer = compressor_client.set_compressor(MODE if on else "off")
    print("pump", MODE if on else "off", "-", reason, answer)


t_start = time.time()
try:
    while not keyboard.is_pressed("escape"):
        for key, new_mode in (("1", "suck"), ("2", "blow"), ("0", "off")):  # change mode while running
            if keyboard.is_pressed(key) and MODE != new_mode:
                if pump:
                    switch(0, "mode change")
                MODE = new_mode
                sign = -1 if MODE == "suck" else 1
                print("mode", MODE)
        line = atom.readline().decode(errors="ignore").split()  # "2512 2.512 715 0.715" (GPIO25 GPIO33)
        now = time.time()
        try:
            adc_op, v_op, adc_raw, v_raw = int(line[0]), float(line[1]), int(line[2]), float(line[3])
        except (ValueError, IndexError):
            if pump and now - last_line > TIMEOUT_S:
                switch(0, "no data from Atom")
            continue
        last_line = now

        p_abs = {"raw": kpa(v_raw), "opamp": kpa((v_op - OFFSET) / GAIN)}
        p = {c: p_abs[c] - ATM_KPA for c in p_abs}  # kPa vs atmosphere

        strength = p[CONFIG] * sign
        starts = [t for t in starts if now - t < 60]
        if abs(p[CONFIG]) > LIMIT_KPA:
            if pump:
                switch(0, "reading out of range")
        elif pump and strength >= OFF_KPA:
            switch(0, "pressure reached")
        elif not pump and MODE != "off" and strength < ON_KPA and now - last_off >= MIN_OFF_S:
            if len(starts) < MAX_STARTS_PER_MIN:
                switch(1, "pressure too weak")

        t = int(now * 1000)
        live_logger.write_log(t, "raw", adc_raw, "%.3f" % v_raw, "%.2f" % p["raw"], pump)
        live_logger.write_log(t, "opamp", adc_op, "%.3f" % v_op, "%.2f" % p["opamp"], pump)

        if RUN_S and now - t_start >= RUN_S:
            print("time is over:", RUN_S, "s")
            break
        if RUN_STARTS and total_starts >= RUN_STARTS and not pump:
            print("starts done:", total_starts)
            break
except KeyboardInterrupt:
    pass
finally:
    if used_api:
        print("off:", compressor_client.set_compressor("off"))  # always switch the pump off on exit
    atom.close()
