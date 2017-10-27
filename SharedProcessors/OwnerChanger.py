#!/usr/bin/env python

from autopkglib import Processor, ProcessorError
import subprocess
import os

__all__ = ["OwnerChanger"]

class ModeChanger(Processor):
	'''Changes file modes'''

	input_variables = {
		'filename': {
			'required': True,
			'description': 'Name of filename resource',
		},
		'recurse': {
			'required': False,
			'description': 'chown(1) recursive mode'
		},
		'owner': {
			'required': True,
			'description': 'chown(1) mode string to apply to file. E.g. "o-w"'
		},
	}
	output_variables = {
	}

	def main(self):
		filename = self.env.get('filename')
		recurse = self.env.get('recurse')
		mode = self.env.get('mode')

		if recurse == True:
			retcode = subprocess.call(['/bin/chown','-R', owner, filename])
		else:
			retcode = subprocess.call(['/bin/chown', owner, filename])
		if retcode:
			raise ProcessorError('Error setting mode (chown %s) for %s' % (owner, filename))

		return
