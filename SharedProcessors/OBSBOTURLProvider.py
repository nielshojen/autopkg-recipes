#!/usr/local/autopkg/python
#
# Copyright 2026 Niels Højen,
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Disabling 'no-env-member' for recipe processors
#
# Modified to add Remote Desktop Standalone and Intune Company Portal
#
#pylint:disable=e1101
"""See docstring for OBSBOTURLProvider class"""

import re
import ssl
import json
import urllib.request, urllib.error, urllib.parse

try:
    from plistlib import loads as load_plist
except ImportError:
    from FoundationPlist import readPlistFromString as load_plist

from autopkglib import Processor, ProcessorError


__all__ = ["OBSBOTURLProvider"]

BASE_URL = "https://resource-cdn.obsbothk.com/download/obsbot-center/"
REMOTE_API_URL = "https://remo-api.obsbot.com/fms/v1/files/cdn/authorization"

class OBSBOTURLProvider(Processor):
    """Provides a download URL for the most recent version of MS Office 2016."""
    input_variables = {
        "file": {
            "required": True,
            "description": "File to generate url for",
        },
    }
    output_variables = {
        "version": {
            "description":
                "The version of the app."
        },
        "url": {
            "description": "Authenticated URL for the app.",
        },
    }
    description = __doc__
    min_delta_version = ""


    def get_authenticated_url(self):
        post_data = {
            "url": f"{BASE_URL}{self.env['file']}"
        }

        data = json.dumps(post_data).encode("utf-8")

        req = urllib.request.Request(
            REMOTE_API_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, context=ctx) as response:
            result = json.loads(response.read().decode("utf-8"))


        self.env['url'] = result["url"]

    def get_version(self):
        match = re.search(r'_(\d+(?:\.\d+)+)_release\.dmg$', self.env['file'])
        return match.group(1) if match else None

    def main(self):
        self.get_authenticated_url()
        self.env['version'] = self.get_version()


if __name__ == "__main__":
    PROCESSOR = OBSBOTURLProvider()
    PROCESSOR.execute_shell()
