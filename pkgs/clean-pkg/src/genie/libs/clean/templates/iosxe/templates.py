DEFAULT = {
    'connect': {},
    'apply_configuration': {
        'configuration': r"%CLEANARG{preconfig_str}",
        'copy_vdc_all': r"%CLEANARG{copy_vdc_all}",
    },
    'change_boot_variable': {
        'images': r"%CLEANARG{boot_variable}",
        'timeout': r"%CLEANARG{timeout}"
    },
    'tftp_boot': {
        'image': r"%CLEANARG{images}",
        'ip_address': r"%CLEANARG{ip_address}",
        'gateway': r"%CLEANARG{gateway}",
        'subnet_mask': r"%CLEANARG{subnet_mask}",
        'tftp_server': r"%CLEANARG{tftp_server}",
        'recovery_password': r"%CLEANARG{recovery_password}",
        'recovery_username':r"%CLEANARG{recovery_username}",
        'save_system_config': r"%CLEANARG{save_system_config}",
        'timeout': r"%CLEANARG{timeout}"
    },
    'install_remove_inactive': {
        'timeout': r"%CLEANARG{timeout}",
    },
    'install_image': {
        'images': r"%CLEANARG{images}",
        'save_system_config': r"%CLEANARG{save_system_config}",
        'install_timeout': r"%CLEANARG{install_timeout}",
        'reload_timeout': r"%CLEANARG{reload_timeout}"
    },
    'ping_server': {
        'server': r"%CLEANARG{server}",
        'vrf': r"%CLEANARG{vrf}",
    },
    'copy_to_linux':{
        'protocol': r"%CLEANARG{protocol}",
        'append_hostname': r"%CLEANARG{hostname_check}",
        'copy_attempts': r"%CLEANARG{copy_attempts}",
        'destination': {
            'directory': r"%CLEANARG{directory}",
            'hostname': r"%CLEANARG{server}"
        },
        'origin': {
            'files': r"%CLEANARG{files_to_copy}",
            'hostname': r"%CLEANARG{server}",
        },
        'overwrite': r"%CLEANARG{overwrite}"
    },
    'copy_to_device': {
        'origin': {
            'files': r"%CLEANARG{files_to_copy}",
            'hostname':  r"%CLEANARG{server}",
        },
        'destination': {
            'directory': r"%CLEANARG{directory}",
        },
        'protocol': r"%CLEANARG{protocol}",
        'vrf': r"%CLEANARG{vrf}",
        'overwrite': r"%CLEANARG{overwrite}",
        'expected_num_images': r"%CLEANARG{num_images}",
        'timeout': r"%CLEANARG{timeout}",
        'check_file_stability': False
    },
    'write_erase': {
        'timeout': r"%CLEANARG{timeout}"
    },
    'reload': {
        'check_modules': {
            'check': r"%CLEANARG{check}"
        },
        'reload_service_args': {
             'timeout': r"%CLEANARG{timeout}",
             'prompt_recovery': r"%CLEANARG{prompt_recovery}"
        }
    },
    'verify_running_image': {
        'images': r"%CLEANARG{images}"
    },
    'backup_file_on_device': {
        'copy_dir': r"%CLEANARG{copy_dir}",
        'copy_file': r"%CLEANARG{file_name}"
    },
    'delete_backup_from_device': {
        'delete_dir': r"%CLEANARG{delete_dir}",
        'delete_dir_stby': r"%CLEANARG{delete_dir_stby}",
        'delete_file': r"%CLEANARG{file_name}"
    },
    'delete_files_from_server': {
        'server':  r"%CLEANARG{server}",
        'files': r"%CLEANARG{files_to_delete}",
        'protocol':  r"%CLEANARG{protocol}"
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


DEFAULT_ARGS = {
    "directory": "bootflash:",
    "vrf": "management",
    "copy_vdc_all": False,
    "overwrite": False,
}