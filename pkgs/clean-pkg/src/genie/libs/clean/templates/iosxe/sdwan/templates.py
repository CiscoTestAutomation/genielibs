DEFAULT = {
    'connect': {},
    'apply_configuration': {
        'configuration': ''
    },
    'expand_image': {
        'image': ''
    },
    'set_controller_mode': {
        'mode': 'enable',
        'reload_timeout': 600,
        'delete_inactive_versions': True
    },
    'change_boot_variable': {
        'images': '',
        'timeout': 150
    },
    'tftp_boot': {
        'image': [],
        'ip_address': [],
        'gateway': '',
        'subnet_mask': '',
        'tftp_server': '',
        'recovery_password': '',
        'timeout': 1200
    },
    'ping_server': {
        'server': ''
    },
     'copy_to_linux':{
        'protocol': '',
        'append_hostname': bool,
        'copy_attempts': 1,
        'destination': {
            'directory': '',
            'hostname': ''
        },
        'origin': {
            'files': [],
            'hostname': '',
        },
        'overwrite': True
    },
    'copy_to_device': {
        'origin': {
            'files': [],
            'hostname': '',
        },
        'destination': {
            'directory': '',
        },
        'protocol': '',
        'vrf': '',
        'timeout': 300,
        'check_file_stability': False
    },
    'write_erase': {
        'timeout': 100
    },
    'reload': {
        'check_modules': {
            'check': False
        },
        'reload_service_args': {
             'timeout': 900,
             'prompt_recovery': False
        }
    },
    'verify_running_image': {
        'images': []
    },
    'backup_file_on_device': {
        'copy_dir': '',
        'copy_file': ''
    },
    'delete_backup_from_device': {
        'delete_dir': '',
        'delete_dir_stby': '',
        'delete_file': ''
    },
    'delete_files_from_server': {
        'server': '',
        'files': [],
        'protocol': ''
    },
    'install_image': {
        'images': [],
        'save_system_config': True,
        'install_timeout': 1000,
        'reload_timeout': 1000
    },
    'powercycle': {},
    'device_recovery': {
        'break_count': 120,
        'console_activity_pattern': 'System Bootstrap',
        'golden_image': [],
        'recovery_password': 'admin',
        'timeout': 1400
    },

    'order': ['connect',
              'apply_configuration',
              'expand_image',
              'change_boot_variable',
              'tftp_boot',
              'set_controller_mode',
              'ping_server',
              'copy_to_linux',
              'copy_to_device',
              'write_erase',
              'reload',
              'verify_running_image',
              'backup_file_on_device',
              'delete_backup_from_device',
              'delete_files_from_server',
              'install_image',
              'powercycle' ]
}
