#!/usr/bin/env python3
"""Log stats module"""

from pymongo import MongoClient

def log_stats():
    """Log stats function"""
    client = MongoClient('mongodb://localhost:27017/')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    status_check = logs_collection.count_documents({"path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{status_check} status check")

    top_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for idx, ip_info in enumerate(top_ips, start=1):
        print(f"\t{ip_info['_id']}: {ip_info['count']}")

if __name__ == "__main__":
    log_stats()
