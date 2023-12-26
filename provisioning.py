import tkinter as tk
import requests

def update_wifi_credentials():
    ssid = ssid_entry.get()
    password = password_entry.get()
    payload = {'ssid': ssid, 'pass': password}
    url = 'http://192.168.4.1/setting'  # Assuming the ESP8266 server is running at this address
    try:
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            status_label.config(text="Credentials updated successfully!")
        else:
            status_label.config(text="Failed to update credentials")
    except requests.RequestException as e:
        status_label.config(text=f"Request failed: {e}")

# Create GUI
root = tk.Tk()
root.title("WiFi Credentials Setup")

ssid_label = tk.Label(root, text="SSID:")
ssid_label.pack()

ssid_entry = tk.Entry(root)
ssid_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")  # Show '*' for password
password_entry.pack()

update_button = tk.Button(root, text="Update Credentials", command=update_wifi_credentials)
update_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
