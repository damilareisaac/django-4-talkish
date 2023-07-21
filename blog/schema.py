from marshmallow import Schema, fields, validate
from .models import Post
from django.contrib.auth.models import User


class UserSchema(Schema):
    username = fields.String(required=True)


class PostSchema(Schema):
    title = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=200,
        ),
    )
    slug = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=200,
        ),
    )
    body = fields.String(
        required=True,
        validate=validate.Length(
            min=100,
            max=20000,
        ),
    )
    publish = fields.DateTime()
    created = fields.DateTime()
    updated = fields.DateTime()
    status = fields.String(
        required=True,
        validate=validate.Length(min=3, max=200),
    )

    author = fields.Method(serialize="get_authors", deserialize="load_authors")

    def get_authors(self, article):
        return UserSchema().dump(article.regions.all(), many=True)

    def load_authors(self, users):
        return [
            User.objects.get_or_create(
                id=user.pop("id", None),
                defaults=user,
            )[0]
            for user in users
        ]
