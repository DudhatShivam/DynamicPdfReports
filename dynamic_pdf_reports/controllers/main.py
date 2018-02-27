from odoo.addons.web.controllers.main import _serialize_exception, content_disposition
from odoo import http
import json
import time
from odoo.http import Controller, route, request
from odoo.tools import html_escape
from odoo.tools.safe_eval import safe_eval
from odoo.addons.web.controllers.main import ReportController

class ReportController(ReportController):

    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        """This function is used by 'qwebactionmanager.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]

        try:
            if type == 'qweb-pdf':
                reportname = url.split('/report/pdf/')[1].split('?')[0]

                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')

                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids, converter='pdf')
                else:
                    # Particular report:
                    data = url_decode(url.split('?')[1]).items()  # decoding the args represented in JSON
                    response = self.report_routes(reportname, converter='pdf', **dict(data))

                report = request.env['ir.actions.report']._get_report_from_name(reportname)
                filename = "%s.%s" % (report.name, "pdf")

                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)

                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(report.print_report_name, {'object': obj, 'time': time})
                        filename = "%s.%s" % (report_name, "pdf")

                    search_model = request.env['dynamic.reportname'].search([('model_id.model', '=', report.model)])
                    if search_model:
                        if search_model.field_id.ttype == 'many2one':
                            field_value = obj.read([search_model.field_id.name])[0]
                            if field_value[search_model.field_id.name]:
                                field = obj.read([search_model.field_id.name])[0][search_model.field_id.name][1]
                                filename = (str(field) or report.name) + '.pdf'

                        else:                            
                            field = obj.read([search_model.field_id.name])[0][search_model.field_id.name]
                            filename = (str(field) or report.name) + '.pdf'
                            # will print the dynamic names for pdf reports
                    
                response.headers.add('Content-Disposition', content_disposition(filename))
                response.set_cookie('fileToken', token)
                return response
            else:
                return
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))