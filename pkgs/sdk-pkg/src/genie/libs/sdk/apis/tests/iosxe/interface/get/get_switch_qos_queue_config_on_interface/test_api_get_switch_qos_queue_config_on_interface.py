import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_switch_qos_queue_config_on_interface


class TestGetSwitchQosQueueConfigOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_switch_qos_queue_config_on_interface(self):
        result = get_switch_qos_queue_config_on_interface(self.device, 'GigabitEthernet3/0/6', '3')
        expected_output = {'0       0     796       0       0     890       0       0    1000       0': {'1       0     956       0       0    1068       0       0    1200       0': {},
                                                                               '2       0       0       0       0       0       0       0       0       0': {},
                                                                               '3       0       0       0       0       0       0       0       0       0': {},
                                                                               '4       0       0       0       0       0       0       0       0       0': {},
                                                                               '5       0       0       0       0       0       0       0       0       0': {},
                                                                               '6       0       0       0       0       0       0       0       0       0': {},
                                                                               '7       0       0       0       0       0       0       0       0       0': {}},
 '0   1  2   200   3   800  19   475   0     0   3  2400      En': {'--------   -------------   ------  ------------': {'2     Shaped           254         255': {}},
                                                                    '--------   -------------   ------  ------------   -------------': {},
                                                                    '0      0     Shared            50           0           0': {},
                                                                    '1      0     Shared            75           0           0': {},
                                                                    '1   1  0     0   4  1200  19   712   8   300   3  2400      En': {},
                                                                    '2      0     Shared         10000           0           0': {},
                                                                    '2   1  0     0   0     0   0     0   0     0   3  2400      En': {},
                                                                    '3      0     Shared         10000           0           0': {},
                                                                    '3   1  0     0   0     0   0     0   0     0   3  2400      En': {},
                                                                    '4      0     Shared         10000           0           0': {},
                                                                    '4   1  0     0   0     0   0     0   0     0   3  2400      En': {},
                                                                    '5      0     Shared         10000           0           0': {},
                                                                    '5   1  0     0   0     0   0     0   0     0   3  2400      En': {},
                                                                    '6      0     Shared         10000           0           0': {},
                                                                    '6   1  0     0   0     0   0     0   0     0   3  2400      En': {},
                                                                    '7      0     Shared         10000           0           0': {},
                                                                    '7   1  0     0   0     0   0     0   0     0   3  2400      En': {},
                                                                    'Port       Port            Port    Port': {},
                                                                    'Priority   Shaped/shared   weight  shaping_step': {},
                                                                    'Priority   Shaped/shared   weight  shaping_step  sharpedWeight': {}},
 'AFD:Disabled FlatAFD:Disabled QoSMap:0 HW Queues: 40 - 47': {'----- --------  --------  --------  --------  ---------  -------': {},
                                                               'DrainFast:Disabled PortSoftStart:2 - 1800': {'DTS  Hardmax  Softmax   PortSMin  GlblSMin  PortStEnd   QEnable': {}}},
 'Asic:0 Core:1 DATA Port:5 GPN:198 LinkSpeed:0x1': {},
 'Weight0 Max_Th0 Min_Th0 Weigth1 Max_Th1 Min_Th1  Weight2 Max_Th2 Min_Th2': {'------- ------- ------- ------- ------- -------  ------- ------- ------': {}}}
        self.assertEqual(result, expected_output)
