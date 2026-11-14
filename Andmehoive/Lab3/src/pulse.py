from machine import Pin, Timer
import time

RELAY_PIN = 26
PULSES_MS = (20, 50, 100, 200, 500)  # commanded pulse lengths
REPEATS = 5                          # pulses per length
GAP_MS = 1000                        # pause between pulses

SCOPE_PIN = 22  # copy of the relay command on the header, for oscilloscope CH1

relay = Pin(RELAY_PIN, Pin.OUT)
scope = Pin(SCOPE_PIN, Pin.OUT)
relay.off()
scope.off()
timer = Timer(0)  # hardware timer ends the pulse, not sleep()
timer.deinit()    # clear a timer left over from an interrupted run
busy = False
t_on = 0
t_off = 0


def end_pulse(t):
    global busy, t_off
    t_off = time.ticks_us()
    relay.off()
    scope.off()
    busy = False


def pulse(ms):
    global busy, t_on
    busy = True
    t_on = time.ticks_us()
    relay.on()
    scope.on()
    timer.init(mode=Timer.ONE_SHOT, period=ms, callback=end_pulse)


print("cmd_ms,n,t_on_us,t_off_us,len_us")
for ms in PULSES_MS:
    for n in range(REPEATS):
        pulse(ms)
        deadline = time.ticks_add(time.ticks_ms(), ms + 200)
        while busy:
            if time.ticks_diff(time.ticks_ms(), deadline) > 0:
                relay.off()
                scope.off()
                print("timer callback did not fire, relay forced off")
                raise SystemExit
        print("%d,%d,%d,%d,%d" % (ms, n, t_on, t_off, time.ticks_diff(t_off, t_on)))
        time.sleep_ms(GAP_MS)
print("done")
