VT4002
======

Python program to control Votsch VT 4002 Thermal Chamber over a serial port.

More details about the VT 4002 EMC is available here:
http://www.v-it.com/en/products/temperature_and_climate_test_chambers/schunk01.c.59549.en?_pid=52043

The software supplied along with the Thermal Chamber works only in Windows.
This was an attempt to create a GNU/Linux solution and Python was the most 
logical choice to achieve it.

Please refer the spec (VT4002_climate_chamber.pdf) if you want to know 
more about it.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

-------------------------------------------------------------------------------

Converted into Python3 like code. Some parametrization (port, address).
Tested on WXP.

The driving/monitoring functions "set_temp" and "read_temp" are now located in VT4002.py module. The module can be run itself, providing some parameters (for example "VT4002.py -p COM3 -t -15 -s ON" to start cooling at -15C or "VT4002.py -p COM3" to read setted and actual temperature and ON/OFF status).
There is a simple GUI for testing VT4002.py module named VT4002_test.pyw - not perfect, but good example howto use it.

VT4002_climate_chamber.pdf file was removed from the git repo - I shouldn't be included in GPL project (I think). Please google it if you need it (or dig it from the repo history).