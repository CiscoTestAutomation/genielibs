from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_sap_pmk_on_cts
from unittest.mock import Mock

class TestConfigureSapPmkOnCts(TestCase):

    def test_configure_sap_pmk_on_cts(self):
        self.device = Mock()
        result = configure_sap_pmk_on_cts(self.device, 'HundredGigE1/0/23', '0000000000000000000000000000000000000000000000000000000012345678', 'gcm-encrypt null gmac no-encap')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface HundredGigE1/0/23','cts manual','sap pmk 0000000000000000000000000000000000000000000000000000000012345678 mode-list gcm-encrypt null gmac no-encap'],)
        )