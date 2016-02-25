import os
import sys

from marionette_driver import By, Wait
from firefox_puppeteer.testcases import FirefoxTestCase


class TestSafeBrowsingPrimaryDownload(FirefoxTestCase):

    data = [
        {
            'platform': ['linux2', 'win32', 'darwin'],
            'files': [
                # Phishing
                "goog-badbinurl-shavar.cache",
                "goog-badbinurl-shavar.pset",
                "goog-badbinurl-shavar.sbstore",
                "goog-malware-shavar.cache",
                "goog-malware-shavar.pset",
                "goog-malware-shavar.sbstore",
                "goog-phish-shavar.cache",
                "goog-phish-shavar.pset",
                "goog-phish-shavar.sbstore",
                "goog-unwanted-shavar.cache",
                "goog-unwanted-shavar.pset",
                "goog-unwanted-shavar.sbstore",

                # Tracking Protections
                "mozstd-track-digest256.cache",
                "mozstd-track-digest256.pset",
                "mozstd-track-digest256.sbstore",
                "mozstd-trackwhite-digest256.cache",
                "mozstd-trackwhite-digest256.pset",
                "mozstd-trackwhite-digest256.sbstore"
                ]
            },
        {
            'platform': ['win32'],
            'files': [
                "goog-downloadwhite-digest256.cache",
                "goog-downloadwhite-digest256.pset",
                "goog-downloadwhite-digest256.sbstore"
            ]
        }
    ]

    browser_prefs = {
        'browser.safebrowsing.downloads.enabled': 'true',
        'browser.safebrowsing.downloads.remote.enabled': 'true',
        'browser.safebrowsing.enabled': 'true',
        'browser.safebrowsing.malware.enabled': 'true',
        'browser.safebrowsing.provider.google.nextupdatetime': 1,
        'browser.safebrowsing.provider.mozilla.nextupdatetime': 1,
        'privacy.trackingprotection.pbmode.enabled': 'true'
    }

    def setUp(self):
        FirefoxTestCase.setUp(self)

        # Restart Browser
        self.restart()

        # Set Browser Preferences
        for item, value in self.browser_prefs.items():
            self.prefs.set_pref(item, value)

        # Set Variable to tmp safebrowsing directory
        self.sb_files_path = os.path.join(self.marionette.instance.profile.profile, 'safebrowsing')

    def test_safe_browsing(self):
        for data in self.data:
            if sys.platform in data['platform']:
                for item in data['files']:
                    self.assertTrue(
                        Wait(self.marionette, timeout=30).until(
                            lambda _: os.path.exists(os.path.join(self.sb_files_path, item))))


        #if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        #    self.verify_files_existence()
        #elif sys.platform.startswith('win32'):
        #    self.verify_win_files_existence()

    # Test all besides windows specific
    def verify_files_existence(self):
        for data in self.data:
            if ('linux' or 'darwin') in data['platform']:
                for item in data['files']:
                    self.assertTrue(
                        Wait(self.marionette, timeout=30).until(
                            lambda _: os.path.exists(os.path.join(self.sb_files_path, item))))

    # Test windows specific files
    def verify_win_files_existence(self):
        for data in self.data:
            if 'win' in data['platform']:
                for item in data['files']:
                    self.assertTrue(
                        Wait(self.marionette, timeout=30).until(
                            lambda _: os.path.exists(os.path.join(self.sb_files_path, item))))
