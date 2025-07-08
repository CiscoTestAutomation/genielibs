from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_retransmit_interval
from unittest.mock import Mock


class TestConfigureOspfRetransmitInterval(TestCase):

    def test_configure_ospf_retransmit_interval(self):
        self.device = Mock()
        result = configure_ospf_retransmit_interval(self.device, ' TenGigabitEthernet1/1/2', ' 10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface  TenGigabitEthernet1/1/2', 'ip ospf retransmit-interval  10'],)
        )
