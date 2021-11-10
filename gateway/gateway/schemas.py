from marshmallow import Schema, fields


class GetVolumeSchema(Schema):
    volume = fields.Float()
    total = fields.Float()
