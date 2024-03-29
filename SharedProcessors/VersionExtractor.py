#!/usr/local/autopkg/python

from autopkglib import Processor, ProcessorError


__all__ = ["VersionExtractor"]


class VersionExtractor(Processor):

    input_variables = {
        "input_file": {
            "required": True,
            "description": "The version string that needs splitting."
        },
        "split_on_in": {
            "required": False,
            "description": "The character(s) to use for splitting the "
                           "version."
        },
        "split_on_out": {
            "required": False,
            "description": "The character(s) to use for splitting the  "
                           "version."
        }
    }
    output_variables = {
        "version": {
            "description": "The cleaned up version string."
        }
    }
    description = __doc__

    def main(self):

        split_on_in = self.env.get("split_on_in")
        split_on_out = self.env.get("split_on_out")
        if split_on_in:
            index = self.env.get("index", 1)
            self.env["version"] = self.env["input_file"].split(split_on_in)[index]
        if split_on_out:
            index = self.env.get("index", 0)
            self.env["version"] = self.env["version"].split(split_on_out)[index]
        self.output("Version: %s" % self.env["version"])


if __name__ == "__main__":
    processor = VersionExtractor()
    processor.execute_shell()
