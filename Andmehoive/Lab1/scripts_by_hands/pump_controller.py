import time
import serial
import compressor_client
import live_logger
import keyboard


SUPPLY_V = 5.0   # MPX5700AP supply voltage
SUCK_KPA = 98   # absolute pressure 1 bar and above -> suck
OFF_KPA = 70     # below 0.7 bar -> off

atom = serial.Serial()
atom.port, atom.baudrate, atom.timeout = "COM5", 115200, 1
atom.dtr = atom.rts = False  # do not reset the Atom on connect
atom.open()
atom.write(b"\x03\x03\x01")  # Ctrl-C: stop running script, Ctrl-A: raw REPL
time.sleep(0.5)
atom.write(open("controller.py", "rb").read() + b"\x04")  # send controller.py, Ctrl-D: run
atom.read_until(b"OK")

mode = None
try:
    while True:
        if keyboard.is_pressed('escape'):
            break
        line = atom.readline().decode(errors="ignore").strip()  # "1.234 V"
        if not line.endswith(" V"):
            continue
        v = float(line[:-2])
        kpa = (v / SUPPLY_V - 0.04) / 0.0012858  # MPX5700AP datasheet formula
        live_logger.write_log(int(time.time() * 1000), v, kpa, mode)
        new_mode = "suck" if kpa >= SUCK_KPA else "off" if kpa < OFF_KPA else mode
        # print("new_mode:", new_mode, "kPa:", kpa, "volts:", v)
        if new_mode != mode:
            mode = new_mode
            compressor_client.set_compressor(mode)
except KeyboardInterrupt:
    pass
finally:
    print("off:", compressor_client.set_compressor("off"))  # always switch the pump off on exit
