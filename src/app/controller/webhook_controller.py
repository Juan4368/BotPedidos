import logging
import os
from typing import Annotated, Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.services.product_service import ProductService
from src.infrastructure.repository.createProductsRepository import ProductRepository
from src.infrastructure.whatsapp_client import WhatsAppClient

router = APIRouter(tags=["webhook"])   # SIN prefix


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo = ProductRepository(db)
    return ProductService(repo)


ServiceDep = Annotated[ProductService, Depends(get_product_service)]

WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
whatsapp_client: Optional[WhatsAppClient] = None

log_path = os.getenv("WEBHOOK_LOG_PATH", "logs/webhook_payloads.txt")
log_dir = os.path.dirname(log_path)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("webhook")
logger.setLevel(logging.INFO)
if not logger.handlers:
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    logger.addHandler(file_handler)

if os.getenv("WHATSAPP_API_URL") and os.getenv("WHATSAPP_TOKEN"):
    whatsapp_client = WhatsAppClient(
        api_url=os.getenv("WHATSAPP_API_URL"),
        token=os.getenv("WHATSAPP_TOKEN"),
    )


@router.get("/webhook")
def whatsapp_verify(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    hub_challenge: int | None = Query(default=None, alias="hub.challenge"),
):
    """
    Endpoint de verificacion para WhatsApp Cloud (GET).
    """
    logger.info(
        "GET /webhook hub.mode=%s hub.verify_token=%s hub.challenge=%s",
        hub_mode,
        hub_verify_token,
        hub_challenge,
    )
    if hub_mode == "subscribe" and hub_verify_token == WHATSAPP_VERIFY_TOKEN:
        return hub_challenge
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


@router.post("/webhook")
async def whatsapp_webhook(request: Request, service: ServiceDep):
    """
    Procesa mensajes entrantes de WhatsApp.
    Si llega texto, busca productos por ese texto y responde con coincidencias.
    """
    if whatsapp_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="WhatsApp client no configurado",
        )

    body = await request.json()
    logger.info("POST /webhook payload es: %s", body)
    try:
        entry = body.get("entry", [])[0]
        change = entry.get("changes", [])[0]
        value = change.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "ignored"}

        message = messages[0]
        logger.info("El mensaje  es: %s", message)
        text = message.get("text", {}).get("body", "").strip()
        sender = message.get("from")

        if not text or not sender:
            return {"status": "ignored"}

        results = service.search_products(text)
        if results:
            lines = [f"{p.nombre} - {p.precio} - stock:{p.stock_actual}" for p in results[:5]]
            reply = "Coincidencias:\n" + "\n".join(lines)
        else:
            reply = "No se encontraron productos para tu busqueda."

        try:
            whatsapp_client.send_message(sender, reply)
        except requests.HTTPError as exc:
            resp = exc.response
            detail = f"WhatsApp API error {resp.status_code if resp else ''}: {resp.text if resp else exc}"
            logger.error(detail)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=detail,
            ) from exc

        return {"status": "ok"}
    except HTTPException:
        # Re-raise HTTP errors (e.g., 503 when el cliente no está configurado).
        raise
    except Exception:
        # Captura el stack trace en el log para depurar 500.
        logger.exception("Error procesando webhook")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno procesando webhook",
        )
