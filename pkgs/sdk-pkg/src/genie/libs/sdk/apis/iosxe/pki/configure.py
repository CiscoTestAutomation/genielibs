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
                                grant_rollover_ca_cert=None,
                                grant_rollover_ra_cert=None,
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
                                database_p12_location = False,
                                p12_storage_location =None,
                                p12_storage_username = None,
                                p12_storage_password = None,
                                database_cnm_location = False,
                                cnm_storage_location =None,
                                cnm_storage_username = None,
                                cnm_storage_password = None,
                                database_crt_location = False,
                                crt_storage_location =None,
                                crt_storage_username = None,
                                crt_storage_password = None,
                                database_pem_location = False,
                                pem_storage_location =None,
                                pem_storage_username = None,
                                pem_storage_password = None,
                                database_ser_location = False,
                                ser_storage_location =None,
                                ser_storage_username = None,
                                ser_storage_password = None,
                                database_crl_location = False,
                                crl_storage_location =None,
                                crl_storage_username = None,
                                crl_storage_password = None,
                                crl_publish = False,
                                pem_publish = False,
                                ser_publish = False,
                                cnm_publish = False,
                                crt_publish = False,
                                p12_publish = False,
                                ECDSA_cdp_url =None,
                                **kwargs):

    '''
        Configure crypto pki server
        Args:
            device ('obj'): Device object
            server_name ('str'): Name for the PKI server
            password ('str'): Password for the server key or database encryption
            auto_rollover_time ('str'): Auto rollover interval for CA key in format <days> <hours> <minutes>
            cdp_url_type ('str'): Type of CDP URL (http | ldap)
            cdp_url_ip_path ('str'): Path or IP for the CDP URL
            crl_file_name ('str'): File name for the CRL (Certificate Revocation List)
            database_archive_type ('str'): Archive type for the CA database (pem | pkcs12)
            archive_password ('str'): Password for encrypting/decrypting the archived database
            database_level ('str'): Level of database details stored (complete | minimum | names)
            database_url_server ('str'): Server type for database URL (http | ldap)
            database_ip_path ('str'): Path to the database files on the specified server
            database_url_storage_location ('str'): Database storage location (cnm | crl | crt | pem | ser | p12)
            database_url_publish ('bool'): Whether to publish the database URL (used when storage_location is cnm, crl, crt, etc.)
            eku_options ('str'): Extended Key Usage options to include in issued certificates
            grant_mode ('str'): Mode for granting certificate requests (auto | none | ra-auto)
            grant_rollover_cert ('str'): Enables automatic rollover of certificate (ca-cert | ra-cert)
            grant_rollover_ca_cert ('str'): Enables automatic rollover for the CA certificate
            grant_rollover_ra_cert ('str'): Enables automatic rollover for the RA certificate
            grant_tp_list ('str'): List of trusted trustpoints for RA mode (up to 5)
            grant_trustpoint ('str'): Label of trustpoint holding the trusted CA certificate
            hash_type ('str'): Hash algorithm for signing operations (md5 | sha1 | sha256 | sha384 | sha512)
            issuer_name ('str'): Issuer name (Distinguished Name) for the CA certificate
            ca_cert_life ('str'): Lifetime for the CA certificate, e.g. "3650 0" (days hours)
            cert_life ('str'): Lifetime for issued certificates, e.g. "365 0"
            crl_life ('str'): CRL validity duration, e.g. "168" (hours) or "168 30" (hours minutes)
            enrol_req_life ('str'): Enrollment request lifetime, e.g. "24" (hours)
            mode ('str'): CA server operating mode (ra | sub-ca)
            mode_ra_transparent ('bool'): Enable transparent RA mode (no client authentication required)
            serial_number ('str'): Last used certificate serial number for resuming CA state
            enrollment_ip ('str'): IP address for enrollment URL
            enrollment_path ('str'): Path for enrollment URL (used with enrollment_ip)
            revoke_chk ('str'): Type of revocation check (none | crl | ocsp)
            key_len ('int'): Key length for generated RSA keypair (e.g., 2048)
            port ('int'): Port for CA server enrollment (default: 80)
            database_p12_location ('bool'): Enable PKCS12 (.p12) database storage
            p12_storage_location ('str'): Location or URL for storing .p12 database files
            p12_storage_username ('str'): Username for .p12 storage authentication
            p12_storage_password ('str'): Password for .p12 storage authentication
            database_cnm_location ('bool'): Enable CNM database storage
            cnm_storage_location ('str'): Location or URL for CNM database storage
            cnm_storage_username ('str'): Username for CNM storage
            cnm_storage_password ('str'): Password for CNM storage
            database_crt_location ('bool'): Enable CRT (certificate) database storage
            crt_storage_location ('str'): Location or URL for CRT storage
            crt_storage_username ('str'): Username for CRT storage
            crt_storage_password ('str'): Password for CRT storage
            database_pem_location ('bool'): Enable PEM-format database storage
            pem_storage_location ('str'): Location or URL for PEM storage
            pem_storage_username ('str'): Username for PEM storage
            pem_storage_password ('str'): Password for PEM storage
            database_ser_location ('bool'): Enable serial-number database storage
            ser_storage_location ('str'): Location or URL for serial number database
            ser_storage_username ('str'): Username for SER storage
            ser_storage_password ('str'): Password for SER storage
            database_crl_location ('bool'): Enable CRL (Certificate Revocation List) storage
            crl_storage_location ('str'): Location or URL for CRL storage
            crl_storage_username ('str'): Username for CRL storage
            crl_storage_password ('str'): Password for CRL storage
            crl_publish ('bool'): Publish CRL database to configured CRL URL
            pem_publish ('bool'): Publish PEM database to configured location
            ser_publish ('bool'): Publish serial-number database to configured location
            cnm_publish ('bool'): Publish CNM database to configured location
            crt_publish ('bool'): Publish CRT database to configured location
            p12_publish ('bool'): Publish P12 database to configured location
            ECDSA_cdp_url ('str'): URL for ECDSA-specific CRL distribution point
        Returns:
            bool: True if configuration is successful, False otherwise
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
                    continue_timer=False),
                Statement(pattern=r'.*Include the router serial number in the subject name*',
                    action=f'sendline(no)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Include an IP address in the subject name*',
                    action=f'sendline(no)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*Request certificate from CA*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False),
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
    if ECDSA_cdp_url:
        server_config.append(f"cdp-url {ECDSA_cdp_url}")
    if database_archive_type:
        server_config.append(f"database archive {database_archive_type}")
        if archive_password:
            server_config.append(f"database archive {database_archive_type} password  {archive_password}")

    if database_level:
        server_config.append(f"database level {database_level}")

    if database_url_storage_location and database_url_server:
        server_config.append(
            f"database url {database_url_storage_location} {database_url_server}")
    if database_url_storage_location:
        server_config.append(
            f"database url {database_url_storage_location}")
    if database_url_server and database_ip_path:
        if database_url_storage_location:
            if database_url_publish:
                server_config.append(f"database url {database_url_storage_location} publish {database_url_server}://{database_ip_path}")
            else:
                server_config.append(f"database url {database_url_storage_location} {database_url_server}://{database_ip_path}")
        else:
            server_config.append(f"database url {database_url_server}://{database_ip_path}")
    if database_p12_location and p12_storage_location and p12_storage_username and p12_storage_password:
        server_config.append(f"database url p12 {p12_storage_location} username {p12_storage_username} password {p12_storage_password}")
    if database_p12_location and p12_publish:
        server_config.append(f"database url p12 publish  {p12_storage_location}")
    if database_p12_location and p12_storage_location:
        server_config.append(f"database url p12 {p12_storage_location}")
    if database_cnm_location and cnm_storage_location and cnm_storage_username and cnm_storage_password:
        server_config.append(f"database url cnm {cnm_storage_location} username {cnm_storage_username} password {cnm_storage_password}")
    if database_cnm_location and cnm_publish:
        server_config.append(f"database url cnm publish  {cnm_storage_location}")
    if database_cnm_location and cnm_storage_location:
        server_config.append(f"database url cnm {cnm_storage_location}")
    if database_crt_location and crt_storage_location and crt_storage_username and crt_storage_password:
        server_config.append(f"database url crt {crt_storage_location} username {crt_storage_username} password {crt_storage_password}")
    if database_crt_location and crt_publish:
        server_config.append(f"database url crt publish  {crt_storage_location}")
    if database_crt_location and crt_storage_location:
        server_config.append(f"database url crt {crt_storage_location}")
    if database_pem_location and pem_storage_location and pem_storage_username and pem_storage_password:
        server_config.append(f"database url pem {pem_storage_location} username {pem_storage_username} password {pem_storage_password}")
    if database_pem_location and pem_publish:
        server_config.append(f"database url pem publish  {pem_storage_location}")
    if database_pem_location and pem_storage_location:
        server_config.append(f"database url pem {pem_storage_location}")
    if database_ser_location and ser_storage_location and ser_storage_username and ser_storage_password:
        server_config.append(f"database url ser {ser_storage_location} username {ser_storage_username} password {ser_storage_password}")
    if database_ser_location and ser_publish:
        server_config.append(f"database url ser publish  {ser_storage_location}")
    if database_ser_location and ser_storage_location:
        server_config.append(f"database url ser {ser_storage_location}")
    if database_crl_location and crl_storage_location and crl_storage_username and crl_storage_password:
        server_config.append(f"database url crl {crl_storage_location} username {crl_storage_username} password {crl_storage_password}")
    if database_crl_location and crl_publish:
        server_config.append(f"database url crl publish  {crl_storage_location}")
    if database_crl_location and crl_storage_location:
        server_config.append(f"database url crl {crl_storage_location}")
    if eku_options:
        server_config.append(f"eku {eku_options}")
    
    if grant_mode:
        server_config.append(f"grant {grant_mode}")

    if grant_rollover_cert:
        server_config.append(f"grant auto rollover {grant_rollover_cert}")
    
    if grant_rollover_ca_cert:
        server_config.append(f"grant auto rollover ca-cert")
    
    if grant_rollover_ra_cert:
        server_config.append(f"grant auto rollover ra-cert")
    
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
                      is_ec_key=None,
                      scepencrypt = None,
                      chain_validation_continue_tp_name=None,
                      rsa_key_size1=None,
                      auto_enroll_timer = None,
                      enrollment_profile = None):
    
    '''
    configure crypto pki trustpoint
    Args:
        default:
            device ('obj'): Device object
            tp_name ('string'): crypto pki trustpoint name
            revoke_check ('string'): revocation-check config to be used
            rsa_key_size ('int'): rsa_key_size value to be used for rsakeypair generation
        optional:
            rsa_key_size1 ('int'): secondary RSA key size value (used when two RSA keypairs are configured)
            rsa_key_usage ('bool'): used to configure rsakeypair 
            auto_enroll_regen ('string'): used for auto-enroll regenerate configuration
            auto_enroll ('bool'): auto enroll needs to be configured or not
            auto_enroll_timer ('int'): used to configure auto-enroll timer
            authorization ('string'): authorization config options to be used with various options
            auth_list_name ('string'): authorization list name
            auth_password ('string'): authorization password
            alt_auth_username ('string'): alternate authorization username config; example we can use "yes"
            alt_auth_username_sec ('string'): configure authorization username alt-subjectname userprinciplename secondary; example we can use "yes"
            auth_username_subjectname_opt ('string'): used to configure authorization username subject name option
            auto_enroll_regen_timer ('int'): used for auto enroll regenerate timer configuration
            auto_trigger ('bool'): if auto trigger needs to be configured
            ca_type ('string'): used to select enrollment CA server type and config 
            ca_ip ('string'): enrollment url ip-address
            certificate_chain_location ('string'): location for storing the certificate chain (e.g., bootflash:, tftp:)
            chain_valid_count ('bool'): used chain valid count with value configuration
            chain_valid_stop ('bool'): if chain validation needs to be stopped
            common_name ('string'): crypto pki subject common name to be used
            crl_cache ('bool'): used for crl cache config if none
            crl_cache_delete_timer ('int'): used for crl cache delete timer configuration
            crl_cache_extend_timer ('int'): used for crl cache extended timer configuration
            default_options ('string'): if any tp_config needs to be defaulted
            eckeypair ('string'): used for eckeypair configuration
            enrollment_profile ('string'): enrollment profile name to be used for trustpoint
            eku_req_option ('string'): used for eku request configuration
            enrollment_mode ('bool'): used to enable enrollment mode config
            enrollment_option ('string'): used to configure enrollment except mode, retry timer and enrollment url
            enrollment_url_path ('string'): used to configure enrollment path except CA server type config ex: to take from tftp, bootflash
            enrol_retry_count ('int'): used to configure enrollment retry counter
            enrol_retry_period ('int'): used to configure enrollment retry period
            exit_flag ('bool'): used for exit
            fingerprint ('string'): used to configure fingerprint configuration
            fqdn_value ('string'): used to configure fully-qualified domain name
            hash_value ('string'): used to configure hash algorithm to be used
            http_proxy ('string'): used to configure http proxy 
            ip_address ('string'): if none variable is set ip address with none option will be configured \
                                    else specified ip address will be getting configured
            ip_ext ('string'): used to configure ip-extension
            match_value ('string'): to configure match a certificate attribute/map
            no_config ('string'): used for unconfiguration of sub configs used in trustpoint
            ocsp_url ('string'): to configure certificate using Online Certificate Status Protocol
            ocsp_port ('int'): ocsp port to be configured
            ocsp_disable ('bool'): to disable ocsp
            on_config ('string'): to create keypair on device
            password_config ('string'): to configure password
            primary_flag ('bool'): used to enable primary config
            regenerate_flag ('bool'): used to configure regenerate
            revocation_check ('string'): used to configure revocation-check config
            root_config ('string'): used to specify root CA configuration or enable root certificate-related parameters
            ser_number ('string'): serial number to be used
            show_tp_config ('bool'): to display the trustpoint configs
            source_interface ('string'): source interface to be used
            storage_location ('string'): storage location like bootflash:, tftp:
            sub_alt_name ('string'): used for subject-alt-name configuration
            sub_name ('string'): used for subject-name configuration
            usage_option ('string'): used for usage config
            vrf ('string'): used for vrf config
            ike ('string'): used to configure IKE identity or usage for VPN certificates
            is_ec_key ('bool'): used for EC key pair
            scepencrypt ('string'): used to configure SCEP encryption type (e.g., 3DES, AES)
            chain_validation_continue_tp_name ('string'): specifies another trustpoint name to continue chain validation with
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
    elif rsa_key_size:
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
    if auto_enroll and not auto_enroll_timer:
        tp_config.append("auto-enroll")
    if auto_enroll and auto_enroll_timer:
        tp_config.append(f"auto-enroll {auto_enroll_timer}")
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
    if chain_validation_continue_tp_name:
        tp_config.append(f"chain-validation continue {chain_validation_continue_tp_name}")
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
    if enrollment_profile:
        tp_config.append(f"enrollment profile {enrollment_profile} ")
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
    if rsa_key_usage and rsa_key_size1:      
       tp_config.append(f"rsakeypair {tp_name} {rsa_key_size} {rsa_key_size1}")
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
    if scepencrypt:
        tp_config.append(f"scepencrypt {scepencrypt}")
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
                      vrf=None,
                      authentication_url=None,
                      reenrollment_url=None
):

    '''
    configure crypto pki enrollment profile
    Args:
         device ('obj'): Device object
         prof_name ('string'): crypto pki enrollment profile name
         method_est ('bool'): if True, uses EST (Enrollment over Secure Transport) as the enrollment method
         enrollment_http_username ('string'): HTTP authentication username for enrollment
         enrollment_http_password_type ('string'): type of HTTP password to configure (e.g., 0 for plaintext, 7 for encrypted)
         enrollment_http_password ('string'): HTTP authentication password for enrollment
         enrollment_url ('string'): HTTP or TFTP URL used for certificate enrollment to the CA server
         authentication_url ('string'): URL used for authentication to the CA server
         source_interface ('string'): source interface to be used for enrollment communication
         exit_flag ('bool'): if True, exits the profile configuration mode after setup
         no_config ('string'): used to unconfigure specific subcommands under the profile
         reenrollment_url ('string'): URL used for reenrollment of certificates
         vrf ('string'): VRF name used for enrollment connectivity
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
    if authentication_url is not None:
        if vrf is not None:
            tp_config.append(f"authentication url {authentication_url} vrf {vrf}")
        else:
            tp_config.append(f"authentication url {authentication_url}")
    if source_interface is not None:
        tp_config.append(f"source-interface {source_interface}")

    if reenrollment_url is not None:
        if vrf is not None:
            tp_config.append(f"reenrollment url {reenrollment_url} vrf {vrf}")
        else:
            tp_config.append(f"reenrollment url {reenrollment_url}")

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
                Statement(pattern=r'.*Do you accept this certificate\? \[yes/no\].*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False),
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
        error_msg = str(e)
        # Check if the error is due to trustpoint already being in use
        if "Trustpoint" in error_msg and "is in use" in error_msg:
            logger.warning(f"Trustpoint {tp_name} is already in use. Deleting it first...")
            try:
                # Delete the existing trustpoint
                unconfigure_trustpoint(device, tp_name)
                logger.info(f"Successfully deleted trustpoint {tp_name}. Retrying import...")
                # Retry the import
                device.configure(import_config, reply=dialog,
                               error_pattern=error_patterns)
            except Exception as retry_error:
                raise SubCommandFailure(
                    f"Failed to configure crypto pki import after deleting trustpoint. "
                    f"Error: {retry_error}"
                )
        else:
            raise SubCommandFailure(
                f"failed to configure crypto pki import. Error: {e}"
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
    dialog = Dialog([
                Statement(pattern=r'.*bytes*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
            ])
    logger.info("Changing crypto pki server state")
    server_config = []
    server_config.append(f"crypto pki server {server_name}")
    server_config.append(f"{state}")
    error_pattern = ["% Please delete your existing CA certificate first."]
    try:
        device.configure(server_config,reply=dialog, error_pattern=error_pattern)
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



def configure_crypto_pki_download_crl(
                                        device,
                                        schedule=False,
                                        prepublish=False,
                                        retries=False,
                                        number_of_retries=None,
                                        interval=False,
                                        retry_time_in_minutes=None,
                                        time=False,
                                        day=None,
                                        hh_mm=None,
                                        trustpoint_name=None,
                                        url=False,
                                        http_or_ldap_url=None
                                    ):
    """
    Configure 'crypto pki crl download' commands with schedule, trustpoint, or URL options.

    Args:
        device (`obj`): Device handle
        schedule (`bool`): Enable schedule block
        prepublish (`bool`): Enable prepublish schedule
        retries (`bool`): Enable retries block
        number_of_retries (`int`): Number of retries (1-15)
        interval (`bool`): Enable interval block under retries
        retry_time_in_minutes (`int`): Interval time in minutes (15-600)
        time (`bool`): Enable schedule time block
        day (`str`): Day of the week (e.g., "Monday")
        hh_mm (`str`): Time string in "HH:MM" format
        trustpoint_name (`str`): Name of trustpoint
        url (`bool`): Enable URL block
        http_or_ldap_url (`str`): HTTP/LDAP CRL download URL

    Raises:
        ValueError: If required values are missing or invalid
        SubCommandFailure: If configuration fails
    """
    cmds = []

    if trustpoint_name:
        cmds.append(f"crypto pki crl download trustpoint {trustpoint_name}")
        

    if url:
        if not http_or_ldap_url:
            raise ValueError("http_or_ldap_url must be provided if url=True")
        cmds.append(f"crypto pki crl download url {http_or_ldap_url}")

    if schedule:
        if prepublish:
            cmds.append("crypto pki crl download schedule prepublish")

        if retries:
            if number_of_retries is None or not (1 <= number_of_retries <= 15):
                raise ValueError("number_of_retries must be between 1 and 15")
            cmds.append(f"crypto pki crl download schedule retries {number_of_retries}")

        if interval:
            if retry_time_in_minutes is None or not (15 <= retry_time_in_minutes <= 600):
                raise ValueError("retry_time_in_minutes must be between 15 and 600")
            cmds.append(f"crypto pki crl download schedule retries interval {retry_time_in_minutes}")

        if time and day:
            valid_days = {
                "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday","Mon","Tue","Wed","Thu","Fri","Sat","Sun"
            }
        
            if day not in valid_days:
                raise ValueError("`day` must be one of Monday to Sunday when `time` is specified")
        
            if not hh_mm:
                raise ValueError("`hh_mm` must be provided when `time` is specified")
        
            cmd = f"crypto pki crl download schedule time {day} {hh_mm}"
            cmds.append(cmd)

    if not cmds:
        raise ValueError("No valid configuration arguments provided.")

    try:
        return device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure CRL download: {e}")


def unconfigure_crypto_pki_download_crl(
                                            device,
                                            schedule=False,
                                            prepublish=False,
                                            retries=False,
                                            number_of_retries=None,
                                            interval=False,
                                            retry_time_in_minutes=None,
                                            time=False,
                                            day=None,
                                            hh_mm=None,
                                            trustpoint_name=None,
                                            url=False,
                                            http_or_ldap_url=None
                                        ):
    """
    Unconfigure 'crypto pki crl download' commands with schedule, trustpoint, or URL options.

    Args:
        device (`obj`): Device handle
        schedule (`bool`): Enable schedule block
        prepublish (`bool`): Unconfigure prepublish schedule
        retries (`bool`): Unconfigure retries block
        number_of_retries (`int`): Number of retries (1-15)
        interval (`bool`): Unconfigure interval block under retries
        retry_time_in_minutes (`int`): Interval time in minutes (15-600)
        time (`bool`): Unconfigure schedule time block
        day (`str`): Day of the week (e.g., "Monday")
        hh_mm (`str`): Time string in "HH:MM" format
        trustpoint_name (`str`): Name of trustpoint
        url (`bool`): Unconfigure URL block
        http_or_ldap_url (`str`): HTTP/LDAP CRL download URL

    Raises:
        ValueError: If required values are missing or invalid
        SubCommandFailure: If unconfiguration fails
    """
    cmds = []

    if trustpoint_name:
        cmds.append(f"no crypto pki crl download trustpoint {trustpoint_name}")
        
    if url:
        if not http_or_ldap_url:
            raise ValueError("http_or_ldap_url must be provided if url=True")
        cmds.append(f"no crypto pki crl download url {http_or_ldap_url}")

    if schedule:
        if prepublish:
            cmds.append("no crypto pki crl download schedule prepublish")

        if retries:
            if number_of_retries is None or not (1 <= number_of_retries <= 15):
                raise ValueError("number_of_retries must be between 1 and 15")
            cmds.append(f"no crypto pki crl download schedule retries {number_of_retries}")

        if interval:
            if retry_time_in_minutes is None or not (15 <= retry_time_in_minutes <= 600):
                raise ValueError("retry_time_in_minutes must be between 15 and 600")
            cmds.append(f"no crypto pki crl download schedule retries interval {retry_time_in_minutes}")

        if time and day:
            valid_days = {
                "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday","Mon","Tue","Wed","Thu","Fri","Sat","Sun"
            }

            if day not in valid_days:
                raise ValueError("`day` must be one of Monday to Sunday when `time` is specified")

            if not hh_mm:
                raise ValueError("`hh_mm` must be provided when `time` is specified")

            cmd = f"no crypto pki crl download schedule time {day} {hh_mm}"
            cmds.append(cmd)

    if not cmds:
        raise ValueError("No valid unconfiguration arguments provided.")

    try:
        return device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure CRL download: {e}")
    

def configure_trustpool_clean(device):
    """
    Clean up the CA Trustpool on a Cisco device.
        Args:
            device (obj): Device object

        Raises:
            SubCommandFailure: On failure to clean trustpool
    """
    try:
        device.configure(["crypto pki trustpool clean"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to clean CA Trustpool: {e}")

def unconfigure_trustpool_clean(device):
    """
    Execute 'no crypto pki trustpool clean'.
        Args:
            device (obj): Device object

        Raises:
            SubCommandFailure: If command execution fails
    """
    try:
        device.configure(["no crypto pki trustpool clean"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute 'no crypto pki trustpool clean': {e}")

def remove_pki_certificate_chain(device, tpname):
    """Unconfigure (remove) PKI certificate chain for a server.
        Args:
            device (`obj`): Device object
            tpname (`str|int`): Trustpoint name or ID for the certificate chain
        Returns:
            None
        Raises:
            SubCommandFailure: If unconfiguration fails
            ValueError: If tpname is empty
    """

    if not tpname:
        raise ValueError("server_name must be provided and non-empty")
    
    error_pattern = [f"Certificate server '{tpname}' is not known"]

    dialog = Dialog([
        Statement(pattern=r'This will remove all certificates for trustpoint',
        action=f'sendline(yes)',
        loop_continue=True,
        continue_timer=False)
    ])

    cmd = f"no crypto pki certificate chain {tpname}"
    logger.debug(cmd)

    try:
        device.configure(cmd, reply=dialog, error_pattern=error_pattern)
    except SubCommandFailure as e:
        logger.error("Failed to remove cert chain")
        raise SubCommandFailure(f"Could not unconfigure certificate chain for '{tpname}': {e}")
        
        
def configure_crypto_pki_crl_request(device, ca_name):
    """
        Execute 'crypto pki crl request <CA_NAME>' command.
            Args:
                device (obj): pyATS device object.
                ca_name (str): CA server name.
            Returns:
                None
            Raises:
                SubCommandFailure: If device.execute fails.
    """
    try:
        device.configure(f"crypto pki crl request {ca_name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure CRL request for CA '{ca_name}': {e}")


def unconfigure_crypto_pki_crl_request(device, ca_name):
    """
    Execute 'no crypto pki crl request <CA_NAME>' command to remove configuration.
        Args:
            device (obj): pyATS device object.
            ca_name (str): CA server name.
        Returns:
            None
        Raises:
            SubCommandFailure: If device.execute fails.
    """
    try:
        device.configure(f"no crypto pki crl request {ca_name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure CRL request for CA '{ca_name}': {e}")


def configure_crypto_isakmp_profile(
                                    device,
                                    profile_name=None,
                                    ca_trustpoint=False,
                                    ca_trustpoint_name=None,
                                    match_certificate=False,
                                    certificate_name=None
                                ):
    """ Configure crypto ISAKMP profile on device
        Args:
            device (`obj`): Device object
            profile_name (`str`): Name of the ISAKMP profile
            ca_trustpoint (`bool`): Flag to enable CA trustpoint configuration. Default is False.
            ca_trustpoint_name (`str`): CA trustpoint name (required if ca_trustpoint=True)
            match_certificate (`bool`): Flag to enable match certificate configuration. Default is False.
            certificate_name (`str`): Certificate name (required if match_certificate=True)
        Returns:
            None
        Raises:
            SubCommandFailure: If configuration fails
    """
    cmds = []
    cmds.append(f"crypto isakmp profile {profile_name}") 

    if ca_trustpoint and ca_trustpoint_name:
        cmds.append(f"ca trust-point {ca_trustpoint_name}")
    if match_certificate and certificate_name:
        cmds.append(f"match certificate {certificate_name}")
    
    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure crypto isakmp profile {profile_name}: {e}")


def unconfigure_crypto_isakmp_profile(device, profile_name):
    """ Unconfigure crypto ISAKMP profile from device
        Args:
            device (`obj`): Device object
            profile_name (`str`): Name of the ISAKMP profile to remove
        Returns:
            None
        Raises:
            SubCommandFailure: If unconfiguration fails
    """
    cmds = [f"no crypto isakmp profile {profile_name}"]
    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure crypto isakmp profile {profile_name}: {e}")

def configure_crypto_pki_http_max_buffer_size(device, size):
    """
        Configure the maximum HTTP buffer size for PKI operations.
        Args:
            device (obj): Device object
            size (int): Buffer size value to set
        Raises:
            SubCommandFailure: If configuration fails
    """
    cmds = [f"crypto pki http max-buffer-size {size}"]
    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure crypto pki http max buffer size {size}: {e}")

def unconfigure_crypto_pki_http_max_buffer_size(device):
    """
        Unonfigure the maximum HTTP buffer size for PKI operations.
        Args:
            device (obj): Device object
        Raises:
            SubCommandFailure: If configuration fails
    """
    cmds = [f"no crypto pki http max-buffer-size"]
    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure crypto pki http max buffer size: {e}")
        
def configure_trustpool_policy(device, source_interface=None, vrf_name=None, ca_bundle_url=None, 
                             ca_bundle_urls=None, revocation_check=None, storage_path=None,
                             chain_validation=None, auto_update=None):
    """
    Configure CA Trustpool policy with mandatory CA URL and optional parameters.

    Args:
        device (obj): Device object
        ca_bundle_url (str, optional): Single CA server bundle URL (for backward compatibility)
        ca_bundle_urls (list, optional): List of CA server bundle URLs for multiple URLs
        source_interface (str, optional): Interface to use as source address for downloads
        vrf_name (str, optional): VRF to use for enrollment and obtaining CRLs
        revocation_check (str, optional): Revocation check method ('crl', 'none', 'ocsp')
        storage_path (str, optional): Storage location for certificates (e.g., 'flash:abc/')
        chain_validation (bool, optional): Enable/disable chain validation
        auto_update (bool, optional): Enable/disable auto-update

    Raises:
        ValueError: If neither ca_bundle_url nor ca_bundle_urls is provided
        Exception: If command execution fails on the device
    """
    
    # Normalize URLs to a list for consistent processing
    urls_to_configure = []
    if ca_bundle_url:
        urls_to_configure.append(ca_bundle_url)
    if ca_bundle_urls:
        if isinstance(ca_bundle_urls, str):
            urls_to_configure.append(ca_bundle_urls)
        elif isinstance(ca_bundle_urls, list):
            urls_to_configure.extend(ca_bundle_urls)
        else:
            raise ValueError("ca_bundle_urls must be a string or list of strings")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls_to_configure:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    dialog = Dialog([
        Statement(pattern=r'.*bytes*',
            action='sendline(yes)',
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r'.*[Cc]onfirm.*',
            action='sendline(y)',
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r'.*[Yy]/[Nn].*',
            action='sendline(y)',
            loop_continue=True,
            continue_timer=False)
    ])
    
    cmds = []
    cmds.append("crypto pki trustpool policy")
    
    # Add all CA bundle URLs
    for url in unique_urls:
        cmds.append(f"cabundle url {url}")
    
    # Add optional configurations
    if source_interface:
        cmds.append(f"source interface {source_interface}")
    
    if vrf_name:
        cmds.append(f"vrf {vrf_name}")
    
    if revocation_check:
        if revocation_check.lower() in ['crl', 'none', 'ocsp']:
            if revocation_check.lower() == 'none':
                cmds.append("revocation-check none")
            elif revocation_check.lower() == 'crl':
                cmds.append("revocation crl")
            elif revocation_check.lower() == 'ocsp':
                cmds.append("revocation ocsp")
        else:
            raise ValueError("revocation_check must be 'crl', 'none', or 'ocsp'")
    
    if storage_path:
        cmds.append(f"storage {storage_path}")
    
    if chain_validation is True:
        cmds.append("chain-validation")
    elif chain_validation is False:
        cmds.append("no chain-validation")
    
    if auto_update is True:
        cmds.append("auto-update")
    elif auto_update is False:
        cmds.append("no auto-update")
    
    error_patterns = ['failed', 'error', 'invalid']
    
    try:
        logger.info(f"Configuring trustpool policy with {len(unique_urls)} CA bundle URL(s)")
        device.configure(cmds, reply=dialog, error_pattern=error_patterns)
        logger.info("Trustpool policy configured successfully")
    except Exception as e:
        urls_str = ', '.join(unique_urls)
        raise Exception(f"Failed to configure trustpool policy with URL(s) '{urls_str}': {e}")


def unconfigure_trustpool_policy(device):
    '''
    Removes the CA Trustpool policy configuration from the device.
    Args:
        device ('obj'): Device object.
    Returns:
        None
    Raises:
        SubCommandFailure: If unconfiguration fails on the device.
    '''
    cmds = ["no crypto pki trustpool policy"]
    try:
        device.configure(cmds, timeout=60)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure trustpool policy: {e}")
         
def configure_pki_vrf_trustpoint(device, trustpoint, vrf_name):
    """
    Configure IP VRF and bind it under a PKI trustpoint.

    Args:
        device ('obj'): Device object
        trustpoint ('str'): Trustpoint name (e.g., 'client')
        vrf_name ('str'): VRF name (e.g., 'pki')

    Returns:
        None

    Raises:
        SubCommandFailure
    """
    try:
        cmds = [
            f"ip vrf {vrf_name}",
            f"crypto pki trustpoint {trustpoint}",
            f"vrf {vrf_name}",
        ]
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure PKI trustpoint {trustpoint} with VRF {vrf_name}: {e}")


def unconfigure_pki_vrf_trustpoint(device, trustpoint, vrf_name):
    """
    Remove VRF and unbind it from the PKI trustpoint.

    Args:
        device ('obj'): Device object
        trustpoint ('str'): Trustpoint name (e.g., 'client')
        vrf_name ('str'): VRF name (e.g., 'pki')

    Returns:
        None

    Raises:
        SubCommandFailure
    """
    try:
        cmds = [
            f"no ip vrf {vrf_name}",
            f"crypto pki trustpoint {trustpoint}",
            f"no vrf {vrf_name}",
        ]
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure PKI trustpoint {trustpoint} or remove VRF {vrf_name}: {e}")
 
def configure_crypto_pki_export_pkcs12_terminal(device, tp_name, password):
    """
    Exports a PKCS#12 certificate bundle to the terminal.
    This method uses the `crypto pki export <trustpoint> pkcs12 terminal password <pwd>` 
    command to print/export the PKCS#12 data directly to the terminal.
    Args:
        device: Device connection object (pyATS/unicon object) used to send commands.
        tp_name (str): Trustpoint name to be exported.
        password (str): Password to protect the PKCS#12 file.
    Returns:
        str | bool:
            - String output containing the PKCS#12 encoded data if successful.
            - False if the export fails.
    """
    cmd = f"crypto pki export {tp_name} pkcs12 terminal password {password}"
    try:
        output = device.configure(cmd)
    except Exception as e:
        logger.error("Error: {}".format(str(e)))
        return False

    return output

def crypto_pki_trustpool_import(device, ca_bundle=False):
    '''
    Imports CA bundle into the PKI trustpool on the device.
    Args:
        device ('obj'): Device object.
        ca_bundle ('bool', optional): Flag to import the CA bundle. Default is False.
    Returns:
        None
    Raises:
        SubCommandFailure: If the trustpool CA bundle import fails on the device.
    '''
    dialog = Dialog([
                Statement(pattern=r'.*bytes*',
                          action=f'sendline(yes)',
                          loop_continue=True,
                          continue_timer=False)
            ])
    error_patterns = ['failed']
    cmds = []
    if ca_bundle:
        cmds.append("crypto pki trustpool import ca-bundle")

    try:
        device.configure(cmds, reply=dialog, error_pattern=error_patterns)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to import trustpool CA bundle: {e}")
    
def remove_grant_auto(device, wait_time=10):
    '''
    Remove the "grant auto" configuration from the currently configured crypto pki server.

    This function identifies the active PKI server on the device, temporarily shuts it down,
    removes the "grant auto" configuration, and then re-enables the server. It ensures that
    the server is restored to an operational state after configuration changes.

    Steps:
        Step 1: Identify the active PKI server on the device.
        Step 2: Check the current PKI server state (enabled/disabled).
        Step 3: Shut down the PKI server if it is enabled.
        Step 4: Remove the "grant auto" configuration.
        Step 5: Re-enable (no shutdown) the PKI server.
        Step 6: Verify that the server is up and configuration is updated.
    Args:
        device ('obj'): Device object representing the target router or switch.
        wait_time ('int', optional): Time in seconds to wait after shutting down
                                     and re-enabling the PKI server. Default is 10 seconds.
    Returns:
        bool:
            - True: If the server is successfully re-enabled and configuration is updated.
            - False: If no PKI server is configured or the server fails to re-enable.
    Raises:
        SubCommandFailure: If configuration commands fail to execute on the device.
    '''

    dialog = Dialog([
        Statement(pattern=r'.*bytes*',
                  action='sendline(yes)',
                  loop_continue=True,
                  continue_timer=False)
    ])

    try:
        op = device.parse("show crypto pki server")
        server_name = list(op['server'].keys())
        if not server_name:
            logger.info("No server configured")
            return False
    except Exception as e:
        logger.error(f"Failed to parse PKI server configuration: {e}")
        return False

    try:
        server_state = op['server'][str(server_name[0])]['status']
        
        if server_state == 'enabled':
            try:
                device.api.change_pki_server_state(server_name[0], "shutdown")
                time.sleep(wait_time)
            except Exception as e:
                logger.error(f"Failed to shutdown PKI server {server_name[0]}: {e}")
                return False

        server_config = [
            f"crypto pki server {server_name[0]}",
            "no grant auto"
        ]
        
        error_pattern = ["% Please delete your existing CA certificate first."]
        logger.info(server_config)
        
        try:
            device.configure(server_config, reply=dialog, error_pattern=error_pattern)
        except SubCommandFailure as e:
            logger.error(f"Failed to configure 'no grant auto' for server {server_name[0]}: {e}")
            return False

        try:
            device.api.change_pki_server_state(server_name[0], "no shutdown")
            time.sleep(wait_time)
        except Exception as e:
            logger.error(f"Failed to re-enable PKI server {server_name[0]}: {e}")
            return False

        # Re-parse to verify server state
        try:
            op = device.parse("show crypto pki server")
            server_state = op['server'][str(server_name[0])]['status']
            if server_state == 'enabled':
                logger.info("Server is enabled and configs are changed")
                return True
            else:
                logger.info("Server is not enabled")
                return False
        except Exception as e:
            logger.error(f"Failed to verify server state after configuration: {e}")
            return False
            
    except Exception as e:
        logger.error(f"Unexpected error during PKI server configuration: {e}")
        return False


 
def import_pkcs12_tftp(device, tftp_ip, file_name, tp_name, format_type, password):
    """
    Imports a PKCS#12 certificate bundle into a Cisco device from a TFTP server.
    This function uses the `crypto pki import` command to import a PKCS#12 
    file over TFTP into a specified trustpoint on the device.
    Args:
        device: Device connection object (pyATS/unicon object) used to send commands.
        tftp_ip (str): IP address of the TFTP server hosting the PKCS#12 file.
        file_name (str): Name of the PKCS#12 file on the TFTP server.
        tp_name (str): Trustpoint name where the certificate will be imported.
        format_type (str): File format type (e.g., 'pkcs12').
        password (str): Password for the PKCS#12 file.
    Returns:
        bool: 
            - True if the import operation succeeded.
            - False if the operation failed.
    Raises:
        ValueError: If password is less than 8 characters long.
    """

    
    try:
        dialog = Dialog([
            Statement(pattern=r'.*Address or name of remote host', action=f'sendline({tftp_ip})',
                      loop_continue=True, continue_timer=False),         
            Statement(pattern=r'.*Source filename', action=f'sendline({file_name})',
                      loop_continue=True, continue_timer=False),
            Statement(pattern=r'.*Do you really want to replace them', action=f'sendline(yes)',
                      loop_continue=True, continue_timer=False),
            Statement(pattern=r'.*hierarchy\?*', action=f'sendline(yes)',
                      loop_continue=True, continue_timer=False)
        ])

        cmd = [f"crypto pki import {tp_name} {format_type} tftp://{tftp_ip}/{file_name} password {password}"]

        error_patterns = [
            'Failed',
            'Possible causes: bad password or corrupted PKCS12',
            'CRYPTO_PKI: Import PKCS12 operation failed, bad HMAC',
            'Error: failed to open file.'
        ]

        op = device.configure(cmd, reply=dialog, error_pattern=error_patterns)
        return True
    except Exception as e:
        logger.error(f"Failed to import PKCS12 from TFTP server {tftp_ip}: {e}")
        return False

def export_pkcs12_tftp(device, tftp_ip, file_name, tp_name, format_type):
    """
        Exports a PKCS#12 certificate bundle from a Cisco device to a TFTP server.
    
        This function uses the `crypto pki export` command to export a PKCS#12 file 
        over TFTP from a specified trustpoint on the device.
    
        Args:
            device: Device connection object (pyATS/unicon object) used to send commands.
            tftp_ip (str): IP address of the TFTP server where the PKCS#12 file will be saved.
            file_name (str): Destination file name for the PKCS#12 bundle on the TFTP server.
            tp_name (str): Trustpoint name from which the certificate is exported.
            format_type (str): File format type (e.g., 'pkcs12').
    
        Returns:
            bool:
                - True if the export operation succeeded.
                - False if the operation failed.
    """
    try:
        password = "cisco123"
        dialog = Dialog([
            Statement(pattern=r'.*Address or name of remote host',
                action=f'sendline({tftp_ip})',
                loop_continue=True,
                continue_timer=False),
            Statement(pattern=r'.*Destination filename',
                action=f'sendline({file_name})',
                loop_continue=True,
                continue_timer=False),
            Statement(pattern=r'.*Do you really want to overwrite it',
                action=f'sendline(yes)',
                loop_continue=True,
                continue_timer=False),
        ])

        cmd = [f"crypto pki export {tp_name} {format_type} tftp://{tftp_ip}/{file_name} password {password}"]

        error_patterns = ['Failed']

        op = device.configure(cmd, reply=dialog, error_pattern=error_patterns)
        return [True, op]
    except Exception as e:
        logger.error(f"Failed to export PKCS12 to TFTP server {tftp_ip}: {e}")
        return [False, str(e)]

def configure_crypto_pki_certificate_map(device,
                                          map_name,
                                          sequence,
                                          issuer_name=False,
                                          subject_check=None,
                                          issuer_check=None,
                                          issuer_check_str=None,
                                          subject_name=False,
                                          subject_check_str=None,
                                          subject_alt_name=False,
                                          subject_alt_check=None,
                                          subject_alt_check_str=None):
    '''
    Configures a crypto PKI certificate map on the device.
    Args:
        device ('obj'): Device object.
        map_name ('str'): Name of the certificate map.
        sequence ('int'): Sequence number for the certificate map entry.
        issuer_name ('bool', optional): Flag to include issuer-name configuration.
        subject_check ('str', optional): Operator for subject-name check (e.g., 'co', 'eq').
        issuer_check ('str', optional): Operator for issuer-name check (e.g., 'co', 'eq').
        issuer_check_str ('str', optional): String to match against the issuer-name field.
        subject_name ('bool', optional): Flag to include subject-name configuration.
        subject_check_str ('str', optional): String to match against the subject-name field.
        subject_alt_name ('bool', optional): Flag to include alt-subject-name configuration.
        subject_alt_check ('str', optional): Operator for alt-subject-name check (e.g., 'co', 'eq').
        subject_alt_check_str ('str', optional): String to match against the alt-subject-name field.
    Returns:
        None
    Raises:
        SubCommandFailure: If configuration fails on the device.
    '''
    cmds = [
        f"crypto pki certificate map {map_name} {sequence}"
    ]

    if issuer_name:
        if issuer_check and issuer_check_str:
            cmds.append(f"issuer-name {issuer_check} {issuer_check_str}")

    if subject_name:
        if subject_check and subject_check_str:
            cmds.append(f"subject-name {subject_check} {subject_check_str}")

    if subject_alt_name:
        if subject_alt_check and subject_alt_check_str:
            cmds.append(f"alt-subject-name {subject_alt_check} {subject_alt_check_str}")

    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure crypto pki certificate map {map_name}: {e}")


def unconfigure_crypto_pki_certificate_map(device, map_name, sequence):
    '''
    Removes a crypto PKI certificate map from the device.
    Args:
        device ('obj'): Device object.
        map_name ('str'): Name of the certificate map to remove.
        sequence ('int'): Sequence number of the certificate map entry to remove.
    Returns:
        None
    Raises:
        SubCommandFailure: If unconfiguration fails on the device.
    '''
    cmds = [f"no crypto pki certificate map {map_name} {sequence}"]
    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure crypto pki certificate map {map_name}: {e}")
        
def configure_pki_export_advanced(device,
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
                                prvt_key_encry=None
                         ):
    """
    Configure crypto pki export (supports PKCS12 and PEM)
        Args:
            device ('obj'): Device object
            tp_name ('str'): Name of the trustpoint to export
            export_type ('str'): Type of export ('pkcs12' or 'pem')
            file_password ('str'): Password to protect the exported file
            pkcs_media_type ('str', optional): Media type for PKCS12 export (e.g., 'bootflash:', 'tftp:')
            pkcs_file ('str', optional): PKCS12 file name for file system export
            pkcs_url ('str', optional): PKCS12 URL for network export
            pem_option ('str', optional): PEM export option ('url' or 'terminal')
            pem_media_type ('str', optional): Media type for PEM export (e.g., 'bootflash:', 'tftp:')
            pem_file ('str', optional): PEM file name for file system export
            pem_url ('str', optional): PEM URL for network export
            prvt_key_encry ('str', optional): Private key encryption option (e.g., 'rollover')
        Returns:
            str: Output from the export command
        Raises:
            ValueError: If invalid or incomplete parameters are provided
            SubCommandFailure: If the export operation fails
    """


    logger.info(f"Starting PKI export for trustpoint '{tp_name}' as {export_type.upper()}")

    dialog = Dialog([
        Statement(pattern=r'.*Address or name of remote host',
                  action='sendline()',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Destination filename',
                  action='sendline()',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Do you really want to overwrite it',
                  action='sendline(yes)',
                  loop_continue=True,
                  continue_timer=False),
    ])

    media_url = ['cns:', 'ftp:', 'http:', 'https:',
                 'null:', 'pram:', 'rcp:', 'scp:', 'sftp:', 'tftp:']
    media_file = ['bootflash:', 'crashinfo:',
                  'flash:', 'nvram:', 'system:', 'tmpsys', 'webui']

    error_patterns = [
        f"% RSA keypair {tp_name} is not exportable.",
        f"% Please delete it or use a different label.",
        f"% Trustpoint {tp_name} is in use."
    ]

    export_config = None

    if export_type.lower() == 'pkcs12':
        if pkcs_media_type in media_file:
            export_config = (
                f"crypto pki export {tp_name} pkcs12 {pkcs_media_type}{pkcs_file} password {file_password}")
        elif pkcs_media_type in media_url:
            export_config = (
                f"crypto pki export {tp_name} pkcs12 {pkcs_media_type}{pkcs_url} password {file_password}")

    elif export_type.lower() == 'pem':
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

    if not export_config:
        raise ValueError("Invalid or incomplete parameters for crypto pki export command")
    logger.info(f"Executing command: {export_config}")
    try:
        output = device.configure(export_config, reply=dialog, error_pattern=error_patterns, timeout=90)
        logger.info(f"Successfully exported {export_type.upper()} for trustpoint '{tp_name}'")
        return output
    except SubCommandFailure as e:
        logger.error(f"Failed to configure crypto pki export for {tp_name}: {e}")
        raise SubCommandFailure(f"Failed to export PKI certificate: {e}")


def configure_pki_import_advanced(device,
                                tp_name,
                                import_type,
                                file_password,
                                pem_option=None,
                                pem_media_type=None,
                                pem_url=None,
                                pkcs_media_type=None,
                                pkcs_url=None
                            ):
    """
    Configure 'crypto pki import' to import certificates or bundles from a TFTP/FTP server.
        Args:
            device ('obj'): Device connection object
            tp_name ('str'): Trustpoint name to import into
            import_type ('str'): 'pem' or 'pkcs12'
            file_password ('str'): Password used to protect the imported file
            pem_option ('str'): Type of PEM import ['url', 'terminal']
            pem_media_type ('str'): Media type for PEM import ['tftp:', 'ftp:', 'scp:', etc.]
            pem_url ('str'): URL or path for PEM import
            pkcs_media_type ('str'): Media type for PKCS12 import ['tftp:', 'ftp:', etc.]
            pkcs_url ('str'): URL or path for PKCS12 import
        Returns:
            str: Device output
        Raises:
            SubCommandFailure: If the import operation fails
    """

    logger.info(f"Starting crypto pki import for trustpoint '{tp_name}' ({import_type})")

    dialog = Dialog([
        Statement(pattern=r'.*Address or name of remote host',
                  action='sendline()',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Source filename',
                  action='sendline()',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Do you want to replace',
                  action='sendline(yes)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Do you accept this certificate',
                  action='sendline(yes)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Password:',
                  action=f'sendline("{file_password}")',
                  loop_continue=True,
                  continue_timer=False)
    ])

    media_url = ['cns:', 'ftp:', 'http:', 'https:',
                 'null:', 'pram:', 'rcp:', 'scp:', 'sftp:', 'tftp:']

    error_patterns = [
        "% Error",
        "% Failed",
        "Certificate import failed",
        "Invalid password",
        "timed out"
    ]

    import_config = None

    if import_type.lower() == "pem":
        if pem_option == "url" and pem_media_type in media_url:
            import_config = f"crypto pki import {tp_name} pem url {pem_media_type}{pem_url} password {file_password}"
        elif pem_option == "terminal":
            import_config = f"crypto pki import {tp_name} pem terminal password {file_password}"
    elif import_type.lower() == "pkcs12":
        if pkcs_media_type in media_url:
            import_config = f"crypto pki import {tp_name} pkcs12 {pkcs_media_type}{pkcs_url} password {file_password}"
    if not import_config:
        raise ValueError("Invalid or missing parameters for crypto pki import command")
    logger.info(f"Executing import command: {import_config}")
    try:
        output = device.configure(import_config, reply=dialog, error_pattern=error_patterns, timeout=120)
        logger.info(f"Successfully imported {import_type.upper()} certificate for trustpoint '{tp_name}'")
        return output
    except SubCommandFailure as e:
        logger.error(f"Failed to import PKI certificate for {tp_name}: {e}")
        raise SubCommandFailure(f"Failed PKI import: {e}")

def change_pki_certificate_hash(device, hash_algorithm=None):
    """
    Change PKI certificate hash algorithm for self-signed certificates
        Args:
            device ('obj'): Device object
            hash_algorithm ('str'): Hash algorithm (sha1, sha256, sha384, sha512, md5)
        Returns:
            True/False
    """
    logger.info(f"Configuring PKI certificate hash algorithm: {hash_algorithm or 'default'}")
    
    try:
        config_commands = []
        if hash_algorithm:
            config_commands.append(f"crypto pki certificate self-signed hash {hash_algorithm}")
            logger.debug(f"Setting hash algorithm to: {hash_algorithm}")
        else:
            config_commands.append("crypto pki certificate self-signed")
            logger.debug("Using default hash algorithm configuration")
        device.configure(config_commands)
        logger.info("Successfully configured PKI certificate hash algorithm")
        return True
    except Exception as e:
        logger.error(f"Failed to configure PKI certificate hash algorithm: {e}")
        return False

def configure_trustpool_import_terminal(device, certificate_content):
    """
    Configure 'crypto pki trustpool import terminal' to import certificates into trustpool.

    Args:
        device ('obj'): Device object
        certificate_content ('str'): PEM certificate content to import

    Returns:
        str: Device output

    Raises:
        SubCommandFailure: If the import operation fails
    """
    
    logger.info("Starting crypto pki trustpool import terminal")

    def send_certificate(spawn):
        time.sleep(5)
        if certificate_content:
            logger.info("Sending certificate content to device...")
            spawn.sendline(certificate_content)
        spawn.sendline()

    dialog = Dialog([
        Statement(
            pattern=r'.*End with a blank line or \"quit\" on a line by itself.*',
            action=send_certificate,
            loop_continue=True,
            continue_timer=False
        ),
        Statement(
            pattern=r'.*Do you accept this certificate.*\[yes/no\].*',
            action='sendline(yes)',
            loop_continue=True,
            continue_timer=False
        ),
        Statement(
            pattern=r'.*[Cc]onfirm.*',
            action='sendline(y)',
            loop_continue=True,
            continue_timer=False
        )
    ])
    
    error_patterns = [
        '% Error',
        '% Failed',
        'Certificate import failed',
        'Invalid certificate'
    ]
    
    cmd = "crypto pki trustpool import terminal"
    
    try:
        logger.info("Executing crypto pki trustpool import terminal")
        output = device.configure(cmd, reply=dialog, error_pattern=error_patterns, timeout=120)
        logger.info("Successfully imported certificate into trustpool via terminal")
        return output
    except SubCommandFailure as e:
        logger.error(f"Failed to import certificate into trustpool: {e}")
        raise SubCommandFailure(f"Failed trustpool terminal import: {e}")
