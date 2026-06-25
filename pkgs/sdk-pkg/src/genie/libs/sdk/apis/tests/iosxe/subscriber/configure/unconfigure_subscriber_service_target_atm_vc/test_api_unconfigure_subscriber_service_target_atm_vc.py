import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.subscriber.configure import unconfigure_subscriber_service_target_atm_vc


class TestUnconfigureSubscriberServiceTargetAtmVc(unittest.TestCase):

    def test_unconfigure_subscriber_service_target_atm_vc(self):
        device = Mock()
        result = unconfigure_subscriber_service_target_atm_vc(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no subscriber service target-atm-vc"
        )
