--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* health
    * Updated default health yaml
        * Changed to new argument style with '--health-tc-uids', '--health-tc-sections'
        * Added 'escape_regex_chars' argument to `get_testcase_name` api action
    * Updated default health yaml
        * Changed to use 'add_total True' for cpu/memory checks

* health plugin
    * Renamed '--health-webex' argument to '--health-notify-webex'.
    * Added DeprecationWarning message for deprecated arguments
    * Suppressed deprecated arguments from CLI help
    * Modified `--health-file` argument
        * File paths or URLs can now be passed as CLI arguments


