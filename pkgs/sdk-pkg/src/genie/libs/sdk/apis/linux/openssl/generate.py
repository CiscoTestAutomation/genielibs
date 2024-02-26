"""Common configure functions for openssl"""

import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def generate_rsa_ssl_key(device, private_key_name, key_size=2048, password=None, aes_key_size=256, path_to_file=None, aes=True):
    """
    Args:
        device('obj'): Device to configure the SSL key on
        private_key_name(`str`): Name of the certificate file
        key_size(`int`, Optional): RSA key bit length, default 2048
        password(`str`, Optional): Password to encrypt the device key, default None
        aes('bool', Optional): Use AES encryption if True, else use 3DES. default to True.
        aes_key_size(`int`, Optional): AES keysize used to encrypt password if provided. Default 256
        path_to_file(`str`, Optional): Absolute path to the directory where the file should be saved, default None
    Raises:
        SubCommandFailure
    """

    # To handle the encryption, aes encryption is used by default
    encryption = f'aes{aes_key_size}'
    if not aes:
        encryption = 'des3'
        
    log.info(f"Configuring RSA private key with {key_size} bits")
    if path_to_file:
        try:
            device.execute(f"mkdir -p {path_to_file}")
            private_key_name = f"{path_to_file}/{private_key_name}"
        except SubCommandFailure as e:
            raise SubCommandFailure(f"Error with sourcing the directory in which to save the private key. Error:\n{e}")

    cmd = [f"openssl genrsa -out {private_key_name} {key_size}"]
    if password:
        log.info(f"Key will be encrypted to file encrypted_{private_key_name}")
        cmd.append(f"openssl rsa -{encryption} -in {private_key_name} -out {private_key_name} -passout pass:{password}")

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure RSA{key_size} key on the device. Error:\n{e}")

def generate_ecc_ssl_key(device, private_key_name, elliptic_curve, password=None, aes_key_size=256, path_to_file=None, aes=True):
    """
    Args:
        device(`obj`): Device to configure the SSL key on
        private_key_name(`str`): Name of the private key file
        elliptic_curve(`str`): Specify which elliptic curve to employ
        password(`str`, Optional): Password to encrypt the private key, default None
        aes('bool', Optional): Use AES encryption if True, else use 3DES. default to True.
        aes_key_size(`int`, Optional): AES keysize used to encrypt password if provided. Default 256
        path_to_file(`str`, Optional): Absolute path to the directory where the file should be saved, default None
    Raises:
        SubCommandFailure
    """

    # To handle the encryption, aes encryption is used by default
    encryption = f'aes{aes_key_size}'
    if not aes:
        encryption = 'des3'

    log.info(f"Configuring ECC private key with {elliptic_curve}")
    if path_to_file:
        try:
            device.execute(f"mkdir -p {path_to_file}")
            private_key_name = f"{path_to_file}/{private_key_name}"
        except SubCommandFailure as e:
            raise SubCommandFailure(f"Error with sourcing the directory in which to save the private key. Error:\n{e}")

    cmd = [f"openssl ecparam -genkey -name {elliptic_curve} -out {private_key_name}"]
    if password:
        log.info(f"Key will be encrypted to file {private_key_name}")
        cmd.append(f"openssl ec -{encryption} -in {private_key_name} -out {private_key_name} -passout pass:{password}")

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure the {elliptic_curve} key on the device. Error:\n{e}")

def generate_ca_certificate(device, private_key_file, subject=None, private_key_password=None,
                            certificate_name=None, path_to_file=None):
    """
    Args:
        device(`obj`): Device to configure the SSL key on
        private_key_file(`str`): Filename or absolute path to a file containing a private key
        subject(`str`, Optional): The subject line for the certificate. Default '/C=/ST=/L=/O=/CN=rootCA'
        private_key_password(`str`, Optional): The password for the private_key_file, if applicable. Default None
        certificate_name(`str`, Optional): The name of the generated certificate file, default 'rootCA.pem'
        path_to_file(`str`, Optional): Absolute path to the directory where the file should be saved, default None
    Raises:
        SubCommandFailure
    """
    if not certificate_name:
        certificate_name = 'rootCA.pem'
    if not subject:
        subject = '/C=/ST=/L=/O=/CN=rootCA'
    if path_to_file:
        try:
            device.execute(f"mkdir -p {path_to_file}")
            certificate_name = f"{path_to_file}/{certificate_name}"
        except SubCommandFailure as e:
            raise SubCommandFailure(f"Error with sourcing the directory in which to save the CA certificate. Error:\n{e}")

    log.info(f"Generating a ca certificate for subject {subject} to be named {certificate_name}")
    cmd = f"openssl req -subj {subject} -x509 -new -nodes -key {private_key_file} -sha256 -out {certificate_name}"
    if private_key_password:
        cmd += f" -passin pass:{private_key_password}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure the ca certificate. Error: \n{e}")

def generate_ssl_certificate(device, device_key_file, ca_certificate_file, private_key_file,
                             device_key_password=None, private_key_password=None,
                             subject=None, csr_name=None, crt_name=None, path_to_file=None, sha_bit_length=256):
    """
    Args:
        device(`obj`): Device to configure the SSL key on
        device_key_file(`str`): Filename or absolute path to a file containing a private key for the device
        ca_certificate_file(`str`): Filename or absolute path to a file containing a CA Certificate
        private_key_file(`str`): Filename or absolute path to a file containing a private key for the certificate
        device_key_password(`str`, Optional): The password for the device_key_file, if applicable. Default None
        subject(`str`, Optional): The subject line for the certificate. Default is '/C=/ST=/L=/O=/CN=$(hostname)'
        private_key_password(`str`, Optional): The password for the private_key_file, if applicable. Default None
        csr_name(`str`, Optional): The name of the generated csr file, default 'device.csr'
        crt_name(`str`, Optional): The name of the generated cst file, default 'device.crt'
        path_to_file(`str`, Optional): Absolute path to the directory where the files should be saved, default None
        sha_bit_length(`int`, Optional): The bit length of the SHA hash of the crt file, default 256
    Raises:
        SubCommandFailure
    """
    if not subject:
        try:
            hostname = device.execute('hostname')
        except SubCommandFailure as e:
            raise SubCommandFailure(f"Failed to fetch hostname to populate default subject. Error:\n{e}")
        subject = f"/C=/ST=/L=/O=/CN={hostname}"
    if not csr_name:
        csr_name = "device.csr"
    if not crt_name:
        crt_name = "device.crt"
    if path_to_file:
        csr_name = f"{path_to_file}/{csr_name}"
        crt_name = f"{path_to_file}/{crt_name}"

    csr_cmd = f"openssl req -subj {subject} -new -key {device_key_file} -out {csr_name}"
    if device_key_password:
        csr_cmd += f" -passin pass:{device_key_password}"

    crt_cmd = f"openssl x509 -req -in {csr_name} -CA {ca_certificate_file} -CAkey {private_key_file} -CAcreateserial -out {crt_name} -sha{sha_bit_length}"
    if private_key_password:
        crt_cmd += f" -passin pass:{private_key_password}"

    cmd = [csr_cmd, crt_cmd]

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to generate the ssl certificate. Error:\n{e}")


def generate_pkcs12(device, device_key_file, device_cert_file, root_cert_file, output_pkcs12_file,
                     passin_password=None, passout_password=None):
    """
    Args:
        device('obj'): Device to configure the SSL key on.
        device_key_file(`str`): Filename or absolute path to a file containing a device key for the certificate.
        device_cert_file(`str`): Filename or absolute path to a file containing a device certificate.
        root_cert_file(`str`): Filename or absolute path to a root certificate.
        output_pkcs12_file(`str`): Filename or absolute path to a output pkcs12 file.
        passin_password(`str`, Optional): The password for the input private key file, if applicable. Default None.
        passout_password(`str`, Optional): The password for the output private key file, if applicable. Default None.
    Raises:
        SubCommandFailure
    """

    cmd = f"openssl pkcs12 -export -chain -inkey {device_key_file} -in {device_cert_file} -CAfile {root_cert_file} -out {output_pkcs12_file}"
    if passin_password:
        cmd += f" -passin pass:{passin_password}"
    if passout_password:
        cmd += f" -passout pass:{passout_password}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to generate pkcs12 file on the device. Error:\n{e}")
