--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* filetransferutils
    * Added entry point to load internal filetransferutils and updated the plugin discovery mechanism.

* fileserver/protocols/scp
    * Added RSA host key generation alongside Ed25519.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* protocols/http
    * Updated stat() to follow redirects and, when HEAD reports `Content-Length 0`, fall back to a ranged GET to derive total size from `Content-Range`.

* bases/fileutils
    * Fix _resolve_fileutils_class to validate protocol and prevent wrapper class resolution


