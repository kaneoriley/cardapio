#PANEL_TYPE_NONE  = None (Just use None instead of PANEL_TYPE_NONE)
PANEL_TYPE_GNOME2 = 1
PANEL_TYPE_AWN    = 2
PANEL_TYPE_DOCKY  = None

POS_TOP    = 0
POS_BOTTOM = 1
POS_LEFT   = 2
POS_RIGHT  = 3

class CardapioAppletInterface:

	panel_type = None

	def setup(self, cardapio):
		"""
		This methods is called right after Cardapio loads its main variables, but
		before it actually loads plugins and builds its GUI.

		IMPORTANT: Do not modify anything inside the "cardapio" variable! It is
		only passed here directly (instead of using a proxy like in the case of
		plugins) because applets are written by "trusted" coders (since there
		will only be 3 or 4 applets total)
		"""
		pass


	def update_from_user_settings(self, settings):
		"""
		This method updates the applet according to the settings in
		settings['applet label'], settings['applet icon'], and settings['open on
		hover']
		"""
		pass


	def get_size(self):
		"""
		Returns the width and height of the applet
		"""
		return 0,0


	def get_position(self):
		"""
		Returns the position of the applet with respect to the screen (same as
		get_origin in GTK)
		"""
		return 0,0


	def get_orientation(self):
		"""
		Returns the edge of the screen at which the panel is placed, using one
		of POS_TOP, POS_BOTTOM, ORIENT_LEFT, ORIENT_RIGHT.
		"""
		return POS_TOP


	def draw_toggled_state(self, state):
		"""
		Draws the panel applet in the toggled/untoggled state depending
		on whether state is True/False. Note that this method should *only
		draw*, but not handle toggling in any way.
		"""
		pass


	def has_mouse_cursor(self, mouse_x, mouse_y):
		"""
		Returns true if the given coordinates is on top of the applet, and False
		otherwise.
		"""
		x, y = self.get_position()
		w, h = self.get_size()
		return ((x <= mouse_x <= x + w) and (y <= mouse_y <= y + h))

