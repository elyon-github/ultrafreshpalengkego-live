# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ultrafresh_reports(models.Model):
    _inherit = 'sale.order'

    def fetch_shop_list(self, ids):
        val = self.fetch_shop_list_data_raw(ids)

        processed = self.process_shop_list_data_raw(val)

        return processed

    def fetch_shop_list_data_raw(self, ids):
        init_query = """SELECT T1.name as order_code, T4.name as prod_name, T2.x_studio_product_notes as ord_notes, T2.product_uom_qty as qty, T6.name as uom
            FROM sale_order T1
            LEFT JOIN sale_order_line T2 ON T2.order_id = T1.id
            LEFT JOIN product_product T3 ON T2.product_id = T3.id
            LEFT JOIN product_template T4 ON T3.product_tmpl_id = T4.id
            LEFT JOIN res_partner T5 ON T5.id = T1.partner_id
            LEFT JOIN uom_uom T6 ON T6.id = T2.product_uom WHERE {}"""

        cond = ""
        ctr = 1
        for id in ids:
            if ctr == len(ids):
                cond += " T1.id = " + str(id.id)
            else:
                cond += " T1.id = " + str(id.id) + " or "
            ctr += 1
        
        self._cr.execute(init_query.format(cond))
        res = self._cr.fetchall()

        return res

    def process_shop_list_data_raw(self, data):
        products = self.extract_products(data)
        new_data = self.construct_details_array(data,products)
        return new_data
    
    def extract_products(self, data):
        init_products = []
        for val in data:
            init_products.append(str(val[1]['en_US']))

        products = set(init_products)
        return list(products)

    def construct_details_array(self, data, products):
        # ('S00022', {'en_US': 'Developer(Plan services)'},None, 120.0, {'en_US': 'Hours'}),
        new_arr = []
        
        for prod in products:
            layer_dict = {'prod': prod, 'total_qtys': [], 'details': []}
            for val in data:
                if prod == val[1]['en_US']:
                    unit = str(val[4]['en_US'])
                    notes = val[2]
                    if notes == None:
                        notes = ""

                    layer_dict['details'].append({'order': str(val[0]),'notes': notes, 'qty': val[3], 'uom': unit})
                    
                    if len(layer_dict['total_qtys']) > 0:
                        for uoms in layer_dict['total_qtys']:
                            if uoms['uom'] == unit:
                                uoms['qty'] += val[3]
                            else:
                                layer_dict['total_qtys'].append({'qty': val[3], 'uom': unit})
                    else:
                        layer_dict['total_qtys'].append({'qty': val[3], 'uom': unit})
            new_arr.append(layer_dict)
        
        return new_arr
