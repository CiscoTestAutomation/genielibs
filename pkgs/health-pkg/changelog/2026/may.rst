--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats_health.yaml
    * Added ``crashinfo`` health check section
        * Calls ``health_crashinfo`` SDK API as a post-processor on each testcase to detect, copy, and delete new crashinfo files generated during the job
        * Uses ``delete_files true`` to remove crashinfo files from the device after copying
        * Controlled by ``health_settings.checks[crashinfo]`` flag
    * Added ``crashinfo_pre_check`` section
        * Runs ``health_crashinfo`` as a post-processor on ``CommonSetup`` to record a baseline of pre-existing crashinfo files, ensuring only files that appear during testcases are flagged
        * Uses ``copy_files false, delete_files false`` — does not touch existing files on device
        * Uses ``failed_result_status passx`` so a pre-existing file does not block the run


