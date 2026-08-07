import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    enable_keepalive_on_interface
)


class TestEnableKeepaliveOnInterface(unittest.TestCase):

    def test_enable_keepalive_on_interface(self):
        device = Mock()

        result = enable_keepalive_on_interface(
            device,
            'Virtual-Template1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Virtual-Template1',
              'keepalive'],)
        )