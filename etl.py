from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ClaimHeader
from pymongo import MongoClient

# ✅ Corrected connection string
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/claims_db"
)
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
        "employer_group_id": claim.member.employer_group_id,
        "provider_id": claim.provider_id,
        "service_date": service_date,
        "total_paid": total_paid,
        "total_billed": total_billed,
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
    print("Total claims found:", len(claims))

    summaries, details = [], []

    for claim in claims:
        transformed = transform_claim(claim)
        summaries.append(
            {
                "claim_id": transformed["claim_id"],
                "member_id": transformed["member_id"],
                "employer_group_id": transformed["employer_group_id"],
                "provider_id": transformed["provider_id"],
                "total_paid": transformed["total_paid"],
                "status": transformed["status"],
            }
        )
        details.append(transformed)

    # Clear old data
    mongo_db.claims_summary.delete_many({})
    mongo_db.claims_detail.delete_many({})

    # Insert new data
    mongo_db.claims_summary.insert_many(summaries)
    mongo_db.claims_detail.insert_many(details)

    print("ETL completed successfully!")


if __name__ == "__main__":
    run_etl()
