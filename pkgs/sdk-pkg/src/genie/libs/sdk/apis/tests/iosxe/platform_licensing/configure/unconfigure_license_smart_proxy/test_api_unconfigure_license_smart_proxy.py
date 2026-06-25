import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_license_smart_proxy


class TestUnconfigureLicenseSmartProxy(unittest.TestCase):

    def test_unconfigure_license_smart_proxy(self):
        device = Mock()

        result = unconfigure_license_smart_proxy(
            device,
            '1.1.1.1',
            80
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no license smart proxy address 1.1.1.1', 'no license smart proxy port 80'],)
        )