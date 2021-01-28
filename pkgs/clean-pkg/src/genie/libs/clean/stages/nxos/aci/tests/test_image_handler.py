import unittest

from genie.libs.clean.stages.nxos.aci.image_handler import ImageHandler

from unittest.mock import Mock


class ValidStructures(unittest.TestCase):

    CONTROLLER_IMAGE = '/path/to/controller_image.bin'
    SWITCH_IMAGE = '/path/to/switch_image.bin'

    EXPECTED_CONTROLLER = [CONTROLLER_IMAGE]
    EXPECTED_SWITCH = [SWITCH_IMAGE]

    def setUp(self):
        self.device = Mock()

    def test_structure_1(self):
        images = [
            self.SWITCH_IMAGE
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)

    def test_structure_2(self):
        images = {
            'switch': [self.SWITCH_IMAGE]
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)

    def test_structure_3(self):
        images = {
            'switch': {
                'file': [self.SWITCH_IMAGE]
            }
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)


class InvalidStructures(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_structure_1_extra_entry(self):
        images = [
            '/path/to/switch_image.bin',
            'invalid entry'
        ]

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)

    def test_structure_2_extra_type(self):
        images = {
            'switch': ['/path/to/switch_image.bin'],
            'this shouldnt work': ['/path/to/switch_image.bin']
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)



if __name__ == '__main__':
    unittest.main()