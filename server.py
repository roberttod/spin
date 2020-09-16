import sys
import socket
import threading
import logging
from resistance import Resistance
from cadence import Cadence
from power import calculate_power
from flask import Flask, jsonify, render_template

gymnasticon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 4000)
gymnasticon.bind(server_address)

app = Flask(__name__)
resistance = Resistance(gymnasticon)
cadence = Cadence(gymnasticon, resistance)


@app.route('/')
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route('/status')
def get_status():
    power = calculate_power(cadence.get(), resistance.get())
    return jsonify({
        "power": power,
        "cadence": cadence.get(),
        "resistanceLevel": resistance.get(),
        "resistanceVoltage": resistance.voltage()
    })

@app.route('/level/set/<level>')
def profile(level):
    print("Set", level)
    resistance.set(int(level))
    return jsonify({
        "value": True
    })

def has_live_threads(threads):
    return True in [t.isAlive() for t in threads]

# app.logger.disabled = True
# log = logging.getLogger('werkzeug')
# log.disabled = True

server = threading.Thread(target=app.run,kwargs=dict(host='0.0.0.0'))
server.daemon = True
server.start()

resistance.daemon = True
resistance.start()

cadence.daemon = True
cadence.start()

threads = [server, resistance, cadence]
running = True

while has_live_threads(threads) and running:
    try:
        [t.join(1) for t in threads
            if t is not None and t.isAlive()]
    except:
        # Ctrl-C handling and send kill to threads
        print "Sending kill to threads..."
        for t in threads:
             if hasattr(t, 'stop'): t.stop()
        running = False
