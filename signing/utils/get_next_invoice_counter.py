from models import SessionLocal, SingleRegistrationResponse


def get_next_invoice_counter(start_from=69):
    db = SessionLocal()
    try:
        last_entry = (
            db.query(SingleRegistrationResponse)
            .order_by(SingleRegistrationResponse.invoice_counter.desc())
            .first()
        )
        if last_entry and last_entry.invoice_counter is not None:
            return last_entry.invoice_counter + 1
        else:
            return start_from
    finally:
        db.close()


def get_next_document_number(number):
    num = int(number) + 1
    return str(num)
