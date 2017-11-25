# -*- coding: utf-8 -*-
from openerp import _, api, fields, models


class service_delivery_form(models.Model):
    _name="service.delivery.form"
    
    name = fields.Char('Name')
    
