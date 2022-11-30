# Genie
from genie.ops.base import Base
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Or, Optional

# This will be used for schema validation in the future
schema = {
    Optional('bootvar'): {
        Optional('current_boot_variable'): str,
        Optional('next_reload_boot_variable'): str,       
        Optional('config_file'): str,
        Optional('bootldr'): str,
        Optional('manual_boot'): bool,
        Optional('enable_break'): bool,        
        Optional('boot_mode'): str,
        Optional('ipxe_timeout'): int,
        Optional('active'): {
            Optional('configuration_register'): str,
            Optional("next_reload_configuration_register"): str,
            Optional('boot_variable'): str,
        },
        Optional('standby'): {
            Optional('configuration_register'): str,
            Optional("next_reload_configuration_register"): str,
            Optional('boot_variable'): str,
        },
		'raw_data': {
		    Or('show bootvar', 'show boot'): str
		}
    },
    'config': {
        'running': str
    },
    Optional('environment'): {
        Any(): {  # switch number - 1
            Optional('fans'): {
                str: {  # 1, 2, 3
                    'healthy': bool,  # True/False
                    'status': str,  # 'ok', 'not present'
                    Optional('model'): str,  # 'ok', 'not present', 'failure'
                }
            },
            Optional('power_supply'): {
                str: {  # 1, 2, 3
                    'healthy': bool,  # True/False
                    Optional('model'): str,
                    'status': str,  # 'ok', 'not present'
                }
            },
            Optional('temperature'): {
                'healthy': bool,  # True/False
                'current_temp_celsius': int,  # 33
                'status': str  # 'ok', 'not present', 'green'
            }
        },
        'raw_data': {
            Or('show env all', 'show environment'): str,
        }
    },
    Optional('neighbors'): {
        str: {  # index 1, 2, 3  ...
            'name': str,  # R6
            Optional('addresses'): list,  # ['192.168.1.1', '2001:db8::1']
            'interface': str,  # Ethernet0/1 (remote interface)
            Optional('local_interface'): str,  # GigabitEthernet1/1 (local interface)
        },
        'raw_data': {
            Optional('show cdp neighbors detail'): str,
            Optional('show lldp neighbors detail'): str
        }
    },
    'interfaces': {
        Any(): {  # Port-channel10
            'enabled': bool,  # True, False
            Optional('last_link_flapped'): str,  # to isoformat
            Optional('line_protocol'): bool,  # up, down -> True/False
            Optional('link_state'): bool,  # up, down -> True/False
            Optional('mac_address'): str,  # 006b.f1ff.be9f (xxxx.xxxx.xxxx format)
            Optional('media_type'): str,
            'mtu': int,  # 1500
            Optional('speed'): str,  # auto, 1000
            Optional('speed_unit'): str,  # Gbps, Mbps
            'status': str,  # up, down
            Optional('duplex'): str  # auto, full, etc
        },
		'raw_data': {
		    Or('show interfaces', 'show interface'): str
		}
    },
    Optional('mac_table'): {
        'vlans': {
            str: {  # 100, 'all'(use 'all' for All/CPU)
                'mac_addresses': {
                    str: {  # 11aa.22ff.ee88
                        'interfaces': {
                            str: {  # Router, Ethernet1/0
                                Optional('age'): str,  # 10, -
                                Optional('type'): Or('static', 'dynamic')  # 'static', 'dynamic'
                            }
                        }
                    }
                },
            }
        },
        'raw_data': {
            'show mac address-table': str
        }
    },
    'inventory': {
        str: {  # index 1, 2, 3 ...
            'name': str,  # <name>
            'description': str,  # Cisco Catalyst Series C9500X-28C8D Chassis
            Optional('pid'): str,  # C9500X-28C8D
            Optional('vid'): str,  # V00
            Optional('sn'): str,  # FDO25030SLN
            Optional('oid'): str  # 1.3.6.1.4.1.9.12.3.1.3.2421
        },
		'raw_data': {
		    Or('show inventory', 'show inventory raw'): str
		}
    },
    'version': {
        'os': str,  # iosxe, nxos, iosxr (same with what Unicon has)
        'platform': str,  # cat9k (same with what Unicon has)
        'version': str,  # 9.3(6) (same with what Unicon has)
        Optional('built_date'): str,  # Sat 14-Mar-20 17:41 -> to isoformat
        Optional('built_by'): str,  # prod_rel_team
        Optional('system_image'): str, # bootflash:packages.conf
		'raw_data': {
		    'show version': str
		}
    },
    Optional('power_inline'): {
        'interface': {
            str: {  # GigabitEthernet1/0/1
                'admin_state': Any(),  # auto
                'oper_state': Any(),  # off
                Optional('power'): Any(),  # 0.0, 26.1
                Optional('device'): Any(),  # IP Phone 8845
                Optional('class'): Any(),  # 2, 4
                Optional('max'): Any(),  # 30.0
                'healthy': bool
            }
        },
        'watts': {
            str: {  # 3
                'module': Any(),  # 3
                'available': Any(),  # 472.0
                'used': Any(),  # 0.0
                'remaining': Any()  # 472.0
            }
        },
        'raw_data': {
            'show power inline': str
		}
    }
}


class Device(Base):
    exclude = []

    def __init__(self, *args, **kwargs):
        kwargs.update({'raw_data': True})
        super().__init__(*args, **kwargs)


class ShowRunningConfig(MetaParser):
    cli_command = 'show running-config'

    def cli(self):
        output = self.device.execute(self.cli_command)
        return {'config': output}
