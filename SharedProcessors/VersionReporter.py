# pylint: disable = invalid-name
# Standard imports
import os
import subprocess
from xml.etree import ElementTree

# Other imports
# pylint: disable=import-error
from autopkglib import Processor, ProcessorError


# Processor information
__all__ = ["VersionReporter"]
__version__ = '1.0.0'


# Class
# pylint: disable = too-few-public-methods
class VersionReporter(Processor):
    '''
        Reports version info
    '''

    description = __doc__

    input_variables = {
        "version": {
            "required": True,
            "description": ("Version."),
        },
    }

    output_variables = {
        "version_reporter_summary_result": {
            "description": "Exiting info.",
        }
    }

    # pylint: disable=too-many-branches
    def main(self):

        # Var declaration
        version = None

        version = self.env["version"] 

        self.env["version_reporter_summary_result"] = {
            "summary_text": "The following data was collected:",
            "data": {
                "version": version,
            },
        }


if __name__ == '__main__':
    PROCESSOR = VersionReporter()