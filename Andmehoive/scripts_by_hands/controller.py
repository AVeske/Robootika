from machine import ADC, Pin
import time

adc = ADC(Pin(25))
adc.atten(ADC.ATTN_11DB)  # 0..~3.3 V
while True:
    volts = adc.read_uv() / 1_000_000
    print("%.3f V" % volts)
    time.sleep_ms(100)
