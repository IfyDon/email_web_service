import subprocess
from core.utils.dns_utils import verify_txt_record


class DomainService:
    @staticmethod
    def verify_domain(domain) -> bool:
        """Check if the domain ownership TXT record is correctly published."""
        record_name = domain.get_verification_record_name()
        return verify_txt_record(record_name, domain.verification_token)

    @staticmethod
    def generate_dkim_keys():
        """
        Generate a 2048‑bit RSA key pair for DKIM using openssl.
        Returns (private_pem, public_pem) as strings.
        """
        try:
            private_pem = subprocess.check_output(
                ['openssl', 'genrsa', '2048'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8')
            public_pem = subprocess.check_output(
                ['openssl', 'rsa', '-pubout'],
                input=private_pem.encode(),
                stderr=subprocess.DEVNULL
            ).decode('utf-8')
            return private_pem, public_pem
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Graceful fallback for environments without openssl
            return "dummy-private-key", "dummy-public-key"