from odoo import models, fields, api

class StaffRequirementsLine(models.Model):
    _name = 'staff.requirements.line'
    _description = 'Staff Requirment'

    staff_request_id = fields.Many2one('employee.allocate', string="staff allocation")
    job_possition_id = fields.Many2one('hr.department', string="Job Position", required=True)
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    sub_total = fields.Float(string="Sub Total")