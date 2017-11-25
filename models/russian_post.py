# -*- coding: utf-8 -*-
from openerp import _, api, fields, models
PARAMS = [
    ("delivery_method_ids", "active_russian_post.ids"),
    
]


class russian_post_settings(models.TransientModel):
    
    _name="russian.post.settings"
    _inherit = 'res.config.settings'


    
    delivery_method_ids = fields.Many2many('delivery.carrier','rps_delivery_rel','rp_id','delivery_id',string="Delivery Methods")
    
    @api.multi
    def set_params(self):
        self.ensure_one()

        for field_name, key_name in PARAMS:
            value = [x.id for x in getattr(self, field_name)]
            self.env['ir.config_parameter'].set_param(key_name, value)

    @api.multi
    def get_default_params(self):
        res = {}
        for field_name, key_name in PARAMS:
            res[field_name] = self.env['ir.config_parameter'].get_param(key_name, '')
            if res['delivery_method_ids']:
                temp_res=res['delivery_method_ids'].strip('[').strip(']').split(',')
                if temp_res and temp_res[0]:
                    res['delivery_method_ids']=[int(x) for x in temp_res]
                else:
                    res['delivery_method_ids']=[]
        return res      
    
class generate_delivery_form(models.TransientModel):
    _name="russian.post.delivery.form"
    
    delivery_method_ids = fields.Many2many('delivery.carrier','rps_delivery_rel','rp_id','delivery_id',string="Delivery Methods",
                                           domain=lambda self:[('id','in',self.env['russian.post.settings'].get_default_params()['delivery_method_ids'])])

    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {
             'ids': context.get('active_ids', []),
             'model': 'hr.contribution.register',
             'form': self.read(cr, uid, ids, context=context)[0]
        }
#         return self.pool['report'].get_action(
#             cr, uid, [], 'hr_payroll.report_contributionregister', data=datas, context=context
#         )    
    
class stock_picking(models.Model):
    _inherit="stock.picking"
    
    service_delivery_form_id = fields.Many2one('service.delivery.form',string="Service Delivery Form")