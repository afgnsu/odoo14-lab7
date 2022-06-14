# -*- coding: utf-8 -*-
# Author : Peter Wu

from odoo import models, fields, api
from odoo.exceptions import UserError

class openacademyscore(models.Model):
    _name = "openacademy.score"
    _description = "開源學園-學年成績記錄"

    @api.depends('score_chinese', 'score_math', 'score_english')
    def _get_tot(self):
        for rec in self:
            rec.score_total = rec.score_chinese + rec.score_math + rec.score_english


    @api.depends('score_chinese', 'score_math', 'score_english')
    def _get_avg(self):
        for rec in self:
            rec.score_avg = (rec.score_chinese + rec.score_math + rec.score_english) / 3


    score_year = fields.Char(string="學年", required=True)
    score_student = fields.Many2one('openacademy.student', string="學生")
    score_chinese = fields.Float(digits=(5, 1),string="國文分數", default=0)
    score_math = fields.Float(digits=(5, 1),string="數學分數", default=0)
    score_english = fields.Float(digits=(5, 1),string="英文分數", default=0)
    score_total = fields.Float(digits=(6, 1),string="總分", compute=_get_tot)
    score_avg = fields.Float(digits=(5, 1),string="平均", compute=_get_avg)


    def name_get(self):
        result = []
        for rec in self:
            myname = "[%s] %s-%s" % (rec.score_year, rec.score_student.student_no, rec.score_student.student_name)
            result.append((rec.id, myname))
        return result

    @api.model
    def create(self, vals):
        if vals['score_chinese'] < 0 or vals['score_math'] < 0 or vals['score_english'] < 0:
            raise UserError("成績不能是負數")
        res = super(openacademyscore, self).create(vals)
        return res


    def _write(self, vals):
        if vals['score_chinese'] < 0 or vals['score_math'] < 0 or vals['score_english'] < 0:
            raise UserError("成績不能是負數")
        res = super(openacademyscore, self)._write(vals)
        return res


    def unlink(self):
        for rec in self:
            if rec.score_chinese > 0 or rec.score_math > 0 or rec.score_english > 0:
                raise UserError("已有成績,不得刪除")
        res = super(openacademyscore, self).unlink()
        return res


