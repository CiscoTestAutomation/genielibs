from unittest import TestCase
from genie.libs.sdk.apis.iosxe.utils import get_show_output_begin
from unittest.mock import Mock


class TestGetShowOutputBegin(TestCase):

    def test_get_show_output_begin(self):
        self.device = Mock()

        results_map = {
            "show version | begin Switch 02": """Switch 02
---------
Switch uptime                      : 1 week, 23 hours, 56 minutes 

Base Ethernet MAC Address          : 00:2f:5c:cc:c0:80
Motherboard Assembly Number        : 73-18274-04
Motherboard Serial Number          : FOC22491Y3C
Model Revision Number              : A0
Motherboard Revision Number        : A0
Model Number                       : C9300-48P
System Serial Number               : FCW2250E0ES
Last reload reason                 : Reload Slot Command
CLEI Code Number                   : INM2110ARB

Switch 03
---------
Switch uptime                      : 1 week, 1 day, 3 minutes 

Base Ethernet MAC Address          : 0c:d0:f8:d9:87:00
Motherboard Assembly Number        : 73-18271-03
Motherboard Serial Number          : FOC22370T2W
Model Revision Number              : A0
Motherboard Revision Number        : A0
Model Number                       : C9300-24P
System Serial Number               : FOC2238Q0P2
Last reload reason                 : redundancy force-switchover
CLEI Code Number                   : INM2T10ARB
"""
        }

        def results_side_effect(command, *args, **kwargs):
            return results_map.get(command)

        self.device.execute.side_effect = results_side_effect

        result = get_show_output_begin(self.device, 'show version', 'Switch 02', None)

        # verify the command executed
        self.assertIn(
            'show version | begin Switch 02',
            self.device.execute.call_args_list[0][0]
        )

        # verify return value
        expected_output = [True, results_map["show version | begin Switch 02"]]
        self.assertEqual(result, expected_output)