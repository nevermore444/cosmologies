from flask import Flask, request, jsonify
import swisseph as swe
import datetime

app = Flask(__name__)
 # Ephemeris data path (put files in the same folder)

@app.route('/calculate', methods=['POST'])
def calculate_chart():
    data = request.json
    date_str = data.get('date')  # 'YYYY-MM-DD'
    time_str = data.get('time')  # 'HH:MM'
    lat = float(data.get('lat'))  # decimal degrees
    lon = float(data.get('lon'))  # decimal degrees

    dt = datetime.datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60)

    planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    results = {}

    for i, name in zip(range(7), planets):
        pos, _ = swe.calc_ut(jd, i)
        results[name] = pos[0]  # Longitude in zodiac

    return jsonify(results)
