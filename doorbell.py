#!/usr/bin/python
# doorbell.py
#
# Copyright 2014 Thomas Sigurdsen <thomas.sigurdsen@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import RPi.GPIO as gpio
from time import sleep
import subprocess


class Rpi(object):

    def __init__(self):
        gpio.setwarnings(True)
        gpio.setmode(gpio.BCM)
        self.rpin = 17
        gpio.setup(self.rpin, gpio.IN)
        self.lightsOn = False
        self.lightsWasOn = False
        self.sendLightsOn()
        self.DEBUG = 0

    def __exit__(self):
        gpio.cleanup()

    def sendLightsOn(self):
        action = "./doorbell.sh "
        if self.lightsOn:
            arg = "True"
        else:
            arg = "False"
        subprocess.call(["ssh", "brhive", action, arg])

    def run(self):
        if self.DEBUG > 0:
            print "PIN: %d has value: " % self.rpin, gpio.input(self.rpin)
        self.lightsWasOn = self.lightsOn
        self.lightsOn = gpio.input(self.rpin)
        if self.lightsOn is not self.lightsWasOn:
            self.sendLightsOn()


def main():
    try:
        pi = Rpi()
        while True:
            pi.run()
            sleep(2)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
