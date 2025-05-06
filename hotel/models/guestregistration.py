# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class GuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Hotel Guest Registration List'
    _order = 'checkin_date desc'

    # ⚫ Foreign Key to Guest
    guest_id = fields.Many2one('hotel.guests', string='Guest', required=True)

    # ⚫ Related Fields (Auto display guest details)
    guest_name = fields.Char(string='Guest Name', related='guest_id.name', store=True)
    contactno = fields.Char(string='Contact No.', related='guest_id.contactno', store=True)
    email = fields.Char(string='Email', related='guest_id.email', store=True)

    # ⚫ Check-in and Check-out Dates
    checkin_date = fields.Date("Check-In Date", default=fields.Date.today)
    checkout_date = fields.Date("Check-Out Date")

    # ⚫ Computed Field: Duration of Stay
    stay_duration = fields.Integer(string='Stay Duration (Days)', compute='_compute_duration', store=True)

    # ⚫ Room Assignment
    room_id = fields.Many2one('hotel.rooms', string='Room')

    # ⚫ State field to track reservation status
    state = fields.Selection([
        ('reserved', 'Reserved'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled')
    ], string="State", default='reserved')

    # ⚫ Compute stay duration based on check-in and check-out dates
    @api.depends('checkin_date', 'checkout_date')
    def _compute_duration(self):
        for rec in self:
            if rec.checkin_date and rec.checkout_date:
                rec.stay_duration = (rec.checkout_date - rec.checkin_date).days
            else:
                rec.stay_duration = 0

    # ⚫ Validation: Check for blank dates
    def _validate_dates(self):
        for rec in self:
            if not rec.checkin_date or not rec.checkout_date:
                raise ValidationError("Check-In and Check-Out dates must not be empty.")

    # ⚫ Check Room Conflict using Stored Function
    def _has_schedule_conflict(self, room_id, checkin_date, checkout_date):
        # Execute raw SQL to call the PostgreSQL function
        self.env.cr.execute("""
            SELECT check_room_conflict(%s, %s, %s);
        """, (room_id.id, checkin_date, checkout_date))
        return self.env.cr.fetchone()[0]

    # ⚫ Button Actions for Reservation, Check-in, Check-out, Cancel
    def action_reserve(self):
        for rec in self:
            # Validate check-in and check-out dates
            rec._validate_dates()
            # Check for room scheduling conflicts
            if rec._has_schedule_conflict(rec.room_id, rec.checkin_date, rec.checkout_date):
                raise ValidationError("Schedule conflict detected for the selected room.")
            # Update the state to 'reserved' if no conflict
            rec.state = 'reserved'

    def action_checkin(self):
        for rec in self:
            # Validate check-in and check-out dates
            rec._validate_dates()
            # Check for room scheduling conflicts
            if rec._has_schedule_conflict(rec.room_id, rec.checkin_date, rec.checkout_date):
                raise ValidationError("Cannot check-in: Room is already booked for the selected dates.")
            # Update the state to 'checked_in' if no conflict
            rec.state = 'checked_in'

    def action_checkout(self):
        for rec in self:
            # Update the state to 'checked_out'
            rec.state = 'checked_out'

    def action_cancel(self):
        for rec in self:
            # Update the state to 'cancelled'
            rec.state = 'cancelled'


# Add a check for overlapping bookings
    @api.constrains('checkin_date', 'checkout_date', 'room_id')
    def _check_room_conflict(self):
        for record in self:
            # Ensure the record is not cancelled before checking for conflicts
            if record.state != 'cancelled':
                # Search for existing reservations that overlap with this one
                overlapping_records = self.search([
                    ('room_id', '=', record.room_id.id),
                    ('state', 'in', ['reserved', 'checked_in']),  # Only reserved or checked-in states
                    ('checkout_date', '>', record.checkin_date),
                    ('checkin_date', '<', record.checkout_date)
                ])
                
                # If there are overlapping records, raise an exception
                if overlapping_records:
                    raise ValidationError('Conflict: This room is already booked for the selected dates.')
