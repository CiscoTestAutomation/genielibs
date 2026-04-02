import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import enable_ipv6_eigrp_router


class TestEnableIpv6EigrpRouter(TestCase):

    def test_enable_ipv6_eigrp_router(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = enable_ipv6_eigrp_router(device, '66', router_id='1.1.1.1')

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('ipv6 router eigrp 66', sent_commands)
        self.assertIn('router-id 1.1.1.1', sent_commands)


if __name__ == '__main__':
    unittest.main()