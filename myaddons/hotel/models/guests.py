# -*- coding: utf-8 -*-

# guests.py

from odoo import models, fields, api
from datetime import date

class Guests(models.Model):
    _name = 'hotel.guests'
    _description = 'Hotel Guests Master List'
    _order = 'lastname, firstname, middlename'


    lastname = fields.Char("Lastname", required=True)
    firstname = fields.Char("Firstname", required=True)
    middlename = fields.Char("Middlename")
    
    address_streetno = fields.Char("Address/ Street & No.")
    address_area = fields.Char("Address / Area,Unit&Bldg,Brgy")
    address_city = fields.Char("Address / City/Town")
    address_province = fields.Char("Address / Province/State")
    zipcode = fields.Char("ZIP Code")
    
    contactno = fields.Char("Contact No.")
    email = fields.Char("Email")
    
    gender = fields.Selection([('FEMALE', 'Female'), ('MALE', 'Male')], string="Gender")
    birthdate = fields.Date("Birthdate")
    photo = fields.Image("Guest Photo")

    name = fields.Char(string="Complete Name", compute="_compute_name", store=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    @api.depends('lastname', 'firstname', 'middlename')
    def _compute_name(self):
        for rec in self:
            names = filter(None, [rec.lastname, rec.firstname, rec.middlename])
            rec.name = ', '.join([rec.lastname or '', rec.firstname or '']) + (' ' + rec.middlename if rec.middlename else '')

    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            if rec.birthdate:
                today = date.today()
                rec.age = today.year - rec.birthdate.year - ((today.month, today.day) < (rec.birthdate.month, rec.birthdate.day))
            else:
                rec.age = 0
