import serial
import paho.mqtt.client as mqtt
from datetime import datetime
import time 

# Serial port configuration
serial_port = 'COM7'
baud_rate = 9600

# MQTT Broker configuration
mqtt_broker = "jrgh91.cloud.shiftr.io"
mqtt_port = 1883
mqtt_topic = "jrgh/temp"
mqtt_username = "jrgh91"  
mqtt_password = "LPV1ZzHPMxFrRjJz"  

# Connect to MQTT Broker
mqtt_client = mqtt.Client(client_id="")  
mqtt_client.username_pw_set(mqtt_username, mqtt_password)  

try:
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
    exit(1)

# Connect to the serial port
ser = serial.Serial(serial_port, baud_rate)

def publish_serial_data_to_mqtt():
    start_time = time.time()  # Record the start time
    duration = 10 * 60  # (10 minutes)
    
    while True:
        current_time = time.time()  # Get the current time
        elapsed_time = current_time - start_time  # Calculate elapsed time

        if elapsed_time >= duration:
            print("10 minutes have passed. Ending script.")
            break
        
        try:
            # Read from the serial port
            serial_line = ser.readline().decode('utf-8').strip()
            
            # Generate a timestamp
            timestamp = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
            
            # Combined message with the timestamp and the serial data
            message = f"{timestamp}, {serial_line}"
            
            # Publish the message to the MQTT topic
            mqtt_client.publish(mqtt_topic, message)
            print(f"{message}")
            
            
        except KeyboardInterrupt:
            print("Stopping...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    try:
        publish_serial_data_to_mqtt()
    finally:
        ser.close()  # Ensure serial connection is closed on exit
