from machine import ADC, Pin
import time

adc = ADC(Pin(25))
adc2 = ADC(Pin(33))

adc.atten(ADC.ATTN_11DB) 
while True:
    volts = adc.read_uv() / 1_000_000
    volts2 = adc2.read_uv() / 1_000_000

    print("%.3f" % volts + " %.3f" % volts2)
    time.sleep_ms(100)
