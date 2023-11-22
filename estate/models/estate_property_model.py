# noinspection PyUnresolvedReferences
from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta
# noinspection PyUnresolvedReferences
from odoo.tools import float_compare, float_is_zero


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"
    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be strictly positive.')
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text(default="When duplicated, status and date are not copied!")
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Float(compute="_compute_total", string="Total Area (sqm)")
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, default='new')

    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user, copy=False)

    tag_ids = fields.Many2many("estate.property.tag")

    offer_ids = fields.One2many("estate.property.offer", "property_id")

    best_price = fields.Float(compute="_compute_max")

    # computing total area from adding living area + garden area
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # extracting maximum price from offers
    @api.depends("offer_ids.price")
    def _compute_max(self):
        for record in self:
            if record.offer_ids:  # Check if offer_ids is not empty
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    # changing garden_area and garden_orientation based on garden field.
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            # Set default values when 'garden' is True
            self.garden_area = 10.0
            self.garden_orientation = 'north'
        else:
            # Clear values when 'garden' is False
            self.garden_area = 0.0
            self.garden_orientation = False

    # Functionality for sold/cancel button on the form view
    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'
        return True

    def action_mark_as_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("A cancelled property cannot be marked as sold.")
            record.state = 'sold'
        return True

    # Python constraints for comparing the expected price and selling price accordingly
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            # Skip the check if the selling price is zero
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            # Check if the expected price is zero (not set) and skip the constraint in this case
            if float_is_zero(record.expected_price, precision_digits=2):
                continue

            # Check if the selling price is less than 90% of the expected price
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1:
                raise exceptions.ValidationError("Selling price cannot be lower than 90% of the expected price.")









