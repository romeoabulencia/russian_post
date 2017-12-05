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
#         datas = {
#              'ids': context.get('active_ids', []),
#              'model': 'hr.contribution.register',
#              'form': self.read(cr, uid, ids, context=context)[0]
#         }
#         return self.pool['report'].get_action(
#             cr, uid, [], 'hr_payroll.report_contributionregister', data=datas, context=context
#         )
        base_params={
            'pdf.F7':{
                "type_blank":' ',
                "from_surname":' ',
                "from_name":' ',
                "from_city":' ',
                "from_street":' ',
                "from_build":' ',
                "from_zip":' ',
                "whom_surname":' ',
                "whom_name":' ',
                "whom_city":' ',
                "whom_street":' ',
                "whom_build":' ',
                "whom_zip":' ',
                "declared_value":' ',
                "COD_amount":' ',
                "tracking_number":' ',
            
            },
            'pdf.F113F117':{
                'from_surname':' ',
                'from_patronymic':' ',
                'from_city':' ',
                'from_street':' ',
                'from_zip':' ',
                'whom_surname':' ',
                'whom_patronymic':' ',
                'whom_city':' ',
                'whom_street':' ',
                'whom_zip':' ',
                'declared_value_num':' ',
                'COD_amount_num':' ',
                'document':' ',
                'document_serial':' ',
                'document_number':' ',
                'document_day':' ',
                'document_year':' ',
                'document_issued_by':' ',
            
            },
            'pdf.F112':{
                'from_surname':' ',
                'from_name':' ',
                'from_birthday':' ',
                'from_region':' ',
                'from_city':' ',
                'from_street':' ',
                'from_build':' ',
                'from_appartment':' ',
                'from_zip':' ',
                'whom_name':' ',
                'who_region':' ',
                'whom_city':' ',
                'whom_street':' ',
                'whom_build':' ',
                'whom_appartment':' ',
                'whom_zip':' ',
                'sum_num':' ',
                'inn':' ',
                'kor_account':' ',
                'current_account':' ',
                'bik':' ',
                'bank_name':' ',
                'document':' ',
                'document_serial':' ',
                'document_number':' ',
                'document_day':' ',
                'document_year':' ',
                'document_issued_by':' ',
                'unit_code':' ',
                'message_part1':' ',
                'message_part2':' ',
                'barcode':' ',
                'to_phone':' ',
                'from_phone':' ',
                'one':' ',
                'two':' ',
                'three':' ',
            
            },
            'pdf.F112EK':{
                'to_zip':' ',
                'to_type':' ',
                'to_name':' ',
                'to_phone':' ',
                'from_zip':' ',
                'from_region':' ',
                'from_city':' ',
                'from_surname':' ',
                'from_name':' ',
                'from_street':' ',
                'from_build':' ',
                'from_appartment':' ',
                'sum_num':' ',
                'barcode':' ',
                'message':' ',
                'cod':' ',
            
            },
            'pdf.F113':{
                'from_surname':' ',
                'from_name':' ',
                'from_region':' ',
                'from_city':' ',
                'from_street':' ',
                'from_build':' ',
                'from_zip':' ',
                'whom_name':' ',
                'whom_city':' ',
                'whom_street':' ',
                'whom_zip':' ',
                'sum_num':' ',
                'inn':' ',
                'kor_account':' ',
                'current_account':' ',
                'bik':' ',
                'bank_name':' ',
                'barcode':' ',
            
            },
            'pdf.F107':{
                'whom':' ',
                'whom_country':' ',
                'whom_city':' ',
                'investment':' ',
                'object':' ',
                'name':' ',
                'count':' ',
                'price':' ',
            
            },
            'pdf.F116':{
                'from_surname':' ',
                'from_country':' ',
                'from_city':' ',
                'from_zip':' ',
                'whom':' ',
                'whom_country':' ',
                'whom_city':' ',
                'whom_street':' ',
                'whom_zip':' ',
                'document':' ',
                'document_serial':' ',
                'document_number':' ',
                'document_day':' ',
                'document_year':' ',
                'document_issued_by':' ',
                'declared_value':' ',
                'COD_amount':' ',
                'tracking_number':' ',
            
            },
            'pdf.CN23':{
                'from_surname':' ',
                'from_country':' ',
                'from_city':' ',
                'from_street':' ',
                'from_zip':' ',
                'whom_surname':' ',
                'whom_country':' ',
                'whom_city':' ',
                'whom_street':' ',
                'whom_zip':' ',
                'object':' ',
                'name':' ',
                'count':' ',
                'brut':' ',
                'price':' ',
            
            },
            'pdf.F103':{
                'list_num':' ',
                'send_date':' ',
                'mail_type':' ',
                'sendr':' ',
                'email':' ',
                'index_from':' ',
                'mail_count':' ',
                'Recipientdetails:':' ',
                'rcpn':' ',
                'index_to':' ',
                'region_to':' ',
                'place_to':' ',
                'street_to':' ',
                'house_to':' ',
                'area_to':' ',
                'location_to':' ',
                'letter_to':' ',
                'slash_to':' ',
                'corpus_to':' ',
                'building_to':' ',
                'room_to':' ',
                'barcode':' ',
                'tel_address':' ',
                'mail_ctg':' ',
                'mass':' ',
                'value':' ',
                'payment':' ',
                'comment':' ',
            
            },
            'pdf.f7':{
                'MailType':' ',
                'MailCtg':' ',
                'PostMark':' ',
                'SNDR':' ',
                'RCPN':' ',
                'Mass':' ',
                'Payment':' ',
                'Value':' ',
                'from_phone':' ',
                'to_phone':' ',
                'SMSNoticeS':' ',
                'SMSNoticeS':' ',
                'street_from':' ',
                'house_from':' ',
                'letter_from':' ',
                'slash_from':' ',
                'corpus_from':' ',
                'building_from':' ',
                'room_from':' ',
                'place_from':' ',
                'area_from':' ',
                'region_from':' ',
                'index_from':' ',
                'street_to':' ',
                'house_to':' ',
                'letter_to':' ',
                'slash_to':' ',
                'corpus_to':' ',
                'building_to':' ',
                'room_to':' ',
                'place_to':' ',
                'area_to':' ',
                'region_to':' ',
                'index_to':' ',
            
            },
            'pdf.CP71':{
                'declared_val_numeric':' ',
                'to_surname':' ',
                'to_street':' ',
                'to_zip':' ',
                'to_country':' ',
                'from_surname':' ',
                'from_city':' ',
                'from_street':' ',
                'from_zip':' ',
            
            },
            'pdf.emspost':{
                'SNDR':' ',
                'RCPN':' ',
                'from_phone':' ',
                'to_phone':' ',
                'street_from':' ',
                'house_from':' ',
                'place_from':' ',
                'area_from':' ',
                'index_from':' ',
                'region_from':' ',
                'street_to':' ',
                'house_to':' ',
                'place_to':' ',
                'area_to':' ',
                'index_to':' ',
                'region_to':' ',
                'SenderName':' ',
                'RecipientName':' ',
                'Description':' ',
                'AgreementNo':' ',
                'MailCtg':' ',
                'Payment':' ',
                'Value':' ',
            
            },
            'http://beta.pbrf.ru/v1/blank/pimpay/':{
                'sndr':' ',
                'street_from':' ',
                'clients':' ',
                'shops':' ',
                'type':' ',
                'house_from':' ',
                'room_from':' ',
                'place_from':' ',
                'region_from':' ',
                'index_from':' ',
                'sum_num':' ',
                'message':' ',
            
            },
            'pdf.PrintAddress':{
                'from_name':' ',
                'from_adress':' ',
                'from_zip':' ',
                'to':' ',
                'count_copy':' ',
            
            },
            
            
            }
        return
    
class stock_picking(models.Model):
    _inherit="stock.picking"
    
    service_delivery_form_id = fields.Many2one('service.delivery.form',string="Service Delivery Form")