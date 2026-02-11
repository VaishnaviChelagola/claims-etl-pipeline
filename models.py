from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class EmployerGroup(Base):
    __tablename__ = "employer_group"
    group_id = Column(Integer, primary_key=True)
    group_name = Column(String)
    industry = Column(String, default="Healthcare")
    members = relationship("Member", back_populates="group")


class Member(Base):
    __tablename__ = "member"
    member_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    employer_group_id = Column(Integer, ForeignKey("employer_group.group_id"))
    group = relationship("EmployerGroup", back_populates="members")
    claims = relationship("ClaimHeader", back_populates="member")


class Provider(Base):
    __tablename__ = "provider"
    provider_id = Column(Integer, primary_key=True)
    hospital_name = Column(String)
    hospital_type = Column(String)
    claims = relationship("ClaimHeader", back_populates="provider")


class ClaimHeader(Base):
    __tablename__ = "claim_header"
    claim_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.member_id"))
    provider_id = Column(Integer, ForeignKey("provider.provider_id"))
    service_date = Column(Date)
    status = Column(String)
    member = relationship("Member", back_populates="claims")
    provider = relationship("Provider", back_populates="claims")
    line_items = relationship("ClaimLineItem", back_populates="claim")


class ClaimLineItem(Base):
    __tablename__ = "claim_line_item"
    line_id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey("claim_header.claim_id"))
    procedure_code = Column(String)
    billed_amount = Column(Float)
    paid_amount = Column(Float)
    claim = relationship("ClaimHeader", back_populates="line_items")
