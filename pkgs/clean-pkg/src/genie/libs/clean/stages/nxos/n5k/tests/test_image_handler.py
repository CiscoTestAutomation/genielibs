import unittest

from genie.libs.clean.stages.nxos.n7k.image_handler import ImageHandler

from unittest.mock import Mock


class ValidStructures(unittest.TestCase):

    KICKSTART_IMAGE = '/path/to/kickstart_image.bin'
    SYSTEM_IMAGE = '/path/to/system_image.bin'

    EXPECTED_KICKSTART = [KICKSTART_IMAGE]
    EXPECTED_SYSTEM = [SYSTEM_IMAGE]

    def setUp(self):
        self.device = Mock()

    def test_structure_1(self):
        images = [
            self.KICKSTART_IMAGE,
            self.SYSTEM_IMAGE
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.kickstart, self.EXPECTED_KICKSTART)
        self.assertEqual(image_handler.system, self.EXPECTED_SYSTEM)


    def test_structure_2(self):
        images = {
            'kickstart': [self.KICKSTART_IMAGE],
            'system': [self.SYSTEM_IMAGE]
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.kickstart, self.EXPECTED_KICKSTART)
        self.assertEqual(image_handler.system, self.EXPECTED_SYSTEM)


    def test_structure_3(self):
        images = {
            'kickstart': {
                'file': [self.KICKSTART_IMAGE]
            },
            'system': {
                'file': [self.SYSTEM_IMAGE]
            }
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.kickstart, self.EXPECTED_KICKSTART)
        self.assertEqual(image_handler.system, self.EXPECTED_SYSTEM)


class InvalidStructures(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_structure_1_missing_entry(self):
        images = [
            '/path/to/kickstart_image.bin',
        ]

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)

    def test_structure_2_missing_kickstart(self):
        images = {
            'system': ['/path/to/system_image.bin']
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)

    def test_structure_2_missing_system(self):
        images = {
            'kickstart': ['/path/to/kickstart_image.bin']
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)

    def test_structure_2_extra_type(self):
        images = {
            'kickstart': ['/path/to/kickstart_image.bin'],
            'system': ['/path/to/system_image.bin'],
            'this shouldnt work': ['/path/to/system_image.bin']
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)

    def test_structure_3_missing_kickstart(self):
        images = {
            'system': {
                'file': ['/path/to/system_image.bin']
            }
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)

    def test_structure_3_missing_system(self):
        images = {
            'kickstart': {
                'file': ['/path/to/system_image.bin']
            }
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)

    def test_structure_3_extra_type(self):
        images = {
            'system': {
                'file': ['/path/to/system_image.bin'],
                'this shouldnt work': ['/path/to/system_image.bin']
            },
            'kickstart': {
                'file': ['/path/to/system_image.bin'],
                'this shouldnt work': ['/path/to/system_image.bin']
            },
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)


if __name__ == '__main__':
    unittest.main()