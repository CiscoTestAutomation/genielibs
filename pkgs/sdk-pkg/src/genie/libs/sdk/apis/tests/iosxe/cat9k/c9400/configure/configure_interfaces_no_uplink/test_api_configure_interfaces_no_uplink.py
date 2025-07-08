from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat9k.c9400.configure import configure_interfaces_no_uplink
from unittest.mock import Mock


class TestConfigureInterfacesNoUplink(TestCase):

    def test_configure_interfaces_no_uplink(self):
        self.device = Mock()
        result = configure_interfaces_no_uplink(self.device, ['TenGigabitEthernet1/0/3'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet1/0/3', 'no uplink'],)
        )
