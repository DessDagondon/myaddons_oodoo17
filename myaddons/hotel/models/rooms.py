#-*-coding: utf-8 -*-

#rooms.py

from odoo import models, fields, api

class Rooms (models.Model):
     _name = 'hotel.rooms'
     _description ='Hotel rooms master list' 
     _order="name"

     name =  fields.Char("Room No.")
     description= fields. Char("Room Description")

     roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type")

