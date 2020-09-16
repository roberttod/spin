import time
from threading import Thread
from pololu_drv8835_rpi import motors, MAX_SPEED
import Adafruit_MCP3008
from PID import PID

CLK  = 26
MISO = 16
MOSI = 20
CS   = 21
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

maxOutput = int(round(2.5 * MAX_SPEED / 5))

levels = [
    77,
    120,
    140,
    149,
    157,
    164,
    172,
    177,
    182,
    190,
    197,
    202,
    209,
    218,
    228,
    258
]

class Resistance(Thread):
    def __init__(self, gymnasticon):
        Thread.__init__(self)

        self.level = 0
        self.stopped = False
        self.pid = PID(180, 0, 80, levels[0])
        self.pid.output_limits = (-maxOutput, maxOutput)
        self.pid.sample_time = 0.05
        self.gymnasticon = gymnasticon

    def get(self):
        return self.level

    def set(self, level):
        self.level = level
        self.pid.setpoint = levels[level]
        self.pid.auto_mode = True 

    def run(self):
        motors.setSpeeds(0, 0)
        try:
            while not(self.stopped):
                vout = self.voltage()
                # if vout < 70 or vout > 260:
                #     print('out of range', vout)
                #     break
                output = int(self.pid(vout))
                if not(output > maxOutput or output < (-1 * maxOutput)):
                    motors.motor1.setSpeed(output)
                time.sleep(0.01)

        finally:
            print('Resistance finall called')
            motors.setSpeeds(0, 0)
    
    def stop(self):
        self.stopped = True
        print('Resistance stop called')
        motors.setSpeeds(0, 0)

    def voltage(self):
        values = []
        for x in range(20):
            values.append(mcp.read_adc(0))
        values.sort()
        mid = len(values) // 2
        return (values[mid] + values[~mid]) / 2
