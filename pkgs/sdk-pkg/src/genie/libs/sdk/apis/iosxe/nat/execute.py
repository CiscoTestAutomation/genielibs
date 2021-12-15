"""Execute CLI functions for nat"""
def execute_clear_nat_translation(device):
    """ Clear All NAT Flows

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = "clear ip nat translation *"
    
    try:
        out = device.execute(cmd)
    except Exception  as err:
        raise Exception(err)

    return out