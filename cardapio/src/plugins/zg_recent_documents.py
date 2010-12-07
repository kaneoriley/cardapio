class CardapioPlugin(CardapioPluginInterface):

	author             = _('Cardapio Team')
	name               = _('Recent documents')
	description        = _('Search for your most recently used files')

	url                = ''
	help_text          = ''
	version            = '0.992'

	plugin_api_version = 1.39

	search_delay_type  = 'local'

	default_keyword    = 'zgeist'

	category_name      = _('Recent Documents')
	category_icon      = 'document-open-recent'
	category_tooltip   = _('Files that you have used recently')

	hide_from_sidebar  = False

	recency_in_days = 30

	def __init__(self, cardapio_proxy): 

		self.c = cardapio_proxy

		self.loaded = False

		try:
			import urllib2, os
			from zeitgeist.client import ZeitgeistClient
			from zeitgeist import datamodel

		except Exception, exception:
			self.cardapio.write_to_log(self, 'Could not import certain modules', is_error = True)
			self.cardapio.write_to_log(self, exception, is_error = True)
			return
		
		self.urllib2         = urllib2
		self.os              = os
		self.datamodel       = datamodel

		if 'ZeitgeistClient' not in globals():
			self.c.write_to_log(self, 'Could not import Zeitgeist', is_error = True)
			return

		try:
			self.zg = ZeitgeistClient()
		except Exception, exception:
			self.c.write_to_log(self, 'Could not start Zeitgeist', is_error = True)
			self.c.write_to_log(self, exception, is_error = True)
			return 

		bus = dbus.SessionBus()

		if bus.request_name('org.freedesktop.Tracker1') != dbus.bus.REQUEST_NAME_REPLY_IN_QUEUE:
			self.c.write_to_log(self, 'Could not find Zeitgeist full-text-search', is_error = True)
			return 

		try:
			fts_object = bus.get_object('org.gnome.zeitgeist.Engine', '/org/gnome/zeitgeist/index/activity')
			self.fts = dbus.Interface(fts_object, 'org.gnome.zeitgeist.Index')
		except Exception, exception:
			self.c.write_to_log(self, 'Could not connect to Zeitgeist full-text-search', is_error = True)
			self.c.write_to_log(self, exception, is_error = True)
			return 

		self.have_sezen = which('sezen')
		if not self.have_sezen:
			self.c.write_to_log(self, 'Sezen not found, so you will not see the "Show additional results" button.', is_warning = True)

		self.action_command = r"sezen '%s'" # NOTE: Seif said he would add this capability into Sezen
		self.action = {
			'name'         : _('Show additional results'),
			'tooltip'      : _('Show additional search results in Sezen'),
			'icon name'    : 'system-search',
			'type'         : 'callback',
			'command'      : self.more_results_action,
			'context menu' : None,
			}

		self.time_range = self.datamodel.TimeRange.always()

		self.event_template = self.datamodel.Event()
		self.loaded = True


	def search(self, text, result_limit):

		self.current_query = text

		text = text.lower()
		self.search_query = text
		# TODO: this is thread unsafe. correct this using a wrapper like
		# for example Tomboy's plugin does
		self.result_limit = result_limit

		if text:
			self.event_template.actor = 'application://' + text + '*'
		else:
			self.event_template.actor = ''

		self.zg.find_events_for_templates(
				[self.event_template],
				self.handle_search_result, 
				timerange = self.time_range, 
				num_events = result_limit,
				result_type = self.datamodel.ResultType.MostRecentSubjects
				)


	def handle_search_result(self, events):

		fts_results = None
		all_events = []

		# TODO: make this asynchronous somehow! (Need to talk to the developers
		# of the FTS extension to add this to the API)
		if self.search_query:

			try:
				fts_results, count = self.fts.Search(
						self.search_query + '*', 
						self.time_range, 
						[], 0, self.result_limit, 2)

			except Exception, exception:
				print exception
				pass

			if fts_results:
				all_events = map(self.datamodel.Event, fts_results)

		parsed_results = [] 
		all_events += events
		urls_seen = set()

		for event in all_events:

			if len(urls_seen) >= self.result_limit: break

			for subject in event.get_subjects():

				dummy, canonical_path = self.urllib2.splittype(subject.uri)
				parent_name, child_name = self.os.path.split(canonical_path)

				if len(urls_seen) >= self.result_limit: break
				if canonical_path in urls_seen: continue
				urls_seen.add(canonical_path)

				item = {
					'name'         : subject.text,
					'icon name'    : subject.mimetype,
					'tooltip'      : canonical_path,
					'command'      : canonical_path,
					'type'         : 'xdg',
					'context menu' : None,
					}

				parsed_results.append(item)


		# TODO: Waiting for Sezen to support command-line arguments...
		if parsed_results and self.have_sezen:
			parsed_results.append(self.action)

		self.c.handle_search_result(self, parsed_results, self.current_query)


	def more_results_action(self, text):

		try:
			subprocess.Popen(self.action_command % text, shell = True)

		except OSError, e:
			self.c.write_to_log(self, 'Error launching plugin action.', is_error = True)
			self.c.write_to_log(self, e, is_error = True)

