from marshmallow import Schema, fields


class OrderSchema(Schema):
    id = fields.Int(required=True)
    cc = fields.Str(required=True)
    type = fields.Str(required=True)
    price = fields.Float()
    quantity = fields.Float()


class VolumeSchema(Schema):
    volume = fields.Float()
    total = fields.Float()
