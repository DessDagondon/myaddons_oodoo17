# -*- coding: utf-8 -*-

# roomtypes.py

from odoo import models, fields, api

class roomtypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'Hotel Roomtype MasterList'
    _order="name"

    name = fields.Char("Roomtype Name")
    description = fields.Char("Roomtype Description")

    photo_bed = fields.Image("Bed Photo")
    photo_restroom = fields.Image("Restroom Photo")

    room_ids = fields.One2many('hotel.rooms', 'roomtype_id', string='Rooms')
    dailycharges_ids=fields.One2many('hotel.dailycharges','roomtype_id', string='Daily Charges')

class dailycharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'hotel roomtype daily charges list'
    
    charge_id = fields.Many2one('hotel.charges',string="Charge Title")
    amount = fields.Float("Daily Amount", digits=(10,2), options={'always_reload': True})
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Roomtype")    
