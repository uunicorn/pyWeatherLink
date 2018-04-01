"""

    This file is part of the pyWeatherLink package,
    Copyright 2008 by Henrik Persson <root@fulhack.info>.

    pyWeatherLink is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    pyWeatherLink is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyWeatherLink.  If not, see <http://www.gnu.org/licenses/>.

"""

from math import log

def f2c(f):
    c = (f-32) * (5.0/9.0)
    return round(c, 1)

def mph2kts(mph):
    kts = mph * 0.868976242
    return round(kts, 2)

def inHg2hPa(inHg):
    return inHg * 33.8638816

# constants
a = 17.271
b = 237.7 # degC

def gamma(T,RH):
    g = (a * T / (b + T)) + log(RH/100.0)
    return g

def dewpoint_approximation(T, RH):
    gm = gamma(T,RH)
    Td = (b * gm) / (a - gm)
    
    return Td
