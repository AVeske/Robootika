# Runs ON THE ATOM (MicroPython), not on the PC.
# No upload needed: live_logger.py sends this file to the Atom and runs it.
# Every 10 ms prints one line "time_ms,microvolts" - the PC reads it over USB-C.
# WARNING: sensor Vout goes straight to G25. Above ~3.3 V the pin dies.
from machine import ADC, Pin
import time

adc = ADC(Pin(25))
adc.atten(ADC.ATTN_11DB)        # input range 0..~3.3 V

PERIOD_MS  = 10
AVERAGE_OF = 32                 # read_uv() calls averaged into one reading


def read_microvolts():
    total = 0
    for _ in range(AVERAGE_OF):
        total += adc.read_uv()
    return total // AVERAGE_OF


def run():
    start = time.ticks_ms()
    next_reading = start
    while True:
        wait_ms = time.ticks_diff(next_reading, time.ticks_ms())
        if wait_ms > 0:
            time.sleep_ms(wait_ms)
        time_ms = time.ticks_diff(time.ticks_ms(), start)
        print("%d,%d" % (time_ms, read_microvolts()))
        next_reading = time.ticks_add(next_reading, PERIOD_MS)


if __name__ == "__main__":
    run()
