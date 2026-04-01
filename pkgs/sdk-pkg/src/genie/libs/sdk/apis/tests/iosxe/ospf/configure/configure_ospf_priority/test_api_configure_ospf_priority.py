from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_priority


class TestConfigureOspfPriority(TestCase):

    def test_configure_ospf_priority(self):
        device = Mock()
        result = configure_ospf_priority(
            device,
            'GigabitEthernet0/0/0',
            0
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/0', 'ip ospf priority 0'],)
        )