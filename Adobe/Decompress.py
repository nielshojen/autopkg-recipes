#!/usr/bin/env python

import subprocess
import os
from autopkglib import Processor, ProcessorError

__all__ = ["Decompress"]

class Decompress(Processor):
	description = "Decompresses 7z files in Reader using Adobe decompress."
	input_variables = {
		"decompressor": {
			"required": True,
			"description": ("Path to decompress folder."),
		}
	}
	output_variables = {
	}

	__doc__ = description

	def decompress_the_file(self):
		folder = self.env.get("decompressor")
		decompress = os.path.join(folder,"decompress")
		if not decompress:
			raise ProcessorError("Decompress binary not found: %s" % (finalize))
		cmd = [decompress]
		os.chdir(decompressor)
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(output, errors) = proc.communicate()
		return errors      

	def main(self):
		self.env["results"] = self.decompress_the_file()
		self.output("Decompressed: %s" % self.env["results"])


if __name__ == '__main__':
    processor = Decompress()
    processor.execute_shell()
    
