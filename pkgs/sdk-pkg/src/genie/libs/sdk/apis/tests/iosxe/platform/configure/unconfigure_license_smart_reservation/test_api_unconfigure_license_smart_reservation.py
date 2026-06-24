import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_license_smart_reservation


class TestUnconfigureLicenseSmartReservation(unittest.TestCase):

    def test_unconfigure_license_smart_reservation(self):
        device = Mock()

        result = unconfigure_license_smart_reservation(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no license smart reservation',)
        )