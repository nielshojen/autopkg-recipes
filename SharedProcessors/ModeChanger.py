#!/usr/bin/env python

from autopkglib import Processor, ProcessorError
import subprocess
import os

__all__ = ["ModeChanger"]

class ModeChanger(Processor):
	'''Changes file modes'''

	input_variables = {
		'filename': {
			'required': True,
			'description': 'Name of filename resource',
		},
		'mode': {
			'required': True,
			'description': 'chmod(1) mode string to apply to file. E.g. "o-w"'
		},
	}
	output_variables = {
	}

	def main(self):
		filename = self.env.get('filename')
		mode = self.env.get('mode')

		retcode = subprocess.call(['/bin/chmod', mode, filename])
		if retcode:
			raise ProcessorError('Error setting mode (chmod %s) for %s' % (mode, filename))

		return
