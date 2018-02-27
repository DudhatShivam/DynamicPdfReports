from odoo.addons.report.controllers.main import ReportController
from odoo.addons.web.controllers.main import _serialize_exception, content_disposition
from odoo import http
import json
from odoo.http import Controller, route, request
from odoo.tools import html_escape
import simplejson

class ReportController(ReportController):
    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):

    	# This method has been overwrite
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

                report = request.env['report']._get_report_from_name(reportname)		
                filename = "%s.%s" % (report.name, "pdf")  
		
                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    # will search the model where reports will get printed 
		    search_model = request.env['dynamic.reportname'].search([('model_id.model', '=', report.model)])
            # Will bring the list of fields that belongs to the selected model		    
		    if search_model:	
			if search_model.field_id.ttype == 'many2one':
				field = obj.read([search_model.field_id.name])[0][search_model.field_id.name][1]
			else:
				field = obj.read([search_model.field_id.name])[0][search_model.field_id.name]
				# will print the dynamic names for pdf reports
			filename = (str(field) or report.name) + '.pdf'
		    
                    if report.print_report_name and not len(obj) > 1:
                        filename = safe_eval(report.print_report_name, {'object': obj, 'time': time})

                response.headers.add('Content-Disposition', content_disposition(filename))
                response.set_cookie('fileToken', token)
                return response
            elif type == 'controller':
                reqheaders = Headers(request.httprequest.headers)
                response = Client(request.httprequest.app, BaseResponse).get(url, headers=reqheaders, follow_redirects=True)
                response.set_cookie('fileToken', token)
                return response
            else:
                return
        except Exception, e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
