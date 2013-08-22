# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import pdb

class account_invoice_line(osv.osv):
    _name = 'account.invoice.line'
    _inherit = "account.invoice.line"

    def _fnct_related_serial_num(self, cr, uid, ids, field_name, args, context=None):

	stock_move_obj = self.pool.get('stock.move')
	stock_move_split_obj = self.pool.get('stock.move.split')

        res = {}
        for line in self.browse(cr, uid, ids, context=context):
		if not line.invoice_id.origin:
			res[line.id] = ''
		else:
		        origin = line.invoice_id.origin
			args = [('origin','=',origin),('product_id','=',line.product_id.id)]
			stock_move_ids = stock_move_obj.search(cr,uid,args)
			if stock_move_ids:
				string_serial_nums = ''
				for move in stock_move_obj.browse(cr,uid,stock_move_ids):
					if not move.prodlot_id.id:
						string_serial_nums = string_serial_nums + ''
					else:
						string_serial_nums = string_serial_nums + move.prodlot_id.name
				res[line.id] = int(string_serial_nums)
				#import pdb;pdb.set_trace()			
			else:
				res[line.id] = ''
        return res

    _columns = {
        'related_serial_num': fields.function(_fnct_related_serial_num, string='Related Serial Numbers'),
    }

account_invoice_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
