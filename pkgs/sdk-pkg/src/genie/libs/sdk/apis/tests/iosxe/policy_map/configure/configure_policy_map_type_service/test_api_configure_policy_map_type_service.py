import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_type_service
)


class TestConfigurePolicyMapTypeService(unittest.TestCase):

    def test_configure_policy_map_type_service(self):
        device = Mock()

        result = configure_policy_map_type_service(
            device,
            'map1',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type service map1'],)
        )

    def test_configure_policy_map_type_service_with_traffic_class(self):
        device = Mock()

        result = configure_policy_map_type_service(
            device,
            policy_map_name='SERVICE_SPOLICE',
            class_name='CLASS_SPOLICE',
            police_input_rate='8000',
            police_input_bc='9000',
            police_input_be='10000',
            aaa_accounting_list='AAA_LIST',
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'policy-map type service SERVICE_SPOLICE',
                    'class type traffic CLASS_SPOLICE',
                    'police input 8000 9000 10000',
                    'accounting aaa list AAA_LIST',
                ],
            )
        )
