CREATE TABLE employer_group (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(100),
    industry VARCHAR(100) DEFAULT 'Healthcare'
);

CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE,
    employer_group_id INT REFERENCES employer_group(group_id)
);

CREATE TABLE provider (
    provider_id SERIAL PRIMARY KEY,
    hospital_name VARCHAR(100),
    hospital_type VARCHAR(100) -- e.g., General, Specialty
);

CREATE TABLE claim_header (
    claim_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES member(member_id),
    provider_id INT REFERENCES provider(provider_id),
    service_date DATE,
    status VARCHAR(50)
);

CREATE TABLE claim_line_item (
    line_id SERIAL PRIMARY KEY,
    claim_id INT REFERENCES claim_header(claim_id),
    procedure_code VARCHAR(20),
    billed_amount NUMERIC(10,2),
    paid_amount NUMERIC(10,2)
);
