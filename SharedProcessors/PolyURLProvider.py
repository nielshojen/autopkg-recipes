#!/usr/bin/python
#
# Copyright 2021 Niels Højen
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

"""See docstring for PolyURLProvider class"""

import json
import ssl
import urllib.request, urllib.error, urllib.parse

from autopkglib import Processor, ProcessorError

__all__ = ["PolyURLProvider"]

DOWNLOADS_URL = "https://api.silica-prod01.io.lens.poly.com/graphql"

class PolyURLProvider(Processor):
    """Provides a version and download url for the Software Pid given."""
    description = __doc__
    input_variables = {
        "product_pid": {
            "required": True,
            "description":
                "Product to fetch URL for. See the list of names "
                "given in the metadata file at %s. "
                "For example, 'lens-desktop-mac'" % DOWNLOADS_URL
        },
    }
    output_variables = {
        "version": {
            "description": "Version of the product.",
        },
        "url": {
            "description": "Download URL.",
        },
    }


    def get_downloads_metadata(self):
        '''Return a deserialized json object from the download metadata.'''
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(DOWNLOADS_URL)
            req.add_header('Content-Type', 'application/json')
            req.add_header('Apollographql-Client-Name', 'poly.com-website')
            QUERY = '{ "query": "query { availableProductSoftwareByPid(pid:\\"%s\\") { name version productBuild { archiveUrl } } }" }' % self.env["product_pid"]
            querydata = QUERY.encode('utf-8')
            metadata = urllib.request.urlopen(req, querydata, context=ctx).read()
            json_data = json.loads(metadata)
        except urllib.error.HTTPError as ValueError:
            raise ProcessorError("Could not parse downloads metadata.")
        return json_data

    def main(self):
        '''Find the download URL and version'''

        metadata = self.get_downloads_metadata()
        metadata = metadata['data']['availableProductSoftwareByPid']

        try:
            download_url = metadata['productBuild']['archiveUrl']
            download_version = metadata['version']
        except KeyError:
            raise ProcessorError("Metadata for product is missing at the "
                                 "expected location in feed.")

        self.env["version"] = download_version
        self.env["url"] = download_url
        self.output("Found download URL %s, version %s" %
                    (self.env["url"],
                    self.env["version"]))


if __name__ == "__main__":
    PROCESSOR = PolyURLProvider()
    PROCESSOR.execute_shell()
