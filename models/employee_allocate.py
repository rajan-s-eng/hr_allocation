from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class EmployeeAllocate(models.Model):
    _name = 'employee.allocate'
    _description = "Employee Allocate"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    staff_requirement_line_ids = fields.One2many('staff.requirements.line', 'staff_request_id', string='Staff Requirement')
    staff_allocation_line_ids = fields.One2many('staff.allocation.line', 'staff_allocation_id', string='Staff Allocate')

    name = fields.Char(string='Reference', readonly=True, index='trigram', default=lambda self: _('New'))
    company_id = fields.Many2one("res.company", string="Requester Company", required=True, default=lambda self: self.env.company, tracking=True)
    requested_user_id = fields.Many2one("res.users", string="Requested By", default=lambda self: self.env.user, tracking=True)
    requeste_date = fields.Datetime(string="Request Date", required=True, default=fields.Datetime.now, tracking=True)
    no_of_days = fields.Char(string="Job Duration", compute="_compute_duration", store=True)
    no_of_hours = fields.Char(string="No. of Hours", compute="_compute_duration", store=True)
    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(string="End Date")
    total = fields.Float(string="Total", compute='_compute_total', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('request_submitted', 'Request Submitted'),
        ('approved', 'Approved'),
        ('allocated', 'Allocated'),
        ('cancelled', 'Cancelled'),
    ], default='draft', readonly=False, string="Status", tracking=True)

    def action_submit(self):
        self.write({'state': 'request_submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_allocate(self):
        self.write({'state': 'allocated'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_set_to_draft(self):
        self.write({'state': 'draft'})

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
                total_minutes = delta.seconds // 60
                hours, minutes = divmod(total_minutes, 60)

                total_hours = days * 24
                
                record.no_of_days = f"{days} Day{'s' if days > 1 else ''}"
                record.no_of_hours = f"{total_hours} Hour{'s' if total_hours > 1 else ''}"
            else:
                record.no_of_days = ''
                record.no_of_hours = ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.allocate') or _("New")
        return super().create(vals_list)

    @api.depends('staff_requirement_line_ids.sub_total')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.staff_requirement_line_ids.mapped('sub_total'))
            print(f"__________________________: {record.total}")
