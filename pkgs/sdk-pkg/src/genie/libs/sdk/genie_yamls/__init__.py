import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

trigger_datafiles = {}
trigger_datafiles['main'] = os.path.join(curr_dir, 'trigger_datafile.yaml')
trigger_datafiles['nxos'] = os.path.join(curr_dir, 'nxos/trigger_datafile_nxos.yaml')
trigger_datafiles['ios'] = os.path.join(curr_dir, 'ios/trigger_datafile_ios.yaml')
trigger_datafiles['iosxe'] = os.path.join(curr_dir, 'iosxe/trigger_datafile_iosxe.yaml')
trigger_datafiles['iosxr'] = os.path.join(curr_dir, 'iosxr/trigger_datafile_xr.yaml')
trigger_datafiles['junos'] = os.path.join(curr_dir, 'junos/trigger_datafile_junos.yaml')
trigger_datafiles['virl'] = os.path.join(curr_dir, 'virl/trigger_datafile_virl.yaml')

verification_datafiles = {}
verification_datafiles['main'] = os.path.join(curr_dir, 'verification_datafile.yaml')
verification_datafiles['nxos'] = os.path.join(curr_dir, 'nxos/verification_datafile_nxos.yaml')
verification_datafiles['ios'] = os.path.join(curr_dir, 'ios/verification_datafile_ios.yaml')
verification_datafiles['iosxe'] = os.path.join(curr_dir, 'iosxe/verification_datafile_iosxe.yaml')
verification_datafiles['iosxr'] = os.path.join(curr_dir, 'iosxr/verification_datafile_xr.yaml')
verification_datafiles['junos'] = os.path.join(curr_dir, 'junos/verification_datafile_junos.yaml')

subsection_datafile = os.path.join(curr_dir, 'subsection_datafile.yaml')
pts_datafile = os.path.join(curr_dir, 'pts_datafile.yaml')


def datafile(mode, os_='main'):
    if mode == 'trigger':
        return trigger_datafiles[os_]
    elif mode == 'verification':
        return verification_datafiles[os_]
    elif mode == 'subsection':
        return subsection_datafile
    elif mode == 'pts':
        return pts_datafile
    elif mode == 'health':
        # import here to avoid circular import error
        import genie.libs.health
        health_datafile = os.path.join(os.path.dirname(genie.libs.health.__file__), 'health_yamls', 'pyats_health.yaml')
        return health_datafile
    else:
        raise Exception('{m} is not a valid datafile mode - valid: '
                        'trigger, verification, subsection, pts or health'.format(m=mode))
