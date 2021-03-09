# Python
import re
import time
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def switch_vm_power(device, vm_id, state):
    """ Switch power of VM On/Off
        Args:
            vm_id ('str'): The id of the VM
            state ('str'): Power state to be switched to, eg. 'on' / 'off'
        Raises:
            N/A
        Returns:
            out ('str'): 
    """
    output = device.execute("vim-cmd vmsvc/power.{state} {vm_id}".\
        format(state=state,
               vm_id=vm_id))
    if '(vim.fault.NotFound)' in output:
        raise ValueError("The given vm_id: {vmid} does not exist.".\
            format(vmid=vm_id))
    

def get_vm_power_state(device, vm_name, vm_id):
    """ Get the power state of VM
        Args:
            vm_name ('str'): Name of the VM
            vm_id ('str'): The id of the VM
        Raises:
            N/A
        Returns:
            ('str'): "on" or "off"
    """
    try:
        log.info("Getting power state of VM {vm}".format(vm=vm_name))
        output = device.execute("vim-cmd vmsvc/power.getstate {vm_id}".\
            format(vm_id=vm_id))
    except Exception as err:
        log.error("Could not get power state of VM {vm} with error: {err}".\
            format(vm=vm_name,
                   err=str(err)))
        return None
        
    if 'Powered on' in output:
        return 'ON'
    else:
        return 'OFF'

def get_server_vm(device, vm_hostname):
    """ Get all VMs on server
        Args:
            vm_hostname ('str'): VM name to check for on ESXI server
        Raises:
            N/A
        Returns:
            devs ('dict'): Dictionary of VMs that are on the ESXI server, 
            where the key is the name of the VM and the value is its VM id.
            
        Parser schema for vim-cmd vmsvc/getallvms
        schema = {
            'vmid': {
                Any(): {
                    'vmid': str,
                    'name': str,
                    'file': str,
                    'guest_os': str,
                    'version': str,
                    Optional('annotation'): str,
                }
            }
        }
    """
    devs = {}
    
    try:
        output = device.parse("vim-cmd vmsvc/getallvms")
    except SchemaEmptyParserError as err:
        log.error("Could not get the VMs on {dev} with error: {err}".\
            format(dev=device.name, err=str(err)))
        return None    
    
    if output is not None:
        vms = output.get('vmid')
        
        for vmid in vms:
            vm_name = vms[vmid].get('name')
            if vm_name == vm_hostname:
                del vms[vmid]['name']
                devs.setdefault(vm_name, vms[vmid])
    else:
        return None
    
    return devs


def get_vm_snapshot(device, vm_name, vm_id, snapshot_name):
    """ Get the snapshot id for the given device
        Args:
            vm_name ('str'): Name of the VM
            vm_id ('str'): The id of the VM
            snapshot_name ('str'): Name of the snapshot to be reverted to, 
                                    Default is golden
        Raises:
            N/A
        Returns:
            ('str'): The snapshot id
    """
    try:
        output = device.parse('vim-cmd vmsvc/snapshot.get {vm_id}'.\
            format(vm_id=vm_id))
        
    except SchemaEmptyParserError as err:
        log.error("Failed to get snapshot {snapshot} on {vm} wtih error:"
                  " {err}".format(snapshot=snapshot_name,
                                  vm=vm_name,
                                  err=str(err)))
        return None
    
    if output:
        vms = output.get('vmid')
        for vmid in vms:
            snapshots = vms[vmid].get('snapshot')
            if snapshots:
                for snapshot_id in snapshots:                    
                    if snapshot_name in snapshots[snapshot_id].get('name'):
                        return int(snapshots[snapshot_id].get('id'))
                        
    return None


def revert_vm_snapshot(device, vm_name, vm_id, vm_snapshot_id,
                                  snapshot_name='golden'):
    """ Revert VM back to provided snapshot
        Args:
            vm_name ('str'): Name of the VM
            vm_id ('int'): The id of the VM on the ESXi server
            vm_snapshot_id ('int'): The id of the required snapshot
            snapshot_name ('str'): Name of the snapshot to be reverted to,
                                    Default is golden         
        Raises:
            N/A
        Retuns:
            vm_recovery_status ('tuple'): String message indicating the recovery 
            status of the each VM.
    """
    
    cmd = 'vim-cmd vmsvc/snapshot.revert {vm_id} {snapshot_id} 0'.\
        format(vm_id=vm_id, snapshot_id=vm_snapshot_id)
    output = device.execute(cmd)
    
    if 'doesnt exist' in output:
        raise Exception("Snapshot not found on {dev}".format(dev=vm_name))
