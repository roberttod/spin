import json
import os

dirname = os.path.dirname(__file__)

rpm_power = json.load(open(os.path.join(dirname, 'rpm_power.json'),)) 

def calculate_power(cadence, power_level):
    values = rpm_power[power_level]

    c1 = { 'cadence': 0, 'power': 0 }
    c2 = { 'cadence': 1000, 'power': 1000 }

    # todo: calculate out of bounds
    if (cadence > values[0]['cadence']):
        for value in values:
            if (value['cadence'] < cadence and value['cadence'] > c1['cadence']):
                c1 = value
            if (value['cadence'] > cadence and value['cadence'] < c2['cadence']):
                c2 = value
    else:
        c1 = values[0]
        c2 = values[1]
    power = findYPoint(c1['cadence'], c2['cadence'], c1['power'], c2['power'], cadence)
    if power < 0: return 0
    return power

def findYPoint(xa,xb,ya,yb,xc):
    m = (ya - yb) / (xa - xb)
    yc = (xc - xb) * m + yb
    return yc
    