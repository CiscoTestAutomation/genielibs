import re
# Genie
from genie.ops.base import Base
from genie.metaparser.util.schemaengine import Any


class Platform(Base):

    schema = {
        'platform': {
            'chassis': Any(),
            'chassis_sn': Any(),
            'rtr_type': Any(),
            'os': Any(),
            'version': Any(),
            'image': Any(),
            'config_register': Any(),
            'main_mem': Any(),
            'dir': Any(),
            'redundancy_mode': Any(),
            'switchover_reason': Any(),
            'redundancy_communication': Any(),
            'swstack': Any(),
            'issu_rollback_timer_state': Any(),
            'issu_rollback_timer_reason': Any(),
            'virtual_device': {
                Any(): {
                    'name': Any(),
                    'status': Any(),
                    'membership': {
                        Any(): {
                            'type': Any(),
                            'status': Any(),
                        },
                    },
                },
            },
            'slot': {
                'rp': {
                    Any(): {
                        'name': Any(),
                        'state': Any(),
                        'swstack_role': Any(),
                        'redundancy_state': Any(),
                        'uptime': Any(),
                        'system_image': Any(),
                        'boot_image': Any(),
                        'config_register': Any(),
                        'sn': Any(),
                        'subslot': {
                            'subslot': {
                                'name': Any(),
                                'state' : Any(),
                                'sn' : Any(),
                            },
                        },
                        'issu': {
                            'in_progress': Any(),
                            'last_operation': Any(),
                            'terminal_state_reached': Any(),
                            'runversion_executed': Any(),
                        },
                    },
                },
                'lc': {
                    Any(): {
                        'name': Any(),
                        'state': Any(),
                        'sn': Any(),
                        'subslot': {
                            Any(): {
                                'name': Any(),
                                'state': Any(),
                                'sn': Any(),
                            },
                        },
                    },
                },
                'oc': {
                    Any(): {
                        'name': Any(),
                        'state': Any(),
                        'sn': Any(),
                    }
                }
            }
        }
    }

    exclude = ['rp_uptime',
               'disk_free_space',
               'uptime',
               'switchover_reason',
               'disk_used_space',
               'total_free_bytes',
               'disk_total_space',
               'main_mem',
               'date',
               'index',
               'chassis_sn',
               'image',
               'sn',
               'rp_boot_image',
               'installed_packages',
               'version']
