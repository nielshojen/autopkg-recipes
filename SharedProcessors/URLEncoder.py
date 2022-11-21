#!/usr/local/autopkg/python

from autopkglib import Processor, ProcessorError


__all__ = ["URLEncoder"]

class URLEncoder(Processor):

    input_variables = {
        "input_url": {
            "required": True,
            "description": "The url that needs to have things like spaces replaced."
        }
    }
    output_variables = {
        "url": {
            "description": "The properly encoded url."
        }
    }
    description = __doc__

    def main(self):

        if self.env.get("input_url"):
            self.env["url"] = self.env.get("input_url").replace(" ", "%20")
        
        self.output("URL: %s" % self.env["url"])


if __name__ == "__main__":
    processor = URLEncoder()
    processor.execute_shell()
