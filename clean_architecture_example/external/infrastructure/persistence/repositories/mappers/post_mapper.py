from core.domain.posts.post import Post, PostContent, PostId, PostTitle
from core.domain.users.user import UserId


def post_from_dict_to_entity(adict: dict) -> Post:
    return Post(
        id=PostId(adict["id"]),
        title=PostTitle(adict["title"]),
        content=PostContent(adict["content"]),
        owner_id=UserId(adict["owner_id"]),
        created_at=adict["created_at"],
        updated_at=adict["updated_at"],
    )
