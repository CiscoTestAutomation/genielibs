from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import unconfigure_ip_ssh_client_algorithm_kex
from unittest.mock import Mock


class TestUnconfigureIpSshClientAlgorithmKex(TestCase):

    def test_unconfigure_ip_ssh_client_algorithm_kex(self):
        self.device = Mock()
        result = unconfigure_ip_ssh_client_algorithm_kex(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip ssh client algorithm kex',)
        )
