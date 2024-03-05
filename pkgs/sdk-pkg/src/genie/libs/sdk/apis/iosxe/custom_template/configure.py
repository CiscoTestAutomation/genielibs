import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_sdm_prefer_custom_template(device, attribute, custom_template=None, entries=None, priority=None):
    """ Configure SDM Prefer Custom Template
        Args:
            device ('obj'): device to use
            attribute ('str'): sdm prefer custom template value (Ex : commit, vlan)
            custom_template ('str'): sdm prefer custom template value (Ex : pbr)
            entries('int'): number of entries
            priority('int'): priority number
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure SDM Prefer Custom Template
    """
    log.info(
        "Configuring SDM Prefer Custom Template with attribute={}".format(attribute)
    )
    config = [f"sdm prefer custom {attribute}"]
    if custom_template and entries and priority:
        config.append(f"{custom_template} {entries} priority {priority}")
    
    try:
        device.configure(config)

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure sdm prefer custom {attribute}".format(attribute=attribute))

def configure_sdm_prefer_custom_fib(device, attribute, entries, priority):
    ''' Configure SDM Prefer Custom Fib
    Args:
        device ('obj') : Device object
        attribute ('str'): sdm prefer custom template value (mac-address, netflow-in/out,sgt_or_mpls_vpn)
        entries('int'): provide the Number of entries
        priority('int'): provide the priority number
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring sdm prefer custom fib
    '''
    config = []
    config.append('sdm prefer custom fib')
    if attribute in ["mac-address","sgt_or_mpls_vpn","netflow_out","netflow_in"]:
        config.append('{attribute} {entries} priority {priority}'.format(attribute=attribute,entries=entries,priority=priority))
    try:
        device.configure(config) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure sdm prefer custom {attribute}. Error:\n{error}".format(
                attribute=attribute,
                error=e)
        )            

def configure_sdm_prefer_core(device):
    ''' Configure SDM Prefer core
    Args:
        device ('obj') : Device object
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring sdm prefer core
    '''
    try:
        device.configure(['sdm prefer core'])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure sdm prefer core. Error:\n{error}".format(error=e)
        )                    


def configure_sdm_prefer(device, template):
    ''' Configure SDM Prefer {template}
    Args:
        device ('obj') : Device object
        template('str') : SDM template

    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring sdm prefer
    '''
    config = f'sdm prefer {template}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure sdm prefer. Error:\n{e}")