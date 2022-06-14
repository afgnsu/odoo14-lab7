# -*- coding: utf-8 -*-
# Author : Peter Wu


import base64
import xlrd
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import sys

XL_CELL_EMPTY = 0
XL_CELL_TEXT = 1
XL_CELL_NUMBER = 2
XL_CELL_DATE = 3
XL_CELL_BOOLEAN = 4
XL_CELL_ERROR = 5
XL_CELL_BLANK = 6


class openacademyscorewizard(models.TransientModel):
    _name = "openacademy.score_import_wizard"

    excel_file = fields.Binary(string=u"Upload CSV File")

    def score_action_import(self):
        if not self.excel_file:
            raise UserError(u"Error!,Not Correct CSV File")
        xls = xlrd.open_workbook(file_contents=base64.decodestring(self.excel_file))
        sheet = xls.sheet_by_index(0)

        nstartrow = 3
        nendrow = sheet.nrows

        if not self.excel_file:
            raise UserError(u"Error!,Not Correct CSV File")
        xls = xlrd.open_workbook(file_contents=base64.decodestring(self.excel_file))
        sheet = xls.sheet_by_index(0)
        myscore_rec = self.env['openacademy.score']
        for row in range(nstartrow - 1, nendrow):

            cell = sheet.cell(row, 0)   # 學年
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                myyear = str(int(cell.value)).strip()
            else:
                myyear = ' '

            cell = sheet.cell(row, 1)   # 學生姓名
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
               myname = cell.value
               myrec = self.env['openacademy.student'].search([('student_name','=',myname)])
               if myrec:
                   myid = myrec.id
               else:
                   myid = 0

            cell = sheet.cell(row, 2)   # 國文成績
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mychinese = cell.value
            else:
                mychinese = 0

            cell = sheet.cell(row, 3)   # 英文成績
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                myenglish = cell.value
            else:
                myenglish = 0

            cell = sheet.cell(row, 4)  # 數學成績
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mymath = cell.value
            else:
                mymath = 0

            if myid > 0 :
                mycount = self.env['openacademy.score'].search_count([('score_year','=',myyear),('score_student','=',myid)])
                if mycount == 0 :
                    myscore_rec.create({'score_year':myyear,'score_student':myid,'score_chinese':mychinese,'score_english':myenglish,'score_math':mymath})
                else:
                    myrec = self.env['openacademy.score'].search([('score_year','=',myyear),('score_student','=',myid)])
                    myrec.write({'score_chinese':mychinese,'score_english':myenglish,'score_math':mymath})


        myviewid = self.env.ref('openacademy.view_openacademy_score_tree')
        return {'view_name': 'openacademyscorewizard',
                'name': (u'openacademy score Data'),
                'views': [[False,'tree'] ],
                'res_model': 'openacademy.score',
                'context': self._context,
                'type': 'ir.actions.act_window',
                'target': 'main',
                'view_id': myviewid.id,
                'flags': {'action_buttons': True},
                'view_mode': 'tree',
                'view_type': 'form'
                }

