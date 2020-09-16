Spin
----

# Installation
```bash
# pip essentials
sudo apt-get install build-essential python-dev python-smbus python-pip git

# pip install
sudo pip install adafruit-mcp3008 wiringpi flask

# for the motor driver
git clone https://github.com/pololu/drv8835-motor-driver-rpi.git
cd drv8835-motor-driver-rpi
sudo python setup.py install


```

# Start server

```bash
sudo python server.py
```