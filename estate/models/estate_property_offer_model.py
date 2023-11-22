# noinspection PyUnresolvedReferences
from odoo import api, fields, models, exceptions
from datetime import timedelta


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Model for Real-Estate Property Offers"
    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    create_date = fields.Datetime(readonly=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.date_deadline = (create_date + timedelta(days=offer.validity)).date()

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                # Fallback in case create_date or date_deadline is not set
                offer.create_date = fields.Datetime.now()
                offer.validity = 7  # Default validity

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == 'cancelled':
                raise exceptions.UserError("Cannot accept an offer for a cancelled property.")

            # Set the buyer and selling price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

            # Update offer status to 'accepted'
            offer.status = 'accepted'
            offer.property_id.state = 'sold'

            # Mark other offers for the same property as 'refused'
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id),
            ])
            other_offers.write({'status': 'refused'})

        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True

