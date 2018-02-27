# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class DynamicReportname(models.Model):

    _name = 'dynamic.reportname'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', 'Model', required=True)
    field_id = fields.Many2one('ir.model.fields', string='Field name', required=True)

    _sql_constraints = [
        ('model_id_unique', 'UNIQUE (model_id)', 'You can not have same model twice !')
    ]
