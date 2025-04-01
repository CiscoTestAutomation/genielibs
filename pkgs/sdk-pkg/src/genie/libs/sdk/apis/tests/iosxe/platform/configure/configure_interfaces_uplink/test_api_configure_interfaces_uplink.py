from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_interfaces_uplink
from unittest.mock import Mock


class TestConfigureInterfacesUplink(TestCase):

    def test_configure_interfaces_uplink(self):
        self.device = Mock()
        result = configure_interfaces_uplink(self.device, ['TenGigabitEthernet2/0/3'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet2/0/3', 'uplink'],)
        )
