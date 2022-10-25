from utils.download_ruc_files import URL, PATH, find_zip_url, scan_files, download_zips, unzipping_files
from unittest import TestCase
import unittest


class MainTest(TestCase):

    def test_find_zip_url(self):
        list_zip_url = find_zip_url(url=URL)

        self.assertEqual(len(list_zip_url), 10)
        print('Test find rucs url complete... ')

    def test_download_zip_rucs(self):
        download_zips()
        list_files = scan_files('.zip')

        self.assertEqual(len(list_files), 10)
        print('Test download ruc files complete... ')

    def test_unziping_rucs(self):
        unzipping_files()
        list_files = scan_files('.txt')

        self.assertEqual(len(list_files), 10)
        print('Test unzipping rucs file complete... ')


if __name__ == '__main__':
    unittest.main()
