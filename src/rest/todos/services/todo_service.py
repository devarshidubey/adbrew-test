from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId
from core.db.mongo import get_collection

todos_col = get_collection("todos")
todos_col.create_index("created_at")

class TodoService:
    @staticmethod
    def create_todo(data):
        todo = {
            "title": data["title"],
            "completed": False,
            "created_at": datetime.utcnow(),
        }
        todos_col.insert_one(todo)
        todo["_id"] = str(todo["_id"])
        return todo

    @staticmethod
    def list_todos(limit = 20, page = 1):
        query = {} #filter if needed

        skip = (page - 1) * limit
        cursor = todos_col.find(query).sort("created_at", -1).skip(skip).limit(limit)

        todos = []
        for todo in cursor:
            todo["_id"] = str(todo["_id"])
            todos.append(todo)

        total = todos_col.count_documents(query)

        return {
            "items": todos,
            "total": total,
            "page": page,
            "limit": limit,
        }