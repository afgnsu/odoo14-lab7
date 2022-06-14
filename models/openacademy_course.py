# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models, fields, api
from odoo.exceptions import UserError


class OpenAcademyCourse(models.Model):
    _name = "openacademy.course"
    _description = "開源學園-課程主檔"

    course_no = fields.Char(string="課程編號", required=True)
    course_name = fields.Char(string="課程名稱", required=True)
    course_type = fields.Selection([('1', '必修'), ('2', '選修')], string="課程型態", required=True)

    def name_get(self):
        result = []
        for record in self:
            if record.course_type == '1':
                myclass = '必修'
            elif record.course_type == '2':
                myclass = '選修'

            myname = "[%s]%s-%s" % (record.course_no, record.course_name, myclass)
            result.append((record.id, myname))
        return result
