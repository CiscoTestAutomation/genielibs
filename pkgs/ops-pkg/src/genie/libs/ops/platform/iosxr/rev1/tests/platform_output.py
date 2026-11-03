'''
Platform Genie Ops Object Outputs for IOSXR (rev1).

Chassis serial number related parser outputs, trimmed to the Rack 0 parts.
'''


class PlatformOutput(object):

    # =========================
    # NCS-5501-SE (fixed chassis)
    # =========================

    # 'admin show diag chassis' output
    ncs5501AdminShowDiagChassisOutput = {
        'rack_num': 0,
        'pid': 'NCS-5501-SE',
        'vid': 'V01',
        'sn': 'FOC23332ACR',
        'clei': 'INMAK00CRA',
        'part_number': '73-17712-06',
        'part_revision': 'H0',
        'hw_version': '1.1',
        'top_assembly_block': {
            'serial_number': 'FOC2335R0FK',
            'part_number': '68-5861-02',
            'part_revision': 'J0',
            'mfg_deviation': '0',
            'hw_version': '1.0',
            'mfg_bits': '1'}}

    # 'show inventory' output
    ncs5501ShowInventoryOutput = {
        'module_name': {
            'Rack 0': {
                'descr': 'NCS5501 1RU Chassis',
                'pid': 'NCS-5501-SE',
                'vid': 'V01',
                'sn': 'FOC2335R0FK'}}}

    # 'show diag details' output
    ncs5501ShowDiagDetailsOutput = {
        'item': {
            'Rack 0': {
                'description': 'NCS5501 1RU Chassis',
                'common_blocks': {
                    'block_signature': '0xabab',
                    'block_version': 3,
                    'block_length': 160,
                    'block_checksum': '0x16ec',
                    'eeprom_size': 65535,
                    'block_count': 6,
                    'fru_major_type': '0x6001',
                    'fru_minor_type': '0x200',
                    'oem_string': 'Cisco Systems, Inc.',
                    'pid': 'NCS-5501-SE',
                    'serial_number': 'FOC23332ACR',
                    'part_number': '73-17712-06',
                    'part_revision': 'H0',
                    'mfg_deviation': '0',
                    'hw_version': '1.1',
                    'mfg_bits': 1,
                    'engineer_use': 0,
                    'snmpoid': '9.12.3.1.3.1800.0.0',
                    'power_consumption': '99 W',
                    'rma_code': '0-0-0-0',
                    'clei_code': 'INMAK00CRA',
                    'vid': 'V01'},
                'chassis_specific_blocks': {
                    'block_signature': '0x6001',
                    'block_version': 3,
                    'block_length': 39,
                    'block_checksum': '0x500',
                    'feature_bits': '0x0',
                    'hw_change_bit': '0xe01ca',
                    'stackmib_oid': 0,
                    'mac_address': 'd4-6a-35-e2-bc-00',
                    'num_of_macs': 1024},
                'second_serial_no_specific_blocks': {
                    'serial_number': 'FOC2335R0FK'},
                'top_assesmbly_blocks': {
                    'block_signature': '0x600a',
                    'block_version': 1,
                    'block_length': 72,
                    'block_checksum': '0xc0f',
                    'serial_number': 'FOC2335R0FK',
                    'part_number': '68-5861-02',
                    'part_revision': 'J0',
                    'mfg_deviation': '0',
                    'hw_version': '1.0',
                    'mfg_bits': 1}}}}

    # Rack 0 with Common Blocks only (no Second Serial / Top Assembly blocks)
    commonBlocksOnlyShowInventoryOutput = {
        'module_name': {
            'Rack 0': {
                'descr': 'NCS5501 1RU Chassis',
                'pid': 'NCS-5501-SE',
                'vid': 'V01',
                'sn': 'FOC2335R0FK'}}}

    commonBlocksOnlyShowDiagDetailsOutput = {
        'item': {
            'Rack 0': {
                'description': 'NCS5501 1RU Chassis',
                'common_blocks': {
                    'block_signature': '0xabab',
                    'block_version': 3,
                    'block_length': 160,
                    'block_checksum': '0x16ec',
                    'pid': 'NCS-5501-SE',
                    'serial_number': 'FOC23332ACR',
                    'part_number': '73-17712-06',
                    'part_revision': 'H0',
                    'clei_code': 'INMAK00CRA',
                    'vid': 'V01'}}}}

    # =========================
    # 8201-32FH
    # =========================

    # 'show diag details' output
    c8201ShowDiagDetailsOutput = {
        'item': {
            'Rack 0-Chassis': {
                'description': 'Cisco 8000 Series 32x400G QSFPDD 1RU Fixed '
                               'System w/HBM',
                'controller_family': '0045',
                'controller_type': '06b1',
                'pid': '8201-32FH',
                'vid': 'V03',
                'udi_description': 'Cisco 8000 Series 32x400G QSFPDD 1RU '
                                   'Fixed System w/HBM',
                'chassis_serial_number': 'FLM263401XF',
                'top_assy_part_number': '68-7325-05',
                'top_assy_revision': 'B0',
                'pcb_serial_number': 'FLM263303GJ',
                'pca_number': '73-20364-02',
                'pca_revision': 'E0',
                'clei_code': 'CMM6210ARC',
                'eci_number': '477690',
                'deviation_number': {
                    '1': '0', '2': '0', '3': '0', '4': '0', '5': '0'},
                'manufacturing_number': '00 00 00 00 00 00 00 00',
                'calibration_data': '00000000',
                'chassis_mac_address': '3c26.e4b6.8c00',
                'mac_address_block_size': '512',
                'hardware_revision': '1.0',
                'device_value_1': '42 e0 00 08 28 00 00 00'}}}

    # =========================
    # 8011-12G12X4Y-A
    # =========================

    # 'show inventory' output
    c8011ShowInventoryOutput = {
        'module_name': {
            'Rack 0': {
                'descr': 'Cisco 8011 Series Fixed 1RU Router 4x1/10/25G '
                         '12x1/10G 12x1G',
                'pid': '8011-12G12X4Y-A',
                'vid': 'V00',
                'sn': 'FDO29180127'}}}

    # 'show diag details' output
    c8011ShowDiagDetailsOutput = {
        'item': {
            'Rack 0-CHASSIS': {
                'description': 'Cisco 8011 Series Fixed 1RU Router '
                               '4x1/10/25G 12x1/10G 12x1G',
                'controller_family': '0045',
                'controller_type': '11a4',
                'udi_description': 'Cisco 8011 Series Fixed 1RU Router '
                                   '4x1/10/25G 12x1/10G 12x1G',
                'mac_address_block_size': '256',
                'base_mac_address': '38aa.0918.4b00',
                'hardware_revision': '9.5',
                'pca_number': '73-21348-05',
                'pca_revision': '03',
                'pcb_serial_number': 'FDO29180127',
                'top_assy_part_number': '68-7689-08',
                'top_assy_revision': '03',
                'chassis_serial_number': 'FDO29180127',
                'clei_code': 'UNASSIGNED',
                'eci_number': '0',
                'pid': '8011-12G12X4Y-A',
                'vid': 'V00',
                'device_value_1': '40 00 00 09 00 00 08 00',
                'deviation_number': {
                    '1': '0', '2': '0', '3': '0', '4': '0', '5': '0'}}}}
