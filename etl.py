from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ClaimHeader
from pymongo import MongoClient

# ✅ Corrected connection string
engine = create_engine("postgresql+psycopg2://user:pass@localhost:5432/claimsdb")
Session = sessionmaker(bind=engine)
session = Session()

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["claims_reporting"]


def transform_claim(claim):
    # Transformation 1: Uniform date format
    service_date = claim.service_date.strftime("%Y-%m-%d")

    # Transformation 2: Calculate totals
    total_paid = sum(li.paid_amount for li in claim.line_items)
    total_billed = sum(li.billed_amount for li in claim.line_items)

    # Transformation 3: Derived status
    if total_paid == 0:
        status = "Submitted"
    elif total_paid < total_billed:
        status = "Processed"
    else:
        status = "Paid"

    # Transformation 4: Combine header + line items
    return {
        "claim_id": claim.claim_id,
        "member_id": claim.member_id,
        "provider_id": claim.provider_id,
        "service_date": service_date,
        "total_paid": total_paid,
        "status": status,
        "line_items": [
            {
                "procedure_code": li.procedure_code,
                "billed": li.billed_amount,
                "paid": li.paid_amount,
            }
            for li in claim.line_items
        ],
    }


def run_etl():
    claims = session.query(ClaimHeader).all()
    summaries, details = [], []

    for claim in claims:
        transformed = transform_claim(claim)
        summaries.append(
            {
                "claim_id": transformed["claim_id"],
                "member_id": transformed["member_id"],
                "provider_id": transformed["provider_id"],
                "total_paid": transformed["total_paid"],
                "status": transformed["status"],
            }
        )
        details.append(transformed)

    mongo_db.claims_summary.insert_many(summaries)
    mongo_db.claims_detail.insert_many(details)


if __name__ == "__main__":
    run_etl()
