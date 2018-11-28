import os
curr_dir = os.path.dirname(os.path.abspath(__file__))

trigger_datafiles = {}
trigger_datafiles['nxos'] = os.path.join(curr_dir, 'nxos/trigger_datafile_nxos.yaml')
trigger_datafiles['iosxe'] = os.path.join(curr_dir, 'iosxe/trigger_datafile_iosxe.yaml')
trigger_datafiles['iosxr'] = os.path.join(curr_dir, 'iosxr/trigger_datafile_xr.yaml')
trigger_datafiles['junos'] = os.path.join(curr_dir, 'junos/trigger_datafile_junos.yaml')

verification_datafiles = {}
verification_datafiles['nxos'] = os.path.join(curr_dir, 'nxos/verification_datafile_nxos.yaml')
verification_datafiles['iosxe'] = os.path.join(curr_dir, 'iosxe/verification_datafile_iosxe.yaml')
verification_datafiles['iosxr'] = os.path.join(curr_dir, 'iosxr/verification_datafile_xr.yaml')
verification_datafiles['junos'] = os.path.join(curr_dir, 'junos/verification_datafile_junos.yaml')

subsection_datafile = os.path.join(curr_dir, 'subsection_datafile.yaml')
pts_datafile = os.path.join(curr_dir, 'pts_datafile.yaml')
