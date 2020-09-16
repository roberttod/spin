import json
import time
import RPi.GPIO as GPIO
from power import calculate_power
from threading import Thread

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class Cadence(Thread):
    def __init__(self, gymnasticon, resistance):
        Thread.__init__(self)
        self.stopped = False
        self.cadence = 0
        self.consecutiveHighs = 0
        self.gymnasticon = gymnasticon
        self.resistance = resistance
        self.revolutions = 0
    def stop(self):
        self.stopped = True
    def get(self):
        return self.cadence
    def run(self):
        lastHigh = time.time()
        while not(self.stopped):
            if GPIO.input(19) == GPIO.HIGH:
                self.consecutiveHighs += 1

            if self.consecutiveHighs == 5:
                now = time.time()
                cadence = int(60 / (now - lastHigh))
                # exclude weird readings
                if cadence < 250:
                    self.cadence = int(60 / (now - lastHigh))
                    self.revolutions += 1
                    lastHigh = now
                    pedal = {
                        "power": calculate_power(self.cadence, self.resistance.get()),
                        "crank": {
                            "timestamp": time.time() * 1000,
                            "revolutions": self.revolutions
                        }
                    }
                    self.gymnasticon.sendto(json.dumps(pedal).encode(), ('localhost', 3000))

            if (self.consecutiveHighs > 0 and GPIO.input(19) != GPIO.HIGH):
                self.consecutiveHighs = 0

            if time.time() - lastHigh > 4:
                self.cadence = 0
            time.sleep(0.001)
