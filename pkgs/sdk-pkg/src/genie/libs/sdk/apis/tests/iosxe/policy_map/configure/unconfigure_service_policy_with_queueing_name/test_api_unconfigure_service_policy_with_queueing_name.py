import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_service_policy_with_queueing_name
)


class TestUnconfigureServicePolicyWithQueueingName(unittest.TestCase):

    def test_unconfigure_service_policy_with_queueing_name(self):
        device = Mock()

        result = unconfigure_service_policy_with_queueing_name(
            device,
            'hundredGigE1/0/5',
            'queueing',
            'nonllq'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface hundredGigE1/0/5',
              'no service-policy type queueing output nonllq'],)
        )