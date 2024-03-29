#!/usr/local/autopkg/python

from autopkglib import Processor, ProcessorError
import subprocess
import os

__all__ = ["MASReceiptWipe"]

class MASReceiptWipe(Processor):
	'''Wipes MAS Receipt file by echoing a 0 into the recipt file'''

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
		cmd = '/bin/echo 0 > ' + filename
		retcode = subprocess.call([cmd], shell = True)
		if retcode:
			raise ProcessorError('Error wiping MAS recipt for %s' % (filename))
		return
