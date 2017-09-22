#!/usr/bin/env python

from autopkglib import Processor, ProcessorError
import subprocess
import os

__all__ = ["MASReceiptWipe"]

class ModeChanger(Processor):
	'''Changes file modes'''

	input_variables = {
		'filename': {
			'required': True,
			'description': 'Name of filename resource',
		},
	}
	output_variables = {
	}

	def main(self):
		filename = self.env.get('filename')

			retcode = subprocess.call(['/bin/chmod', mode, filename])
		if retcode:
			raise ProcessorError('Error setting mode (chmod %s) for %s' % (mode, filename))

		return
