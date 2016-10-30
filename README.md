# LentoDVD Speed Limiter

Control the maximum speed of your DVD/CD drive from the system tray.
Works with Ubuntu Unity and Gnome.

Uses the `eject` tool to set the speed limit.

![alt tag](https://raw.githubusercontent.com/sneakypete81/lento_dvd/gh-pages/img/lento_dvd_screenshot.png)

# Usage

**Install**:

    $ sudo apt-get install eject
    $ sudo pip install git+https://github.com/sneakypete81/lento_dvd.git

**Run**

To run *LentoDVD*, start it from Unity Dash or Gnome Desktop Menu (whichever
desktop you use).

# Development

## Project directory layout

- `bin/` - entry point scripts
- `img/` - image files used in runtime (icons)
- `lento_dvd/` - root application package (all source code)
- `Makefile` - provides basic tasks for development
- `setup.py` - python packaging script
- `README` - readme file for distributed package
- `README.md` - this file

## Python 2 and Python 3

Current indicator implementation runs on both Python 2.7 and Python 3. All
tests are as well executed on "both pythons".

## Running and testing

**Running tests**

    $ make venv  # run only once, or run again to re-create the virtualenv
    $ make tests

**Getting test coverage (reports to ./coverage/)**

    $ make cover

**Creating python source package**

    $ make sdist

**Running without installing**

    $ make run

**Building and installing/uninstalling locally**

    $ sudo make install
    $ sudo make uninstall

**Cleaning up the project directory (remove dist/, \*.pyc, etc.)**

    $ make clean

**Reminder - release process**

1. Make changes, update and run tests, ensure good coverage
2. Update setup.py and change the version according to [semantic versioning](http://semver.org/)
3. Tag new version; tag format is 'vX.Y.Z'; e.g.: v1.2.1
4. Push changes and a new tag

# Copying

Copyright 2016, [Pete Burgers](https://github.com/sneakypete81)

This Application Indicator is distributed under
[GNU GENERAL PUBLIC LICENSE](http://www.gnu.org/licenses/gpl.html),
either version 3 of the License, or (at your option) any later version.

![GPLv3](http://www.gnu.org/graphics/gplv3-88x31.png)

Boilerplate code adapted from [Vagrant AppIndicator](https://github.com/candidtim/vagrant-appindicator),
thanks @candidtim!
