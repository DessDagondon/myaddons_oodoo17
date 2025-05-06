# -*- coding: utf-8 -*-

# charges.py

from odoo import models, fields, api

class Charges(models.Model):
    _name = 'hotel.charges'
    _description = 'Hotel Charges Master List'
    _order="name"

    name = fields.Char("Charge Name")
    description = fields.Char("Charge Description")
