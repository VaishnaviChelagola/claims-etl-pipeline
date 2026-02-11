-- Employer Groups
INSERT INTO employer_group (group_id, group_name) VALUES
(1, 'TechCorp'),
(2, 'HealthPlus'),
(3, 'EduWorld');

-- Members
INSERT INTO member (first_name, last_name, dob, employer_group_id) VALUES
('Alice', 'Smith', '1985-02-10', 1),
('Bob', 'Johnson', '1990-07-21', 2),
('Carol', 'Lee', '1978-11-05', 3);

-- Providers
INSERT INTO provider (hospital_name, hospital_type) VALUES
('City General Hospital', 'General'),
('Metro Specialty Hospital', 'Cardiology'),
('Community Health Center', 'Primary Care');

-- Claim Headers
INSERT INTO claim_header (member_id, provider_id, service_date, status) VALUES
(1, 1, '2026-01-15', 'Submitted'),
(2, 2, '2026-01-20', 'Processed'),
(3, 3, '2026-01-25', 'Paid');

-- Claim Line Items (10 rows total)
INSERT INTO claim_line_item (claim_id, procedure_code, billed_amount, paid_amount) VALUES
(1, 'PROC100', 300, 0),
(1, 'PROC101', 200, 0),
(2, 'PROC102', 500, 300),
(2, 'PROC103', 250, 200),
(2, 'PROC104', 150, 100),
(3, 'PROC105', 400, 400),
(3, 'PROC106', 600, 600),
(3, 'PROC107', 200, 200),
(3, 'PROC108', 350, 350),
(3, 'PROC109', 150, 150);
