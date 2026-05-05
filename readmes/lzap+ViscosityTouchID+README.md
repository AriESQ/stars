## Viscosity TouchID Helper

What you need:

- Viscosity
- Password
- OTP TOKEN URL

Download from the Releases page:

https://github.com/lzap/ViscosityTouchID/releases

How to compile it yourself:

	make install

## First use

The first use must be done via MacOS Terminal, just run the app:

	/Applications/VisTouchID.app/Contents/MacOS/VisTouchID

It will ask for three things:

	Password: YOURPWD
	OTP Token URL: http://874389436289643984623...
	VPN Profile: My Home VPN

It stores the data in MacOS Keychain under VisTouchID key.

## How it works

Then just run it from the command line or dock to connect to the VPN. It always
requires fingerprint or password check. It also assumes that username is already
pre-filled in the Viscosity dialog.

It concatenates your password and OTP together and confirms the dialog.

During the second run, MacOS will ask to allow permission to "control your
system", because it uses Automation via Apple Script to type your credentials.
You need to confirm this.

It will also asks you to allow Keychain access once, or forever by typing in
your MacOS password.

## License

PUBLIC DOMAIN

Use with care, check your company policy before using this helper.
