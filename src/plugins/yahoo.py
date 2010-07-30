import json
import gio
import urllib

from glib import GError
from locale import getdefaultlocale

class CardapioPlugin(CardapioPluginInterface):

	"""
	Yahoo plugin based on it's BOSS web search API. We're using BOSS because
	it has no limits for search count per IP. The documentation says that Yahoo
	could start taking money for using BOSS but even if they will, they will
	leave a free version with limited search count available too.

	Documentation can be found at:
	http://developer.yahoo.com/search/boss/boss_guide/index.html

	This plugin will try to localize each and every search but will do it on
	a best-effort manner.

	All it's web requests are asynchronous and cancellable.
	"""

	# Cardapio's variables
	author = 'Pawel Bara'
	name = _('Yahoo')
	description = _("Perform a search using Yahoo")
	version = '0.91b'

	url = ''
	help_text = ''

	plugin_api_version = 1.35

	search_delay_type = 'remote search update delay'

	category_name = _('Yahoo Results')
	category_tooltip = _('Results found using Yahoo')

	category_icon = 'system-search'
	fallback_icon = ''

	hide_from_sidebar = True

	def __init__(self, cardapio_proxy):
		cardapio_proxy.write_to_log(self, 'initializing Yahoo plugin')

		self.cardapio = cardapio_proxy

		self.cancellable = gio.Cancellable()

		# we'll try to get locale here; we'll pass it as an argument for every
		# Yahoo search; for some locales this will work, for others (most of
		# them probably) it'll just be ignored; we could try to obey this table...
		# http://developer.yahoo.com/search/boss/boss_guide/supp_regions_lang.html
		# ... but I think it's an overkill
		locale_code = getdefaultlocale()[0].lower()
		language, region = locale_code[:2], locale_code[3:]

		# Yahoo's API arguments (my AppID and a request for a search with
		# maximum four results in raw json format and given language)
		self.api_base_args = {
			'appid'    : 'TuNKmOzV34GRC9mrBNZMgr.vY1xPMLMH9U3PsOYkg8WvYnFawnB5gKd4GsrUbqluzg--',
			'format'   : 'json',
			'style'    : 'raw',
			'count'    : self.cardapio.settings['search results limit'],
			'lang'     : language,
			'region'   : region
		}

		# Yahoo's base URLs (search and search more variations)
		self.api_base_url = 'http://boss.yahooapis.com/ysearch/web/v1/{0}?' + urllib.urlencode(self.api_base_args)
		self.web_base_url = 'http://search.yahoo.com/search?{0}'

		self.loaded = True

	def search(self, text):
		if len(text) == 0:
			return

		self.current_query = text

		self.cardapio.write_to_log(self, 'searching for {0} using Yahoo'.format(text), is_debug = True)

		self.cancellable.reset()

		# prepare final API URL
		final_url = self.api_base_url.format(urllib.quote(text, ''))

		self.cardapio.write_to_log(self, 'final API URL: {0}'.format(final_url), is_debug = True)

		# asynchronous and cancellable IO call
		self.current_stream = gio.File(final_url)
		self.current_stream.load_contents_async(self.show_search_results,
			cancellable = self.cancellable,
			user_data = text)

	def show_search_results(self, gdaemonfile, result, text):
		"""
		Callback to asynchronous IO (Yahoo's API call).
		"""

		# watch out for connection problems
		try:
			json_body = self.current_stream.load_contents_finish(result)[0]

			# watch out for empty input
			if len(json_body) == 0:
				return

			response = json.loads(json_body)
		except (ValueError, GError) as ex:
			self.cardapio.handle_search_error(self, 'error while obtaining data: {0}'.format(str(ex)))
			return

		# decode the result
		try:
			items = []

			response_body = response['ysearchresponse']

			# if we have any results...
			if response_body['totalhits'] != '0':
				# remember them all
				for item in response_body['resultset_web']:
					items.append({
						'name'         : item['title'],
						'tooltip'      : item['url'],
						'icon name'    : 'text-html',
						'type'         : 'xdg',
						'command'      : item['url'],
						'context menu' : None
					})

			# always add 'Search more...' item
			search_more_args = { 'p' : text }

			items.append({
				'name'         : _('Show additional results'),
				'tooltip'      : _('Show additional search results in your web browser'),
				'icon name'    : 'system-search',
				'type'         : 'xdg',
				# TODO: cardapio later unquotes this and then quotes it again;
				# it's screwing my quotation
				'command'      : self.web_base_url.format(urllib.urlencode(search_more_args)),
				'context menu' : None
			})

			# pass the results to Cardapio
			self.cardapio.handle_search_result(self, items, self.current_query)

		except KeyError:
			self.cardapio.handle_search_error(self, "Incorrect Yahoo's JSON structure")

	def cancel(self):
		self.cardapio.write_to_log(self, 'cancelling a recent Yahoo search (if any)', is_debug = True)

		if not self.cancellable.is_cancelled():
			self.cancellable.cancel()