from machine import Pin
import time

RELAY_PIN = 26  # Grove; if the relay does not click, try 32

relay = Pin(RELAY_PIN, Pin.OUT)
relay.off()

for i in range(10):
    relay.on()
    print("on", i)
    time.sleep_ms(500)
    relay.off()
    print("off", i)
    time.sleep_ms(1500)
