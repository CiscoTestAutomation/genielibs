import unittest

from genie.libs.clean.stages.iosxe.image_handler import ImageHandler

from unittest.mock import Mock


class ValidStructures(unittest.TestCase):

    IMAGE = '/path/to/image.bin'
    PACKAGE_1 = '/path/to/package1.bin'
    PACKAGE_2 = '/path/to/package2.bin'

    EXPECTED_IMAGE = [IMAGE]
    EXPECTED_SINGLE_PKG = [PACKAGE_1]
    EXPECTED_DOUBLE_PKG = [PACKAGE_1, PACKAGE_2]

    def setUp(self):
        self.device = Mock()

    def test_structure_1_without_package(self):
        images = [
            self.IMAGE,
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)

    def test_structure_1_with_package(self):
        images = [
            self.IMAGE,
            self.PACKAGE_1
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)
        self.assertEqual(image_handler.packages, self.EXPECTED_SINGLE_PKG)

    def test_structure_1_with_packages(self):
        images = [
            self.IMAGE,
            self.PACKAGE_1,
            self.PACKAGE_2
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)
        self.assertEqual(image_handler.packages, self.EXPECTED_DOUBLE_PKG)

    def test_structure_2_without_packages(self):
        images = {
            'image': [
                self.IMAGE
            ],
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)

    def test_structure_2_with_package(self):
        images = {
            'image': [
                self.IMAGE
            ],
            'packages': [
                self.PACKAGE_1
            ]
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)
        self.assertEqual(image_handler.packages, self.EXPECTED_SINGLE_PKG)

    def test_structure_2_with_packages(self):
        images = {
            'image': [
                self.IMAGE
            ],
            'packages': [
                self.PACKAGE_1,
                self.PACKAGE_2
            ]
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)
        self.assertEqual(image_handler.packages, self.EXPECTED_DOUBLE_PKG)

    def test_structure_3_without_packages(self):
        images = {
            'image': {
                'file': [
                    self.IMAGE
                ]
            }
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)

    def test_structure_3_with_package(self):
        images = {
            'image': {
                'file': [
                    self.IMAGE
                ]
            },
            'packages': {
                'file': [
                    self.PACKAGE_1
                ]
            }
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)
        self.assertEqual(image_handler.packages, self.EXPECTED_SINGLE_PKG)

    def test_structure_3_with_packages(self):
        images = {
            'image': {
                'file': [
                    self.IMAGE
                ]
            },
            'packages': {
                'file': [
                    self.PACKAGE_1,
                    self.PACKAGE_2
                ]
            }
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.image, self.EXPECTED_IMAGE)
        self.assertEqual(image_handler.packages, self.EXPECTED_DOUBLE_PKG)


class InvalidStructures(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_structure_1_missing_entry(self):
        images = []

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)


if __name__ == '__main__':
    unittest.main()