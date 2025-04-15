
# -*- coding: utf-8 -*-

#roomtypes.py

from odoo import models, fields, api

class Roomtypes (models.Model):
    _name = 'hotel.roomtypes'
    _description = 'Hotel Room Types Master List'

    name = fields.Char("Roomtype Name")
    description = fields.Char("Roomtype Description")
    
    photo_bed = fields. Image("Bed Photo") 
    photo_restroom = fields. Image("Restroom Photo")
    
    room_id = fields.One2many('hotel.rooms', 'roomtype_id', string='Rooms')

    # New fields for daily charge and additional charges
    daily_charge = fields.Float("Daily Charge")
    additional_charges = fields.Float("Additional Charges")

    #photo_bed = fields.Image("Bed Photo,attachment=True)
    #photo_restroom =fields.Image("Restroom Photo",attachments=True)