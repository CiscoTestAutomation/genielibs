--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* genie.libs.conf
    * Fix ParsedInterfaceName to avoid crash with unsupported graph

* nxos
    * Fix feature service-acceleration
        * Add `https_proxy` and `https_port` to the list of attributes to be handled by the conf model
        * Add unit tests
    * Fix nxapi_method_restconf api
        * output from a rest call is a response object, not a list
        * fixed api call to check for instance of `output.json()` which is a list.


