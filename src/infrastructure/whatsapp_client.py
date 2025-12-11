import logging

import requests

logger = logging.getLogger("whatsapp_client")


class WhatsAppClient:
    def __init__(self, api_url: str, token: str):
        # api_url debe ser https://graph.facebook.com/v22.0/<PHONE_NUMBER_ID>
        self.api_url = api_url.rstrip("/")
        self.token = token

    def send_message(self, recipient_id: str, message: str):
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {"body": message},
        }
        response = requests.post(
            f"{self.api_url}/messages",
            json=payload,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10,
        )
        logger.info(
            "WhatsApp API response status=%s body=%s",
            response.status_code,
            response.text,
        )
        response.raise_for_status()
        return response.json()
