"""Live pressure log + automatic gripping.

    python live_logger.py [COM6]

Sends atom_sensor.py to the Atom over USB-C and runs it there, reads the sensor,
writes every reading (one per 10 ms) to log.csv right away and switches the
compressor through compressor_client.py:
  - pressure outside safe range  -> off
  - object held                  -> off, the vacuum keeps holding it
  - no object                    -> suck

Esc or Ctrl-C stops and turns the compressor off.
If this script is killed, the compressor keeps running:  python compressor_client.py off
"""
import sys
import time
from pathlib import Path

import serial

from compressor_client import set_compressor

try:
    import msvcrt                          # Windows console keyboard
except ImportError:
    msvcrt = None                          # elsewhere only Ctrl-C works

# --- Settings -----------------------------------------------------------------
SERIAL_PORT = sys.argv[1] if len(sys.argv) > 1 else "COM6"
HERE        = Path(__file__).parent
ATOM_SCRIPT = HERE / "atom_sensor.py"      # runs on the Atom
LOG_FILE    = HERE / "log.csv"
PRINT_EVERY = 10           # console line every 10 readings = 10 times a second

SENSOR_SUPPLY_V = 5.0      # MPX5700AP supply voltage

# Compressor logic, absolute pressure in kPa
SAFE_MIN_KPA      = 30.0   # outside SAFE_MIN..SAFE_MAX something is wrong
SAFE_MAX_KPA      = 210.0
HOLDING_BELOW_KPA = 75.0   # vacuum under the cup = object is held


def microvolts_to_kpa(microvolts):
    """MPX5700AP datasheet: Vout = Vsupply * (0.0012858 * P + 0.04). Returns absolute kPa."""
    volts = microvolts / 1_000_000
    return (volts / SENSOR_SUPPLY_V - 0.04) / 0.0012858


def choose_mode(pressure_kpa):
    """What the compressor should do at this pressure. Returns (mode, reason)."""
    if not SAFE_MIN_KPA <= pressure_kpa <= SAFE_MAX_KPA:
        return "off", "out of safe range"
    if pressure_kpa < HOLDING_BELOW_KPA:
        return "off", "object held"
    return "suck", "no object"


def esc_pressed():
    """Non-blocking: True if Esc was hit in this console."""
    if msvcrt is None:
        return False
    while msvcrt.kbhit():
        key = msvcrt.getch()
        if key in (b"\x00", b"\xe0"):      # arrows/F-keys: swallow the 2nd byte
            msvcrt.getch()
        elif key == b"\x1b":
            return True
    return False


def connect_atom(port):
    """Open USB-C serial to the Atom and run atom_sensor.py on it.
    The file is sent from the PC every time, so it never has to be uploaded."""
    atom = serial.Serial()
    atom.port     = port
    atom.baudrate = 115200
    atom.timeout  = 0.2                    # readline() waits at most 0.2 s
    atom.dtr = atom.rts = False            # do not reset the Atom
    atom.open()
    atom.write(b"\x03\x03")                # Ctrl-C: stop whatever runs on the Atom
    time.sleep(0.3)
    atom.write(b"\x01")                    # Ctrl-A: raw REPL, takes code without echo
    time.sleep(0.3)
    atom.write(b"\x04")                    # Ctrl-D with no code: soft reboot, clean memory
    time.sleep(1.2)
    atom.read(200000)                      # throw away old output and prompts

    code = ATOM_SCRIPT.read_bytes()
    for start in range(0, len(code), 256): # small chunks: the Atom's input buffer is small
        atom.write(code[start:start + 256])
        time.sleep(0.01)
    atom.write(b"\x04")                    # Ctrl-D: run the code
    atom.read_until(b"OK")                 # the Atom confirms, then its output follows
    return atom


def main():
    atom = connect_atom(SERIAL_PORT)
    log = open(LOG_FILE, "w")
    log.write("time_ms,microvolts,pressure_kpa,compressor\n")

    mode = "off"
    reading_count = 0
    received = b""

    print("Running  (Esc to quit)")
    try:
        while True:
            if esc_pressed():
                print("Esc -> stopping")
                break

            received += atom.readline()
            if not received.endswith(b"\n"):
                continue                   # no complete line yet
            line = received.decode(errors="replace").strip()
            received = b""

            fields = line.split(",")
            if len(fields) != 2 or not fields[0].isdigit() or not fields[1].isdigit():
                if line and not line.startswith(">>>"):
                    print("Atom:", line)   # e.g. an error if atom_sensor.py is not uploaded
                continue
            time_ms, microvolts = int(fields[0]), int(fields[1])
            pressure_kpa = microvolts_to_kpa(microvolts)

            new_mode, reason = choose_mode(pressure_kpa)
            if new_mode != mode:
                mode = new_mode
                print("%7d ms  %s (%.1f kPa) -> %s" % (time_ms, reason, pressure_kpa, mode),
                      set_compressor(mode))

            log.write("%d,%d,%.3f,%s\n" % (time_ms, microvolts, pressure_kpa, mode))
            log.flush()                    # the file is up to date after every reading

            reading_count += 1
            if reading_count % PRINT_EVERY == 0:
                print("%7d ms | %7d uV | %6.1f kPa | %s" %
                      (time_ms, microvolts, pressure_kpa, mode))
    except KeyboardInterrupt:
        print("Ctrl-C -> stopping")
    finally:
        reply = set_compressor("off")      # compressor first, everything else after
        print("Compressor -> off", reply)
        if reply.get("ok") is False:
            print("WARNING: compressor may still be running - run: python compressor_client.py off")
        try:
            atom.write(b"\x03\x02")        # Ctrl-C: stop atom_sensor, Ctrl-B: normal REPL
        except Exception:
            pass
        atom.close()
        log.close()


if __name__ == "__main__":
    main()
