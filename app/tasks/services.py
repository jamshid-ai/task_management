from datetime import datetime
from elasticsearch import Elasticsearch, NotFoundError
from uuid import uuid4
from ..core.elastic import get_elasticsearch_client


class TaskService:
    def __init__(self):
        self.es = get_elasticsearch_client()
        self.index = "tasks"

    async def create_task(self, title: str, description: str, status: str, username: str):
        task_id = str(uuid4())  # Generate a unique task ID
        task_doc = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": status,
            "username": username,  # Changed from user_id to username
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Index the task document in Elasticsearch
        self.es.index(index=self.index, id=task_id, body=task_doc)
        return task_doc

    async def get_task(self, task_id: str, username: str, is_admin: bool):
        try:
            response = self.es.get(index=self.index, id=task_id)
            task = response["_source"]

            # Ensure the task belongs to the user, unless the user is an admin
            if task["username"] != username and not is_admin:
                return None

            return task
        except NotFoundError:
            return None

    async def update_task(self, task_id: str, title: str, description: str, status: str, username: str, is_admin: bool):
        task = await self.get_task(task_id, username, is_admin)
        if not task:
            return None

        task["title"] = title if title is not None else task["title"]
        task["description"] = description if description is not None else task["description"]
        task["status"] = status if status is not None else task["status"]
        task["updated_at"] = datetime.utcnow()

        # Update the task document in Elasticsearch
        self.es.index(index=self.index, id=task_id, body=task)
        return task

    async def delete_task(self, task_id: str, username: str, is_admin: bool):
        task = await self.get_task(task_id, username, is_admin)
        if not task:
            return False

        # Delete the task document by ID
        self.es.delete(index=self.index, id=task_id)
        return True

    async def list_tasks(self, username: str, is_admin: bool):
        # Build a query to list tasks, optionally filtering by username unless admin
        query = {"query": {"match_all": {}}} if is_admin else {
            "query": {"match": {"username": username}}  # Filter by username
        }

        response = self.es.search(index=self.index, body=query)
        tasks = [hit["_source"] for hit in response["hits"]["hits"]]
        return tasks

