import sys
from pathlib import Path
import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Base, EmployerGroup, Member, Provider, ClaimHeader, ClaimLineItem

# -----------------------------
# CONFIGURATION
# -----------------------------
NUM_GROUPS = 5
NUM_MEMBERS = 50
NUM_PROVIDERS = 10
NUM_CLAIMS = 100
MAX_LINE_ITEMS_PER_CLAIM = 5

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/claims_db"

# -----------------------------
# SETUP
# -----------------------------
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def seed_employer_groups():
    groups = []
    for _ in range(NUM_GROUPS):
        group = EmployerGroup(
            group_name=fake.company(),
            industry=random.choice(["Healthcare", "IT", "Finance", "Education"]),
        )
        session.add(group)
        groups.append(group)

    session.commit()
    return groups


def seed_members(groups):
    members = []
    for _ in range(NUM_MEMBERS):
        member = Member(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=65),
            employer_group_id=random.choice(groups).group_id,
        )
        session.add(member)
        members.append(member)

    session.commit()
    return members


def seed_providers():
    providers = []
    for _ in range(NUM_PROVIDERS):
        provider = Provider(
            hospital_name=fake.company() + " Hospital",
            hospital_type=random.choice(
                ["General", "Cardiology", "Orthopedic", "Primary Care"]
            ),
        )
        session.add(provider)
        providers.append(provider)

    session.commit()
    return providers


def seed_claims(members, providers):
    for _ in range(NUM_CLAIMS):
        member = random.choice(members)
        provider = random.choice(providers)

        claim = ClaimHeader(
            member_id=member.member_id,
            provider_id=provider.provider_id,
            service_date=fake.date_between(start_date="-1y", end_date="today"),
            status="Submitted",  # Placeholder, will be updated
        )

        session.add(claim)
        session.commit()  # commit to get claim_id

        # Add line items
        line_items = []
        for _ in range(random.randint(1, MAX_LINE_ITEMS_PER_CLAIM)):
            billed = round(random.uniform(100, 1000), 2)
            paid = round(random.uniform(0, billed), 2)

            line = ClaimLineItem(
                claim_id=claim.claim_id,
                procedure_code="PROC" + str(random.randint(100, 999)),
                billed_amount=billed,
                paid_amount=paid,
            )
            session.add(line)
            line_items.append((billed, paid))

        session.commit()

        # Calculate status based on line items
        total_paid = sum(li[1] for li in line_items)
        total_billed = sum(li[0] for li in line_items)

        if total_paid == 0:
            claim.status = "Submitted"
        elif total_paid < total_billed:
            claim.status = "Processed"
        else:
            claim.status = "Paid"

        session.commit()


def run_seed():
    # Clear existing data
    print("Clearing existing data...")
    session.query(ClaimLineItem).delete()
    session.query(ClaimHeader).delete()
    session.query(Member).delete()
    session.query(Provider).delete()
    session.query(EmployerGroup).delete()
    session.commit()

    print("Seeding employer groups...")
    groups = seed_employer_groups()

    print("Seeding members...")
    members = seed_members(groups)

    print("Seeding providers...")
    providers = seed_providers()

    print("Seeding claims and line items...")
    seed_claims(members, providers)

    print("✅ Data seeding completed!")


if __name__ == "__main__":
    run_seed()
