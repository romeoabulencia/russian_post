# -*- coding: utf-8 -*-
from openerp import _, api, fields, models
from openerp.osv import osv

class delivery_carrier(models.Model):
    _inherit="delivery.carrier"

class russian_post_settings(osv.osv_memory):
    
    _name="russian.post.settings"
    _inherit = 'res.config.settings'

    
    delivery_method_ids = fields.Many2many('delivery.carrier','rps_delivery_rel','rp_id','delivery_id',string="Delivery Methods")