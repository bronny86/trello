from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__="cards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.Date) # date of creation
    status = db.Column(db.String)
    priority = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="cards")
    comments = db.relationship("Comment", back_populates="card", cascade="all, delete")

class CardSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    comments = fields.List(fields.Nested("CommentSchema", exclude=["card"]))

    class Meta:
        fields = ("id", "title", "description", "date", "status", "priority", "user", "comments")
        ordered = True

card_schema = CardSchema()
cards_schema = CardSchema(many=True)