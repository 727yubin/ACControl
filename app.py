'''
# Copyright 2018 Yubin Lee <727yubin@gmail.com>
# Released under CC BY-NC-SA
# Based on Rui Santos' code, found at randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/.
#Used under a CC BY-NC-SA license.
'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

app = Flask(__name__)

users = {
	"user" : generate_password_hash('user') # For added security, run this beforehand, and put the resulting string in place of generate_password_hash()
}

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
	2 : {'name' : 'AC 1', 'state' : GPIO.LOW},
	3 : {'name' : 'AC 2', 'state' : GPIO.LOW},
	4 : {'name' : 'AC 3', 'state' : GPIO.LOW},
	14 : {'name' : 'AC 4', 'state' : GPIO.LOW},
	15 : {'name' : 'AC 5', 'state' : GPIO.LOW},
	17 : {'name' : 'AC 6', 'state' : GPIO.LOW},
	18 : {'name' : 'AC 7', 'state' : GPIO.LOW},
	22 : {'name' : 'AC 8', 'state' : GPIO.LOW},
	23 : {'name' : 'AC 9', 'state' : GPIO.LOW},
	27 : {'name' : 'AC 10', 'state' : GPIO.LOW},
	}

@auth.verify_password
def verify_password(username, password):
	if username in users:
		return check_password_hash(users.get(username), password)
	return False

@app.route('/')
@auth.login_required
def index():
	return redirect("/app", code = 302)

# Set each pin as an output and make it low:
for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

@app.route("/app")
def main():
	# For each pin, read the pin state and store it in the pins dictionary:
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)
	# Put the pin dictionary into the template data dictionary:
	templateData = {'pins' : pins}

	# Pass the template data into the template main.html and return it to the user
	return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/app/<changePin>/<action>")
def action(changePin, action):
	# Convert the pin from the URL into an integer:
	changePin = int(changePin)
	# Get the device name for the pin being changed:
	deviceName = pins[changePin]['name']
	# If the action part of the URL is "on," execute the code indented below:
	if action == "on":
		# Set the pin high:
		GPIO.output(changePin, GPIO.HIGH)
		# Save the status message to be passed into the template:
		message = "Turned " + deviceName + " on."
	if action == "off":
		GPIO.output(changePin, GPIO.LOW)
		message = "Turned " + deviceName + " off."

	# For each pin, read the pin state and store it in the pins dictionary:
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)

	# Along with the pin dictionary, put the message into the template data dictionary:
	templateData = {'pins' : pins}

	return render_template('main.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)