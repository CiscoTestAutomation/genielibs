--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe/cat9k
    * Added new stage to support StackWise Virtual unconfiguration
    * Modified verify_stack_wise_virtual_config step to verify StackWise Virtual configuration on all device members

* clean-pkg
    * skip the SVL interfaces in configure_interface stage as they are not supported in SVL.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* stages
    * Update Connect stage to use parameters.internal for correct result_rollup handling

* stages/iosxe
    * Update Connect stage to use parameters.internal for correct result_rollup handling


