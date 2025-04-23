from odoo import models, fields, api

class StaffRequirementsLine(models.Model):
    _name = 'staff.requirements.line'
    _description = 'Staff Requirment'

    staff_request_id = fields.Many2one('employee.allocate', string="staff allocation")
    job_position_id = fields.Many2one('hr.job', string="Job Position", required=True)
    name = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity", default=1.0)
    unit_price = fields.Float(string="Unit Price")
    sub_total = fields.Float(string="Sub Total", compute='_compute_sub_total', store=True)

    @api.onchange('job_position_id')
    def onchange_job_position_id(self):
        for rec in self.filtered('job_position_id'):
            rec.name = rec.job_position_id.display_name

    @api.depends('quantity', 'unit_price')
    def _compute_sub_total(self):
        for rec in self:
            rec.sub_total = rec.quantity * rec.unit_price
