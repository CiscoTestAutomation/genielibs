import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_platform_acl_egress_dscp_enable


class TestUnconfigurePlatformAclEgressDscpEnable(unittest.TestCase):

    def test_unconfigure_platform_acl_egress_dscp_enable(self):
        device = Mock()

        result = unconfigure_platform_acl_egress_dscp_enable(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no platform access-list egress-dscp enable',)
        )