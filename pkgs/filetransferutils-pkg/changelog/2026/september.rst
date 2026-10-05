--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* iosxe
    * Modified
        * File transfers temporarily use the requested source interface and restore the original interface configuration afterward.

* filetransferutils
    * Modified
        * HTTP filesize checks now include the HTTP status, reason, redirect URL, and relevant response headers in diagnostic errors while redacting URL credentials.


--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* iosxr
    * Added automatic temporary transfer routing to FileUtils.
        * A temporary host route towards the file transfer endpoint is now installed for the duration of a copy and removed afterwards. This is the default behaviour on IOSXR and requires no opt-in flag.
        * The route is only installed when the transfer endpoint is a remote IP address, a management gateway is declared in the testbed, and the device does not already reach the endpoint via that gateway. A DNS hostname or a device local path (``disk0:``, ``harddisk:`` ...) never triggers a route.


