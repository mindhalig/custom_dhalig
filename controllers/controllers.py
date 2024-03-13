# -*- coding: utf-8 -*-
# from odoo import http


# class CustomDhalig(http.Controller):
#     @http.route('/custom_dhalig/custom_dhalig/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_dhalig/custom_dhalig/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_dhalig.listing', {
#             'root': '/custom_dhalig/custom_dhalig',
#             'objects': http.request.env['custom_dhalig.custom_dhalig'].search([]),
#         })

#     @http.route('/custom_dhalig/custom_dhalig/objects/<model("custom_dhalig.custom_dhalig"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_dhalig.object', {
#             'object': obj
#         })
