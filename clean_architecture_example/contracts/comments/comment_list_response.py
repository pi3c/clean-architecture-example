from dataclasses import dataclass

from contracts.comments.comment_details_response import CommentDetailsResponse


@dataclass(frozen=True)
class CommentListResponse:
    data: list[CommentDetailsResponse]
    count: int
