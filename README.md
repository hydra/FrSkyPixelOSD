# PixelOSD
PixelOSD is a pixel-based OSD product launched by FrSky.
It allows users to set the content and location of the OSD based on graphics.The protocol & API interface definition are public to whom
may want to develop on it.

## OSD Modules
At present, there are two kinds of products: independent OSD module for average user and OSDMini for FC factory.
It can totally replace the MAX7456 solution and bring graphic features.

Up to now, iNav,Betaflight,ArduPilot are all working on supporting on it.


### Standalone OSD module
#### Specifications:
* Size:              19x18x3 (LxWxH in mm)
* Current:           38mA @ 5V
* Operating Voltage: 5v
* Weight：           1.5g

#### Interface
* +5v：      VCC 5V
* VID_GND:   Video GND
* VID_IN:    Video Input
* VID_OUT:   Video Output
* RX/TX:     USART to Flight Controller

### OSDMini for Flight controller factories
#### Specifications:
* Size:              7x7x2 (LxWxH in mm)
* Current:           35mA @ 3.3V
* Operating Voltage: 3.3v
* Weight：           <1g

#### Interface
* 3.3v：   VCC 3.3V
* GND:     GND
* RX/TX:   USART to Flight Controller
* VI:      Video Input
* VO:      Video Output
* D/C/G:   Program Port
