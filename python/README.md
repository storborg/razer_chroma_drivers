# razerdriver

A Python module to control the razer-chroma-driver kernel module via device
file reads/writes. Currently only supports keyboards.

### Install

Use pip to install directly from this directory:

    $ pip install -e .

### Use

Quick start:

    >>> import razerdriver

    >>> devices = razerdriver.find_devices()
    >>> devices

    >>> device = devices[0]
    >>> device.set_reactive_mode((255, 0, 0))
    >>> device.set_static_mode((0, 255, 255))
    >>> device.set_breath_mode((0, 0, 255), (255, 0, 0))

A few examples are in the ``examples/`` directory. Note that they may require
additional dependencies, including ``numpy`` and ``PyAudio``.

### Silly Keyboard Ideas

- monitor system parameters (temperature, cpu load, etc)
- monitor external data (weather, time of day, location)
- RF spectrum (either wifi/ble usage or SDR input)
- snake game (implemented)
- simon game (partially implemented)
- tetris? can this work on a 6x16 grid? probably not
- pong?
- music/audio visualization (some basic playing around with pyaudio)
- xorg display driver
- "ambilight" style where bottom of screen is used to control colors
- better reactive effects... maybe water ripples emanating from keypresses
- notifications (flash/change color for email, etc)
- key heatmap visualization
