import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import stack_ports_enable_disable


class TestStackPortsEnableDisable(unittest.TestCase):

    def test_stack_ports_enable_disable(self):
        device = Mock()

        result = stack_ports_enable_disable(device, 1, 2, 'enable')

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('switch 1 stack port 2 enable',)
        )