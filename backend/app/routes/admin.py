from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services import recipe_service
from app.middleware.auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return recipe_service.get_admin_stats(db)


@router.get("/users")
def list_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    users = recipe_service.get_all_users(db)
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
        }
        for u in users
    ]


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    if user_id == admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete yourself")
    recipe_service.delete_user(db, user_id)
    return {"message": "User deleted"}


@router.get("/recipes")
def list_recipes(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return recipe_service.get_all_recipes_admin(db)


@router.get("/comments")
def list_comments(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return recipe_service.get_all_comments_admin(db)


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    recipe_service.delete_comment(db, comment_id)
    return {"message": "Comment deleted"}
