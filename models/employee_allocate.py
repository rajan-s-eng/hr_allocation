from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class EmployeeAllocate(models.Model):
    _name = 'employee.allocate'
    _description = "Employee Allocate"

    staff_requirement_line_ids = fields.One2many('staff.requirements.line', 'staff_request_id', string='Staff Requirement')
    staff_allocation_line_ids = fields.One2many('staff.allocation.line', 'staff_allocation_id', string='Staff Allocate')

    name = fields.Char(string='Reference', readonly=True, index='trigram', default=lambda self: _('New'))
    company_id = fields.Many2one("res.company", string="Requester Company", required=True)
    requested_user_id = fields.Many2one("res.users", string="Request By")
    requeste_date = fields.Datetime(string="Request Date", required=True, default=fields.Datetime.now)
    job_duration = fields.Char(string="Job Duration", compute="_compute_duration")
    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(string="End Date")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('request_submitted', 'Request Submitted'),
        ('approved', 'Approved'),
        ('allocated', 'Allocated'),
        ('cancelled', 'Cancelled'),
    ], default='draft', readonly=False, string="Status")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_('Start date must be earlier than or equal to the end date.'))

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                days = delta.days
                record.job_duration = f"{days} day{'s' if days > 1 else ''}"
            else:
                record.job_duration = ""

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.allocate') or _("New")
        return super().create(vals_list)