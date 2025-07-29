from models import SessionLocal, SingleRegistrationResponse


def format_response_model(date):
    if date:
        return date.strftime("%d-%m-%YT%H:%M:%S")
    return None


def get_the_last_irns():
    db = SessionLocal()
    try:
        last_data = (
            db.query(SingleRegistrationResponse)
            .order_by(SingleRegistrationResponse.id.desc())
            .first()
        )

        return {
            "previousIrn": last_data.irn if last_data else None,
            "documentNumber": last_data.document_number if last_data else None,
            "invoiceCounter": last_data.invoice_counter if last_data else None,
            "Date": format_response_model(last_data.date if last_data else None),
            "systemNumber": "0FF925838A",
            "systemType": "POS",
        }

    finally:
        db.close()
