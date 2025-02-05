from copy import deepcopy

DEFAULT = {
    'connect': {},

    'reset_configuration': {},

    'apply_configuration': {
        'configuration': r"%CLEANARG{apply_configuration__configuration}",
    },

    'install_remove_inactive': {
        'timeout': r"%CLEANARG{install_remove_inactive__timeout}"
    },

    'install_remove_smu': {
        'timeout': r"%CLEANARG{install_remove_smu__timeout}"
    },

    'configure_management': {
        'protocols': r"%CLEANARG{configure_management__protocols}",
    },

    'copy_to_device': {
        'destination': {
            'directory': r"%CLEANARG{copy_to_device__destination_directory}",
        },
        'protocol': r"%CLEANARG{copy_to_device__protocol}",
        'overwrite': r"%CLEANARG{copy_to_device__overwrite}",
        'expected_num_images': r"%CLEANARG{copy_to_device__expected_num_images}",
        'timeout': r"%CLEANARG{copy_to_device__timeout}",
        'check_file_stability': r"%CLEANARG{copy_to_device__check_file_stability}"
    },

    'install_image': {
        'install_timeout': r"%CLEANARG{install_image__install_timeout}",
        'reload_timeout': r"%CLEANARG{install_image__reload_timeout}",
    },

    'install_smu': {
        'install_timeout': r"%CLEANARG{install_smu__install_timeout}",
    },

    'order': [
        'connect',
        'reset_configuration',
        'install_remove_inactive',
        'install_remove_smu',
        'configure_management',
        'apply_configuration',
        'copy_to_device',
        'install_image',
        'install_smu'
    ]
}

DEFAULT_ARGS = {
    "copy_to_device__destination_directory": "bootflash:",
    "copy_to_device__timeout": 1800,
    "copy_to_device__overwrite": False,
    "copy_to_device__check_file_stability": False,
    "configure_management__protocols": ['telnet', 'ssh', 'netconf',  'tftp', 'http'],
    "install_image__install_timeout": 1800,
    "install_image__reload_timeout": 1800,
    "install_smu__install_timeout": 700,
    "install_remove_inactive__timeout": 180,
    "install_remove_smu__timeout": 700,
    "apply_configuration__configuration": "",
    "copy_to_device__protocol": "http",
    "copy_to_device__expected_num_images": 1,
}


# LOAD_IMAGE
LOAD_IMAGE = deepcopy(DEFAULT)
LOAD_IMAGE.pop('reset_configuration')
LOAD_IMAGE.get('order').remove('reset_configuration')
LOAD_IMAGE_ARGS = deepcopy(DEFAULT_ARGS)
