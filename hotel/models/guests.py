# -*- coding: utf-8 -*-

# guests.py

from odoo import models, fields, api
from datetime import date

class Guests(models.Model):
    _name = 'hotel.guests'
    _description = 'Hotel Guests Master List'
    _order = 'lastname, firstname, middlename'

    lastname = fields.Char("Last Name")
    firstname = fields.Char("First Name")    
    middlename = fields.Char("Middle Name")        

    address_streetno = fields.Char("Address /Street & No.")
    address_area = fields.Char("Address /Bldg/Area/Brgy")
    address_city = fields.Char("Address /City/Town")                        
    address_province = fields.Char("Address /Province/State")
    zipcode = fields.Char("Zip Code")
    contactno = fields.Char("Contact No.")
    email = fields.Char("Email")
    gender = fields.Selection([
        ('FEMALE', 'Female'),
        ('MALE', 'Male')
    ], string="Gender")
    birthdate = fields.Date("Birthdate")
    photo = fields.Image("Guest Photo") 

    name = fields.Char(string='Guest Name', compute='_compute_name')
    age = fields.Integer(string='Age', compute='_compute_age')

    @api.depends('lastname', 'firstname', 'middlename')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.lastname}, {rec.firstname} {rec.middlename}"

    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            if rec.birthdate:
                today = date.today()
                born = rec.birthdate
                rec.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                rec.age = 0
