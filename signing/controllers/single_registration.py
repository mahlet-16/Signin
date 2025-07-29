import os

import requests
from dotenv import load_dotenv

from models import SessionLocal, SingleRegistrationResponse
from utils import (
    get_next_document_number,
    get_next_invoice_counter,
    get_seller_data,
    get_the_last_irns,
    get_the_last_token,
    sign_request_payload,
)

load_dotenv()
API_KEY = os.getenv("API_KEY")
CERTIFICATE = os.getenv("CERTIFICATE")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
TIN = os.getenv("TIN")


def single_registration(request_body):
    if not request_body:
        print("Request body is empty. Please provide valid data.")
        return {"error": "Request body is empty. Please provide valid data."}
    if (
        not request_body.get("LegalName")
        or not request_body.get("Phone")
        or not request_body.get("Email")
        or not request_body.get("IdType")
        or not request_body.get("IdNumber")
    ):
        print("Missing required fields in request body.")
        return {"error": "Missing required fields in request body."}
    try:
        tokens = get_the_last_token()
        if not tokens:
            print("No tokens found. Please login first.")
            return {"error": "No tokens found. Please login first."}
        ACCESS_TOKEN = tokens.get("access_token")
        if not ACCESS_TOKEN:
            print("Access token not found in the last tokens.")
            return {"error": "Access token not found in the last tokens."}
    except Exception as e:
        print(f"Error retrieving tokens: {e}")
        return {"error": "Failed to retrieve tokens"}

    try:
        seller_data = get_seller_data()
        if not seller_data:
            print("Error retrieving seller data.")
            return {"error": "Error retrieving seller data."}
    except Exception as e:
        print("Error retrieving seller data:", e)
        return {"error": "Failed to retrieve seller data"}

    try:
        daynamic_data = get_the_last_irns()
        if not daynamic_data:
            print("Error retrieving last IRNs.")
            return {"error": "Error retrieving last IRNs."}
    except Exception as e:
        print(f"Error retrieving last IRNs: {e}")
        return {"error": "Failed to retrieve last IRNs"}

    url = "https://core.mor.gov.et/v1/register"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    request_object = {
        "BuyerDetails": {
            "LegalName": request_body.get("LegalName"),
            "Phone": request_body.get("Phone"),
            "Email": request_body.get("Email"),
            "IdType": request_body.get("IdType"),
            "IdNumber": request_body.get("IdNumber"),
        },
        "DocumentDetails": {
            "DocumentNumber": daynamic_data.get("documentNumber"),
            "Date": daynamic_data.get("Date"),
            "Type": "INV",
        },
        "ItemList": [
            {
                "ItemCode": "1111",
                "ProductDescription": "string",
                "Quantity": 1,
                "UnitPrice": 1000,
                "TaxAmount": 150,
                "TaxCode": "VAT15",
                "Discount": 0,
                "ExciseTaxValue": 0,
                "HarmonizationCode": None,
                "NatureOfSupplies": "Goods",
                "PreTaxValue": 1000,
                "LineNumber": 1,
                "TotalLineAmount": 1150,
                "Unit": "PCS",
            }
        ],
        "PaymentDetails": {"Mode": "CASH", "PaymentTerm": "IMMIDIATE"},
        "ReferenceDetails": {
            "PreviousIrn": daynamic_data.get("previousIrn"),
            "RelatedDocument": None,
        },
        "SellerDetails": {
            "LegalName": seller_data.get("sellerLegalName"),
            "Phone": seller_data.get("sellerPhone"),
            "Region": seller_data.get("sellerRegion"),
            "Tin": seller_data.get("sellerTin"),
            "VatNumber": seller_data.get("sellerVatNumber"),
            "Wereda": seller_data.get("sellerWoreda"),
            "City": None,
            "Email": seller_data.get("sellerEmail"),
            "HouseNumber": None,
            "Locality": None,
            "SubCity": None,
        },
        "SourceSystem": {
            "CashierName": "AAA",
            "InvoiceCounter": daynamic_data.get("invoiceCounter"),
            "SalesPersonName": "AAA",
            "SystemNumber": daynamic_data.get("systemNumber"),
            "SystemType": daynamic_data.get("systemType"),
        },
        "ValueDetails": {
            "TaxValue": 150,
            "TotalValue": 1150,
            "Discount": None,
            "ExciseValue": 0,
            "IncomeWithholdValue": 0,
            "TransactionWithholdValue": 0,
            "InvoiceCurrency": "ETB",
        },
        "TransactionType": "B2C",
        "Version": "1",
    }

    signature_b64 = sign_request_payload(request_object)
    if not signature_b64:
        print("Failed to generate signature. Aborting.")
        return {"error": "Failed to sign request"}

    final_payload = {
        "request": request_object,
        "signature": signature_b64,
        "certificate": CERTIFICATE,
    }

    try:
        response = requests.post(url, headers=headers, json=final_payload)
        response.raise_for_status()

        json_data = response.json()
        try:
            db = SessionLocal()
            records = SingleRegistrationResponse(
                irn=json_data["body"].get("irn"),
                ack_date=json_data["body"].get("ackDate"),
                status=json_data["body"].get("status"),
                signed_qr=json_data["body"].get("signedQR"),
                document_number=get_next_document_number(
                    json_data["body"].get("documentNumber")
                ),
                signed_invoice=json_data["body"].get("signedInvoice"),
                conversation_id=json_data["body"].get("0"),
                invoice_counter=get_next_invoice_counter(),
            )
            db.add(records)
            db.commit()
            db.refresh(records)

            return json_data

        finally:
            db.close()
    except requests.exceptions.HTTPError as err:
        return {"error": err.response.text}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
