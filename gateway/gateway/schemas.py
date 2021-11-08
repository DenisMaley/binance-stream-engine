from marshmallow import Schema, fields


class VolumeSchema(Schema):
    amount = fields.Int(required=True)
