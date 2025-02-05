from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_service_all_algs
from unittest.mock import Mock


class TestConfigureNatServiceAllAlgs(TestCase):

    def test_configure_nat_service_all_algs(self):
        self.device = Mock()
        result = configure_nat_service_all_algs(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip nat service all-algs',)
        )
