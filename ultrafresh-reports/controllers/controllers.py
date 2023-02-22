# -*- coding: utf-8 -*-
# from odoo import http


# class Ultrafresh-reports(http.Controller):
#     @http.route('/ultrafresh-reports/ultrafresh-reports', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ultrafresh-reports/ultrafresh-reports/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ultrafresh-reports.listing', {
#             'root': '/ultrafresh-reports/ultrafresh-reports',
#             'objects': http.request.env['ultrafresh-reports.ultrafresh-reports'].search([]),
#         })

#     @http.route('/ultrafresh-reports/ultrafresh-reports/objects/<model("ultrafresh-reports.ultrafresh-reports"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ultrafresh-reports.object', {
#             'object': obj
#         })
