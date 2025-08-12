import unittest
from unittest.mock import Mock, MagicMock, patch
from pyats.topology.device import Device
from genie.libs.sdk.apis.iosxe.health.health import health_cpu


class TestHealthCpu(unittest.TestCase):
    def test_health_cpu(self):
        dev1 = Device('r1', os='iosxe', platform='iosxe')
        output1 = {
          'five_sec_cpu_total': 0,
          'five_sec_cpu_interrupts': 0,
          'one_min_cpu': 0,
          'five_min_cpu': 0,
          'nonzero_cpu_processes': ['process1', 'process2'],
          'sort': {
              1: {
                  'process': 'process1',
                  'pid': 127,
                  'runtime': 1003398,
                  'invoked': 123494916,
                  'usecs': 8,
                  'tty': 0,
                  'five_sec_cpu': 0.07,
                  'one_min_cpu': 0.04,
                  'five_min_cpu': 0.05
              },
              2: {
                  'process': 'process2',
                  'pid': 112,
                  'runtime': 1205941,
                  'invoked': 10486225,
                  'usecs': 115,
                  'tty': 0,
                  'five_sec_cpu': 0.07,
                  'one_min_cpu': 0.05,
                  'five_min_cpu': 0.07
              }
          },
        }
        output2 = {
            'cpu_utilization': {
                'five_sec_cpu_total': 0.01,
                'one_min_cpu': 0.02,
                'five_min_cpu': 0.07,
                'core': {
                    'Core 0': {
                        'core_cpu_util_five_secs': 00.01,
                        'core_cpu_util_one_min': 0.01,
                        'core_cpu_util_five_min': 0.01
                    },
                    'Core 1': {
                        'core_cpu_util_five_secs': 0.01,
                        'core_cpu_util_one_min': 0.01,
                        'core_cpu_util_five_min': 0.01
                    },
                    'Core 2': {
                        'core_cpu_util_five_secs': 0.01,
                        'core_cpu_util_one_min': 0.01,
                        'core_cpu_util_five_min': 0.01
                    }
                }
            },
            'sort': {
                0: {
                    'ppid': 17811,
                    'five_sec_cpu': 0.01,
                    'one_min_cpu': 0.02,
                    'five_min_cpu': 0.01,
                    'status': 'S',
                    'size': 299824,
                    'process': 'process3'
                },
                1: {
                    'ppid': 15826,
                    'five_sec_cpu': 0.01,
                    'one_min_cpu': 0.02,
                    'five_min_cpu': 0.03,
                    'status': 'S',
                    'size': 794488,
                    'process': 'process1'
                }
            }
        }
        output3 = {
            "cpu_utilization": {
                "five_sec_cpu_total": 0.01,
                "one_min_cpu": 0.02,
                "five_min_cpu": 0.15,
                "core": {
                    "Core 0": {
                        "core_cpu_util_five_secs": 0.02,
                        "core_cpu_util_one_min": 0.01,
                        "core_cpu_util_five_min": 0.12
                    },
                    "Core 1": {
                        "core_cpu_util_five_secs": 0.01,
                        "core_cpu_util_one_min": 0.01,
                        "core_cpu_util_five_min": 0.13
                    },
                    "Core 2": {
                        "core_cpu_util_five_secs": 0.03,
                        "core_cpu_util_one_min": 0.01,
                        "core_cpu_util_five_min": 0.14
                    },
                    "Core 4": {
                        "core_cpu_util_five_secs": 0.02,
                        "core_cpu_util_one_min": 0.02,
                        "core_cpu_util_five_min": 0.15
                    },
                    "Core 6": {
                        "core_cpu_util_five_secs": 0.02,
                        "core_cpu_util_one_min": 0.02,
                        "core_cpu_util_five_min": 0.18
                    },
                    "Core 7": {
                        "core_cpu_util_five_secs": 0.04,
                        "core_cpu_util_one_min": 0.02,
                        "core_cpu_util_five_min": 0.15
                    }
                }
            },
            "sort": {
                "0": {
                    "ppid": 16358,
                    "five_sec_cpu": 0.02,
                    "one_min_cpu": 0.02,
                    "five_min_cpu": 0.06,
                    "status": "S",
                    "size": 297280,
                    "process": "fed main event"
                },
                "1": {
                    "ppid": 6649,
                    "five_sec_cpu": 0.02,
                    "one_min_cpu": 0.01,
                    "five_min_cpu": 0.14,
                    "status": "S",
                    "size": 909712,
                    "process": "linux_iosd-imag"
                },
                "2": {
                    "ppid": 6960,
                    "five_sec_cpu": 0.01,
                    "one_min_cpu": 0.01,
                    "five_min_cpu": 0.02,
                    "status": "S",
                    "size": 76160,
                    "process": "sif_mgr"
                }
            }
        }

        dev1.parse = Mock()
        dev1.parse.side_effect = [output1, output2]
        result = health_cpu(dev1, processes=['process1', 'process2', 'process3'])
        expected_output = {'health_data': [{'process': 'process1', 'value': 0.07}, {'process': 'process1_1', 'value': 0.01}, 
                                           {'process': 'process2', 'value': 0.07}, {'process': 'process3', 'value': 0.01}]}
        self.assertEqual(result, expected_output)
        
        dev2 = Device('r2', os='iosxe', platform='iosxe')
        dev2.parse = Mock()
        dev2.parse.side_effect = [output1, output2]
        result = health_cpu(dev2, processes=['process1', 'process2', 'process3'], add_total=True)
        expected_output = {'health_data': [{'process': 'ALL_PROCESSES', 'value': 0.01}, {'process': 'process1', 'value': 0.07},
                                           {'process': 'process1_1', 'value': 0.01}, {'process': 'process2', 'value': 0.07}, {'process': 'process3', 'value': 0.01}]}
        self.assertEqual(result, expected_output)
        
        dev3 = Device('r3', os='iosxe', platform='iosxe')
        dev3.parse = Mock()
        dev3.parse.side_effect = [output1]
        result = health_cpu(dev3, command='test_command', processes=['process1', 'process2', 'process3'])
        expected_output = {'health_data': [{'process': 'process1', 'value': 0.07}, {'process': 'process2', 'value': 0.07}]}
        self.assertEqual(result, expected_output)

        dev4 = Device('r4', os='iosxe', platform='iosxe')
        dev4.parse = Mock()
        dev4.parse.side_effect = [output3]
        result = health_cpu(dev4, command='test_command', processes=['fed', 'linux_iosd-imag', 'sif_mgr'])
        expected_output = {'health_data': [{'process': 'linux_iosd-imag', 'value': 0.02}, {'process': 'sif_mgr', 'value': 0.01}]}
        self.assertEqual(result, expected_output)
      
     