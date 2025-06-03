from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_acl_protocol_port


class TestConfigureAclProtocolPort(TestCase):

    def test_configure_acl_protocol_port(self):
        self.device = Mock()
        configure_acl_protocol_port(self.device, 'ip', 'racl_ipv41', 'permit', 'tcp', 'range', 5500, 5600)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended racl_ipv41', 'permit tcp any any range 5500 5600'],)
        )
