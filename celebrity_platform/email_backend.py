"""
Custom SMTP backend that uses certifi's CA bundle.

Needed on Windows with Python 3.12+ where the bundled SSL certificates
don't cover all CAs (e.g. Resend's cert chain), causing
CERTIFICATE_VERIFY_FAILED errors.
"""
import ssl
import smtplib

import certifi
from django.core.mail.backends.smtp import EmailBackend as _DjangoSMTPBackend
from django.core.mail.utils import DNS_NAME


class EmailBackend(_DjangoSMTPBackend):
    """Drop-in replacement that forces SSL verification via certifi."""

    def open(self):
        if self.connection:
            return False

        connection_params = {"local_hostname": DNS_NAME.get_fqdn()}
        if self.timeout is not None:
            connection_params["timeout"] = self.timeout

        # Build an SSL context that trusts certifi's CA bundle
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        if self.ssl_keyfile:
            ssl_context.load_cert_chain(certfile=self.ssl_certfile, keyfile=self.ssl_keyfile)

        try:
            if self.use_ssl:
                # Port 465 — direct SSL/TLS (Resend's recommended setup)
                connection_params["context"] = ssl_context
                self.connection = smtplib.SMTP_SSL(self.host, self.port, **connection_params)
            else:
                self.connection = smtplib.SMTP(self.host, self.port, **connection_params)
                if self.use_tls:
                    # Port 587 — STARTTLS upgrade
                    self.connection.ehlo()
                    self.connection.starttls(context=ssl_context)
                    self.connection.ehlo()

            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except OSError:
            if not self.fail_silently:
                raise
