from osv import osv, fields
import tools
import netsvc
import time
import pooler


class res_currency_rate(osv.osv):

    _inherit = "res.currency.rate"
    _columns = {
        'rate_extra': fields.float('Conversion Rate', digits=(12, 6), required=True),
    }

    def onchange_rate_extra(self, cr, uid, ids, rate_extra):
        if rate_extra == 0: rate_extra = 1
        result = {'value': {
            'rate': 1 / rate_extra,
        }
        }

        return result

res_currency_rate()


class Currency(osv.osv):
    def _current_rate_extra(self, cr, uid, ids, name, arg, context={}):
        res = {}
        if 'date' in context:
            date = context['date']
        else:
            date = time.strftime('%Y-%m-%d')
        date = date or time.strftime('%Y-%m-%d')
        for id in ids:
            cr.execute("SELECT currency_id, rate_extra "
                       "FROM res_currency_rate "
                       "WHERE currency_id = %s AND name <= %s ORDER BY name desc LIMIT 1", (id, date))
            if cr.rowcount:
                id, rate_extra = cr.fetchall()[0]
                res[id] = rate_extra
            else:
                res[id] = 0
        return res
    _inherit = "res.currency"
    _columns = {
        'rate_extra': fields.function(_current_rate_extra, method=True, string='Conversion Rate', digits=(12, 6),
                                      help='Rate = 1/Conversion Rate : example : 1 EUR = 11.25 MAD'),
    }

Currency()
