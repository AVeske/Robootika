"""Vacuum gripper control for the MG400, driven by a pressure sensor.

    python pump_control.py

The M5Stack Atom (pressure.py, already uploaded to it) measures the sensor with
adc.read_uv() every 100 ms and sends the result over USB. This script converts
it to pressure and drives the pump:
  - cup open to air (no object)  -> pump sucks
  - object held                  -> pump off, the vacuum keeps holding it
  - pressure outside safe range  -> pump off (safety interlock)

Esc or Ctrl-C stops the script and turns the pump off.
The interlock lives here: if this process is killed, the pump keeps running -
use the task 'Pump: OFF now'.
"""
import json
import time
import urllib.request

import serial

try:
    import msvcrt                          # Windows console keyboard
except ImportError:
    msvcrt = None                          # elsewhere only Ctrl-C works

# --- Settings -----------------------------------------------------------------
SERIAL_PORT      = "COM6"
SAMPLE_PERIOD_MS = 100
PUMP_API_URL     = "http://127.0.0.1:8000/api/pump"
LOG_FILE         = "log.csv"

SENSOR_SUPPLY_V  = 5.0     # MPX5700AP supply voltage

# Pump logic, ABSOLUTE pressure in kPa. The gap between the two is hysteresis.
NO_OBJECT_ABOVE_KPA   = 90.0   # cup open to air -> suck
OBJECT_HELD_BELOW_KPA = 75.0   # vacuum formed   -> pump off

# Safety limits, pressure RELATIVE to atmosphere in kPa. A normal grip is about -40.
SAFE_MIN_KPA = -70.0
SAFE_MAX_KPA = 110.0

ATMOSPHERE_SAMPLES = 10    # readings averaged at start-up to measure atmospheric pressure


def voltage_to_kpa(voltage):
    """MPX5700AP datasheet formula: Vout = Vsupply * (0.0012858 * P + 0.04).
    Returns absolute pressure in kPa."""
    return (voltage / SENSOR_SUPPLY_V - 0.04) / 0.0012858


class AtomADC:
    """The sensor ADC of the M5Stack Atom, used from the PC.

    The PC cannot reach the Atom's pins, so pressure.py on the Atom does the
    measuring (average of 32 adc.read_uv() calls) and prints every result as
    't_ms,voltage,p_kpa,g_kpa'. This class reads those lines back, so here too
    the value comes from adc.read_uv()."""

    def __init__(self, port, period_ms):
        self.serial = serial.Serial()
        self.serial.port     = port
        self.serial.baudrate = 115200
        self.serial.timeout  = 0.2         # read() waits at most 0.2 s
        self.serial.dtr = self.serial.rts = False   # do not reset/bootload the Atom
        self.serial.open()
        self.serial.write(b"\x03\x03")     # Ctrl-C: stop whatever runs on the Atom
        time.sleep(0.3)
        self.serial.read(200000)           # throw away old output
        self.serial.write(b"\x04")         # Ctrl-D: soft reboot MicroPython
        time.sleep(1.2)
        self.serial.read(200000)
        self.serial.write(b"import pressure; pressure.run(%d)\r\n" % period_ms)

        self.received = b""                # bytes of a line that is not complete yet
        self.waiting = []                  # measurements received but not read yet
        self.time_ms = None                # Atom time of the last read_uv() value

    def read_uv(self):
        """Next measurement in microvolts, or None if nothing arrived within 0.2 s."""
        if not self.waiting:
            self.received += self.serial.read(256)
            *lines, self.received = self.received.split(b"\n")
            for line in lines:
                fields = line.decode(errors="replace").strip().split(",")
                if len(fields) < 2 or not fields[0].isdigit():
                    continue               # header, comment or broken line
                try:
                    self.waiting.append((int(fields[0]), float(fields[1])))
                except ValueError:
                    continue
        if not self.waiting:
            return None
        self.time_ms, voltage = self.waiting.pop(0)
        return round(voltage * 1_000_000)

    def close(self):
        try:
            self.serial.write(b"\x03")     # Ctrl-C: stop pressure.run() on the Atom
        except Exception:
            pass
        self.serial.close()


def choose_pump_mode(pressure_kpa, relative_kpa, current_mode):
    """Decide what the pump should do. Returns (mode, reason)."""
    if not SAFE_MIN_KPA <= relative_kpa <= SAFE_MAX_KPA:     # safety always wins
        return "off", "SAFETY: %+.1f kPa vs atmosphere" % relative_kpa
    if pressure_kpa > NO_OBJECT_ABOVE_KPA:
        return "suck", "no object"
    if pressure_kpa < OBJECT_HELD_BELOW_KPA:
        return "off", "object held"
    return current_mode, "no change"


def set_pump(mode):
    """Send 'suck' or 'off' to the pump service. Returns its reply as a dict."""
    body = json.dumps({"mode": mode}).encode()
    request = urllib.request.Request(PUMP_API_URL, body, {"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(request, timeout=3).read())
    except Exception as error:
        return {"ok": False, "error": str(error)}


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


def main():
    adc = AtomADC(SERIAL_PORT, SAMPLE_PERIOD_MS)
    log = open(LOG_FILE, "w")
    log.write("time_ms,voltage_v,pressure_kpa,relative_kpa,pump_mode\n")

    atmosphere_readings = []
    atmosphere_kpa = None                  # unknown until start-up readings are in
    pump_mode = "off"
    samples_per_second = 1000 // SAMPLE_PERIOD_MS
    sample_count = 0

    print("Measuring atmospheric pressure, keep the cup open...  (Esc to quit)")
    try:
        while True:
            if esc_pressed():
                print("Esc -> stopping")
                break

            uv = adc.read_uv()
            if uv is None:                 # nothing arrived yet
                continue
            voltage = uv / 1_000_000
            pressure_kpa = voltage_to_kpa(voltage)

            # Start-up: measure atmosphere before the pump is switched on
            if atmosphere_kpa is None:
                atmosphere_readings.append(pressure_kpa)
                if len(atmosphere_readings) == ATMOSPHERE_SAMPLES:
                    atmosphere_kpa = sum(atmosphere_readings) / ATMOSPHERE_SAMPLES
                    print("Atmosphere %.1f kPa" % atmosphere_kpa)
                    if not 50.0 < atmosphere_kpa < 130.0:
                        print("WARNING: implausible atmosphere - check sensor supply / wiring")
                    pump_mode = "suck"
                    print("Pump -> suck", set_pump(pump_mode))
                continue

            relative_kpa = pressure_kpa - atmosphere_kpa
            new_mode, reason = choose_pump_mode(pressure_kpa, relative_kpa, pump_mode)
            if new_mode != pump_mode:
                pump_mode = new_mode
                print("%7d ms  %s (%.1f kPa) -> %s" % (adc.time_ms, reason, pressure_kpa, pump_mode),
                      set_pump(pump_mode))

            log.write("%d,%.4f,%.3f,%.3f,%s\n" %
                      (adc.time_ms, voltage, pressure_kpa, relative_kpa, pump_mode))
            log.flush()

            sample_count += 1
            if sample_count % samples_per_second == 0:
                print("%7d ms | %.3f V | %6.1f kPa | %+6.1f kPa vs atm | pump %s" %
                      (adc.time_ms, voltage, pressure_kpa, relative_kpa, pump_mode))
    except KeyboardInterrupt:
        print("Ctrl-C -> stopping")
    finally:
        reply = set_pump("off")            # pump first, everything else after
        print("Pump -> off", reply)
        if reply.get("ok") is False:
            print("WARNING: pump may still be running - run task 'Pump: OFF now'")
        adc.close()
        log.close()


if __name__ == "__main__":
    main()
