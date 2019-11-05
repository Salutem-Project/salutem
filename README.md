# Salutem

Safety System focused around tracking the location of each user.

## High-level ideals

The system is constructed of three key parts: remotes, base stations, and a central server to process information.  
The remotes will consist of BLE devices with two buttons on the face that, when pressed, emit a signal that specify the user is in distress. The devices will emit a signal every 800ms containing the ID of the device.  
Each base station will look for BLE signals, any signals received are forwarded to the central server along with the signal strength and the ID of the current base station.  
The central server accepts the information from each of the base stations and logs each signal record. Every 3000ms, the central server looks at the previous information and calculates the suggested location of each device. In the case a signal for an active remote isn't recorded for 20 seconds, an SOS is assumed.  

The central server is also in charge of presenting the information to any security personnel.

## API Logical Resources

`_GeneralAPI` - Used as a base for all other resources. This creates an interface with the database and provides defaults for error's and general handling.
