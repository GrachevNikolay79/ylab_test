import json
from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas import PostCreate, PostModel
from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.db import AbstractCache, get_cache, get_session
from src.models.post import Post
from src.services import ServiceMixin

__all__ = ("PostService", "get_post_service")

REDIS_POST_BASE_NUM: int = 1


class PostService(ServiceMixin):
    def get_post_list(self) -> dict:
        """Получить список постов."""
        posts = self.session.query(Post).order_by(Post.created_at).all()
        return {"posts": [PostModel(**post.dict()) for post in posts]}

    def get_post_detail(self, item_id: int) -> Optional[dict]:
        """Получить детальную информацию поста."""
        self.cache.select(REDIS_POST_BASE_NUM)
        if cached_post := self.cache.get(key=f"{item_id}"):
            return json.loads(cached_post)

        post = self.session.query(Post).filter(Post.id == item_id).first()
        if post:
            self.cache.set(key=f"{post.id}", value=post.json(), expire=CACHE_EXPIRE_IN_SECONDS)
        return post.dict() if post else None

    def create_post(self, post: PostCreate) -> dict:
        """Создать пост."""
        new_post = Post(title=post.title,
                        description=post.description,
                        author_id=post.author_id)
        self.session.add(new_post)
        self.session.commit()
        self.session.refresh(new_post)

        self.cache.select(REDIS_POST_BASE_NUM)
        self.cache.set(key=f"{new_post.id}", value=new_post.json(), expire=CACHE_EXPIRE_IN_SECONDS)
        return new_post.dict()


# get_post_service — это провайдер PostService. Синглтон
@lru_cache()
def get_post_service(cache: AbstractCache = Depends(get_cache),
                     session: Session = Depends(get_session)) -> PostService:
    return PostService(cache=cache, session=session)
