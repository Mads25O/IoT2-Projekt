import base64
from io import BytesIO
from flask import Flask, render_template
from matplotlib.figure import Figure 
from get_sensor_data import get_kontor_dht11_data, get_kontor_ccs811_data, get_vejrst_sensor_data, get_tyveri_sensor_data, get_motor_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

def kontor_co2():
    timestamps, co2 = get_kontor_ccs811_data(10)
    
    fig = Figure()
    ax = fig.subplots()
    ax.plot(timestamps, co2, c = "#11F", marker = "o")
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 6)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("CO2")
    ax.invert_xaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def kontor_temp():
    timestamps, temp, hum = get_kontor_dht11_data(10)
    
    fig = Figure()
    ax = fig.subplots()
    ax.plot(timestamps, temp, c = "#11F", marker = "o")
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(6, 5.5)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature Celsius")
    ax.invert_xaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def kontor_hum():
    timestamps, temp, hum = get_kontor_dht11_data(10)
    
    fig = Figure()
    ax = fig.subplots()
    ax.plot(timestamps, hum, c = "#11F", marker = "o")
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(6, 5.5)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Humidity %")
    ax.invert_xaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

@app.route("/kontor/")
def kontor():
    timestamps, status, battery = get_motor_data(1)
    battery_percentage = str(battery).strip("[]")
    
    window = 'Closed'
    if status == [0]:
        window = 'Lukket'
    if status == [1]:
        window = 'Åbent'

    kontor_cotwo = kontor_co2()
    kontor_temperature = kontor_temp()
    kontor_humidity = kontor_hum()
    return render_template('kontor.html', kontor_cotwo = kontor_cotwo, kontor_temperature = kontor_temperature, kontor_humidity = kontor_humidity, battery_percentage = battery_percentage, window = window)

def vejrst_temp():
    timestamps, temp, hum, battery = get_vejrst_sensor_data(10)
    
    fig = Figure()
    ax = fig.subplots()
    ax.plot(timestamps, temp, c = "#11F", marker = "o")
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 6)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature")
    ax.invert_xaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def vejrst_hum():
    timestamps, temp, hum, battery = get_vejrst_sensor_data(10)
    
    fig = Figure()
    ax = fig.subplots()
    ax.plot(timestamps, hum, c = "#11F", marker = "o")
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 6)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Humidity %")
    ax.invert_xaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def pir_data():
    timestamps, pir_tal = get_tyveri_sensor_data(500)

    time_list = []
    x = 0
    for i in timestamps:
        time = f"{(str(timestamps[x])[9:11])}:00"
        date = f"D. {(str(timestamps[x])[:5])}"

        time_date = str(time), str(date)
        time_date = str(time_date)
        time_date = time_date.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
        time_list.append(time_date)


        x += 1
    

    time_dict = {i:time_list.count(i) for i in time_list}

    hours_date = time_dict.keys()
    dubli = time_dict.values()

    hours_date, dubli = zip(*time_dict.items())
    hours_date = list(hours_date)
    dubli = list(dubli)

    fig = Figure()
    ax = fig.subplots()

    ax.bar(hours_date, dubli)
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 6)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_xlabel("Timestamp")
    ax.invert_xaxis()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

@app.route("/vejrstation/")
def vejrstation():
    timestamps, temp, hum, battery = get_vejrst_sensor_data(1)
    vejrst_temperature = vejrst_temp()
    vejrst_humidity = vejrst_hum()
    battery_percentage = str(battery).strip("[]")
    return render_template('vejrstation.html', vejrst_temperature = vejrst_temperature, vejrst_humidity = vejrst_humidity, battery_percentage = battery_percentage)

@app.route("/tyverialarm/")
def tyverialarm():
    tyveri_sensor_data = pir_data()
    last_pir_data = get_tyveri_sensor_data(1)
    last_pir_data = f" {str(last_pir_data[0])[2:19]}"
    return render_template('tyverialarm.html', tyveri_sensor_data = tyveri_sensor_data, last_pir_data = last_pir_data)

if __name__ == "__main__":
    app.run()