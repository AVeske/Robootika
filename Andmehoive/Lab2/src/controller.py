from machine import ADC, Pin
import time

adc = ADC(Pin(25))   # op-amp output
adc2 = ADC(Pin(33))  # raw sensor
adc.atten(ADC.ATTN_11DB)   # 0..3.3 V
adc2.atten(ADC.ATTN_11DB)  # 0..3.3 V

PERIOD_MS = 10  # 100 Hz

next_t = time.ticks_ms()
while True:
    raw = adc.read()
    volts = adc.read_uv() / 1_000_000
    raw2 = adc2.read()
    volts2 = adc2.read_uv() / 1_000_000
    print("%d %.3f %d %.3f" % (raw, volts, raw2, volts2))  # GPIO25 adc, V, GPIO33 adc, V
    next_t = time.ticks_add(next_t, PERIOD_MS)
    time.sleep_ms(max(0, time.ticks_diff(next_t, time.ticks_ms())))
