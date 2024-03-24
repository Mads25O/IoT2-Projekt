import sqlite3
from datetime import datetime

def get_kontor_dht11_data(number_of_rows):
    
    query = """SELECT * FROM kontor_dht11 ORDER BY datetime DESC;"""
    
    datetimes = []
    temperatures = []
    humidities = []


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            datetimes.append(row[0])
            temperatures.append(row[1])
            humidities.append(row[2])
        return datetimes, temperatures, humidities

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_kontor_ccs811_data(number_of_rows):
    
    query = """SELECT * FROM kontor_ccs811 ORDER BY datetime DESC;"""
    
    datetimes = []
    co2 = []


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            datetimes.append(row[0])
            co2.append(row[1])
        return datetimes, co2

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_motor_data(number_of_rows):
    
    query = """SELECT * FROM motor ORDER BY datetime DESC LIMIT 1;"""

    timestamps = []
    motor_status = []
    battery = []

    try:
        conn = sqlite3.connect("database/motor.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            timestamps.append(row[0])
            motor_status.append(row[1])
            battery.append(row[2])
        return timestamps, motor_status, battery

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_vejrst_sensor_data(number_of_rows):
    query = """SELECT * FROM vejrstation ORDER BY datetime DESC LIMIT 10;"""
    
    datetimes = []
    temperatures = []
    humidities = []
    battery = []


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            datetimes.append(row[0])
            temperatures.append(row[1])
            humidities.append(row[2])
            battery.append(row[3])
        return datetimes, temperatures, humidities, battery

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_tyveri_sensor_data(number_of_rows):
    query = """SELECT * FROM tyverialarm ORDER BY datetime DESC;"""
    
    datetimes = []
    motion = []


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            datetimes.append(row[0])
            motion.append(row[1])
        return datetimes, motion

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()