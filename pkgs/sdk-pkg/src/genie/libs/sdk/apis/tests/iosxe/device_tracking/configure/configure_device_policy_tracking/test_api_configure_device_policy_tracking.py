from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.controllers.clear import clear_controllers_ethernet_controller


class TestClearControllersEthernetController(TestCase):

    def test_clear_controllers_ethernet_controller(self):
        device = Mock()
        result = clear_controllers_ethernet_controller(device, 'HundredGigE2/0/15')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify execute was called with the correct command
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear controllers ethernet-controller HundredGigE2/0/15',)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()