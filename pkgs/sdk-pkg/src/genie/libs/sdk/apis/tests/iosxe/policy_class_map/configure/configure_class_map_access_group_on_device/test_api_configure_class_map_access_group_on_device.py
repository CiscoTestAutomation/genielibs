import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import configure_class_map_access_group_on_device


class TestConfigureClassMapAccessGroupOnDevice(unittest.TestCase):

    def test_configure_class_map_access_group_on_device(self):
        device = Mock()

        result = configure_class_map_access_group_on_device(
            device,
            'cm-acl100',
            '100'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['class-map match-all cm-acl100', 'match access-group 100'],)
        )