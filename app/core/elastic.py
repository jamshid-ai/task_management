from elasticsearch import Elasticsearch
from ..config import elastic_settings

es = Elasticsearch(
    hosts=[elastic_settings.hosts],  # Adjust the host as needed
    http_auth=(elastic_settings.username, elastic_settings.password) # Replace with your credentials
)

def get_elasticsearch_client():
    if not es.ping():
        raise ValueError("Connection failed to Elasticsearch")
    return es


def create_indexes():
    # Define the mapping for users index
    user_mapping = {
        "mappings": {
            "properties": {
                "username": {"type": "keyword"},
                "hashed_password": {"type": "text"},
                "role": {"type": "keyword"}
            }
        }
    }

    # Create the users index
    es.indices.create(index="users", body=user_mapping)

    # Define the mapping for tasks index
    task_mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "description": {"type": "text"},
                "status": {"type": "keyword"},
                "username": {"type": "keyword"},
                "created_at": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "updated_at": {"type": "date", "format": "strict_date_optional_time||epoch_millis"}
            }
        }
    }

    # Create the tasks index
    es.indices.create(index="tasks", body=task_mapping)

# Define the index name
INDEX_NAME = "tasks"

# Step 2: Define the new index mapping
NEW_INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "status": {"type": "keyword"},
            "username": {"type": "keyword"},  # Updated field from user_id to username
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"}
        }
    }
}

# Step 3: Delete the existing index
def delete_existing_index():
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Index {INDEX_NAME} deleted.")
    else:
        print(f"Index {INDEX_NAME} does not exist.")

# Step 4: Create the new index with updated mappings
def create_new_index():
    es.indices.create(index=INDEX_NAME, body=NEW_INDEX_MAPPING)
    print(f"Index {INDEX_NAME} created with updated mappings.")

# # Execute the steps
# delete_existing_index()
# create_new_index()
