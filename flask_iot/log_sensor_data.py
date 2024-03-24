import sqlite3
from datetime import datetime, timedelta

def create_table(table_name, column_name, database_path):
    
    query = f"""CREATE TABLE IF NOT EXISTS {table_name} (datetime TEXT NOT NULL, {column_name});"""

    try:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()

def log_kontor_dht11_data(temp, hum):
    
    create_table('kontor_dht11', 'temperature INT NOT NULL, humidity INT NOT NULL', 'database/sensor_data.db')

    query = """INSERT INTO kontor_dht11 (datetime, temperature, humidity) VALUES (?, ?, ?);"""

    now = datetime.utcnow()+timedelta(hours=1)
    now = now.strftime("%d/%m/%y %H:%M:%S")
    data =  (now, temp, hum)


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()

def log_kontor_ccs811_data(co2):
    
    create_table('kontor_ccs811', 'co2 INT NOT NULL', 'database/sensor_data.db')

    query = """INSERT INTO kontor_ccs811 (datetime, co2) VALUES (?, ?);"""

    now = datetime.utcnow()+timedelta(hours=1)
    now = now.strftime("%d/%m/%y %H:%M:%S")
    data =  (now, co2)


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()

def log_vejrst_data(temp, hum, battery):

    create_table('vejrstation', 'temperature INT NOT NULL, humidity INT NOT NULL, battery INT NOT NULL', 'database/sensor_data.db')

    query = """INSERT INTO vejrstation (datetime, temperature, humidity, battery) VALUES (?, ?, ?, ?);"""

    now = datetime.utcnow()+timedelta(hours=1)
    now = now.strftime("%d/%m/%y %H:%M:%S")
    data =  (now, temp, hum, battery)


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()

def log_motor_data(status, battery):
    
    create_table('motor', 'status INT NOT NULL, battery INT NOT NULL', 'database/motor.db')

    query = """INSERT INTO motor (datetime, status, battery) VALUES (?, ?, ?);"""

    now = datetime.utcnow()+timedelta(hours=1)
    now = now.strftime("%d/%m/%y %H:%M:%S")

    data =  (now, status, battery)

    try:
        conn = sqlite3.connect("database/motor.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()

def log_motor_status(status):

    create_table('motor', 'status INT NOT NULL, battery INT', 'database/motor.db')

    query = """INSERT INTO motor (datetime, status, battery) VALUES (?, ?, ?);"""

    now = datetime.utcnow()+timedelta(hours=1)
    now = now.strftime("%d/%m/%y %H:%M:%S")

    data =  (now, status)

    try:
        conn = sqlite3.connect("database/motor.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()

def log_pir_data():

    create_table('tyverialarm', 'motion_detected INT NOT NULL', 'database/sensor_data.db')

    query = """INSERT INTO tyverialarm (datetime, motion_detected) VALUES (?, ?);"""

    now = datetime.utcnow()+timedelta(hours=1)
    now = now.strftime("%y-%m-%d %H:%M:%S")
    print(now)
    data = (now, 1)


    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()