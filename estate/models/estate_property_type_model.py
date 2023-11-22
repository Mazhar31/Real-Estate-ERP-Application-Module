# noinspection PyUnresolvedReferences
from odoo import fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "Model for Real-Estate Property Types"
    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]

    name = fields.Char(required=True)

