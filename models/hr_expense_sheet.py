from odoo import fields,models
from odoo.exceptions import UserError

class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def reimberse_trip_sheet(self):
        for each_2 in self.expense_line_ids:
            petrol_record = self.env['petrol.record'].search([('expense_id','=',each_2.id)])
            if petrol_record:
                for line in petrol_record:
                    line.to_reimberse = line.to_reimberse - each_2.total_amount
                    line.amount = each_2.total_amount
                    line.status = 'approved'
        for each in self.expense_line_ids:
             m = each.vehicle_req
             for trip_line in self.env['trip.sheet'].search([('vehicle_req', '=', m.id)]).vehicle_trip_sheet_lines:
                 if each == trip_line.expense_id:
                     trip_line.given = self.total_amount
                     trip_line.reimbursed_expenses = trip_line.reimbursed_expenses - self.total_amount
        for each_1 in self.expense_line_ids:
            m_1 = each_1.vehicle_req
            for eachbetta_line in self.env['trip.sheet'].search([('vehicle_req', '=', m_1.id)]).betta_lines:
                if each_1 == eachbetta_line.expense_id:
                    eachbetta_line.spended = self.total_amount
                    eachbetta_line.reimbursed_expenses = eachbetta_line.reimbursed_expenses - self.total_amount
            contract = self.env['pending.contracts'].search(
                [('vehicle_req', '=', each_1.vehicle_req.id), ('vehicle_id', '=', each_1.vehicle_id.id)])
            if len(contract) > 0:
                for con in contract:
                    con.cdac = con.cdac + each_1.total_amount
                    con.balance = con.freight - con.cdac


    def approve_expense_sheets(self):
        for each_2 in self.expense_line_ids:
            petrol_record = self.env['petrol.record'].search([('expense_id','=',each_2.id)])
            if petrol_record:
                for line in petrol_record:
                    line.to_reimberse = line.to_reimberse - each_2.total_amount
                    line.amount = each_2.total_amount
                    line.status = 'approved'
        for each in self.expense_line_ids:
             m = each.vehicle_req
             for trip_line in self.env['trip.sheet'].search([('vehicle_req', '=', m.id)]).vehicle_trip_sheet_lines:
                 if each == trip_line.expense_id:
                     trip_line.given = self.total_amount
                     trip_line.reimbursed_expenses = trip_line.reimbursed_expenses - self.total_amount
        for each_1 in self.expense_line_ids:
            m_1 = each_1.vehicle_req
            for eachbetta_line in self.env['trip.sheet'].search([('vehicle_req', '=', m_1.id)]).betta_lines:
                if each_1 == eachbetta_line.expense_id:
                    eachbetta_line.spended = self.total_amount
                    eachbetta_line.reimbursed_expenses = eachbetta_line.reimbursed_expenses - self.total_amount
            contract = self.env['pending.contracts'].search(
                [('vehicle_req', '=', each_1.vehicle_req.id), ('vehicle_id', '=', each_1.vehicle_id.id)])
            if len(contract) > 0:
                for con in contract:
                    con.cdac = con.cdac + each_1.total_amount
                    con.balance = con.freight - con.cdac

        return super(HrExpenseSheet, self).approve_expense_sheets()



    def action_sheet_move_create(self):
        result = super(HrExpenseSheet, self).action_sheet_move_create()
        for petrol in self.expense_line_ids:
            if petrol.internal_fuel == True:
                raise UserError('Sorry This is an Expense generated For Petrol which is filled from our company petrol bunk ,you can only pay this amount through freight bill')

        # For Payment Of Purchase Order
        for invoice in self.expense_line_ids:
            if invoice.invoice_id:
                if invoice.invoice_id.amount_residual > 0:
                    paid = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                   active_ids=invoice.invoice_id.ids).create({
                        'payment_date': invoice.invoice_id.invoice_date,
                        'journal_id': self.env['account.journal'].search(
                        [('name', '=', 'Bank'), ('company_id', '=', self.env.user.company_id.id)]).id,
                        # 'payment_method_id':1,
                        'amount': invoice.total_amount,

                    })
                    paid._create_payments()

                # paid = self.env['account.payment'].create({
                #     'partner_type': 'supplier',
                #     'partner_id': invoice.invoice_id.partner_id.id,
                #     'state': 'draft',
                #     'payment_type': 'outbound',
                #     'destination_account_id': self.env['account.account'].search(
                #         [('name', '=', 'Account Payable'expense)]).id,expense
                #     'invoice_ids': [(6, 0, ([invoice.invoice_id.id]))],
                #     'payment_method_id': 1,
                #     'amount': invoice.total_amount,
                #     'journal_id': self.env['account.journal'].search(
                #         [('name', '=', 'Bank'), ('company_id', '=', self.env.user.company_id.id)]).id,
                #     'payment_date': datetime.now().date(),
                #     'communication': invoice.invoice_id.number,
                # })
                # paid.action_validate_invoice_payment()


        return result
