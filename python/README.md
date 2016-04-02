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
