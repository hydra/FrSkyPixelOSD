FrSkyOSD v2.0.0-beta.2 (20200622)
=================================

## New features

- Added support for uploading user programs to the OSD using
  the Pawn language, run them and invoke their public functions
  remotely from the UART API.
- Added user configurable brightness, horizontal offset and vertical
  offset. These parameters allow configuring the OSD to match your
  own setup better and can be easily changed with the [FrSky OSD
  app](https://github.com/FrSkyRC/FrSkyOSDApp/releases).
- Added high level widget and very optimized implementations that
  can be used to draw complex elements with minimal code on the host
  side.
- Added artificial horizon widget, with ladder and line styles.
- Added sidebar widget, with ability to scroll and display a labelled
  value that automatically converts between units in order to use
  the same amount of digits.
- Added graph widget, which displays a graph with a value changing
  over time. The graph automatically changes scale and offset in
  response to the provided data and might optionally contain labels.
- Added a character based gauge widget that can be used to display
  a battery meter with a single character and painting over a
  region of the character defined in its metadata.
- New APIs for reducing the amount of data sent to perform some
  operations, specially character drawing and matrix manipulation.
- Python SDK and OSD simulator are now publicly available for
  developers, to make developing programs that interact with the OSD
  easier.

## Improvements

- Font rastering has been made ~3.5x faster, leaving more room
  for drawing vector graphics.
- Runtime penalty for bitmap color inversion has been reduced by 50%.
  Drawing color inverted bitmaps is still slower than non color
  inverted ones, but the difference is much smaller.
- Signal detection has been made more tolerant with non standard
  compliant cameras.
- Video overriding output has been made ~25% faster, leaving more
  time for actual drawing.

## Fixes

- Fixed incompatibilities with some NTSC cameras
- Fixed slightly incorrect timings in NTSC video generation that
  could produce an incorrect image with some goggles/screens.
- Fixed incorrect transaction counter reset that could cause
  flickering under some specific circumstances.

## Fixes since beta1

- Fixed overflow in sidebar label when using left orientation.
- Fixed crashes in edge cases of the graph widget.
- Fixed incorrect index adressing in the chargauge widget.

## Changes since beta1
- Optimized graph widget rendering.
- Make graphs immediate instead of batching updates by default.
- Change graphs from using 16 bit integers to 24 bits for increased precision.
- Added support for the graph widget in the Python SDK.
- Allow `counts_per_step == 0` in static sidebar widgets.
- Improved shape filling algorithms, making them ~25% faster.
- Make the simulator always print a warning message when an error is returned to the host.
- Added support for showing the character grid in the simulator.

## Testing version 2.0.0-beta2

- Follow the [general instructions for firmware upgrades](README.md).
- Download a nightly build of INAV from [here](https://github.com/iNavFlight/inav/actions/runs/144061316)
  and flash your flight controller with it.
- Download a nightly build INAV configurator from [here](https://drive.google.com/drive/folders/1qLdovu8kmf0oxgtOjjjhycgF4comZlsL) in order to be able to configure INAV (latest stable release won't work).
- Update the font in the OSD from the nightly build of the configurator.
- No further configuration is required.
- If you find any bugs in the OSD, please open an issue in this
  repository. If after investigating the problem, turns out the bug is
  in INAV/BF instead of the OSD we'll forward the issue appropriately.
- Last but not least, thank you so much for helping us testing the
  beta for version 2.0!
