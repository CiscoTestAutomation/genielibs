import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_platform_acl_egress_dscp_enable


class TestConfigurePlatformAclEgressDscpEnable(unittest.TestCase):

    def test_configure_platform_acl_egress_dscp_enable(self):
        device = Mock()

        result = configure_platform_acl_egress_dscp_enable(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('platform access-list egress-dscp enable',)
        )