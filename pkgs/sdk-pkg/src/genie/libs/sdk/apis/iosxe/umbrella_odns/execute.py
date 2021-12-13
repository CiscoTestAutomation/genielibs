"""Execute umbrella dns command"""

def execute_test_ngdns_lookup(
    device, 
    domain_name,
):
    """ Execute dns query using test cli
        Args:
            device ('obj'): device to use
            domain_name ('str'): URL whihc we want to validate
        Returns:
            test execution command 
        Raises:
            SubCommandFailure: test ngdns cli
    """
    cmd = "test ngdns lookup {}".format(domain_name)

    try:
        out = device.execute(cmd)
    except Exception  as err:
        raise Exception(err)

    return out

def execute_clear_dns_statistics(
    device,
):
    """ Execute test CLI to Clear umbrella dns querey/response statistics
        Args:
            device ('obj'): device to use
        Returns:
            clear statistics execution command
        Raises:
            SubCommandFailure: test ngdns cli
    """
    cmd = "clear dns-umbrella statistics"

    try:
        out = device.execute(cmd)
    except Exception  as err:
        raise Exception(err)
    return out

