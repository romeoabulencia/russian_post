# -*- coding: utf-8 -*-
from openerp import _, api, fields, models
PARAMS = [
    ("delivery_method_ids", "active_russian_post.ids"),
    ('access_token','russian_post_access_token'),
    
]


class russian_post_settings(models.TransientModel):
    
    _name="russian.post.settings"
    _inherit = 'res.config.settings'


#     delivery_method_ids = fields.Many2many('delivery.carrier','rps_delivery_rel','rp_id','delivery_id',string="Delivery Methods")
    delivery_method_ids = fields.Many2many('service.delivery.form','rps_delivery_form_setting_rel','rp_id','delivery_id',string="Delivery Methods")
    access_token = fields.Char(string="Access Token")
    
    @api.multi
    def set_params(self):
        self.ensure_one()

        for field_name, key_name in PARAMS:
            try:
                value = [x.id for x in getattr(self, field_name)]
            except:
                value = getattr(self, field_name) 
            self.env['ir.config_parameter'].set_param(key_name, value)

    @api.multi
    def get_default_params(self):
        res = {}
        for field_name, key_name in PARAMS:
            res[field_name] = self.env['ir.config_parameter'].get_param(key_name, '')
    
            if res['delivery_method_ids'] and type(res['delivery_method_ids'])==unicode:
                temp_res=res['delivery_method_ids'].strip('[').strip(']').split(',')
                if temp_res and temp_res[0]:
                    res['delivery_method_ids']=[int(x) for x in temp_res]
                else:
                    res['delivery_method_ids']=[]
        return res      
    
class generate_delivery_form(models.TransientModel):
    _name="russian.post.delivery.form"
    
    @api.model
    def _get_delivery_form(self):
        target_ids = self.env['russian.post.settings'].get_default_params()['delivery_method_ids']
        res=[('','')]
        if target_ids:
            self.env.cr.execute('select api_url,name from service_delivery_form where id in %s',(tuple(target_ids),))
            res=self.env.cr.fetchall()
        return res
#     delivery_method_ids = fields.Many2many('delivery.carrier','rps_delivery_rel','rp_id','delivery_id',string="Delivery Methods",
#                                            domain=lambda self:[('id','in',self.env['russian.post.settings'].get_default_params()['delivery_method_ids'])])
    delivery_method = fields.Selection('_get_delivery_form',string="Delivery Methods",required=True)
    

    @api.multi
    def _get_data(self,target_field,object):
        res = []
        if target_field == 'barcode':
            for x in object.order_line:
                if x.product_id and x.product_id.barcode:
                    res.append(x.product_id.barcode)
        elif target_field in ['from_build','house_to','house_from','room_from','whom_build','building_from','building_to','room_to']:
            res.append(object.street.split(' ')[0])
        
        elif target_field == 'document_day':
            date =object.date_order.split('-') 
            month =date[1]
            day = date[2]
            res.append('%s / %s' % (day,month))
        elif target_field == 'document_year':
            date =object.date_order.split('-')
            res.append(date[0])
        elif target_field in ['name','object']:
            for x in object.move_lines:
                res.append(x.product_id.name)
        elif target_field == 'bank_name':
            for x in obj.bank_journal_ids:
                res.append(x.bank_id.name)
        elif target_field == 'count':
            temp = 0
            for x in obj.move_lines:
                temp+=x.product_uom_qty
            res.append(temp)
        return ', '.join(res) or ' '
    
    @api.multi
    def print_report(self):
        context = self.env.context
        if context :
            form_url=""
            if context.get('delivery_method'):
                form_url=context['delivery_method']
            if context.get('active_model')=='stock.picking' and context.get('active_id'):
                stock_picking_obj=self.env['stock.picking'].browse(context['active_id'])
                #check if there's a sale order connected to the target stock_picking and a partner entry related to that.
                if stock_picking_obj.sale_id and stock_picking_obj.sale_id.partner_id:
                    sale_order=stock_picking_obj.sale_id
                    company=stock_picking_obj.company_id
                    partner=stock_picking_obj.sale_id.partner_id
                    access_token=self.env['russian.post.settings'].get_default_params()['access_token']
        
                    if form_url=='http://pbrf.ru/pdf.F7':
                        data={
                        'type_blank':' ',
                        'from_surname':company.name or ' ',
                        'from_name':company.name or ' ',
                        'from_city':company.city or ' ',
                        'from_street':company.street or company.street2 or ' ',
                        'from_build':self._get_data('from_build',sale_order) or ' ',
                        "from_zip":company.zip or ' ',
                        'whom_surname':partner.name or ' ',
                        'whom_name':partner.name or ' ',
                        'whom_city':company.city or ' ',
                        'whom_street':partner.street or partner.street2 or ' ',
                        'whom_build':self._get_data('whom_build',partner) or ' ',
                        'whom_zip':partner.zip or ' ',
                        'declared_value':sale_order.amount_total or ' ',
                        'COD_amount':str(sale_order.amount_total) or ' ',
                        'tracking_number':' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.F113F117':
                        data={
                        'from_surname':company.name or ' ',
                        'from_patronymic':' ',
                        'from_city':company.city or ' ',
                        'from_street':company.street or company.street2 or ' ',
                        "from_zip":company.zip or ' ',
                        'whom_surname':partner.name or ' ',
                        'whom_patronymic':' ',
                        'whom_city':company.city or ' ',
                        'whom_street':partner.street or partner.street2 or ' ',
                        'whom_zip':partner.zip or ' ',
                        'declared_value_num':' ',
                        'COD_amount_num':' ',
                        'document':sale_order.name or ' ',
                        'document_serial':sale_order.name or ' ',
                        'document_number':sale_order.name or ' ',
                        'document_day':self._get_data('document_day',sale_order) or ' ',
                        'document_year':self._get_data('document_year',sale_order) or ' ',
                        'document_issued_by':company.name or ' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.F112':
                        data={
                        'from_surname':company.name or ' ',
                        'from_name':company.name or ' ',
                        'from_birthday':' ',
                        'from_region':company.state_id.name or ' ',
                        'from_city':company.city or ' ',
                        'from_street':company.street or company.street2 or ' ',
                        'from_build':self._get_data('from_build',sale_order) or ' ',
                        'from_appartment':' ',
                        "from_zip":company.zip or ' ',
                        'whom_name':partner.name or ' ',
                        'who_region':' ',
                        'whom_city':company.city or ' ',
                        'whom_street':partner.street or partner.street2 or ' ',
                        'whom_build':self._get_data('whom_build',partner) or ' ',
                        'whom_appartment':' ',
                        'whom_zip':partner.zip or ' ',
                        'sum_num':sale_order.amount_total or 0,
                        'inn':company.vat or ' ',
                        'kor_account':partner.bank_account_account or ' ',
                        'current_account':' ',
                        'bik':' ',
                        'bank_name':self._get_data('bank_name',company) or ' ',
                        'document':sale_order.name or ' ',
                        'document_serial':sale_order.name or ' ',
                        'document_number':sale_order.name or ' ',
                        'document_day':self._get_data('document_day',sale_order) or ' ',
                        'document_year':self._get_data('document_year',sale_order) or ' ',
                        'document_issued_by':company.name or ' ',
                        'unit_code':' ',
                        'message_part1':' ',
                        'message_part2':' ',
                        'barcode':self._get_data('barcode',sale_order) or ' ',
                        'to_phone':partner.phone or ' ',
                        'from_phone':company.phone or ' ',
                        'one':' ',
                        'two':' ',
                        'three':' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.F112EK':
                        data={
                        'to_zip':partner.zip or ' ',
                        'to_type':' ',
                        'to_name':' ',
                        'to_phone':partner.phone or ' ',
                        "from_zip":company.zip or ' ',
                        'from_region':company.state_id.name or ' ',
                        'from_city':company.city or ' ',
                        'from_surname':company.name or ' ',
                        'from_name':company.name or ' ',
                        'from_street':company.street or company.street2 or ' ',
                        'from_build':self._get_data('from_build',sale_order) or ' ',
                        'from_appartment':' ',
                        'sum_num':sale_order.amount_total or 0,
                        'barcode':self._get_data('barcode',sale_order) or ' ',
                        'message':' ',
                        'cod':' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.F113':
                        data={
                        'from_surname':company.name or ' ',
                        'from_name':company.name or ' ',
                        'from_region':company.state_id.name or ' ',
                        'from_city':company.city or ' ',
                        'from_street':company.street or company.street2 or ' ',
                        'from_build':self._get_data('from_build',sale_order) or ' ',
                        "from_zip":company.zip or ' ',
                        'whom_name':partner.name or ' ',
                        'whom_city':company.city or ' ',
                        'whom_street':partner.street or partner.street2 or ' ',
                        'whom_zip':partner.zip or ' ',
                        'sum_num':sale_order.amount_total or 0,
                        'inn':company.vat or ' ',
                        'kor_account':partner.bank_account_account or ' ',
                        'current_account':' ',
                        'bik':' ',
                        'bank_name':self._get_data('bank_name',company) or ' ',
                        'barcode':self._get_data('barcode',sale_order) or ' ',
                    
                    }
                        
                    elif form_url=='http://pbrf.ru/pdf.F107':
                        data={
                        'whom':partner.name or ' ',
                        'whom_country':company.country_id.name or ' ',
                        'whom_city':company.city or ' ',
                        'investment':' ',
                        'object':self._get_data('object',stock_picking_obj) or ' ',
                        'name':self._get_data('name',stock_picking_obj) or ' ',
                        'count':self._get_data('count',stock_picking_obj) or ' ',
                        'price':sale_order.amount_total or ' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.F116':
                        data={
                        'from_surname':company.name or ' ',
                        'from_country':company.country_id.name or ' ',
                        'from_city':company.city or ' ',
                        "from_zip":company.zip or ' ',
                        'whom':partner.name or ' ',
                        'whom_country':company.country_id.name or ' ',
                        'whom_city':company.city or ' ',
                        'whom_street':partner.street or partner.street2 or ' ',
                        'whom_zip':partner.zip or ' ',
                        'document':sale_order.name or ' ',
                        'document_serial':sale_order.name or ' ',
                        'document_number':sale_order.name or ' ',
                        'document_day':self._get_data('document_day',sale_order) or ' ',
                        'document_year':self._get_data('document_year',sale_order) or ' ',
                        'document_issued_by':company.name or ' ',
                        'declared_value':sale_order.amount_total or ' ',
                        'COD_amount':str(sale_order.amount_total) or ' ',
                        'tracking_number':' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.CN23':
                        data={
                        'from_surname':company.name or ' ',
                        'from_country':company.country_id.name or ' ',
                        'from_city':company.city or ' ',
                        'from_street':company.street or company.street2 or ' ',
                        "from_zip":company.zip or ' ',
                        'whom_surname':partner.name or ' ',
                        'whom_country':company.country_id.name or ' ',
                        'whom_city':company.city or ' ',
                        'whom_street':partner.street or partner.street2 or ' ',
                        'whom_zip':partner.zip or ' ',
                        'object':self._get_data('object',stock_picking_obj) or ' ',
                        'name':self._get_data('name',stock_picking_obj) or ' ',
                        'count':self._get_data('count',stock_picking_obj) or ' ',
                        'brut':' ',
                        'price':sale_order.amount_total or ' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.F103':
                        data={
                        'list_num':' ',
                        'send_date':sale_order.order_date or ' ',
                        'mail_type':3,
                        'sendr':company.name or ' ',
                        'email':' ',
                        'index_from':' ',
                        'mail_count':' ',
                        'Recipientdetails:':' ',
                        'rcpn':partner.name or " ",
                        'index_to':partner.zip or ' ',
                        'region_to':partner.state_id.name or ' ',
                        'place_to':partner.street or ' ',
                        'street_to':partner.street or ' ',
                        'house_to':self._get_data('house_to',partner) or ' ',
                        'area_to':sale_order.street2 or ' ',
                        'location_to':partner.street or ' ',
                        'letter_to':' ',
                        'slash_to':' ',
                        'corpus_to':' ',
                        'building_to':self._get_data('building_to',partner) or ' ',
                        'room_to':self._get_data('room_to',partner) or ' ',
                        'barcode':self._get_data('barcode',sale_order) or ' ',
                        'tel_address':partner.phone or ' ',
                        'mail_ctg':3,
                        'mass':' ',
                        'value':sale_order.amount_untaxed or 0 ,
                        'payment':sale_order.amount_total or 0,
                        'comment':sale_order.note or ' ',
                    
                    }
                    elif form_url=='https://api.pbrf.ru/pdf.f7':
                        data={
                        'MailType':' ',
                        'MailCtg':3,
                        'PostMark':' ',
                        'SNDR':company.name or ' ',
                        'RCPN':partner.name or ' ',
                        'Mass':' ',
                        'Payment':sale_order.amount_total or 0,
                        'Value':str(sale_order.amount_total) or '0',
                        'from_phone':company.phone or ' ',
                        'to_phone':partner.phone or ' ',
                        'SMSNoticeS':' ',
                        'SMSNoticeS':' ',
                        'street_from':company.street or ' ',
                        'house_from':self._get_data('house_from',company) or ' ',
                        'letter_from':' ',
                        'slash_from':' ',
                        'corpus_from':' ',
                        'building_from':self._get_data('building_from',company) or ' ',
                        'room_from':self._get_data('room_from',company) or ' ',
                        'place_from':company.street or ' ',
                        'area_from':company.street2 or ' ',
                        'region_from':company.state_id.name or ' ',
                        'index_from':' ',
                        'street_to':partner.street or ' ',
                        'house_to':self._get_data('house_to',partner) or ' ',
                        'letter_to':' ',
                        'slash_to':' ',
                        'corpus_to':' ',
                        'building_to':self._get_data('building_to',partner) or ' ',
                        'room_to':self._get_data('room_to',partner) or ' ',
                        'place_to':partner.street or ' ',
                        'area_to':sale_order.street2 or ' ',
                        'region_to':partner.state_id.name or ' ',
                        'index_to':partner.zip or ' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.CP71':
                        data={
                        'declared_val_numeric':' ',
                        'to_surname':partner.name or  ' ',
                        'to_street':' ',
                        'to_zip':partner.zip or ' ',
                        'to_country':' ',
                        'from_surname':company.name or ' ',
                        'from_city':company.city or ' ',
                        'from_street':company.street or company.street2 or ' ',
                        "from_zip":company.zip or ' ',
                    
                    }
                    elif form_url=='https://api.pbrf.ru/pdf.emspost':
                        data={
                        'SNDR':company.name or ' ',
                        'RCPN':partner.name or ' ',
                        'from_phone':company.phone or ' ',
                        'to_phone':partner.phone or ' ',
                        'street_from':company.street or ' ',
                        'house_from':self._get_data('house_from',company) or ' ',
                        'place_from':company.street or ' ',
                        'area_from':company.street2 or ' ',
                        'index_from':' ',
                        'region_from':company.state_id.name or ' ',
                        'street_to':partner.street or ' ',
                        'house_to':self._get_data('house_to',partner) or ' ',
                        'place_to':partner.street or ' ',
                        'area_to':sale_order.street2 or ' ',
                        'index_to':partner.zip or ' ',
                        'region_to':partner.state_id.name or ' ',
                        'SenderName':' ',
                        'RecipientName':' ',
                        'Description':' ',
                        'AgreementNo':' ',
                        'MailCtg':3,
                        'Payment':sale_order.amount_total or 0,
                        'Value':str(sale_order.amount_total) or '0',
                    
                    }
                    elif form_url=='http://beta.pbrf.ru/v1/blank/pimpay/':
                        data={
                        'sndr':' ',
                        'street_from':company.street or ' ',
                        'clients':' ',
                        'shops':' ',
                        'type':' ',
                        'house_from':self._get_data('house_from',company) or ' ',
                        'room_from':self._get_data('room_from',company) or ' ',
                        'place_from':company.street or ' ',
                        'region_from':company.state_id.name or ' ',
                        'index_from':' ',
                        'sum_num':sale_order.amount_total or 0,
                        'message':' ',
                    
                    }
                    elif form_url=='http://pbrf.ru/pdf.PrintAddress':
                        data={
                        'from_name':company.name or ' ',
                        'from_adress':' ',
                        "from_zip":company.zip or ' ',
                        'to':' ',
                        'count_copy':' ',
                    
                    }
                    #pbrf.ru api execution
                    #sample: https://pbrf.ru/%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F/%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D0%B0
                    #todo:
                    #proper data generation of the following data keys:

#                     index_from
#                     bik
#                     current_account
#                     MailCtg
#                     message
#                     letter_to
#                     tracking_number
#                     from_apartment
#                     corpus_to
#                     slash_to
#                     mail_count
                    import urllib
                    import json
                    params={}    
                    params['access_token'] = access_token
                    params['data'] = json.dumps(data)
                     
                    params = urllib.urlencode(params)
                    f = urllib.urlopen(form_url, params)
                    print f.read()                    
                            
            
            
        return
    
class stock_picking(models.Model):
    _inherit="stock.picking"
    
    service_delivery_form_id = fields.Many2one('service.delivery.form',string="Service Delivery Form")