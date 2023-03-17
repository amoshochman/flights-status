from marshmallow import Schema, fields, ValidationError

class AddressSchema(Schema):
    street = fields.String(required=True)
    line1 = fields.String(required=True)
    line2 = fields.String(required=True)
    country = fields.String(required=True)
    postcode = fields.Integer(required=True)

class OneLineAddressSchema(Schema):
    searchTerm = fields.String(required=True)

class DeliverySchema(Schema):
    userId = fields.Integer(required=True)
    timeslotId = fields.Integer(required=True)