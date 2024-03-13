from odoo import models, fields, api
import base64
import xlrd
import logging
import io
import xlsxwriter

_logger = logging.getLogger(__name__)

class ImportSOLinesWizard(models.TransientModel):
    _name = 'import.so.lines.wizard'
    _description = 'Import SO Lines Wizard'

    data_file = fields.Binary(string="Excel File", help="Upload the Excel file here.")

    def action_import_so_lines(self):
        if not self.data_file:
            return {'type': 'ir.actions.act_window_close'}
        
        excel_file_data = base64.b64decode(self.data_file)
        workbook = xlrd.open_workbook(file_contents=excel_file_data)
        sheet = workbook.sheet_by_index(0)

        sale_order_id = self._context.get('active_id')
        if not sale_order_id:
            _logger.error('No active Sale Order ID found in context.')
            return {'type': 'ir.actions.act_window_close'}

        for row_idx in range(1, sheet.nrows):
            product_code = sheet.cell(row_idx, 0).value
            qty = sheet.cell(row_idx, 1).value
            unit_price = sheet.cell(row_idx, 2).value

          
            product = self.env['product.template'].search([('default_code', '=', product_code)], limit=1)
            
            if product:
                self.env['sale.order.line'].create({
                    'order_id': sale_order_id,
                    'product_id': product.id,
                    'product_uom_qty': qty,
                    'price_unit': unit_price,
                })
                _logger.info(f'SO line added for product {product_code}')
            else:
                _logger.warning(f'Product not found for code {product_code}')

        return {'type': 'ir.actions.act_window_close'}

    def generate_excel_template(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Template')


        header = ['Product Code', 'Qty', 'Unit Price']
        for col, head in enumerate(header):
            worksheet.write(0, col, head)

        workbook.close()
        output.seek(0)
        return base64.b64encode(output.read())

    def action_download_template(self):
        excel_content = self.generate_excel_template()
        return {
            'type': 'ir.actions.act_url',
            'url': 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,%s' % excel_content.decode(),
            'target': 'self',
            'filename': 'SO_Lines_Template.xlsx'
        }