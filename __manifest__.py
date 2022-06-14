# -*- coding: utf-8 -*-
# Author : Peter Wu

{
    'name': 'Openacademy',
    'version': '14.0',
    'sequence': 100,
    'category': 'Student Academy Score system',
    'website': 'https://www.alldo.com.tw',
    'summary': 'Student Academy Score system',
    'description': """
     開源學園-學生成績系統
     """,
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/openacademy_course.xml',
        'views/openacademy_student.xml',
        'views/openacademy_teacher.xml',
        'views/openacademy_class.xml',
        'views/openacademy_menu.xml',
    ],

    'installable': True,
    'application': True,
}
