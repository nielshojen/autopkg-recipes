#!/usr/local/autopkg/python

import datetime
import re
from xml.dom.minidom import parse, parseString
import urllib.request, urllib.error, urllib.parse
import json

from autopkglib import Processor, ProcessorError

__all__ = ["SourceForgeURLProvider"]

FILE_INDEX_URL = 'https://sourceforge.net/projects/%s/rss'
PROJECT_NAME_URL = 'https://sourceforge.net/rest/p/%s'

class SourceForgeURLProvider(Processor):
	'''Provides URL to the latest file that matches a pattern for a particular SourceForge project.'''

	input_variables = {
		'SOURCEFORGE_PROJECT_NAME': {
			'required': False,
			'description': 'Numerical ID of SourceForge project. One of SOURCEFORGE_PROJECT_ID or SOURCEFORGE_PROJECT_NAME must be specified.',
			},
		'SOURCEFORGE_PROJECT_ID': {
			'required': False,
			'description': 'Numerical ID of SourceForge project. One of SOURCEFORGE_PROJECT_ID or SOURCEFORGE_PROJECT_NAME must be specified.',
			},
		'SOURCEFORGE_FILE_PATTERN': {
			'required': True,
			'description': 'Pattern to match SourceFile files on',
			},
	}
	output_variables = {
		'url': {
			'description': 'URL to the latest SourceForge project download'
		}
	}

	description = __doc__

	def get_sf_project_id(self, pname):
		# borrowed from https://gist.github.com/homebysix/9468859a76ac82f1d121
		try:
			f = urllib.request.urlopen(PROJECT_NAME_URL % pname)
			raw_json = f.read()
			f.close()
		except:
			raise ProcessorError('Could not retrieve project name URL for "%s"' % pname)

		parsed_json = json.loads(raw_json)

		for tools in parsed_json['tools']:
			try:
				return tools['sourceforge_group_id']
			except KeyError:
				pass

	def get_sf_file_url(self, proj_id, pattern):
		flisturl = FILE_INDEX_URL % proj_id

		try:
			f = urllib.request.urlopen(flisturl)
			rss = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve RSS feed %s' % flisturl)

		re_file = re.compile(self.env.get('SOURCEFORGE_FILE_PATTERN'), re.I)

		rss_parse = parseString(rss)

		items = []

		for i in  rss_parse.getElementsByTagName('item'):
			pubDate = i.getElementsByTagName('pubDate')[0].firstChild.nodeValue
			link = i.getElementsByTagName('link')[0].firstChild.nodeValue

			pubDatetime = datetime.datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S UT')

			if re_file.search(link):
				items.append((pubDatetime, link),)

		items.sort(key=lambda r: r[0])

		if len(items) < 1:
			raise ProcessorError('No matched files')

		return items[-1][1]

	def main(self):
		proj_name = self.env.get('SOURCEFORGE_PROJECT_NAME')
		proj_id  = self.env.get('SOURCEFORGE_PROJECT_ID')
		file_pat = self.env.get('SOURCEFORGE_FILE_PATTERN')

		if not proj_id:
			if not proj_name:
				raise ProcessorError('One of SOURCEFORGE_PROJECT_ID or SOURCEFORGE_PROJECT_NAME must be specified.')

			proj_id = self.get_sf_project_id(proj_name)
			self.output('Found SourceForge project ID %s for %s' % (proj_id, proj_name))


		self.env['url'] = self.get_sf_file_url(proj_name, file_pat)
		self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
	processor = SourceForgeURLProvider()
	processor.execute_shell()
