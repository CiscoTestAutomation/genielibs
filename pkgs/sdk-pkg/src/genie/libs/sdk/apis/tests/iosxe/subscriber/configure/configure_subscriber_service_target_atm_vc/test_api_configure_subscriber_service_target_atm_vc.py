import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.subscriber.configure import configure_subscriber_service_target_atm_vc


class TestConfigureSubscriberServiceTargetAtmVc(unittest.TestCase):

    def test_configure_subscriber_service_target_atm_vc(self):
        device = Mock()
        result = configure_subscriber_service_target_atm_vc(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "subscriber service target-atm-vc"
        )
