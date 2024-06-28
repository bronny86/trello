from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.comment import Comment, comment_schema, comments_schema
from models.card import Card

# /cards/<int:card_id>/comments
comments_bp = Blueprint("comments", __name__, url_prefix="/<int:card_id>/comments")

# we already get the comments while fetching cards so no need for get comments route here

@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(card_id):
    # get the comment object from the request body
    body_data = request.get_json()
    # fetch the card with that ID - card_id
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # if card exists create an instance of comment model 
    if card:
        comment = Comment(
            message=body_data.get("message"),
            date=date.today(),
            card=card,
            user_id=get_jwt_identity()
        )
    # add and commit the session
        db.session.add(comment)
        db.session.commit()
    # return the created commit
        return comment_schema.dump(comment), 201
    # else if card doesnt exist return error like card does not exist
    else:
        return {"error": f"Card with id {card_id} not found"}, 404
    
   # Delete Comment - /cards/card_id/comments/comment_id

@comments_bp.route("/<int:comment_id>", methods=["DELETE"])

@jwt_required()

def delete_comment(card_id, comment_id):

    # fetch the comment from the db with that id - comment_id

    stmt = db.select(Comment).filter_by(id=comment_id)

    comment = db.session.scalar(stmt)

    # if comment exists

    if comment:

        # delete the comment

        db.session.delete(comment)

        db.session.commit()

        # return some message

        return {"message": f"Comment '{comment.message}' deleted successfully"}

    # else

    else:

        # return an error saying comment does not exist

        return {"error": f"Comment with id {comment_id} not found"}, 404
    
    # editing the comment - /cards/card_id/comments/comment_id
@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_comment(card_id, comment_id):
    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        comment.message = body_data.get("message") or comment.message
        db.session.commit()
        return comment_schema.dump(comment)
    else:
        return {"error": f"Comment with id {comment_id} not found"}, 404