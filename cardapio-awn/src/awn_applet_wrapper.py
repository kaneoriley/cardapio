# Copyright (C) 2010 Pawel Bara (keirangtp at gmail com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from awn.extras import awnlib, __version__

from AwnApplet import AwnApplet

if __name__ == "__main__":
	awnlib.init_start(AwnApplet, {
		"name"           : "Cardapio's applet",
		"short"          : "cardapio",
		"version"        : __version__,
		"description"    : "Replace your menu with Cardapio",
		"theme"          : "cardapio-256",
		"author"         : "Keiran",
		"copyright-year" : "2010",
		"authors"        : [ "Pawel Bara" ]
	})

