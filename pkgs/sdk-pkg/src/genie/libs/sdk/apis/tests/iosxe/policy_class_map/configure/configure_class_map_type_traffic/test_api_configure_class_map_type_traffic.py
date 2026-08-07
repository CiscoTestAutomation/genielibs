import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.policy_class_map.configure import (
    configure_class_map_type_traffic,
)


class TestConfigureClassMapTypeTraffic(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_configure_class_map_type_traffic(self):
        result = configure_class_map_type_traffic(
            self.device,
            class_name='CLASS_SPOLICE',
            match_type='match-any',
            output_acl='isg_acl1',
            input_acl='isg_acl1',
        )
        self.assertIsNone(result)
        self.device.configure.assert_called_once_with([
            'class-map type traffic match-any CLASS_SPOLICE',
            'match access-group output name isg_acl1',
            'match access-group input name isg_acl1',
        ])
