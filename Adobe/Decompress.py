#!/usr/bin/env python

import subprocess
import os
from autopkglib import Processor, ProcessorError

__all__ = ["Decompress"]

class Decompress(Processor):
	description = "Decompresses an 7z file using Adobe decompress."
	input_variables = {
		"decompressor": {
			"required": True,
			"description": ("Path to decompress binary."),
		}
	}
	output_variables = {
	}

	__doc__ = description

	def decompress_the_files(self):
		if not decompress:
			raise ProcessorError("decompress binary not found: %s" % (decompress))
		cmd = ["decompress"]
		proc = subprocess.Popen(os.chdir(decompress),cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(output, errors) = proc.communicate()
		return errors      

	def main(self):
		'''Does nothing except decompresses the file'''
		if "file" in self.env:
			self.output("Decompressing with %s" % (self.env["decompress"]))
		self.env["results"] = self.decompress_the_files()
		self.output("Decompressed: %s" % self.env["results"])


if __name__ == '__main__':
    processor = LZMADecompress()
    processor.execute_shell()
    
