import time
import Adafruit_GPIO.SPI as SPI
from pololu_drv8835_rpi import motors, MAX_SPEED
import Adafruit_MCP3008

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

def get():
    currentVoltage = mcp.read_adc(0)
    n = filter(lambda x: ((x > currentVoltage - 3) and x < (currentVoltage + 3)), levels)
    v = n[0]
    return levels.index(v)

def set(targetLevel):
    try:
        targetVoltage = levels[targetLevel]
        currentVoltage = mcp.read_adc(0)

        if (currentVoltage > targetVoltage):
            print("Positioning down to L:", targetLevel, "V:", targetVoltage)
            while mcp.read_adc(0) > targetVoltage:
                print(mcp.read_adc(0))
                motors.motor1.setSpeed(int(round(-2.4 * MAX_SPEED / 6)))
                time.sleep(0.1)

        if (currentVoltage < targetVoltage):
            print("Positioning up to L:", targetLevel, "V:", targetVoltage)
            while mcp.read_adc(0) < targetVoltage:
                print(mcp.read_adc(0))
                motors.motor1.setSpeed(int(round(2.4 * MAX_SPEED / 6)))
                time.sleep(0.1)

        motors.setSpeeds(0, 0)
        time.sleep(0.25)

        # at high levels, many adjustments need to be made
        if (not(mcp.read_adc(0) > targetVoltage - 1 and mcp.read_adc(0) < targetVoltage + 1)):
            set(targetLevel)

    finally:
        # Stop the motors, even if there is an exception
        # or the user presses Ctrl+C to kill the process.
        motors.setSpeeds(0, 0)

set(0)
