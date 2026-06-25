import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_service_policy_with_queueing_name
)


class TestConfigureServicePolicyWithQueueingName(unittest.TestCase):

    def test_configure_service_policy_with_queueing_name(self):
        device = Mock()
        device.configure.return_value = (
            'interface FourHundredGigE1/0/17\r\n'
            'interface FourHundredGigE1/0/17\r\n'
            'service-policy type queue output llq\r\n'
            'service-policy type queue output llq\r\n'
        )

        result = configure_service_policy_with_queueing_name(
            device,
            'FourHundredGigE1/0/17',
            'queue',
            'llq'
        )

        self.assertEqual(
            result,
            'interface FourHundredGigE1/0/17\r\n'
            'interface FourHundredGigE1/0/17\r\n'
            'service-policy type queue output llq\r\n'
            'service-policy type queue output llq\r\n'
        )
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface FourHundredGigE1/0/17',
              'service-policy type queue output llq'],)
        )