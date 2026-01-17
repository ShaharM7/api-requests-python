from typing import Any, Dict, List

from src.base_client import BaseClient


def list_posts(client: BaseClient) -> List[Dict[str, Any]]:
    """GET /posts and return the list."""
    raise NotImplementedError("TODO: implement list_posts")


def get_post(client: BaseClient, post_id: int) -> Dict[str, Any]:
    """GET /posts/{post_id} and return the post."""
    raise NotImplementedError("TODO: implement get_post")


def create_post(client: BaseClient, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST /posts with JSON payload and return the created post."""
    raise NotImplementedError("TODO: implement create_post")


def update_post(
    client: BaseClient, post_id: int, payload: Dict[str, Any]
) -> Dict[str, Any]:
    """PUT /posts/{post_id} with JSON payload and return updated post."""
    raise NotImplementedError("TODO: implement update_post")


def delete_post(client: BaseClient, post_id: int) -> None:
    """DELETE /posts/{post_id}."""
    raise NotImplementedError("TODO: implement delete_post")


def main() -> None:
    client = BaseClient()
    posts = list_posts(client)
    print(f"Retrieved {len(posts)} posts")

    first_post = get_post(client, post_id=1)
    print(f"First post title: {first_post.get('title')}")

    created = create_post(
        client,
        payload={"title": "hello", "body": "world", "userId": 1},
    )
    print(f"Created post id: {created.get('id')}")

    updated = update_post(client, post_id=1, payload={"title": "updated"})
    print(f"Updated post title: {updated.get('title')}")

    delete_post(client, post_id=1)
    print("Deleted post")


if __name__ == "__main__":
    main()
