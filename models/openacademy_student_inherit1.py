# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models, fields, api
from odoo.exceptions import UserError


class openacademystudentinherit1(models.Model):
    _inherit = "openacademy.student"

    student_contact_phone = fields.Char(string="聯絡人電話")
