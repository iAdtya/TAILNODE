import os
import requests
from supabase import create_client, Client


def create_supabase_client():
    url = "https://seuqlacxzpyohiajgvei.supabase.co"
    key = "your_key_here"
    return create_client(url, key)


def fetch_users():
    headers = {"app-id": "65f30ebc41074b0d23df9bc7"}
    response = requests.get("https://dummyapi.io/data/v1/user", headers=headers)
    return response.json()["data"]


def insert_users_to_db(supabase, users):
    for user in users:
        user = {k.lower(): v for k, v in user.items()}  # Convert keys to lowercase
        supabase.table("users").insert(user).execute()


def fetch_posts(user_id):
    headers = {"app-id": "65f30ebc41074b0d23df9bc7"}
    response = requests.get(
        f"https://dummyapi.io/data/v1/user/{user_id}/post", headers=headers
    )
    return response.json()["data"]


def insert_posts_to_db(supabase, posts):
    for post in posts:
        text = post["text"]
        owner_id = post["id"]
        supabase.table("posts").insert({"text": text, "id": owner_id}).execute()


def main():
    supabase = create_supabase_client()

    users = fetch_users()
    insert_users_to_db(supabase, users)

    user_ids = [user["id"] for user in users]
    for user_id in user_ids:
        posts = fetch_posts(user_id)
        insert_posts_to_db(supabase, posts)


if __name__ == "__main__":
    main()
