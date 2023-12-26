from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt
import json

root=Tk()
root.geometry('800x400')

#########       Connection Establish        #################
aws_iot_endpoint = 'a2ab8m2ptljxzx-ats.iot.eu-north-1.amazonaws.com'
port = 8883  # MQTT port for AWS IoT Core
cert_file = 'C:/Users/spiri/PycharmProjects/IOT_Gen1/device_cert.crt' # Path to your device certificate
key_file = 'C:/Users/spiri/PycharmProjects/IOT_Gen1/private_key.key' # Path to your device private key
ca_file = 'C:/Users/spiri/PycharmProjects/IOT_Gen1/amazon.pem' # Path to the root CA certificate
topic1 = 'sensors/pub' #Publish
topic2 = 'sensors/sub' #Subscribe
#########       Connection Establish        #################

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic1)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    update_icons(payload)
    # Process the received data here
def update_icons(data):
    # Assuming data contains temperature, humidity, and soil moisture values
    temperature = data.get('temperature', '')
    humidity = data.get('humidity', '')
    soil_moisture = data.get('soil_moisture', '')

    # Update icons or images for temperature, humidity, and soil moisture
    update_temperature_icon(temperature)
    update_humidity_icon(humidity)
    update_soil_moisture_icon(soil_moisture)
def update_temperature_icon(temperature):
    temperature_label.configure(text=f"Temperature: {temperature} °C")

def update_humidity_icon(humidity):
    humidity_label.configure(text=f"Humidity: {humidity}%")

def update_soil_moisture_icon(soil_moisture):
    soil_moisture_label.configure(text=f"Soil Moisture: {soil_moisture}%")

Label_frame = customtkinter.CTkFrame(root,width=600,height=300)
Label_frame.propagate(0)
Label_frame.pack(side="left")

temperature_label = customtkinter.CTkLabel(Label_frame, text="Temperature: \n")
temperature_label.pack(side="left",padx=10,pady=10)

humidity_label = customtkinter.CTkLabel(Label_frame, text="Humidity: \n")
humidity_label.pack(side="left",padx=10,pady=10)

soil_moisture_label = customtkinter.CTkLabel(Label_frame, text="Soil Moisture: \n")
soil_moisture_label.pack(side="left",padx=10,pady=10)

def publish_messages(message):
    client.publish(topic2,json.dumps(message),qos=0)

def Room1():
    publish_messages('ON1')

def Room2():
    publish_messages('OFF1')

def Room3():
    publish_messages('ON3')


def Room4():
    publish_messages('OFF3')


Buttons_frame = customtkinter.CTkFrame(root,width=200,height=200)
Buttons_frame.propagate(0)
Buttons_frame.pack()

room1_button = customtkinter.CTkButton(Buttons_frame,text="Room1",width=40,corner_radius=10,hover_color="pink",command=Room1)
room1_button.pack(pady=10)

room2_button = customtkinter.CTkButton(Buttons_frame,text="Room2",width=40,corner_radius=10,hover_color="pink",command=Room2)
room2_button.pack(pady=10)

room3_button = customtkinter.CTkButton(Buttons_frame,text="Room3",width=40,corner_radius=10,hover_color="pink",command=Room3)
room3_button.pack(pady=10)

room4_button = customtkinter.CTkButton(Buttons_frame,text="Room4",width=40,corner_radius=10,hover_color="pink",command=Room4)
room4_button.pack(pady=10)

# Initialize MQTT client
client = mqtt.Client()
client.tls_set(certfile=cert_file,keyfile=key_file,ca_certs=ca_file)
client.on_connect = on_connect
client.on_message = on_message

# Connect to AWS IoT Core
client.connect(aws_iot_endpoint, port=port, keepalive=60)
def start_update_icons():
    data={'temperature':20,'humidity':20,'soil_moisture':20}
    update_icons(data)

# Function to start MQTT loop and Tkinter main loop
def start_mqtt_and_tkinter():
    # Loop to maintain the connection and handle incoming messages
    client.loop_start()
root.after(1000,start_update_icons)
# Start both MQTT loop and Tkinter main loop in a separate thread or process
start_mqtt_and_tkinter()

root.mainloop()