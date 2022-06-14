# -*- coding: utf-8 -*-
# Author : Peter Wu

from odoo import models, fields, api
from odoo.exceptions import UserError


class openacademyteacher(models.Model):
    _name = "openacademy.teacher"
    _description = "開源學園-教職主檔"

    teacher_no = fields.Char(string="教職編號")
    teacher_name = fields.Char(string="教員姓名")


    def name_get(self):
        result = []
        for record in self:
            myname = "[%s]%s" % (record.teacher_no, record.teacher_name)
            result.append((record.id, myname))
        return result


class openacademyclass(models.Model):
    _name = "openacademy.studentclass"
    _description = "開源學園-班級-導師主檔"

    student_class_name = fields.Char(string="班級")
    student_teacher = fields.Many2one('openacademy.teacher', string="班導")


    def name_get(self):
        result = []
        for record in self:
            myname = "[%s]%s" % (record.student_class_name, record.student_teacher.teacher_name)
            result.append((record.id, myname))
        return result
