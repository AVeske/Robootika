from machine import ADC, Pin
import time

adc = ADC(Pin(25))
adc.atten(ADC.ATTN_11DB)  # 0..3.3 V

PERIOD_MS = 10  # 100 Hz

next_t = time.ticks_ms()
while True:
    raw = adc.read()                   # 0..4095
    volts = adc.read_uv() / 1_000_000
    print("%d %.3f" % (raw, volts))    # "1043 0.839"
    next_t = time.ticks_add(next_t, PERIOD_MS)
    time.sleep_ms(max(0, time.ticks_diff(next_t, time.ticks_ms())))
