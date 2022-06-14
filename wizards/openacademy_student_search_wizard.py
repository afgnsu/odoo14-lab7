# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models, fields, api
from odoo.exceptions import UserError


class openacademystudentsearchwizard(models.TransientModel):
    _name = "openacademy.student_search_wizard"

    student_name = fields.Char(string="學生姓名")
    student_class = fields.Selection([('1', '一年級'), ('2', '二年級'), ('3', '三年級')], string="年級")
    student_fm = fields.Selection([('M', '男'), ('F', '女')], string="性別")

    def run_student_search(self):
        domain = []  # ==> ['|',('','=',''),('','=','')]
        if self.student_name:
            domain.append(('student_name', 'ilike', self.student_name))
        if self.student_class:
            domain.append(('student_class', '=', self.student_class))
        if self.student_fm:
            domain.append(('student_fm', '=', self.student_fm))

        if not domain:
            domain = [(1, '=', 1)]

        myviewid = self.env.ref('openacademy.view_openacademy_student_tree')

        return {'view_name': 'openacademystudentwizard',
                'name': (u'openacademy student Data'),
                'views': [[False, 'tree'], [False, 'form']],
                'res_model': 'openacademy.student',
                'context': self._context,
                'type': 'ir.actions.act_window',
                'view_id': myviewid.id,
                'target': 'main',
                'domain': domain,
                'flags': {'action_buttons': True},
                'view_mode': 'form',
                'view_type': 'form'
                }
