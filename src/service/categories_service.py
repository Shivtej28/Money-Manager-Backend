
from re import sub
from fastapi import status
from ..scehmas.request_model import CreateCategory, UpdateCategory, CategoryResponse, UpdateSubCategory, Response
from sqlalchemy.orm import Session
from ..models.data_model import Category, Subcategory
# from ..utils.response import Response
from sqlalchemy import and_


class CategoryService:
    def __init__(self) -> None:
        pass

    def create_category(self, category: CreateCategory, db: Session, user):
        user_id = user.get("sub")
        existing_category = db.query(Category).filter(and_(
            Category.user_id == user_id, Category.category_name == category.category_name, Category.type_of == category.type_of)).first()
        if existing_category:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Category exisited with same details", result=None)

        db_category = Category(
            user_id=user_id, category_name=category.category_name, type_of=category.type_of)
        db.add(db_category)
        db.commit()
        for sub_category in category.sub_categories:
            db_sub_catgeory = Subcategory(category_id=db_category.category_id, user_id=user_id,
                                          subcategory_name=sub_category, type_of=db_category.type_of)
            db.add(db_sub_catgeory)

        db.commit()
        db.refresh(db_category)
        return Response(status_code=status.HTTP_201_CREATED, is_success=True, message="Category Created Successfully", result=None)

    def get_all_categories(self, db: Session, user):
        user_id = user.get("sub")
        categories = db.query(Category).filter(
            Category.user_id == user_id).all()
        result = []
        for category in categories:
            to_add_sub_category = [UpdateSubCategory(
                id=sub.subcategory_id, subcategory_name=sub.subcategory_name, type_of=sub.type_of) for sub in category.subcategories]

            print(to_add_sub_category)
            to_add = CategoryResponse(category_id=category.category_id, category_name=category.category_name,
                                      type_of=category.type_of, subcategories=to_add_sub_category)
            result.append(to_add)
        if categories is None:
            Response(status_code=status.HTTP_200_OK, is_success=False,
                     message="Please Add Category", result=None)
        return Response(status_code=status.HTTP_200_OK, is_success=True, message="Category Created Successfully", result=result)

    def update_categories(self, id, db: Session, user, category: UpdateCategory):
        user_id = user.get("sub")
        db_category = db.query(Category).filter(
            Category.category_id == id).first()

        if db_category is None:
            Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False,
                     message="Category with ID dodes not exist", result=None)

        db_category.category_name = category.category_name
        db_category.type_of = category.type_of
        db.commit()
        for sub_category in category.sub_category:
            db_subcategory = db.query(Subcategory).filter(
                Subcategory.subcategory_id == sub_category.id).first()
            if db_subcategory:
                db_subcategory.subcategory_name = sub_category.subcategory_name
                db_subcategory.type_of = sub_category.type_of
            else:
                db_sub_catgeory = Subcategory(category_id=db_category.category_id, user_id=user_id,
                                              subcategory_name=sub_category.subcategory_name, type_of=sub_category.type_of)
                db.add(db_sub_catgeory)
            
        db.commit()
        db.refresh(db_category)
        return Response(status_code=status.HTTP_201_CREATED, is_success=True, message="Category Created Successfully", result=None)


category_service = CategoryService()
