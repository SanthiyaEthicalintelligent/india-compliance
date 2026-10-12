import frappe
from frappe.utils import flt


def sync_tax_rate_display(doc, method=None):
    """Show the item-wise GST rate in the Taxes table's Rate column.

    The taxes table row carries the template's default rate (e.g. 9), while the
    amount is calculated from the Item Tax Template (e.g. 2.5). When every item
    gives the same rate for a tax account, the row rate follows it. Mixed slabs,
    or an item without a template, keep the template rate. Only the displayed
    rate changes, the amounts are already calculated.
    """
    if doc.docstatus != 0:
        return

    for tax in doc.get("taxes") or []:
        if tax.charge_type != "On Net Total" or not tax.account_head:
            continue

        rates = set()
        for item in doc.get("items") or []:
            item_tax_rate = frappe.parse_json(item.item_tax_rate or "{}")
            if tax.account_head not in item_tax_rate:
                rates = set()
                break
            rates.add(flt(item_tax_rate[tax.account_head]))

        if len(rates) == 1:
            tax.rate = rates.pop()
