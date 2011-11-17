PYTHON = `which python`

ifeq ($(DESTDIR),)
DESTDIR = 
endif

ifeq ($(PREFIX),)
PREFIX = $(DESTDIR)/usr
endif

all:
	@echo "make install - Install on local system"
	@echo "make uninstall - Remove from local system"
	@echo "make buildsrc - Generate a deb source package"
	@echo "make clean - Get rid of scratch and byte files"

buildsrc:
	debuild -S

clean:
	$(MAKE) -f $(CURDIR)/debian/rules clean
	find . -name '*.pyc' -delete

install: install-alone install-panel install-docky install-awn install-shell

install-alone:
	python -m compileall src/
	python -m compileall src/plugins/
	
	# remove old files which have been renamed or moved to another package
	rm -rf $(PREFIX)/lib/cardapio/cardapio.py
	rm -rf $(PREFIX)/lib/cardapio/cardapio.pyc
	rm -rf $(PREFIX)/lib/cardapio/plugins/firefox_bookmarks.py
	rm -rf $(PREFIX)/lib/cardapio/plugins/firefox_bookmarks.pyc
	
	mkdir -p $(PREFIX)/lib/cardapio
	cp -f src/cardapio $(PREFIX)/lib/cardapio/
	cp -f src/Cardapio.py $(PREFIX)/lib/cardapio/
	cp -f src/Cardapio.pyc $(PREFIX)/lib/cardapio/
	cp -f src/Constants.py $(PREFIX)/lib/cardapio/
	cp -f src/Constants.pyc $(PREFIX)/lib/cardapio/
	cp -f src/DesktopEnvironment.py $(PREFIX)/lib/cardapio/
	cp -f src/DesktopEnvironment.pyc $(PREFIX)/lib/cardapio/
	cp -f src/CardapioGtkView.py $(PREFIX)/lib/cardapio/
	cp -f src/CardapioGtkView.pyc $(PREFIX)/lib/cardapio/
	cp -f src/CardapioViewInterface.py $(PREFIX)/lib/cardapio/
	cp -f src/CardapioViewInterface.pyc $(PREFIX)/lib/cardapio/
	cp -f src/CardapioAppletInterface.py $(PREFIX)/lib/cardapio/
	cp -f src/CardapioAppletInterface.pyc $(PREFIX)/lib/cardapio/
	cp -f src/CardapioSimpleDbusApplet.py $(PREFIX)/lib/cardapio/
	cp -f src/CardapioSimpleDbusApplet.pyc $(PREFIX)/lib/cardapio/
	cp -f src/CardapioPluginInterface.py $(PREFIX)/lib/cardapio/
	cp -f src/CardapioPluginInterface.pyc $(PREFIX)/lib/cardapio/
	cp -f src/OptionsWindow.py $(PREFIX)/lib/cardapio/
	cp -f src/OptionsWindow.pyc $(PREFIX)/lib/cardapio/
	cp -f src/misc.py $(PREFIX)/lib/cardapio/
	cp -f src/misc.pyc $(PREFIX)/lib/cardapio/
	cp -f src/GMenuHelper.py $(PREFIX)/lib/cardapio/
	cp -f src/GMenuHelper.pyc $(PREFIX)/lib/cardapio/
	cp -f src/XDGMenuHelper.py $(PREFIX)/lib/cardapio/
	cp -f src/XDGMenuHelper.pyc $(PREFIX)/lib/cardapio/
	cp -f src/IconHelper.py $(PREFIX)/lib/cardapio/
	cp -f src/IconHelper.pyc $(PREFIX)/lib/cardapio/
	cp -f src/SettingsHelper.py $(PREFIX)/lib/cardapio/
	cp -f src/SettingsHelper.pyc $(PREFIX)/lib/cardapio/
	cp -f res/cardapio.desktop $(PREFIX)/lib/cardapio/
	
	mkdir -p $(PREFIX)/lib/cardapio/ui
	cp -f src/ui/cardapio.ui $(PREFIX)/lib/cardapio/ui/
	cp -f src/ui/options.ui $(PREFIX)/lib/cardapio/ui/
	
	mkdir -p $(PREFIX)/lib/cardapio/plugins
	cp -f src/plugins/* $(PREFIX)/lib/cardapio/plugins/
	
	mkdir -p $(PREFIX)/share/locale
	cp -rf locale/* $(PREFIX)/share/locale/
	
	mkdir -p $(PREFIX)/share/pixmaps
	cp -f res/cardapio*.png $(PREFIX)/share/pixmaps/
	cp -f res/cardapio*.svg $(PREFIX)/share/pixmaps/
	
	mkdir -p $(PREFIX)/bin
	ln -fs $(PREFIX)/lib/cardapio/cardapio $(PREFIX)/bin/cardapio
	
	mkdir -p $(PREFIX)/share/applications
	cp -f res/cardapio.desktop $(PREFIX)/share/applications/
	
	mkdir -p $(DESTDIR)/usr/share/dbus-1/services
	cp res/cardapio.service $(DESTDIR)/usr/share/dbus-1/services/cardapio.service
  

install-panel: install-alone
	python -m compileall src/gnomepanel/
	cp -f src/gnomepanel/cardapio-gnome-panel-applet $(PREFIX)/lib/cardapio/
	
	mkdir -p $(PREFIX)/lib/cardapio/gnomepanel
	cp -f src/gnomepanel/CardapioGnomeApplet* $(PREFIX)/lib/cardapio/gnomepanel/
	cp -f src/gnomepanel/CardapioGnomeAppletFactory* $(PREFIX)/lib/cardapio/gnomepanel/
	cp -f src/gnomepanel/__init__* $(PREFIX)/lib/cardapio/gnomepanel/
	
	mkdir -p $(PREFIX)/bin
	ln -fs $(PREFIX)/lib/cardapio/cardapio-gnome-panel-applet $(PREFIX)/bin/cardapio-gnome-panel-applet
	
	mkdir -p $(DESTDIR)/usr/lib/bonobo/servers
	#cp -f src/gnomepanel/cardapio.server $(DESTDIR)/usr/lib/bonobo/servers/
	for f in locale/*; \
		do test -f $$f/LC_MESSAGES/cardapio.mo && msgunfmt -o $$f.po $$f/LC_MESSAGES/cardapio.mo || true; \
	done
	intltool-merge -b locale src/gnomepanel/cardapio.server $(DESTDIR)/usr/lib/bonobo/servers/cardapio.server
	rm locale/*.po


install-docky: install-alone
	python -m compileall src/docky/
	cp -f res/cardapioDocky.desktop $(PREFIX)/lib/cardapio/
	
	mkdir -p $(PREFIX)/lib/cardapio/docky
	cp -f src/docky/DockySettingsHelper* $(PREFIX)/lib/cardapio/docky/
	cp -f src/docky/__init__* $(PREFIX)/lib/cardapio/docky/
	
	if test -d $(PREFIX)/share/dockmanager; then \
		mkdir -p $(PREFIX)/share/dockmanager/metadata; \
		mkdir -p $(PREFIX)/share/dockmanager/scripts; \
		cp -f src/docky/cardapio_helper.py.info $(PREFIX)/share/dockmanager/metadata/; \
		cp -f src/docky/cardapio_helper.py $(PREFIX)/share/dockmanager/scripts/; \
		chmod +x $(PREFIX)/share/dockmanager/scripts/cardapio_helper.py; \
	fi


install-awn: install-alone
	mkdir -p $(PREFIX)/lib/cardapio
	cp -f src/awn/CardapioAwnWrapper.py $(PREFIX)/lib/cardapio/
	cp -f src/awn/CardapioAwnApplet.py $(PREFIX)/lib/cardapio/
	
	mkdir -p $(DESTDIR)/usr/share/avant-window-navigator/applets
	cp -f src/awn/cardapio.desktop $(DESTDIR)/usr/share/avant-window-navigator/applets

install-shell: install-alone
	mkdir -p $(PREFIX)/share/gnome-shell/extensions
	cp -rf src/gnomeshell/cardapio@varal.org $(PREFIX)/share/gnome-shell/extensions/

uninstall: uninstall-alone uninstall-panel uninstall-docky uninstall-awn uninstall-shell

uninstall-alone: uninstall-panel uninstall-docky uninstall-awn uninstall-shell
	rm -rf $(PREFIX)/lib/cardapio
	rm -rf $(PREFIX)/bin/cardapio
	rm -rf $(PREFIX)/share/pixmaps/cardapio*
	rm -rf $(PREFIX)/share/applications/cardapio.desktop
	rm -f $(DESTDIR)/usr/share/dbus-1/services/cardapio.service
	find $(PREFIX)/share/locale -name '*cardapio.*' -delete
	
	# remove old files which have been renamed or moved to another package
	rm -rf $(PREFIX)/lib/cardapio/cardapio.py
	rm -rf $(PREFIX)/lib/cardapio/cardapio.pyc
	rm -rf $(PREFIX)/lib/cardapio/plugins/firefox_bookmarks.py
	rm -rf $(PREFIX)/lib/cardapio/plugins/firefox_bookmarks.pyc

uninstall-panel:
	rm -rf $(PREFIX)/bin/cardapio-gnome-panel-applet 
	rm -f $(DESTDIR)/usr/lib/bonobo/servers/cardapio.server

uninstall-docky:
	if test -d $(PREFIX)/share/dockmanager; then\
		rm -rf $(PREFIX)/share/dockmanager/metadata/cardapio_helper.py.info; \
		rm -rf $(PREFIX)/share/dockmanager/scripts/cardapio_helper.py; \
	fi

uninstall-awn:
	rm -rf $(PREFIX)/lib/cardapio/CardapioAwnWrapper.*
	rm -rf $(PREFIX)/lib/cardapio/CardapioAwnApplet.*
	rm -rf $(DESTDIR)/usr/share/avant-window-navigator/applets/cardapio.desktop

uninstall-shell:
	rm -rf $(PREFIX)/share/gnome-shell/extensions/cardapio@varal.org


# I hear these are useful in Gentoo, so I'm leaving them here:

oldinstall:
	$(PYTHON) setup.py install --root $(DESTDIR) --install-layout=deb $(COMPILE)

olduninstall:
	$(PYTHON) setup.py install --root $(DESTDIR) --install-layout=deb $(COMPILE) --record file_list.txt
	cat file_list.txt | xargs rm -rf
	rm file_list.txt
	rm -rf /usr/lib/python2.6/dist-packages/cardapio/
	rm -rf /usr/local/lib/python2.6/dist-packages/cardapio/

oldclean:
	$(PYTHON) setup.py clean
	$(MAKE) -f $(CURDIR)/debian/rules clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete


