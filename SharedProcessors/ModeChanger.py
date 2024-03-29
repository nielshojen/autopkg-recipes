#!/usr/local/autopkg/python

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
		'recurse': {
			'required': False,
			'description': 'chmod(1) recursive mode'
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
		recurse = self.env.get('recurse')
		mode = self.env.get('mode')

		if recurse == True:
			retcode = subprocess.call(['/bin/chmod','-R', mode, filename])
		else:
			retcode = subprocess.call(['/bin/chmod', mode, filename])
		if retcode:
			raise ProcessorError('Error setting mode (chmod %s) for %s' % (mode, filename))

		return
