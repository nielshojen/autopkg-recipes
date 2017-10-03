#!/usr/bin/env python

from autopkglib import Processor, ProcessorError


__all__ = ["VersionExtractor"]


class VersionExtractor(Processor):

    input_variables = {
        "input": {
            "required": True,
            "description": "The version string that needs splitting."
        },
        "split_on_in": {
            "required": True,
            "description": "The character(s) to use for splitting the "
                           "version. (Defaults to a space.)"
        },
        "split_on_out": {
            "required": True,
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
        split_on_out = self.env.get("split_on_out", " ")
        index = self.env.get("index", 1)
        self.env["version"] = self.env["version"].split(split_on_in)[index]
        index = self.env.get("index", 0)
        self.env["version"] = self.env["version"].split(split_on_out)[index]
        self.output("Version: %s" % self.env["version"])


if __name__ == "__main__":
    processor = VersionSplitter()
    processor.execute_shell()
