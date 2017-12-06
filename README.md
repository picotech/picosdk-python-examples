# picosdk-python-examples

*picosdk-python-examples* contains an example Python module for PicoScope oscilloscopes.

## Getting started

### Prerequisites

* A PicoScope oscilloscope using one of the following PicoScope drivers:
  * ps2000
  * ps2000a
  * ps3000
  * ps3000a
  * ps4000
  * ps4000a
  * ps5000a
  * ps6000
* [Python 2.7](https://www.python.org/download/releases/2.7/) 

#### Microsoft Windows

* For best experience on Microsoft Windows [Python(x,y)](https://python-xy.github.io/) suite is recommended.

#### Linux and Mac OS X

* For Streaming mode data collection, the [pytables](http://www.pytables.org/) module is required.
* The `block_capture` and `streaming_capture` examples require [matplotlib](http://matplotlib.org/) and [signal](https://docs.python.org/2/library/signal.html).
* PicoPyScope example has been written for use with [PyQtGraph](http://www.pyqtgraph.org/).

**Notes:** The code is not much different from Python3 and can be easily converted with the [2to3](https://docs.python.org/2/library/2to3.html) utility.
The module has been tested and proved working on Linux (including ARM derivatives), Microsoft Windows and Mac OS X.

### Installing drivers

Drivers are available for the following platforms. Refer to the subsections below for further information.

#### Microsoft Windows

* Download the PicoSDK (32-bit or 64-bit) driver package installer from our [Downloads page](https://www.picotech.com/downloads).

#### Linux

* Follow the instructions from our [Linux Software & Drivers for Oscilloscopes and Data Loggers page](https://www.picotech.com/downloads/linux) to install the required driver packages for your product.

#### Mac OS X

* Visit our [Downloads page](https://www.picotech.com/downloads) and download the PicoScope Beta for Mac OS X application.

### Installing the python driver bindings

A `distutils` installer is provided. After you have installed the PicoSDK
driver package (see above), the Python installer can be used as follows:

    python setup.py install

on macOS and Linux you will either need to use `sudo` with this command, to
install into the system folders, or to install for the current user only you
can use:

    python setup.py install --user

Within python, the library for `import` is called `picosdk`.

### Scripts

#### python-picoscope

* block_capture.py - comprehensive suite for testing block collection (-h to see all options)
* stream_capture.py - streaming testing utility, including some performance tests (-h to see all options)
* picopyscope.py - simple PC oscilloscope UI

**Note:** A basic script requires just a few lines as below. Most functions have been decorated with docstrings.

```python
from picosdk import ps2000

if __name__ == "__main__":
    ps = ps2000.Device()
    status = ps.open_unit()
    if status == ps.m.pico_num("PICO_OK"):
        s, state = ps.get_channel_state(channel=ps.m.Channels.A)
        state.enabled = True
        state.range = ps.m.Ranges.r5v
        status = ps.set_channel(channel=ps.m.Channels.A, state=state)
        if status == ps.m.pico_num("PICO_OK"):
            s, index = ps.locate_buffer(channel=ps.m.Channels.A,
                                        samples=1000,
                                        segment=0,
                                        mode=ps.m.RatioModes.raw,
                                        downsample=0)
            status = ps.collect_segment(segment=0, interval=1000)
            if status == ps.m.pico_num("PICO_OK"):
                status, data = ps.get_buffer_volts(index=index)
                print data
                exit(0)
    print ps.m.pico_tag(status)
```

### Programmer's Guides

You can download Programmer's Guides providing a description of the API functions for the relevant PicoScope or PicoLog driver from our [Documentation page](https://www.picotech.com/library/documentation).

## Obtaining support

Please visit our [Support page](https://www.picotech.com/tech-support) to contact us directly or visit our [Test and Measurement Forum](https://www.picotech.com/support/forum17.html) to post questions.

## Contributing

Contributions are welcome. Please refer to our [guidelines for contributing](.github/CONTRIBUTING.md) for further information.

## Applications written by our customers

The following are Python examples written by our customers:

* [pico-python](https://github.com/colinoflynn/pico-python)
* [PicoPy](https://github.com/hgomersall/PicoPy)
* [picotools](https://github.com/znuh/picotools)
* [TC08-Command-Line](https://github.com/timfish/TC08-Command-Line)
* [usbtc08](https://github.com/bankrasrg/usbtc08)
* [picostream](https://github.com/jbentham/picostream)

## Copyright and licensing

See [LICENSE.md](LICENSE.md) for license terms. 

*PicoScope* and *PicoLog* are registered trademarks of Pico Technology Ltd. 

*Windows* is a registered trademark of Microsoft Corporation. 

*Mac* and *OS X* are registered trademarks of Apple, Inc. 

*Linux* is the registered trademark of Linus Torvalds in the U.S. and other countries.

Copyright © 2014-2017 Pico Technology Ltd. All rights reserved. 
