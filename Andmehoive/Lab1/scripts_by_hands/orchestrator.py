import subprocess

subprocess.Popen(["python", "-m", "mpremote", "connect", "COM6", "run", "controller.py"])
subprocess.Popen(["python", "pump_controller.py"]).wait()

