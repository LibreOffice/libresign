# LibreOffice Appliances project's "LibreSign"

# Install

To install use pip (only Python 3 is supported)
```
pip install libresign
```

# Running

```
libresign [ --onlyweb ] [ --noinfo ] [ --nolibreoffice ] [ --sign ] [ --conference ] [ --noremote ] [ --libresign-home ]

--onlyweb: Run only the web server for the control panel (--nolibreoffice --noinfo)
--noinfo: Don't show the information screen.
--nolibreoffice: Don't start LibreOffice.
--sign: Run in digital signage mode.
--conference: Run in conference mode. (default)
--noremote: Don't run the Impress Remote web server.
--libresign-home: Specify the installation directory of libresign. (default: ~/.libresign)
```

The program has been tested on Debian Testing and Arch Linux ARM on the Raspberry Pi 3 B+.

# Development


For development, use the supplied debug.sh script to automatically set up and run the program after you've made your changes,

```
git clone https://github.com/LibreOffice/libresign
cd libresign
./debug.sh
```

You can also create a package and install it manually

```
python setup.py sdist
pip install dist/libresign-x.x.x.tar.gz
```

The code is in the `libresign` directory, the Flask templates and other files are in `templates` and `static`. `signd.py` is the entry point which runs the Flask app (`flaskapp.py`), the informational screen (`infoscreen.py`) and LibreOffice (`locontrol.py`).

# Background

This is one of four repositories - and the main one - created for the 2019 GSOC project "LibreOffice Appliances", intended to create a [digital signage](https://en.wikipedia.org/wiki/Digital_signage) solution using [LibreOffice](https://libreoffice.org) Impress. 

The other three repositories are [JavaScript Impress Remote client](https://github.com/rptr/impress-remote-js), [JavaScript Impress Remote server](https://github.com/rptr/irpjs) and [JavaScript Impress Remote Protocol library](https://github.com/rptr/irpjs-client).

The original project proposal can be found [here](https://docs.google.com/document/d/1FZKM2I_5Fc2ENsLxlMmkWTo6GJaS8_QHiYEERIVxVfY/edit).

In short, the aim was to create a program which would run on a single-board computer (a Raspberry Pi was used during development) connected to a TV screen displaying LibreOffice Impress presentations automatically. A "conference mode" was also added, where users can upload presentations, select them to be played and then control the presentation with the Impress Remote. For this the JavaScript/ browser version of the Impress Remote was created as part of the GSOC project.

## Wishlist

Feel free to add anything here.

## Contributors

Rasmus P J <wasmus@zom.bi>

