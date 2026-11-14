from machine import Pin
import time

# Static test: relay and G22 on for 10 s, off for 10 s, so a multimeter or
# an untriggered oscilloscope shows a steady level.
relay = Pin(26, Pin.OUT)
scope = Pin(22, Pin.OUT)

for i in range(3):
    relay.on()
    scope.on()
    print("ON  - G22 3.3 V, NO 5 V")
    time.sleep(10)
    relay.off()
    scope.off()
    print("OFF - G22 0 V, NO 0 V")
    time.sleep(10)
print("done")
