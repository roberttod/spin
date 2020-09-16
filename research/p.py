import time
import json
import threading
import Adafruit_GPIO.SPI as SPI
from pololu_drv8835_rpi import motors, MAX_SPEED
import Adafruit_MCP3008
from PID import PID

maxOutput = int(round(2.4 * MAX_SPEED / 6))

pid = PID(150, 0, 80, setpoint=160)
pid.output_limits = (-maxOutput, maxOutput)
pid.sample_time = 0.05

CLK  = 26
MISO = 16
MOSI = 20
CS   = 21
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

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

motors.setSpeeds(0, 0)

plot_v = [mcp.read_adc(0)]
plot_t = [time.time()]
plot_s = [0]

def get():
    currentVoltage = mcp.read_adc(0)
    n = filter(lambda x: ((x > currentVoltage - 3) and x < (currentVoltage + 3)), levels)
    v = n[0]
    return levels.index(v)

motor_speed = 0

def set():
    try:
        lastV = accurate_voltage()
        while True:
            vout = accurate_voltage()
            if vout > lastV + 30 or vout < lastV - 30:
              continue
            lastV = vout
            if vout < 70 or vout > 260:
              print('out of range', vout)
              break
            output = int(pid(vout))
            #print('motor:', output, "pot", mcp.read_adc(0))
            if not(output > maxOutput or output < (-1 * maxOutput)):
                # print('set speed')
                motor_speed = output
                motors.motor1.setSpeed(output)


        # targetVoltage = levels[targetLevel]
        # currentVoltage = mcp.read_adc(0)

        # if (currentVoltage > targetVoltage):
        #     print("Positioning down to L:", targetLevel, "V:", targetVoltage)
        #     while mcp.read_adc(0) > targetVoltage:
        #         print(mcp.read_adc(0))
        #         motors.motor1.setSpeed(int(round(-2.4 * MAX_SPEED / 6)))
        #         time.sleep(0.1)

        # if (currentVoltage < targetVoltage):
        #     print("Positioning up to L:", targetLevel, "V:", targetVoltage)
        #     while mcp.read_adc(0) < targetVoltage:
        #         print(mcp.read_adc(0))
        #         motors.motor1.setSpeed(int(round(2.4 * MAX_SPEED / 6)))
        #         time.sleep(0.1)

        # motors.setSpeeds(0, 0)
        # time.sleep(0.25)

        # # at high levels, many adjustments need to be made
        # if (not(mcp.read_adc(0) > targetVoltage - 1 and mcp.read_adc(0) < targetVoltage + 1)):
        #     set(targetLevel)

    finally:
        # Stop the motors, even if there is an exception
        # or the user presses Ctrl+C to kill the process.
        motors.setSpeeds(0, 0)
        print('V')
        print('\n'.join(map(str, plot_v)))
        print('T')
        print('\n'.join(map(str, plot_t)))
        #print('S')
        #print('\n'.join(map(str, plot_s)))

def accurate_voltage():
    values = []
    for x in range(20):
        values.append(mcp.read_adc(0))
    values.sort()
    mid = len(values) // 2
    return (values[mid] + values[~mid]) / 2

def plot_vt():
    global plot_v
    global plot_v
    last_v = mcp.read_adc(0)
    while True:
        vout = accurate_voltage()
        if vout > last_v + 30 or vout < last_v - 30:
              continue
        print(vout)
        last_v = vout
        plot_v.append(vout)
        plot_t.append(time.time())
        plot_s.append(motor_speed)
        time.sleep(0.1)

x = threading.Thread(target=plot_vt)
x.daemon = True
x.start()
set()



