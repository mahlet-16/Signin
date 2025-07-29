from models import SellerDetails, SessionLocal


def get_seller_data():
    db = SessionLocal()
    try:
        last_data = db.query(SellerDetails).order_by(SellerDetails.id.desc()).first()
        return {
            "sellerEmail": last_data.email if last_data else None,
            "sellerLegalName": last_data.legal_name if last_data else None,
            "sellerPhone": last_data.phone if last_data else None,
            "sellerRegion": last_data.region if last_data else None,
            "sellerTin": last_data.tin if last_data else None,
            "sellerVatNumber": last_data.vat_number if last_data else None,
            "sellerWoreda": last_data.wereda if last_data else None,
        }
    finally:
        db.close()
