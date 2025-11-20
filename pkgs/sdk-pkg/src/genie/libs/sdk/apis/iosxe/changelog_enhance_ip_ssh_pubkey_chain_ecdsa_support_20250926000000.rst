--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------
* IOSXE
    * Added configure_ip_ssh_stricthostkeycheck:
        * API to configure SSH strict host key checking
        * Examples:
            * Enable strict host key checking: device.api.configure_ip_ssh_stricthostkeycheck()
    * Added unconfigure_ip_ssh_stricthostkeycheck:
        * API to unconfigure SSH strict host key checking
        * Examples:
            * Disable strict host key checking: device.api.unconfigure_ip_ssh_stricthostkeycheck()

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------
* IOSXE
    * Enhanced configure_ip_ssh_pubkey_chain:
        * Added ECDSA key type support and improved key type detection
        * Enhanced key-string handling with better folding (70 chars per line) and timeout management
        * Improved key-hash processing with automatic key type detection for RSA, ECDSA, and Ed25519
        * Added better error handling and prompt management for both key-string and key-hash modes
        * Fixed dialog handling to prevent buffer overflow issues with delays between lines
        * Updated examples to show ECDSA key usage patterns
        * Enhanced exit handling and configuration mode cleanup
        * Examples:
            * ECDSA key-string: configure_ip_ssh_pubkey_chain(username='cisco', key_string='ecdsa-sha2-nistp256 AAAAE2VjZHNh...')
            * ECDSA key-hash with type: configure_ip_ssh_pubkey_chain(username='cisco', key_hash='ecdsa-sha2-nistp256 A1B2C3D4...')
            * Auto-detected hash: configure_ip_ssh_pubkey_chain(username='cisco', key_hash='A1B2C3D4...') # Defaults to ssh-rsa
    * Enhanced unconfigure_ip_ssh_pubkey_chain:
        * Improved configuration mode exit handling with better prompt detection
        * Added better cleanup logic to ensure proper return to exec mode
        * Enhanced error handling for removal operations
        * Fixed prompt checking and fallback mechanisms