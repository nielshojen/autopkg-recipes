#!/usr/bin/env python

from autopkglib import Processor, ProcessorError


__all__ = ["VersionExtractor"]


class VersionExtractor(Processor):

    input_variables = {
        "input_file": {
            "required": True,
            "description": "The version string that needs splitting."
        },
        "split_on_in": {
            "required": True,
            "description": "The character(s) to use for splitting the "
                           "version. (Defaults to a space.)"
        },
        "split_on_out": {
            "required": False,
            "description": "The character(s) to use for splitting the  "
                           "version. (Defaults to 0.)"
        }
    }
    output_variables = {
        "version": {
            "description": "The cleaned up version string."
        }
    }
    description = __doc__

    def main(self):

        split_on_in = self.env.get("split_on_in", " ")
        index = self.env.get("index", 0)
        self.env["version"] = self.env["version"].split(split_on_in)[index]
        self.output("Version: %s" % self.env["version"])


if __name__ == "__main__":
    processor = VersionExtractor()
    processor.execute_shell()
