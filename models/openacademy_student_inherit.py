# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models, fields, api
from odoo.exceptions import UserError


class openacademystudentinherit(models.Model):
    _inherit = "openacademy.student"

    course_ids = fields.Many2many('openacademy.course', 'openacademy_student_course_rel', 'student_id', 'course_id',
                                  string="選課內容")
