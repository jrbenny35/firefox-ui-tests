import os
import sys

from marionette_driver import By, Wait

from firefox_puppeteer.testcases import FirefoxTestCase

from firefox_puppeteer.ui.browser.window import BrowserWindow


class TestSafeBrowsingPrimaryDownload(FirefoxTestCase):

    data = [
        {
            'platform': ['linux', 'win', 'darwin'],
            'files': [
                # Phishing
                "goog-phish-shavar.cache",
                "goog-phish-shavar.pset",
                "goog-phish-shavar.sbstore",
                "goog-malware-shavar.cache",
                "goog-malware-shavar.pset",
                "goog-malware-shavar.sbstore",
                "goog-badbinurl-shavar.cache",
                "goog-badbinurl-shavar.pset",
                "goog-badbinurl-shavar.sbstore",
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
            'platform': ['win'],
            'files': [
                "goog-downloadwhite-digest256.cache",
                "goog-downloadwhite-digest256.pset",
                "goog-downloadwhite-digest256.sbstore"
            ]
        }
    ]

    def setUp(self):
        FirefoxTestCase.setUp(self)

        # Restart Browser
        self.restart()

        # Set Browser URL
        self.test_url = 'https://mozqa.com'

        # Set Browser Preferences
        self.prefs.set_pref('browser.safebrowsing.provider.google.nextupdatetime', 1)
        self.prefs.set_pref('browser.safebrowsing.provider.mozilla.nextupdatetime', 1)
        self.prefs.set_pref('browser.safebrowsing.enabled', 'true')
        self.prefs.set_pref('browser.safebrowsing.malware.enabled', 'true')
        self.prefs.set_pref('browser.safebrowsing.downloads.enabled', 'true')
        self.prefs.set_pref('browser.safebrowsing.downloads.remote.enabled', 'true')
        self.prefs.set_pref('privacy.trackingprotection.pbmode.enabled', 'true')

        # Set variable to join path
        self.sb_files_path = os.path.join(self.marionette.instance.profile.profile, 'safebrowsing')

    def test_safe_browsing(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.test_url)

        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            self.verify_files_existence()
        elif sys.platform.startswith('win32'):
            self.verify_win_files_existence()

    # Test all besides windows specific
    def verify_files_existence(self):
        for data in self.data:
            if ('linux' or 'darwin') in data['platform']:
                for item in data['files']:
                    self.assertTrue(
                        Wait(self.marionette, timeout=300).until(
                            lambda _: os.path.exists(os.path.join(self.sb_files_path, item))))

    # Test windows specific files
    def verify_win_files_existence(self):
        for data in self.data:
            if 'win' in data['platform']:
                for item in data['files']:
                    self.assertTrue(
                        Wait(self.marionette, timeout=300).until(
                            lambda _: os.path.exists(os.path.join(self.sb_files_path, item))))
