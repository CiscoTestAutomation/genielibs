import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_redistribute_internal


class TestConfigureBgpRedistributeInternal(unittest.TestCase):

    def test_configure_bgp_redistribute_internal(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_redistribute_internal(device, "1")
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1",
                "bgp redistribute-internal",
            ],)
        )