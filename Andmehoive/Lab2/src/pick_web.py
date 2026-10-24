"""Web page for the pick test: robot takes the glass from slot 1 and puts it to slot 2, N times.

usage: python pick_web.py ../../Lab1/data/l1_pick_10x.csv
then open http://127.0.0.1:8010

Before: save the pick place to slot 1 and the place place to slot 2 in the MG400 page
(http://127.0.0.1:8000). Save the pose where the cup TOUCHES the glass.
The robot goes there from LIFT_MM above. The next cycle takes the glass back (2 -> 1).
"""
import json
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import serial

import compressor_client
import live_logger

PORT = "COM5"
WEB_PORT = 8010
API = os.environ.get("MG400_API", "http://127.0.0.1:8000")

SUPPLY_V = 5.0       # MPX5700AP supply voltage
ATM_KPA = 96.2       # atmosphere, kPa absolute (raw sensor in open air)
GAIN = 5.24          # op-amp: V_out = GAIN * V_sensor + OFFSET
OFFSET = -1.27
ON_KPA = 15          # suction: pump on when vacuum is weaker than this
OFF_KPA = 30         # suction: pump off when vacuum reaches this
TIMEOUT_S = 0.5      # no line from Atom -> pump off

LIFT_MM = 40         # approach and lift height above the slot
GRIP_TIMEOUT_S = 5   # no -30 kPa in this time -> grip failed, stop
HOLD_KPA = -15       # after lift the vacuum must stay below this
BLOW_S = 0.5         # blow pulse to release the glass
MOVE_TIMEOUT_S = 25  # one robot move

state = {"p_raw": 0.0, "p_opamp": 0.0, "pump": 0, "mode": "off", "rows": 0,
         "step": "ready", "cycle": 0, "cycles": [], "error": "", "running": False,
         "reached": 0}  # reached = how many times suction got to OFF_KPA
lock = threading.Lock()
stop_flag = threading.Event()


# ---------- MG400 API ----------
def api(path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read())


def slot(n):
    s = api("/api/locations")["slots"][n - 1]
    if not s["set"]:
        raise RuntimeError(f"slot {n} is empty, save it in the MG400 page")
    return s


def move(x, y, z, r):
    api("/api/move", {"x": x, "y": y, "z": z, "r": r})
    end = time.time() + MOVE_TIMEOUT_S
    while time.time() < end:
        if stop_flag.is_set():
            raise RuntimeError("stopped")
        pose = api("/api/status")["pose"]
        if all(abs(a - b) <= 2.0 for a, b in zip(pose[:3], (x, y, z))):
            return
        time.sleep(0.05)
    raise RuntimeError("move timed out")


def wait(seconds):
    end = time.time() + seconds
    while time.time() < end:
        if stop_flag.is_set():
            raise RuntimeError("stopped")
        time.sleep(0.02)


# ---------- pump ----------
def set_pump(on, mode=None):
    """on=1 runs the pump in `mode` (suck/blow), on=0 stops it."""
    with lock:
        state["pump"] = on
    compressor_client.set_compressor(mode if on else "off")


def set_mode(mode):
    """suck = keep vacuum with the band, blow = blow until off, off = pump off."""
    with lock:
        state["mode"] = mode
    if mode == "blow":
        set_pump(1, "blow")
    elif mode == "off":
        set_pump(0)


def atom_loop():
    """Reads the Atom at 100 Hz, writes the log, keeps the vacuum in suck mode."""
    atom = serial.Serial()
    atom.port, atom.baudrate, atom.timeout = PORT, 115200, 0.1
    atom.dtr = atom.rts = False
    atom.open()
    atom.write(b"\x03\x03\x01")
    time.sleep(0.5)
    atom.write(open("controller.py", "rb").read() + b"\x04")
    atom.read_until(b"OK")
    last_line = time.time()

    def kpa(v):
        return (v / SUPPLY_V - 0.04) / 0.0012858 - ATM_KPA

    try:
        while True:
            line = atom.readline().decode(errors="ignore").split()
            now = time.time()
            try:
                adc_op, v_op, adc_raw, v_raw = int(line[0]), float(line[1]), int(line[2]), float(line[3])
            except (ValueError, IndexError):
                if state["pump"] and now - last_line > TIMEOUT_S:
                    stop_flag.set()
                    set_mode("off")
                    with lock:
                        state["error"] = "no data from Atom for 0.5 s, pump off"
                continue
            last_line = now
            p_raw, p_op = kpa(v_raw), kpa((v_op - OFFSET) / GAIN)
            with lock:
                state["p_raw"], state["p_opamp"] = p_raw, p_op
                state["rows"] += 1
                mode, pump = state["mode"], state["pump"]
            if mode == "suck":
                if pump and -p_raw >= OFF_KPA:
                    set_pump(0)
                    with lock:
                        state["reached"] += 1
                elif not pump and -p_raw < ON_KPA:
                    set_pump(1, "suck")
            t = int(now * 1000)
            live_logger.write_log(t, "raw", adc_raw, "%.3f" % v_raw, "%.2f" % p_raw, state["pump"])
            live_logger.write_log(t, "opamp", adc_op, "%.3f" % v_op, "%.2f" % p_op, state["pump"])
    except Exception as e:  # USB pulled etc.
        stop_flag.set()
        with lock:
            state["error"] = f"Atom: {e} - pump off, restart the program"
    finally:
        compressor_client.set_compressor("off")
        with lock:
            state["pump"] = 0


# ---------- pick sequence ----------
def step(text):
    with lock:
        state["step"] = text
    print(text)


def pick_cycle(n, a, b):
    """Take the glass at slot a, put it to slot b."""
    sa, sb = slot(a), slot(b)
    t0 = time.time()
    step(f"{n}: above slot {a}")
    move(sa["x"], sa["y"], sa["z"] + LIFT_MM, sa["r"])
    step(f"{n}: down to glass")
    move(sa["x"], sa["y"], sa["z"], sa["r"])
    step(f"{n}: suck")
    reached = state["reached"]
    set_mode("suck")
    t_suck = time.time()
    while state["reached"] == reached and state["p_raw"] > -OFF_KPA:
        if time.time() - t_suck > GRIP_TIMEOUT_S:
            raise RuntimeError(f"no grip: only {state['p_raw']:.1f} kPa in {GRIP_TIMEOUT_S} s")
        wait(0.02)
    grip_s = time.time() - t_suck
    wait(0.3)
    step(f"{n}: lift")
    move(sa["x"], sa["y"], sa["z"] + LIFT_MM, sa["r"])
    p_lift = state["p_raw"]
    if p_lift > HOLD_KPA:
        raise RuntimeError(f"glass lost after lift: {p_lift:.1f} kPa")
    step(f"{n}: carry to slot {b}")
    move(sb["x"], sb["y"], sb["z"] + LIFT_MM, sb["r"])
    step(f"{n}: down")
    move(sb["x"], sb["y"], sb["z"], sb["r"])
    p_carry = state["p_raw"]
    step(f"{n}: blow")
    set_mode("blow")
    wait(BLOW_S)
    set_mode("off")
    step(f"{n}: up")
    move(sb["x"], sb["y"], sb["z"] + LIFT_MM, sb["r"])
    return {"n": n, "from": a, "to": b, "grip_s": round(grip_s, 2), "p_lift": round(p_lift, 1),
            "p_carry": round(p_carry, 1), "cycle_s": round(time.time() - t0, 1), "ok": True}


def run_picks(count):
    stop_flag.clear()
    with lock:
        state["running"], state["error"], state["cycles"] = True, "", []
    try:
        for n in range(1, count + 1):
            a, b = (1, 2) if n % 2 else (2, 1)
            with lock:
                state["cycle"] = n
            result = pick_cycle(n, a, b)
            with lock:
                state["cycles"].append(result)
        step(f"done: {count} picks")
    except Exception as e:
        set_mode("off")
        with lock:
            state["error"] = state["error"] or str(e)  # keep the first reason (e.g. no data from Atom)
            state["cycles"].append({"n": state["cycle"], "ok": False, "error": state["error"]})
        step("stopped")
    finally:
        with lock:
            state["running"] = False


def stop_all():
    stop_flag.set()
    set_mode("off")
    try:
        api("/api/stop", {})
    except Exception:
        pass
    step("STOP")


# ---------- web ----------
PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Pick test</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:system-ui,sans-serif;margin:16px;max-width:760px;background:#fafafa;color:#222}
h1{font-size:20px;margin:0 0 12px}
.row{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.box{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px 14px;min-width:120px}
.big{font-size:28px;font-weight:600}
.lbl{font-size:12px;color:#666}
button{font-size:16px;padding:10px 16px;border-radius:8px;border:1px solid #aaa;background:#fff;cursor:pointer}
button:disabled{opacity:.4}
#stop{background:#d22;color:#fff;border:none;font-size:22px;padding:14px 28px}
.err{color:#c00;font-weight:600}
table{border-collapse:collapse;width:100%;background:#fff}
td,th{border:1px solid #ddd;padding:4px 8px;text-align:right;font-size:14px}
</style></head><body>
<h1>Pick test — klaas slotist 1 slotti 2</h1>
<div class="row">
 <div class="box"><div class="lbl">rõhk raw, kPa</div><div class="big" id="p_raw">-</div></div>
 <div class="box"><div class="lbl">rõhk opamp, kPa</div><div class="big" id="p_opamp">-</div></div>
 <div class="box"><div class="lbl">pump / režiim</div><div class="big" id="pump">-</div></div>
 <div class="box"><div class="lbl">tsükkel</div><div class="big" id="cycle">-</div></div>
</div>
<div class="row"><button id="stop" onclick="post('/stop')">STOP</button></div>
<div class="row">
 <button onclick="post('/mode',{mode:'suck'})">Imemine</button>
 <button onclick="post('/mode',{mode:'blow'})">Puhumine</button>
 <button onclick="post('/mode',{mode:'off'})">Pump seis</button>
 <button onclick="post('/goto',{slot:1})">Slot 1 kohale</button>
 <button onclick="post('/goto',{slot:2})">Slot 2 kohale</button>
</div>
<div class="row">
 <input id="n" type="number" value="10" min="1" max="50" style="width:70px;font-size:16px">
 <button id="run" onclick="post('/run',{n:+document.getElementById('n').value})">Auto: N haaret</button>
</div>
<div class="row"><span class="lbl">samm:&nbsp;</span><span id="step">-</span></div>
<div class="row err" id="error"></div>
<table><thead><tr><th>#</th><th>kust→kuhu</th><th>vaakum s</th><th>tõstes kPa</th><th>viies kPa</th><th>tsükkel s</th><th>ok</th></tr></thead><tbody id="tb"></tbody></table>
<p class="lbl" id="log"></p>
<script>
function post(u,b){fetch(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{})})}
async function tick(){
 try{const s=await (await fetch('/state')).json();
  p_raw.textContent=s.p_raw.toFixed(1); p_opamp.textContent=s.p_opamp.toFixed(1);
  pump.textContent=(s.pump?'ON ':'off ')+s.mode; cycle.textContent=s.cycle;
  step.textContent=s.step; error.textContent=s.error; run.disabled=s.running;
  log.textContent='logi: '+s.log+', '+s.rows+' mõõtmist';
  tb.innerHTML=s.cycles.map(c=>c.ok?`<tr><td>${c.n}</td><td>${c.from}→${c.to}</td><td>${c.grip_s}</td><td>${c.p_lift}</td><td>${c.p_carry}</td><td>${c.cycle_s}</td><td>✔</td></tr>`
   :`<tr><td>${c.n}</td><td colspan="5" style="text-align:left">${c.error}</td><td>✘</td></tr>`).join('');
 }catch(e){}
 setTimeout(tick,200)}
tick()
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, code, body, kind="application/json"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self.send(200, PAGE, "text/html; charset=utf-8")
        elif self.path == "/state":
            with lock:
                self.send(200, json.dumps(dict(state, log=live_logger.NAME)))
        else:
            self.send(404, "{}")

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/stop":
            stop_all()
        elif self.path == "/mode" and body.get("mode") in ("suck", "blow", "off"):
            set_mode(body["mode"])
        elif self.path == "/run" and not state["running"]:
            threading.Thread(target=run_picks, args=(int(body.get("n", 10)),), daemon=True).start()
        elif self.path == "/goto" and not state["running"]:
            def go(n=int(body.get("slot", 1))):
                try:
                    s = slot(n)
                    stop_flag.clear()
                    step(f"going above slot {n}")
                    move(s["x"], s["y"], s["z"] + LIFT_MM, s["r"])
                    step(f"above slot {n}")
                except Exception as e:
                    with lock:
                        state["error"] = str(e)
            threading.Thread(target=go, daemon=True).start()
        self.send(200, json.dumps({"ok": True}))


if __name__ == "__main__":
    compressor_client.set_compressor("off")
    threading.Thread(target=atom_loop, daemon=True).start()
    server = ThreadingHTTPServer(("127.0.0.1", WEB_PORT), Handler)
    print(f"open http://127.0.0.1:{WEB_PORT}  (Ctrl+C to quit)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop_flag.set()
        print("off:", compressor_client.set_compressor("off"))
