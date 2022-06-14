# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models, fields, api
from odoo.exceptions import UserError


class openacademyrespartnerinherit(models.Model):
    _inherit = "res.partner"

    fax = fields.Char(string="傳真")

    @api.model
    def create(self, vals):
        if 'fax' in vals and not vals['fax']:
            vals['fax'] = '123456789'
        res = super(openacademyrespartnerinherit, self).create(vals)

        return res
