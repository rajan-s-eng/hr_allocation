from odoo import models, fields, api

class StaffAllocationLine(models.Model):
    _name = 'staff.allocation.line'
    _description = 'Staff Allocate'

    staff_allocation_id = fields.Many2one('employee.allocate', string="staff Allocation")

    job_position_id = fields.Many2one('hr.job', string="Job Position", required=True)
    employee_ids = fields.Many2many('hr.employee', 'emp_staff_allocation_rel', 'staff_allocation_id', 'employee_id', string="Employee", required=True)
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    no_of_days = fields.Char(string="No of Days", compute="_compute_duration")
    no_of_hours = fields.Char(string="No of Hours", compute="_compute_duration")

    @api.onchange('job_position_id')
    def onchange_job_position_id(self):
        for rec in self.filtered('job_position_id'):
            rec.start_date = rec.staff_allocation_id.start_date
            rec.end_date = rec.staff_allocation_id.end_date

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                days = delta.days

                total_hours = days * 24

                record.no_of_days = f"{days} Day{'s' if days > 1 else ''}"
                record.no_of_hours = f"{total_hours} Hour{'s' if total_hours > 1 else ''}"
            else:
                record.no_of_days = ""
                record.no_of_hours = ""
