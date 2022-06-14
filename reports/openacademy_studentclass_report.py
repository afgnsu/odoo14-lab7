# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models,fields,api


class openacademtstudentclassreport(models.AbstractModel):
    _name = "report.openacademy.studentclass_report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['openacademy.studentclass'].browse(docids)

        res_doc = []
        for line in docs:
            line_doc = []
            for student_line in line.student_line:
                if student_line.student_class == '1':
                    myclass = '一年級'
                elif student_line.student_class == '2':
                    myclass = '二年級'
                elif student_line.student_class == '3':
                    myclass = '三年級'
                if student_line.student_fm == 'M':
                    myfm = '男'
                elif student_line.student_fm == 'F':
                    myfm = '女'

                line_temp = {
                    'student_no': student_line.student_no,
                    'student_name': student_line.student_name,
                    'student_contact': student_line.student_contact,
                    'student_class': myclass,
                    'student_fm': myfm,
                    'student_memo': student_line.student_memo.replace('\n','\\n') if student_line.student_memo else ' ',
                }
                line_doc.append(line_temp)
            temp = {
                'student_class_name': line.student_class_name,
                'student_teacher': line.student_teacher.teacher_name,
                'student_line' : line_doc,
            }
            res_doc.append(temp)

        docargs = {
            'doc_ids': docids,
            'doc_model': 'openacademy.studentclass',
            'docs': res_doc,
        }
        return docargs