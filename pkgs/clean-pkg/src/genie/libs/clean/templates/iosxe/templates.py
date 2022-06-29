DEFAULT = {
    'connect': {},
    'apply_configuration': {
        'configuration': ''
    },
    'change_boot_variable': {
        'images': [],
        'timeout': 150
    },
    'tftp_boot': {
        'image': [],
        'ip_address': [],
        'gateway': '',
        'subnet_mask': '',
        'tftp_server': '',
        'recovery_password': '',
        'recovery_username': '',
        'save_system_config': bool,
        'timeout': 1200
    },
    'install_remove_inactive': {
        'timeout': 180
    },
    'install_image': {
        'images:': [],
        'save_system_config': True,
        'install_timeout': 1000,
        'reload_timeout': 1000
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
    'powercycle': {},

    'order': ['connect',
              'apply_configuration',
              'change_boot_variable',
              'tftp_boot',
              'install_remove_inactive',
              'install_image',
              'ping_server',
              'copy_to_linux',
              'copy_to_device',
              'write_erase',
              'reload',
              'verify_running_image',
              'backup_file_on_device',
              'delete_backup_from_device',
              'delete_files_from_server',
              'powercycle']
}
