import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_device_classifier_operator


class TestUnconfigureDeviceClassifierOperator(unittest.TestCase):

    def test_unconfigure_device_classifier_operator(self):
        device = Mock()

        result = unconfigure_device_classifier_operator(
            device, 'condition', 'COND_TEST_A', 'AND'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no device classifier condition COND_TEST_A op AND',)
        )