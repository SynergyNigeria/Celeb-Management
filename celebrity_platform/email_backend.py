"""
Custom email backend that uses Resend's HTTP API instead of SMTP.

Render's free tier blocks outbound SMTP ports (465/587), so we send
via Resend's REST API over HTTPS (port 443) which is always open.
"""
import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class EmailBackend(BaseEmailBackend):
    """Sends email via Resend HTTP API — works on Render free tier."""

    def open(self):
        resend.api_key = settings.RESEND_API_KEY
        return True

    def close(self):
        pass

    def send_messages(self, email_messages):
        resend.api_key = settings.RESEND_API_KEY
        sent = 0
        for msg in email_messages:
            try:
                to = msg.to if isinstance(msg.to, list) else list(msg.to)
                body = msg.body

                # Use HTML alternative if available
                html_body = None
                for content, mimetype in getattr(msg, "alternatives", []):
                    if mimetype == "text/html":
                        html_body = content
                        break

                params = {
                    "from": msg.from_email or settings.DEFAULT_FROM_EMAIL,
                    "to": to,
                    "subject": msg.subject,
                }
                if html_body:
                    params["html"] = html_body
                else:
                    params["text"] = body

                resend.Emails.send(params)
                sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent

