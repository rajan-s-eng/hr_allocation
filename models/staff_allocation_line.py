from odoo import models, fields, api

class StaffAllocationLine(models.Model):
    _name = 'staff.allocation.line'
    _description = 'Staff Allocate'

    staff_allocation_id = fields.Many2one('employee.allocate', string="staff Allocation")

    job_possition_id = fields.Many2one('hr.department', string="Job Position", required=True)
    employee = fields.Char(string="Employee", required=True)
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    no_of_days = fields.Char(string="No Of Days")