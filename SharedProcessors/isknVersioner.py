#!/usr/bin/env python


import re

from autopkglib import ProcessorError
from autopkglib.URLGetter import URLGetter

try:
    from plistlib import readPlistFromString
except ImportError:
    from plistlib import readPlistFromBytes as readPlistFromString

__all__ = ["isknVersioner"]

base_url = "http://s3.amazonaws.com/imagink/Repository/OS_X/Updates.xml"

class isknVersioner(URLGetter):
    """Provides Version and url for Repaper from iskn"""

    input_variables = {}
    output_variables = {
        "version": {"description": ("The version of the update as extracted from the metadata."
            )
        },
        "url": {"description": "URL to the latest installer."},
    }
    description = __doc__
    min_delta_version = ""

    def sanity_check_expected_triggers(self, item):
        """Raises an exeception if the Trigger Condition or
        Triggers for an update don't match what we expect.
        Protects us if these change in the future."""
        # MS currently uses "Registered File" placeholders, which get replaced
        # with the bundle of a given application ID. In other words, this is
        # the bundle version of the app itself.
        if not item.get("Trigger Condition") == ["and", "Registered File"]:
            raise ProcessorError(
                "Unexpected Trigger Condition in item %s: %s"
                % (item["Title"], item["Trigger Condition"])
            )

    def get_installs_items(self, item):
        """Attempts to parse the Triggers to create an installs item using
        only manifest data, making the assumption that CFBundleVersion and
        CFBundleShortVersionString are equal. Skip SkypeForBusiness as its
        xml does not contain a 'Trigger Condition'"""
        if self.env["product"] != "SkypeForBusiness":
            self.sanity_check_expected_triggers(item)
        version = self.get_version(item)
        # Skipping CFBundleShortVersionString because it doesn't contain
        # anything more specific than major.minor (no build versions
        # distinguishing Insider builds for example)
        installs_item = {
            "CFBundleVersion": version,
            "path": PROD_DICT[self.env["product"]]["path"],
            "type": "application",
        }
        return [installs_item]

    def get_version(self, item):
        """Extracts the version of the update item."""
        # If the 'Update Version' key exists we pull the "full" version string
        # easily from this
        if item.get("Update Version"):
            self.output(
                "Extracting version %s from metadata 'Update Version' key"
                % item["Update Version"]
            )
            return item["Update Version"]

    def get_installer_info(self):
        self.output("Requesting xml: %s" % base_url)
        data = self.download(base_url)
        metadata = readPlistFromString(data)


        self.env["version"] = self.get_version(item)
        self.env["minimum_os_version"] = pkginfo["minimum_os_version"]
        self.env["minimum_version_for_delta"] = self.min_delta_version
        self.env["additional_pkginfo"] = pkginfo
        self.env["url"] = item["Location"]
        self.output("Additional pkginfo: %s" % self.env["additional_pkginfo"])

    def main(self):
        self.get_installer_info()


if __name__ == "__main__":
    PROCESSOR = isknVersioner()
    PROCESSOR.execute_shell()