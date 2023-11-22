# noinspection PyUnresolvedReferences
from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Model for Real-Estate Property Tags"
    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.')
    ]

    name = fields.Char(required=True)

