# GPIOControl
Controlling Raspberry Pi GPIO Pins from a Web Browser

The principal of my school had an idea to control ACs over a network via a Raspberry Pi, instead of switching on the circuit breakers on the other side of the corridors every day.

This program sets up a website that needs credentials to log in, and provides 10 buttons to control 10 GPIO pins. More can be added to the dictionary of pins.

# Dependencies
- A Raspberry Pi running Raspbian
- Python 3
- Flask (`sudo pip3 install Flask`)
- A network connection

# Execution
1. Connect ACs (or LEDs to test) to GPIO pins in the program. This program uses Broadcom numbering.
2. Make sure `app.py` and `templates/` are in the same folder.
3. Run `sudo python3 app.py`
4. Log in using credentials (defaults: username `user` password `user`)
5. Control away!

Notes:
To add credentials, place the following in the `users.csv` file:
`username,hashed_password` with a new account-password pair on every new line.
Generate the hashed password in Python 3 by executing the following:
```
>>> from werkzeug.security import generate_password_hash, check_password_hash
>>> generate_password_hash("your_desired_password")
```

License: CC BY-NC-SA
