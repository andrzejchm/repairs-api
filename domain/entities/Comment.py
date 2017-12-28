from marshmallow import Schema, fields, post_load


class Comment:
    def __init__(self, id, repair_id, contents, date, username):
        self.id = id
        self.repair_id = repair_id
        self.contents = contents
        self.date = date
        self.username = username


class CommentSchema(Schema):
    id = fields.Integer(required=True, load_from="id", dump_to="id")
    repair_id = fields.Integer(required=True, load_from="repair_id", dump_to="repair_id")
    contents = fields.Str(required=True, load_from="contents", dump_to="contents")
    date = fields.Integer(required=True, load_from="date", dump_to="date")
    username = fields.Str(required=True, load_from="username", dump_to="username")

    @post_load
    def make_comment(self, data):
        return Comment(**data)


class PostCommentSchema(Schema):
    contents = fields.Str(required=True, load_from="contents", dump_to="contents")
    date = fields.Integer(required=True, load_from="date", dump_to="date")
    username = fields.Str(required=True, load_from="username", dump_to="username")

    @post_load
    def make_comment(self, data):
        return Comment(id=None, repair_id=None, **data)
