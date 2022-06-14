# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models, fields, api, _
from odoo.exceptions import UserError


class openacademyexceldownloadfile(models.Model):
    _name = "openacademy.excel_download"
    _order = "create_date desc"

    xls_file = fields.Binary(string="下載檔案")
    xls_file_name = fields.Char(string="下載檔案描述")
    run_desc = fields.Char(string=u"匯出檔描述")
