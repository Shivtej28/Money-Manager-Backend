from unicodedata import category
from fastapi import APIRouter

router = APIRouter(prefix="/api/categeroies", tags=["Categories"])


@router.post("/")
def createt_category():
    return True