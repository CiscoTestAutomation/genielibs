# Copyright (c) 2022 by Cisco Systems, Inc.
# All rights reserved.


import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_gnxi(
    device,
    enable=True,
    server=False,
    secure_server=False,
    secure_port=None,
    port=None,
    secure_allow_self_signed_trustpoint=False,
    secure_client_auth=False,
    secure_init=False,
    secure_password_auth=False,
    secure_peer_verify_trustpoint=None,
    secure_trustpoint=None):
    """
    Create new vrf definition
        Args:
            device ('obj'): device to use
            enable ('bool', optional): Enable and start GNxI
            server ('bool', optional): Enable the GNxI (insecure) server
            secure-server ('bool', optional): Enable the GNxI secure server
            secure-port ('int', optional): Set GNxI secure server port
            port ('int', optional):  gnxi (insecure) server port
            secure-allow-self-signed-trustpoint ('bool', optional): Allow the GNxI secure server to use the self-signed certificate. Requires service internal configuration.
            secure-client-auth ('bool', optional): Enable client authentication
            secure-init ('bool', optional): Enable the GNxI secure server by using the primary self-signed cert
            secure-password-auth ('bool', optional): Enable password authentication
            secure-peer-verify-trustpoint ('str', optional): Set GNxI server peer validation trustpoint
            secure-trustpoint ('str', optional): Set GNxI server certificate trustpoint
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure GNxI
    """
    cmd_list = []

    log.info("Configuring GNXI")
    if enable:
        cmd_list.append('gnxi')
    if secure_port:
        cmd_list.append(f"gnxi secure-port {secure_port}")
    if port:
        cmd_list.append(f"gnxi port {port}")
    if secure_allow_self_signed_trustpoint:
        cmd_list.append("gnxi secure-allow-self-signed-trustpoint")
    if secure_client_auth:
        cmd_list.append("gnxi secure-client-auth")
    if secure_password_auth:
        cmd_list.append("gnxi secure-password-auth")
    if secure_peer_verify_trustpoint:
        cmd_list.append(f"gnxi secure-peer-verify-trustpoint {secure_peer_verify_trustpoint}")
    if secure_trustpoint:
        cmd_list.append(f"gnxi secure-trustpoint {secure_trustpoint}")
    if secure_init:
        cmd_list.append("gnxi secure-init")
    if server:
        cmd_list.append("gnxi server")
    if secure_server:
        cmd_list.append("gnxi secure-server")

    try:
        device.configure(cmd_list)
        return cmd_list
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure GNxI. Error:\n{e}")
