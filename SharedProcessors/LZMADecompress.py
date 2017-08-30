#!/usr/bin/env python

import subprocess
from autopkglib import Processor, ProcessorError

__all__ = ["LZMADecompress"]

class LZMADecompress(Processor):
	description = "Decompresses an LZMA file using Adobe finalize."
	input_variables = {
		"lzma_file": {
			"required": True,
			"description": ("Path to .lzma file."),
		},
		"decompressor": {
			"required": True,
			"description": ("Path to finalize binary."),
		}
	}
	output_variables = {
	}

	__doc__ = description

	def decompress_the_file(self):
		file = self.env.get("lzma_file")
		if not file:
			raise ProcessorError("lzma_file not found: %s" % (file))
		finalize = self.env.get("decompressor")
		if not finalize:
			raise ProcessorError("finalize binary not found: %s" % (finalize))
		cmd = [finalize,file]
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(output, errors) = proc.communicate()
		return errors      

	def main(self):
		'''Does nothing except decompresses the file'''
		if "lzma_file" in self.env:
			self.output("Using input LZMA file %s decompressing with %s" % (self.env["lzma_file"], self.env["decompressor"]))
		self.env["results"] = self.decompress_the_file()
		self.output("Decompressed: %s" % self.env["results"])


if __name__ == '__main__':
    processor = LZMADecompress()
    processor.execute_shell()
    
