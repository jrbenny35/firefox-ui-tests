import sys
import os
from marionette_driver import By, Wait
from marionette.marionette_test import skip_if_e10s

from firefox_puppeteer.testcases import FirefoxTestCase

from firefox_puppeteer.ui.browser.window import BrowserWindow


class TestSafeBrowsingPrimaryDownload(FirefoxTestCase):

    file_names = [
        "goog-phish-shavar.cache",
        "goog-phish-shavar.pset",
        "goog-phish-shavar.sbstore",
        "goog-malware-shavar.cache",
        "goog-malware-shavar.pset",
        "goog-malware-shavar.sbstore",
        "goog-badbinurl-shavar.cache",
        "goog-badbinurl-shavar.pset",
        "goog-badbinurl-shavar.sbstore"
    ]

    win_file_names = [
        "goog-downloadwhite-digest256.cache",
        "goog-downloadwhite-digest256.pset",
        "goog-downloadwhite-digest256.sbstore"
    ]

    tracking_protection = [
        "mozstd-track-digest256.cache",
        "mozstd-track-digest256.pset",
        "mozstd-track-digest256.sbstore",
        "mozstd-trackwhite-digest256.cache",
        "mozstd-trackwhite-digest256.pset",
        "mozstd-trackwhite-digest256.sbstore"
    ]

    def setUp(self):
        FirefoxTestCase.setUp(self)
        safe_browsing_path = os.path.join(self.marionette.instance.profile.profile, 'safebrowsing')
        files_location = safe_browsing_path

    def test_safe_browsing(self):
        if sys.platform.startswith('win32'):
            self.verify_win_files_existence()
        else:
            self.verify_files_existence()

    def verify_files_existence(self):
        for file in self.file_names:
            if self.assertTrue(
                    Wait(self.marionette, timeout=60).until(
                        lambda _: os.path.exists(os.path.join(self.filesLocation, file)))):
                self.verify_tracking_protection_existence()

    def verify_win_files_existence(self):
        for file in self.win_file_names:
            if self.assertTrue(
                    Wait(self.marionette, timeout=60).until(
                        lambda _: os.path.exists(os.path.join(self.filesLocation, file)))):
                self.verify_tracking_protection_existence()

    def verify_tracking_protection_existence(self):
        for file in self.tracking_protection:
            self.assertTrue(
                Wait(self.marionette, timeout=60).until(
                    lambda _: os.path.exists(os.path.join(self.filesLocation, file))))
