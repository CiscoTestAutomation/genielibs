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


class ImageOverride(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.clean = {
            'tftp_boot': {
                'image': ['/path/to/my/image.bin']
            },
            'change_boot_variable': {
                'images': ['/path/to/my/image.bin']
            },
            'expand_image': {
                'image': ['/path/to/my/image.bin']
            },
            'verify_running_image': {
                'images': ['/path/to/my/image.bin']
            },
            'install_image': {
                'images': ['/path/to/my/image.bin']
            },
            'install_packages': {
                'packages': ['/path/to/my/package.bin']
            },
        }

        images = ['/path/to/image.bin', '/path/to/package.bin']

        self.image_handler = ImageHandler(self.device, images)

    def test_image_override_tftp_boot(self):
        self.image_handler.override_stage_images = True
        self.image_handler.update_section('tftp_boot')
        self.assertEqual(self.image_handler.device.clean['tftp_boot'], {'image': ['/path/to/image.bin']})

    def test_image_override_change_boot_variable(self):
        self.image_handler.override_stage_images = True
        self.image_handler.update_section('change_boot_variable')
        self.assertEqual(self.image_handler.device.clean['change_boot_variable'], {'images': ['/path/to/image.bin']})

    def test_image_override_expand_image(self):
        self.image_handler.override_stage_images = True
        self.image_handler.update_section('expand_image')
        self.assertEqual(self.image_handler.device.clean['expand_image'], {'image': ['/path/to/image.bin']})

    def test_image_override_verify_running_image(self):
        self.image_handler.override_stage_images = True
        self.image_handler.update_section('verify_running_image')
        self.assertEqual(self.image_handler.device.clean['verify_running_image'], {'images': ['/path/to/image.bin']})

        self.device.clean['verify_running_image']['verify_md5'] = True
        self.image_handler.update_section('verify_running_image')
        self.assertEqual(self.image_handler.device.clean['verify_running_image'],
            {'images': ['/path/to/image.bin'], 'verify_md5': True})
        self.device.clean['verify_running_image']['verify_md5'] = False

    def test_image_override_install_image(self):
        self.image_handler.override_stage_images = True
        self.image_handler.update_section('install_image')
        self.assertEqual(self.image_handler.device.clean['install_image'], {'images': ['/path/to/image.bin']})

    def test_image_override_install_packages(self):
        self.image_handler.override_stage_images = True
        self.image_handler.update_section('install_packages')
        self.assertEqual(self.image_handler.device.clean['install_packages'], {'packages': ['/path/to/package.bin']})


    def test_image_no_override_tftp_boot(self):
        self.image_handler.override_stage_images = False
        self.image_handler.update_section('tftp_boot')
        self.assertEqual(self.image_handler.device.clean['tftp_boot'], {'image': ['/path/to/my/image.bin']})

    def test_image_no_override_change_boot_variable(self):
        self.image_handler.override_stage_images = False
        self.image_handler.update_section('change_boot_variable')
        self.assertEqual(self.image_handler.device.clean['change_boot_variable'], {'images': ['/path/to/my/image.bin']})

    def test_image_no_override_expand_image(self):
        self.image_handler.override_stage_images = False
        self.image_handler.update_section('expand_image')
        self.assertEqual(self.image_handler.device.clean['expand_image'], {'image': ['/path/to/my/image.bin']})

    def test_image_no_override_verify_running_image(self):
        self.image_handler.override_stage_images = False
        self.image_handler.update_section('verify_running_image')
        self.assertEqual(self.image_handler.device.clean['verify_running_image'], {'images': ['/path/to/my/image.bin']})

        self.device.clean['verify_running_image']['verify_md5'] = True
        self.image_handler.update_section('verify_running_image')
        self.assertEqual(self.image_handler.device.clean['verify_running_image'],
            {'images': ['/path/to/my/image.bin'], 'verify_md5': True})
        self.device.clean['verify_running_image']['verify_md5'] = False

    def test_image_no_override_install_image(self):
        self.image_handler.override_stage_images = False
        self.image_handler.update_section('install_image')
        self.assertEqual(self.image_handler.device.clean['install_image'], {'images': ['/path/to/my/image.bin']})

    def test_image_no_override_install_packages(self):
        self.image_handler.override_stage_images = False
        self.image_handler.update_section('install_packages')
        self.assertEqual(self.image_handler.device.clean['install_packages'], {'packages': ['/path/to/my/package.bin']})

if __name__ == '__main__':
    unittest.main()
