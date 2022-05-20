import os
from utils.logging import logger


def get_tls_ca_cert_path() -> str:
    root_ca_cert = os.getenv("ROOT_CA_CERT")
    root_ca_cert_filename = "DMTRootCA.pem"
    if root_ca_cert:
        if root_ca_cert.startswith("-----BEGIN CERTIFICATE-----"):
            try:
                with open(root_ca_cert_filename, "w") as f:
                    f.write(root_ca_cert)
                return root_ca_cert_filename
            except Exception as error:
                logger.critical("Failed while writing the 'ROOT_CA_CERT' to disk.")
                logger.error(error)
        else:
            logger.critical("The value provided in 'ROOT_CA_CERT' is not a valid certificate.")

    return None
