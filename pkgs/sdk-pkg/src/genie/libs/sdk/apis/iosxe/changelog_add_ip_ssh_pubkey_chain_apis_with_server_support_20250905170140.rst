--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------
* IOSXE
    * Added configure_ip_ssh_pubkey_chain:
        * API to configure SSH public key chain for user and server authentication
        * Supports both username and server IP address configurations
        * Supports both key-string (interactive) and key-hash (direct) modes
        * Examples:
            * Username with key-string: configure_ip_ssh_pubkey_chain(username='cisco', key_string='ssh-rsa ...')
            * Username with key-hash: configure_ip_ssh_pubkey_chain(username='cisco', key_hash='1234567890abcdef')
            * Server with key-string: configure_ip_ssh_pubkey_chain(server='192.168.1.100', key_string='ssh-rsa ...')
            * Server with key-hash: configure_ip_ssh_pubkey_chain(server='192.168.1.100', key_hash='1234567890abcdef')
    * Added unconfigure_ip_ssh_pubkey_chain:
        * API to unconfigure SSH public key chain for user and server authentication
        * Supports both username and server IP address configurations
        * Examples:
            * Username: unconfigure_ip_ssh_pubkey_chain(username='cisco')
            * Server: unconfigure_ip_ssh_pubkey_chain(server='192.168.1.100')
