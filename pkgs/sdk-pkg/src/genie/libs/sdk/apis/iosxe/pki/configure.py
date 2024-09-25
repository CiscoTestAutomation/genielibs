import time
from unicon.eal.dialogs import Statement, Dialog
import logging 

logger = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

def configure_crypto_pki_server(device, 
                                server_name=None,
                                password=None,
                                auto_rollover_time=None, 
                                cdp_url_type=None, 
                                cdp_url_ip_path=None,
                                crl_file_name=None,
                                database_archive_type=None, 
                                archive_password=None, 
                                database_level=None, 
                                database_url_server=None, 
                                database_ip_path=None, 
                                database_url_storage_location=None, 
                                database_url_publish=False, 
                                eku_options=None, 
                                grant_mode=None, 
                                grant_rollover_cert=None,
                                grant_tp_list=None, 
                                grant_trustpoint=None, 
                                hash_type=None, 
                                issuer_name=None, 
                                ca_cert_life=None, 
                                cert_life=None,
                                crl_life=None, 
                                enrol_req_life=None, 
                                mode=None, 
                                mode_ra_transparent=False, 
                                serial_number=None,
                                enrollment_ip=None,
                                enrollment_path=None,
                                revoke_chk=None,
                                key_len=None,
                                port=80,
                                **kwargs):

    ''' 
        Configure crypto pki server
        Args:
            device ('obj'): Device object
            server_name ('str'): Name for the pki server
            auto_rollover_time('str'): Auto rollover time <days> <hours> <minutes>
            cdp_url_server ('str') : cdp url server (http | ldap)
            cdp_url_ip_path ('str') : cdp url ip path 
            database_archive_type ('str') : Database archive type either pem or pkcs12
            archive_password ('str') : Database archive password
            archive_encryption_type ('int') : Database archive encryption type (0-9)
            database_level ('str') : Database level (complete|minimum|names)
            database_url_server ('str') : Database server (http | ldap) 
            database_ip_path ('str') : Exact path for database file
            database_url_storage_location ('str') : Database url storage location (cnm|crl|crt etc.)
            database_url_publish ('bool') : Database url publish option for cnm, crl,crt
            database_user ('str') : Database username
            eku_options ('str') : eku options that needs to be configured (1 or more)
            grant_mode ('str') : Grant request mode (auto | none | ra-auto)
            grant_rollover_cert ('str') : Grant auto rollover certificate (ca-cert | ra-cert)
            grant_tp_list ('str') : grant trustpoints (upto 5 trustpoints)
            grant_trustpoint ('str') : Label of trustpoint holding trusted CA cert
            hash_type ('str') : Hash algorithm type (md5, sha1, sha256, sha384, sha512)
            issuer_name ('str') : Issuer name to be configured
            ca_cert_life ('str') : Ca certificate lifetime in format <days(0-7305)> <hours(0-23)> or  <days(0-7305)> <hours(0-23)> <minutes(0-59)>
            cert_life ('str') : Certificate lifetime in format <days(0-7305)> <hours(0-23)> or  <days(0-7305)> <hours(0-23)> <minutes(0-59)>
            crl_life ('str') : crl lifetime in format <hours(0-336)> or  <hours(0-336)> <minutes(0-59)>
            enrol_req_life ('str') : enrollment request lifetime in format <hours(0-1000)> or  <hours(0-1000)> <minutes(0-59)>
            mode ('str') : Modes (ra|sub-cs)
            mode_ra_transparent ('bool') : True if want to enable transparent in ra mode
            serial_number ('str') : serial number of last issued ceritificate 
            enrollment_ip ('str') : Ip address for CA server enrollment URL
            enrollment_path ('str') : Path for CA server enrollment URL
            revoke_chk ('str') : Type of revocation check (none|crl|ocsp)
            key_len ('int') : Key length for RSA keypair 
            port ('int') : Port number for CA server enrollment
        Returns:
            True/False
    '''

    if kwargs:
        from genie.libs.sdk.apis.iosxe.eaptls.configure import configure_crypto_pki_server as eaptls_configure_crypto_pki_server
        return eaptls_configure_crypto_pki_server(device=device, server_name=server_name, issuer_name=issuer_name, 
                                                  password=password, **kwargs)

    dialog = Dialog([
                Statement(pattern=r'.*Password:',
                    action=f'sendline({password})',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Re-enter password:',
                    action=f'sendline({password})',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Do you accept this certificate.*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
            ])

    logger.info("Configuring crypto pki server")

    server_config = []
    server_config.append(f"ip http server")

    if mode and enrollment_ip and enrollment_path is None:
        server_config.append(f"crypto pki trustpoint {server_name}")
        server_config.append(f"enroll url http://{enrollment_ip}:{port}")
        if revoke_chk:
            server_config.append(f"revocation-check {revoke_chk}")
        if key_len:
            server_config.append(f"rsakeypair {server_name} {key_len}")
        if hash_type:
            server_config.append(f"hash {hash_type}")
    
    if mode and enrollment_ip and enrollment_path:
        server_config.append(f"crypto pki trustpoint {server_name}")
        server_config.append(f"enroll url http://{enrollment_ip}:{port}/{enrollment_path}")
        if revoke_chk:
            server_config.append(f"revocation-check {revoke_chk}")
        if key_len:
            server_config.append(f"rsakeypair {server_name} {key_len}")
        if hash_type:
            server_config.append(f"hash {hash_type}")

    server_config.append(f"crypto pki server {server_name}")
    if auto_rollover_time:
        server_config.append(f"auto-rollover {auto_rollover_time}")
    
    if cdp_url_type and cdp_url_ip_path and crl_file_name:
        server_config.append(f"cdp-url {cdp_url_type}://{cdp_url_ip_path}/{crl_file_name}.crl")

    if database_archive_type:
        server_config.append(f"database archive {database_archive_type}")
        if archive_password:
            server_config.append(f"database archive {database_archive_type} password  {archive_password}")

    if database_level:
        server_config.append(f"database level {database_level}")

    if database_url_storage_location:
        server_config.append(
            f"database url {database_url_storage_location} {database_url_server}")

    if database_url_server and database_ip_path:
        if database_url_storage_location:
            if database_url_publish:
                server_config.append(f"database url {database_url_storage_location} publish {database_url_server}://{database_ip_path}")
            else:
                server_config.append(f"database url {database_url_storage_location} {database_url_server}://{database_ip_path}")
        else:
            server_config.append(f"database url {database_url_server}://{database_ip_path}")

    if eku_options:
        server_config.append(f"eku {eku_options}")
    
    if grant_mode:
        server_config.append(f"grant {grant_mode}")

    if grant_rollover_cert:
        server_config.append(f"grant auto rollover {grant_rollover_cert}")
    
    if grant_tp_list:
        server_config.append(f"grant auto tp-list {grant_tp_list}")
            
    if grant_trustpoint:
        server_config.append(f"grant auto trustpoint {grant_trustpoint}")
        
    if hash_type:
        server_config.append(f"hash {hash_type}")

    if issuer_name:
        server_config.append(f"issuer-name {issuer_name}")

    if ca_cert_life:
        server_config.append(f"lifetime ca-certificate {ca_cert_life}")

    if cert_life:
        server_config.append(f"lifetime certificate {cert_life}")

    if crl_life:
        server_config.append(f"lifetime crl {crl_life}")

    if enrol_req_life:
        server_config.append(f"lifetime enrollment-request {enrol_req_life}")

    if mode_ra_transparent:
        server_config.append(f"mode ra transparent")

    if mode:
        server_config.append(f"mode {mode}")

    if serial_number:
        server_config.append(f"serial-number {serial_number}")
   
    device.configure(server_config, error_pattern=[f'{issuer_name} is not a valid subject name'])
    time.sleep(20)

    error_patterns = ['Please set clock calender-valid or enable NTP', 'Error in receiving Certificate Authority certificate', 
                          'Failed to authenticate the Certificate Authority']
    command = [f'crypto pki server {server_name}', 'no shut']

    if password:
        try:
            device.configure(command, reply=dialog, error_pattern=error_patterns)
        except Exception as e:
            logger.error("Failed to bring up crypto server")
            return False
    else:
        logger.error("Please set either password or archive password")
        return False

    return True

def configure_trustpoint(device,
                      revoke_check,
                      tp_name,
                      rsa_key_size=None,
                      rsa_key_usage=False,
                      auto_enroll_regen=None,
                      auto_enroll=False,
                      authorization=None,
                      auth_list_name=None,
                      auth_password=None,
                      alt_auth_username=None,
                      alt_auth_username_sec=None,
                      auth_username_subjectname_opt=None,
                      auto_enroll_regen_timer=None,
                      auto_trigger=False,
                      ca_type=None,
                      ca_ip=None,
                      certificate_chain_location=None,
                      chain_valid_count=False,
                      chain_valid_stop=False,
                      common_name=None,
                      crl_cache=False,
                      crl_cache_delete_timer=False,
                      crl_cache_extend_timer=False,
                      default_options=None,
                      eckeypair=None,
                      eku_req_option=None,
                      enrollment_mode=False,
                      enrollment_option=None,
                      enrollment_url_path=None,
                      enrol_retry_count=False,
                      enrol_retry_period=False,
                      exit_flag=False,
                      fingerprint=None,
                      fqdn_value=None,
                      hash_value=None,
                      http_proxy=None,
                      ip_address=None,
                      ip_ext=None,
                      match_value=None,
                      no_config=None,
                      ocsp_url=None,
                      ocsp_port=False,
                      ocsp_disable=False,
                      on_config=None,
                      password_config=None,
                      primary_flag=False,
                      regenerate_flag=False,
                      revocation_check=None,
                      root_config=None,
                      ser_number=None,
                      show_tp_config=False,
                      source_interface=None,
                      storage_location=None,
                      sub_alt_name=None,
                      usage_option=None,
                      vrf=None,
                      sub_name=None,
                      ike=None,
                      is_ec_key=None):
    
    '''
    configure crypto pki trustpoint
    Args:
        default:
            device ('obj'): Device object
            tp_name ('string'): crypto pki trustpoint name
            revoke_check ('string'): revocation-check config to be used
            rsa_key_size ('int'): rsa_key_size value to be used for rsakeypair generation
        optional:
            authorization ('string'): authorization config options to be used with variuos options
            auth_list_name('string'): authorization list name
            auth_password('string'): authorization password
            alt_auth_username('string'): alternate authorization username config; example we can use "yes"
            alt_auth_username_sec('string'): configure authorization username alt-subjectname userprinciplename secondary; example we can use "yes"
            auth_username_subjectname_opt('string'): used to configure authorization username subject name option
            auto_enroll ('bool'): auto enroll needs to be configured or not
            auto_enroll_regen ('string'): used for auto-enroll regenerate configuration
            auto_enroll_regen_timer('int'): used for auto enroll regenerate timer configuration
            auto_trigger ('bool'): if auton trigger needs to be configured
            ca_ip ('string'): enrollment url ip-address
            certificate_chain_location ('string'): used for certificate chain configuration
            chain_valid_count ('bool'): used chain valid count with value configuration
            chain_valid_stop ('bool'): if chain validation needs to be stopped
            common_name ('string'): crypto pki subject common name to be used
            crl_cache ('bool'): used for crl cache config is none
            crl_cache_delete_timer('int'): used for crl cache delete timer configuration
            crl_cache_extend_timer('int'): used for crl cache extended timer configuration
            default_options ('string'): if any tp_config needs to be defaulted
            eckeypair ('string'): used for eckeypair configuration
            eku_req_option ('string'): used for eku request configuration
            enrollment_mode ('bool'): used to enable enrollment mode config
            enrollment_option('string'): used to configure enrollment except mode, retry timer and enrollment url
            enrol_retry_count ('int'): used to configure enrollment retry counter
            enrol_retry_period ('int'): used to configure enrollment retry period
            ca_type ('string'): used to select enrollment ca server type and config 
            enrollment_url_path ('string'): used to configure enrollment path except ca server type config ex: to take from tftp, bootflash
            fingerprint ('string'): used to configure fingerprint configuration
            fqdn_value ('string'): used to configure fully-qualified domain name
            hash_value ('string'): used to configure hash algorithm to be used
            http_proxy ('string'): used to configure http proxy 
            ip_address ('string'): if none variable is set ip address with none option will be configured \
                                    else specified ip address will be getting configured
            ip_ext ('string'): used to configure ip-extension
            match_value('string'): to configure match a certificate attibutes/maps
            ocsp_url ('string'): to configure certificate using Online Certificate Status Protocol
            ocsp_port('int'): ocsp port to be configured
            ocsp_disable ('bool'): to disable ocsp
            on_config ('string'): to create keypair on device
            password_config ('string'): to configure password
            primary_flag ('bool'): used to enable primary config
            regenerate_flag ('bool'): used to configure regenerate
            revocation_check ('string'): used to configure revocation-check config
            rsa_key_usage('bool'): used to configure rsakeypair 
            ser_number('string'): serial number to be used
            show_tp_config('bool'): to display the trustpoint configs
            source_interface('string'): soure interface to be used
            storage_location('string'): storage location like bootflash: tftp: 
            sub_alt_name('string'): used for subject-alt-name configuration
            usage_option('string'): used for usage config
            vrf('string'): used for crf config
            no_config('string'): used for unconfiguration of sub configs used in trustpoint
            exit_flag('bool'): used for exit
            is_ec_key('bool'): used for ec key pair
        
    Returns: 
        None
    Raises:
        SubCommandFailure
    '''
    
    logger.debug("configuring crypto pki trustpoint")
    tp_config = []    
    tp_config.append(f"crypto pki trustpoint {tp_name}")
    tp_config.append(f"revocation-check {revoke_check}")
    if is_ec_key:
        tp_config.append(f"eckeypair {tp_name}")
    else:
        tp_config.append(f"rsakeypair {tp_name} {rsa_key_size}")
    if authorization is not None:
        if auth_list_name is not None:
            tp_config.append(f"authorization list {auth_list_name}")
        if auth_password is not None:
            tp_config.append(f"authorization password {auth_password}")
        if alt_auth_username is not None:
            tp_config.append("authorization username alt-subjectname userprinciplename")
        if alt_auth_username_sec is not None:
            tp_config.append("authorization username alt-subjectname userprinciplename secondary")
        if auth_username_subjectname_opt is not None:
            tp_config.append(f"authorization username subjectname {auth_username_subjectname_opt}")
    if auto_enroll:
        tp_config.append("auto-enroll")
    if auto_enroll_regen is not None:
        if auto_enroll_regen ==  "regenerate":
            tp_config.append("auto-enroll regenerate")
    if auto_enroll_regen_timer is not None:
        tp_config.append(f"auto-enroll {auto_enroll_regen_timer} regenerate")
    if auto_trigger:
        tp_config.append("auto-trigger")
    if certificate_chain_location is not None:
        tp_config.append(f"certificate chain {certificate_chain_location}")
    if chain_valid_count:
       tp_config.append(f"chain-validation continue {chain_valid_count}")
    if chain_valid_stop:
        tp_config.append("chain-validation stop")
    if common_name is not None:
        tp_config.append(f"subject-name {common_name}")
    if crl_cache:
       tp_config.append("crl cache none ")
    if crl_cache_delete_timer:
        tp_config.append(f"crl cache delete-after {crl_cache_delete_timer}")
    if crl_cache_extend_timer:
        tp_config.append(f"crl cache extend {crl_cache_extend_timer}")
    if default_options is not None:
        tp_config.append(f"default {default_options}")
    if eckeypair is not None:
        tp_config.append(f"eckeypair {eckeypair}")
    if eku_req_option is not None:
        tp_config.append(f"eku request {eku_req_option}")
    if enrollment_mode:
        tp_config.append("enrollment mode  ra")
    if enrollment_option is not None:
        tp_config.append(f"enrollment {enrollment_option}")
    if enrol_retry_count:
       tp_config.append(f"enrollment retry count  {enrol_retry_count}")
    if enrol_retry_period:
       tp_config.append(f"enrollment retry period {enrol_retry_period}")
    if ca_type is not None:
        if ca_type == "microsoft":
            tp_config.append(f"enrollment url http://{ca_ip}:80/certsrv/mscep/mscep.dll ")
        else:
            tp_config.append(f"enrollment url http://{ca_ip}:80 ")
    if enrollment_url_path is not None:
        tp_config.append(f"enrollment url {enrollment_url_path}")
    if fingerprint is not None: 
        tp_config.append(f"fingerprint {fingerprint}")
    if fqdn_value is not None:
        if fqdn_value == "none":
            tp_config.append("fqdn none")
        else:
            tp_config.append(f"fqdn {fqdn_value}")
    if hash_value is not None:
        tp_config.append(f"hash {hash_value}")
    if http_proxy is not None:
        tp_config.append(f"http-proxy {http_proxy}")
    if ip_address is not None:
        if ip_address ==  "none":
            tp_config.append("ip-address none")
        else:
            tp_config.append(f"ip-address {ip_address}")
    if ip_ext is not None:
        tp_config.append(f"ip-extension {ip_ext}")
    if match_value is not None:
        tp_config.append(f"match {match_value}")
    if ocsp_url is not None:
       tp_config.append(f"ocsp url http://{ocsp_url}:{ocsp_port}")
    if ocsp_disable:
        tp_config.append("ocsp disable-nonce")
    if on_config is not None:
        tp_config.append(f"on {on_config}")
    if password_config is not None:
        tp_config.append(f"password {password_config}")
    if primary_flag:
        tp_config.append("primary")
    if regenerate_flag:
        tp_config.append("regenerate")
    if revocation_check is not None:
        if revocation_check == "none":
            tp_config.append("revocation-check none")
        else:
            tp_config.append(f"revocation-check {revocation_check}")
    if root_config is not None:
        tp_config.append(f"root {root_config}")
    if rsa_key_usage:      
       tp_config.append(f"rsakeypair {tp_name} {rsa_key_size} {rsa_key_size}")
    if ser_number is not None:
        if ser_number ==  "none":
            tp_config.append("serial-number none")
        else:
            tp_config.append("serial-number")
    if show_tp_config:
        tp_config.append("show")
    if source_interface is not None:
        tp_config.append(f"source interface {source_interface}")
    if storage_location is not None:
        tp_config.append(f"storage {storage_location}")
    if sub_alt_name is not None:
        tp_config.append(f"subject-alt-name {sub_alt_name}")
    if sub_name is not None:
        tp_config.append(f"subject-name {sub_name}")
    if ike is not None:
        tp_config.append("usage ike")
    if usage_option is not None:
        tp_config.append(f"usage {usage_option}")
    if vrf is not None:
       tp_config.append(f"vrf {vrf}")
    if no_config is not None:
        tp_config.append(f"no {no_config}")
    if exit_flag:
        tp_config.append("exit")
    
    error_patterns = ["The command you have entered is available in the IOS.sh",
                        "% Authorization list  does not exist",
                        "is not a valid subject name",
                        "Explicit device name must be specified",
                        "% Enrollment profile test does not exist",
                        "CRYPTO_PKI: There should be atleast one '.' [other than the trailing '.'] in the domain name"]
    try:
        device.configure(tp_config, error_pattern = error_patterns)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("Failed to configure trust point",
                "Error:\n{error}".format(error=e)
        )
    )

def configure_crypto_pki_profile(device,
                      prof_name,
                      method_est=False,
                      enrollment_http_username=None,
                      enrollment_http_password_type=None,
                      enrollment_http_password=None,
                      enrollment_url=None,
                      source_interface=None,
                      exit_flag=False,
                      no_config=None,
                      vrf=None
):

    '''
    configure crypto pki enrollment profile
    Args:
         device('obj'): Device object
         prof_name('string'): crypto pki enrollment profile name
         method_est('bool'): use EST method
         enrollment_http_username('string'): http authentication username
         enrollment_http_password_type('bool'): http password type
         enrollment_http_password('string'): http authentication password 
         enrollment_url('string'): http or tftp url used for enrollment to CA
         source_interface('string'): source interface for enrollment
         vrf('string'): used for crf config
         no_config('string'): used for unconfiguration of sub configs used in trustpoint
         exit_flag('bool'): used for exit
    Returns: 
        None
    Raises:
        SubCommandFailure
    '''
    
    logger.debug("configuring crypto pki profile enrollment")

    tp_config = [f"crypto pki profile enrollment {prof_name}"]   

    if method_est:
        tp_config.append("method-est")

    if enrollment_http_username is not None:
        assert enrollment_http_password is not None, "A password is required when enrollment_http_username is given"
        if enrollment_http_password_type is not None:
            tp_config.append(f"enrollment http username {enrollment_http_username} password {enrollment_http_password_type} {enrollment_http_password}")
        else:
            tp_config.append(f"enrollment http username {enrollment_http_username} password {enrollment_http_password}")

    if enrollment_url is not None:
        if vrf is not None:
            tp_config.append(f"enrollment url {enrollment_url} vrf {vrf}")
        else:
            tp_config.append(f"enrollment url {enrollment_url}")

    if source_interface is not None:
        tp_config.append(f"source interface {source_interface}")

    if no_config is not None:
        tp_config.append(f"no {no_config}")

    if exit_flag:
        tp_config.append("exit")
    
    error_patterns = ["The command you have entered is available in the IOS.sh",
                        ]
    
    try:
        device.configure(tp_config, error_pattern = error_patterns)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("Failed to configure trust point",
                "Error:\n{error}".format(error=e)
        )
    )

def unconfigure_crypto_pki_profile(device,
                           prof_name):
    '''
    unconfiguring crypto pki profile enrollment
    Args:
        device ('obj'): Device object
        prof_name ('str'): Name of the trsutpoint
    Returns:
        None
    Raises:
        SubCommandFailure
    '''

    dialog = Dialog([
                Statement(pattern=r'.*Are you sure you want to do this.*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
                ])

    logger.debug("Unconfiguring crypto pki profile enrollment")

    tp_unconfig = (f"no crypto pki profile enrollment {prof_name}")
    try:
        device.configure(tp_unconfig, reply=dialog, error_pattern=["Can't find profile"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("Failed to unconfigure enrollment profile"
                "Error:\n{error}".format(error=e)
            )
        )

def unconfigure_crypto_pki_server(device,
                                  server_name):
    '''
        Configure crypto pki server
        Args:
            device ('obj'): Device object
            server_name ('str'): Name for the pki server
    '''

    error_pattern = [f"Certificate server '{server_name}' is not known"]
    dialog = Dialog([
                Statement(pattern=r'CA certificate, Keypair, CRL and database files will be deleted. Do you wish to continue\? \[yes/no\]:',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
            ])

    logger.info("Unconfiguring crypto pki server")

    server_unconfig = f'no crypto pki server {server_name}'

    try:
        device.configure(server_unconfig, reply=dialog, error_pattern=error_pattern)
    except Exception as e:
        logger.error("Failed to unconfigure crypto server")
        return False

    return True

def unconfigure_trustpoint(device,
                           tp_name):
    '''
    unconfiguring crypto pki trustpoint
    Args:
        device ('obj'): Device object
        tp_name ('str'): Name of the trsutpoint
    Returns:
        None
    Raises:
        SubCommandFailure
    '''

    dialog = Dialog([
                Statement(pattern=r'.*Are you sure you want to do this.*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
                ])

    logger.debug("Unconfiguring crypto pki trustpoint")

    tp_unconfig = (f"no crypto pki trustpoint {tp_name}")
    try:
        device.configure(tp_unconfig, reply=dialog, error_pattern=["Can't find policy"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("Failed to configure trust point"
                "Error:\n{error}".format(error=e)
            )
        )

def configure_pki_enroll(device,
                        tp_name,
                        password,
                        serial_sub_name=False):
    '''
        Configuring crypto pki enroll
        Args:
            device ('obj'): Device object
            tp_name ('str'): name of the trustpoint
            password ('str'): password to be configured for the pki enroll
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    serial_sub_name_value = 'yes' if serial_sub_name else 'no'

    dialog = Dialog([
                Statement(pattern=r'.*Do you want to continue with re\-enrollment\? \[yes/no\].*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Password:',
                    action=f'sendline({password})',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Re-enter password:',
                    action=f'sendline({password})',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Include the router serial number in the subject name\? \[yes/no\].*',
                    action=f'sendline({serial_sub_name_value})',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Include an IP address in the subject name\? \[no\].*',
                    action=f'sendline(no)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Request certificate from CA\? \[yes/no\].*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Generate Self Signed Router Certificate\? \[yes/no\].*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Display Certificate Request to terminal\? \[yes/no\].*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Send Certificate Request to file system\? \[yes/no\].*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)

                ])
    error_patterns = ["CA server trustpoint is not known",
                       "% You must authenticate the Certificate Authority before you can enroll with it.",
                       "% Attempting authentication first.",
                       "% Error in receiving Certificate Authority certificate: status = FAIL, cert length = 0"]

    logger.debug("Configuring crypto pki enroll server")
    pki_enroll_config = (f"crypto pki enroll {tp_name}")
    try:
        device.configure(pki_enroll_config, reply=dialog, error_pattern=error_patterns)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("failed to configure crypto pki enroll"
                "Error:\n{error}".format(error=e)
            )
        )

def configure_pki_authenticate(device,
                        tp_name):
    '''
        Configuring crypto pki authenticate server
        Args:
            device ('obj'): Device object
            tp_name ('str'): Name of the trsutpoint
            
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    dialog = Dialog([
                Statement(pattern=r'.*Do you accept this certificate\? \[yes/no\].*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
                ])

    logger.debug("Configuring crypto pki authenticate server")
    
    error_patterns = ["CA server trustpoint is not known",
                       "% Please delete your existing CA certificate first.",
                       "% You must use 'no crypto pki trustpoint <trustpoint-name>' to delete the CA certificate",
                       "% Certificate Authority (trustpoint) {trustpoint_name} is unknown"]
    pki_authenticate_config = (f"crypto pki authenticate {tp_name}")
    try:
        device.configure(pki_authenticate_config, reply=dialog, error_pattern=error_patterns)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("failed to configure crypto pki authenticate"
                "Error:\n{error}".format(error=e)
            )
        )


def configure_pki_import(device,
                         tp_name,
                         import_type,
                         pkcs_media_type=None,
                         pkcs_file=None,
                         pkcs_url=None,
                         file_password=None,
                         pem_option=None,
                         pem_media_type=None,
                         pem_file=None,
                         pem_url=None,
                         is_hierarchy='no',
                         is_pem_exportable_url=False,
                         is_pem_usage_keys_url=False,
                         is_pem_usage_keys_exportable_url=False,
                         pem_import_cert=None,
                         is_key_replace='yes'
                         ):
    '''
        Configuring crypto pki authenticate server
        Args:
            device ('obj'): Device object
            tp_name ('str'): Name of the trustpoint
            import_type ('str'): Type of import [certificate, pkcs12, pem]
            pkcs_media_type ('str'): Filesytem for importing pkcs12 file
            pkcs_file ('str'): Pkcs file name that needs import
            pkcs_url ('str'): pkcs file url
            file_password ('str'): Passphrase used to protect the pkcs12 file
            pem_option ('str'): Different Pem import options
            pem_media_type ('str'): Filesytem for importing pem file
            pem_file ('str'): pem file name that needs import
            pem_url ('str'): pem file url
            is_hierarchy ('str'): update all hierarchy chain ca's
            is_pem_exportable_url ('bool'): True if pem is import as exportable
            is_pem_usage_keys_url ('bool'): True if pem is import with usage-keys url
            is_pem_usage_keys_exportable_url ('bool'): True if pem is import with usage-keys as exportable
            pem_import_cert ('bool'): Defaults to None
            is_key_replace ('string'): Defauls to 'yes'
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    
    logger.debug("Configuring crypto pki import")
    dialog = Dialog([
        Statement(pattern=r'.*Source filename \[.*?\]\?\s*$',
                    action='sendline()',
                    loop_continue=True,
                    continue_timer=False),
        Statement(pattern=r'.*the hierarchy.*',
                  action=f'sendline({is_hierarchy})',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*End with a blank line or the word "quit" on a line by itself.*?$',
                  action=f'sendline({pem_import_cert})',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*% Do you really want to replace them.*?$',
                  action=f'sendline({is_key_replace})',
                  loop_continue=True,
                  continue_timer=False)
    ])
    media_url = ['cns:', 'ftp:', 'http:', 'https:',
                 'null:', 'pram:', 'rcp:', 'scp:', 'sftp:', 'tftp:']
    media_file = ['bootflash:', 'crashinfo:',
                  'flash:', 'nvram:', 'system:', 'tmpsys', 'webui']
    error_patterns = ["% PEM files import failed.",
                      "% Please delete it or use a different label.",
                      "% Trustpoint {tp_name} is in use."]
    if import_type == 'certificate':
        import_config = f"crypto pki import {tp_name} certificate"
    elif import_type == 'pkcs12':
        if pkcs_media_type in media_file:
            import_config = (
                f"crypto pki import {tp_name} pkcs12 {pkcs_media_type}{pkcs_file} password {file_password}")
        elif pkcs_media_type in media_url:
            import_config = (
                f"crypto pki import {tp_name} pkcs12 {pkcs_media_type}{pkcs_url} password {file_password}")
        else:
            import_config = (
                f"crypto pki import {tp_name} pkcs12 {pkcs_file} password {file_password}")

    elif import_type == 'pem':
        if pem_option == 'url':
            if pem_media_type in media_file:
                import_config = (
                    f"crypto pki import {tp_name} pem url {pem_media_type}{pem_file} password {file_password}")
            elif pem_media_type in media_url:
                import_config = (
                    f"crypto pki import {tp_name} pem url {pem_media_type}{pem_url} password {file_password}")
        elif pem_option == 'exportable':
            if is_pem_exportable_url:
                import_config = (
                    f"crypto pki import {tp_name} pem exportable url {pem_media_type}{pem_file} password {file_password}")
            else:
                import_config = (
                    f"crypto pki import {tp_name} pem exportable terminal password {file_password}")
        elif pem_option == 'usage-keys':
            if is_pem_usage_keys_url:
                import_config = (
                    f"crypto pki import {tp_name} pem usage-keys url {pem_media_type}{pem_file} password {file_password}")
            else:
                import_config = (
                    f"crypto pki import {tp_name} pem usage-keys terminal password {file_password}")
            if is_pem_usage_keys_exportable_url:
                import_config = (
                    f"crypto pki import {tp_name} pem usage-keys exportable url {pem_media_type}{pem_file} password {file_password}")
            else:
                import_config = (
                    f"crypto pki import {tp_name} pem usage-keys exportable terminal password {file_password}")
        elif pem_option == 'terminal':
            import_config = (
                f"crypto pki import {tp_name} pem terminal password {file_password}")
    
    try:
        device.configure(import_config, reply=dialog,
                         error_pattern=error_patterns)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("failed to configure crypto pki import"
                         "Error:\n{error}".format(error=e)
                         )
        )


def configure_pki_export(device,
                         tp_name,
                         export_type,
                         file_password,
                         pkcs_media_type=None,
                         pkcs_file=None,
                         pkcs_url=None,
                         pem_option=None,
                         pem_media_type=None,
                         pem_file=None,
                         pem_url=None,
                         prvt_key_encry=None,
                         ):
    '''
        Configuring crypto pki export
        Args:
            device ('obj'): Device object
            tp_name ('str'): Name of the trustpoint
            export_type ('str'): Type of import [certificate, pkcs12, pem]
            pkcs_media_type ('str'): Filesytem for importing pkcs12 file
            pkcs_file ('str'): Pkcs file name that needs import
            pkcs_url ('str'): pkcs file url
            file_password ('str'): Passphrase used to protect the pkcs12 file
            pem_option ('str'): Different Pem import options
            pem_media_type ('str'): Filesytem for importing pem file
            pem_file ('str'): pem file name that needs import
            pem_url ('str'): pem file url
            prvt_key_encry ('str'): Encrypt the private key
        Returns:
            certificate
        Raises:
            SubCommandFailure
    '''

    logger.debug("Configuring crypto pki export")
    dialog = Dialog([
        Statement(pattern=r'.*Destination filename.*',
                    action='sendline(\r)',
                    loop_continue=True,
                    continue_timer=False)
    ])
    media_url = ['cns:', 'ftp:', 'http:', 'https:',
                 'null:', 'pram:', 'rcp:', 'scp:', 'sftp:', 'tftp:']
    media_file = ['bootflash:', 'crashinfo:',
                  'flash:', 'nvram:', 'system:', 'tmpsys', 'webui']

    error_patterns = ["% RSA keypair {tp_name} is not exportable.",
                      "% Please delete it or use a different label.",
                      "% Trustpoint {tp_name} is in use."]

    if export_type == 'pkcs12':
        if pkcs_media_type in media_file:
            export_config = (
                f"crypto pki export {tp_name} pkcs12 {pkcs_media_type}{pkcs_file} password {file_password}")
        elif pkcs_media_type in media_url:
            export_config = (
                f"crypto pki export {tp_name} pkcs12 {pkcs_media_type}{pkcs_url} password {file_password}")
    elif export_type == 'pem':
        if pem_option == 'url':
            if pem_media_type in media_file:
                export_config = (
                    f"crypto pki export {tp_name} pem url {pem_media_type}{pem_file} {prvt_key_encry} password {file_password}")
            elif pem_media_type in media_url:
                export_config = (
                    f"crypto pki export {tp_name} pem url {pem_media_type}{pem_url} {prvt_key_encry} password {file_password}")

        elif pem_option == 'terminal':
            if prvt_key_encry == 'rollover':
                export_config = (
                    f"crypto pki export {tp_name} pem terminal {prvt_key_encry}")
            else:
                export_config = (
                    f"crypto pki export {tp_name} pem terminal {prvt_key_encry} password {file_password}")
    try:
        output = device.configure(export_config, reply=dialog,
                         error_pattern=error_patterns)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("failed to configure crypto pki export"
                         "Error:\n{error}".format(error=e)
                         )
        )
    # Returns the exported certificate
    return output

def change_pki_server_state(device,
                            server_name,
                            state='shutdown'):
    '''
        Changing the state of pki server.
        Args:
            device ('obj'): Device object
            server_name ('str'): server name
            state ('str'): shutdown|no shutdown
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    logger.info("Changing crypto pki server state")
    server_config = []
    server_config.append(f"crypto pki server {server_name}")
    server_config.append(f"{state}")
    try:
        device.configure(server_config)
        time.sleep(10)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("failed to change pki server state"
                "Error:\n{error}".format(error=e)
            )
        )
    return True
    
def configure_pki_authenticate_certificate(device, certificate, label_name):
    """ Pastes certificate on device
        Args:
            device (`obj`): Device object
            certificate ('str'): Certificate to be pasted
            label_name ('str'): Label name
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to paste certificate on device
    """
    def cert_key_handler(spawn, data):
        spawn.sendline(data)
        spawn.sendline('quit')
    
    dialog = Dialog(
                [
                    Statement(
                        r"^.*Are you sure you want to do this\? \[yes/no\]\s?.*$",
                        action="sendline(yes)",
                        loop_continue=True,
                    ),
                    Statement(
                        r'^.*End with a blank line or the word "quit" on a line by itself\s?.*',
                        action=cert_key_handler,
                        args={"data": certificate},
                        loop_continue=True,
                        continue_timer=False
                    ),
                    Statement(
                        r".*Do you accept this certificate\? \[yes/no\]:.*", 
                        action="sendline(yes)", loop_continue=True
                    ),
                ]
            )

    try:
       device.configure("crypto pki authenticate {label_name}"
                        .format(label_name=label_name), reply=dialog, timeout=200)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Paste certificate on device "
            "Error: {error}".format(error=e)
            )
    
def configure_no_pki_enroll(device, tp_name):
    '''
        Configuring crypto pki enroll
        Args:
            device ('obj'): Device object
            tp_name ('str'): name of the trustpoint
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    logger.debug("Cancelling crypto pki enroll server")
    pki_no_enroll_config = (f"no crypto pki enroll {tp_name}")
    try:
        device.configure(pki_no_enroll_config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            logger.error("failed to cancel crypto pki enroll"
                "Error:\n{error}".format(error=e)
            )
        )


