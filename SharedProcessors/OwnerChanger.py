#!/usr/local/autopkg/python

from autopkglib import Processor, ProcessorError
import subprocess
import os

__all__ = ["OwnerChanger"]

class OwnerChanger(Processor):
	'''Changes file modes'''

	input_variables = {
		'target': {
			'required': True,
			'description': 'Name of target resource',
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
		target = self.env.get('target')
		recurse = self.env.get('recurse')
		owner = self.env.get('owner')

		if recurse == True:
			retcode = subprocess.call(['/usr/sbin/chown', '-R', owner, target])
		
		else:
			retcode = subprocess.call(['/usr/sbin/chown', owner, target])
		
		if retcode:
			raise ProcessorError('Error setting mode (chown %s) for %s' % (owner, target))
		
		return
