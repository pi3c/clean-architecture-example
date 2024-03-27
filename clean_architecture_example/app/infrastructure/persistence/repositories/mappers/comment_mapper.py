from app.domain.comments.comment import Comment, CommentContent, CommentId
from app.domain.posts.post import PostId
from app.domain.users.user import UserId


def comment_from_dict_to_entity(adict: dict) -> Comment:
    return Comment(
        id=CommentId(adict["id"]),
        content=CommentContent(adict["content"]),
        post_id=PostId(adict["post_id"]),
        owner_id=UserId(adict["owner_id"]),
        created_at=adict["created_at"],
        updated_at=adict["updated_at"],
    )
