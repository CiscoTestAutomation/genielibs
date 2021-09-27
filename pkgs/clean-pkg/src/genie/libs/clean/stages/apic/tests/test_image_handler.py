import unittest

from genie.libs.clean.stages.apic.image_handler import ImageHandler

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
            self.CONTROLLER_IMAGE,
            self.SWITCH_IMAGE
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.controller, self.EXPECTED_CONTROLLER)
        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)

    def test_structure_1_only_controller(self):
        images = [
            self.CONTROLLER_IMAGE
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.controller, self.EXPECTED_CONTROLLER)

    def test_structure_1_only_switch(self):
        images = [
            self.SWITCH_IMAGE
        ]

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)

    def test_structure_2(self):
        images = {
            'controller': [self.CONTROLLER_IMAGE],
            'switch': [self.SWITCH_IMAGE]
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.controller, self.EXPECTED_CONTROLLER)
        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)

    def test_structure_2_only_controller(self):
        images = {
            'controller': [self.CONTROLLER_IMAGE],
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.controller, self.EXPECTED_CONTROLLER)

    def test_structure_2_only_switch(self):
        images = {
            'switch': [self.SWITCH_IMAGE]
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)


    def test_structure_3(self):
        images = {
            'controller': {
                'file': [self.CONTROLLER_IMAGE]
            },
            'switch': {
                'file': [self.SWITCH_IMAGE]
            }
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.controller, self.EXPECTED_CONTROLLER)
        self.assertEqual(image_handler.switch, self.EXPECTED_SWITCH)

    def test_structure_3_only_controller(self):
        images = {
            'controller': {
                'file': [self.CONTROLLER_IMAGE]
            }
        }

        image_handler = ImageHandler(self.device, images)

        self.assertEqual(image_handler.controller, self.EXPECTED_CONTROLLER)

    def test_structure_3_only_switch(self):
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

    def test_structure_2_extra_type(self):
        images = {
            'controller': ['/path/to/controller_image.bin'],
            'switch': ['/path/to/switch_image.bin'],
            'this shouldnt work': ['/path/to/switch_image.bin']
        }

        with self.assertRaises(Exception):
            ImageHandler(self.device, images)



if __name__ == '__main__':
    unittest.main()