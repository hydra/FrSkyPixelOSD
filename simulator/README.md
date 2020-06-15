FrSky Pixel OSD Simulator
========================

The FrSky Pixel OSD simulator is a command line application that simulates an
instance of the real hardware, using the same drawing engine and showing its
output in a GUI window.

By default, the simulator listens on localhost on TCP port 1983, but it can
also use a serial port so with the help of an UART-to-USB adapter any device
can be connected to the simulator while thiking its talking to the real hardware.
This allows doing development on devices that interact with the OSD without
having to use a dedicated screen or an AV-to-USB video adapter.

The simulator supports exactly the same API and functions as the real device,
including font uploads, widgets and the virtual machine.

Additionaly, it's able to provide more detailed error messages in case of
errors (via the console). It also prints other interesting statistics that
can help you understand how your application interacts with the OSD better.

Use `osd-simulator --help` to list all the available help options. When its
GUI window is open, you can also press `h` to get a list of the available
keyboard commands.


## Dependencies

macOS and Windows binaries are fully static and shouldn't need any libraries.
However, Linux binaries require SDL2 and SDL\_ttf2 to be installed in the system.

## Acknowledgements

The Pixel OSD simulator bundles a copy of the Vision OSD font designed by
[Olivier C](https://www.youtube.com/channel/UC7dLZs5jMR1DLFT8V5fWnsQ).
