# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models, fields, api, _
from odoo.exceptions import UserError
from io import BytesIO
import base64
from odoo.exceptions import UserError


class openacademystudentexportwizard(models.TransientModel):
    _name = "openacademy.student_export_wizard"

    student_name = fields.Char(string="學生姓名")
    student_class = fields.Selection([('1', '一年級'), ('2', '二年級'), ('3', '三年級')], string="年級")
    student_fm = fields.Selection([('M', '男'), ('F', '女')], string="性別")

    def student_export_list(self):
        domain = []  # ==> ['|',('','=',''),('','=','')]
        if self.student_name:
            domain.append(('student_name', 'ilike', self.student_name))
        if self.student_class:
            domain.append(('student_class', '=', self.student_class))
        if self.student_fm:
            domain.append(('student_fm', '=', self.student_fm))

        if not domain:
            domain = [(1, '=', 1)]

        myrec = self.env['openacademy.student'].search(domain)
        if not self.student_name and not self.student_class and not self.student_fm:
            myexportname = "全校"
        else:

            myexportname = "(%s-%s)-%s" % (
            self.student_class, self.student_fm, self.student_name if self.student_name else ' ')
        myxlsfilename = _(u"學生名單-%s.xls" % myexportname)
        myrundesc = _(u"學生名單-%s.xls" % myexportname)

        mytitle = "學生名單列表: %s" % (myexportname)
        import xlwt
        user_tz = self.env.user.tz
        borders = xlwt.Borders()  # Create Borders
        borders.left = xlwt.Borders.THIN  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x40
        borders.right_colour = 0x40
        borders.top_colour = 0x40
        borders.bottom_colour = 0x40

        center_alignment = xlwt.Alignment()  # Create Alignment
        center_alignment.horz = xlwt.Alignment.HORZ_CENTER
        center_alignment.vert = xlwt.Alignment.VERT_CENTER

        title_font = xlwt.Font()  # Create the Font
        title_font.height = 0x00C8 * 3

        title_style = xlwt.XFStyle()  # Create Style
        title_style.borders = borders  # Add Borders to Style
        title_style.alignment = center_alignment
        title_style.font = title_font
        # myxlsfilename = rack.name +'.xls'

        wb = xlwt.Workbook(encoding='utf-8')
        ws1 = wb.add_sheet(u'學生名單列表')

        content_font = xlwt.Font()
        content_font.height = 0x00C8 * 1
        content_style = xlwt.XFStyle()  # Create Style

        content_style.borders = borders  # Add Borders to Style

        content_alignment = xlwt.Alignment()  # Create Alignment
        content_alignment.horz = xlwt.Alignment.HORZ_LEFT
        content_alignment.vert = xlwt.Alignment.VERT_CENTER
        content_style.alignment = content_alignment
        content_style.alignment.wrap = 1
        content_style.font = content_font

        # Openacademy Student
        row = 1

        ws1.write(row, 4, (mytitle if mytitle else ''), title_style)
        row += 3
        titles1 = [
            "學號",
            "學生姓名",
            "學生聯絡人",
            "班別",
            "性別",
            "備註",
        ]
        col = 0
        for title in titles1:
            ws1.write(row, col, title, content_style)
            col += 1
            ws1.row(row).height = 1000
            ws1.col(0).width = 3600  # student no
            ws1.col(1).width = 3600  # student name
            ws1.col(2).width = 3600  # contact name
            ws1.col(3).width = 3600  # class
            ws1.col(4).width = 1800  # fm
            ws1.col(5).width = 7200  # memo

        for line in myrec:
            s1 = line.student_no
            s2 = line.student_name
            s3 = line.student_contact
            s4 = line.student_class
            if s4 == '1':
                myclass = '一年級'
            elif s4 == '2':
                myclass = '二年級'
            elif s4 == '3':
                myclass = '三年級'
            s5 = line.student_fm
            if s5 == 'F':
                mysex = '女生'
            else:
                mysex = '男生'
            s6 = line.student_memo

            # print(s1,s2,s3,s4,s5,s6,s7,s8)
            row += 1

            ws1.write(row, 0, (s1 if s1 else ' '), content_style)
            ws1.write(row, 1, (s2 if s2 else ' '), content_style)
            ws1.write(row, 2, (s3 if s3 else ' '), content_style)
            ws1.write(row, 3, (myclass if s4 else ' '), content_style)
            ws1.write(row, 4, (mysex if s5 else ' '), content_style)
            ws1.write(row, 5, (s6 if s6 else ' '), content_style)

        output = BytesIO()

        wb.save(output)
        myxlsfile = base64.standard_b64encode(output.getvalue())
        myrec = self.env['openacademy.excel_download']
        myrec.create({'xls_file': myxlsfile, 'xls_file_name': myxlsfilename, 'run_desc': myrundesc})
        myviewid = self.env.ref('openacademy.openacademy_excel_download_tree')

        return {
            'view_name': 'openacademyexcelwizard',
            'name': (u'Openacademy Student Records Export'),
            'type': 'ir.actions.act_window',
            'res_model': 'openacademy.excel_download',
            'view_id': myviewid.id,
            'flags': {'action_buttons': False},
            'view_type': 'form',
            'view_mode': 'tree',
            'target': 'main'}
