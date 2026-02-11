from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["claims_reporting"]


@app.get("/claims/summary")
def get_claims_summary():
    return list(db.claims_summary.find({}, {"_id": 0}))


@app.get("/claims/by-group/{group_id}")
def get_claims_by_group(group_id: int):
    return list(db.claims_summary.find({"employer_group_id": group_id}, {"_id": 0}))


@app.get("/claims/status-counts")
def get_status_counts():
    pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
    return list(db.claims_summary.aggregate(pipeline))
