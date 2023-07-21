# from import_export import resources, fields
# from myapp.models import Report
# from datetime import date, datetime


# class ReportResource(resources.ModelResource):
#     price = fields.Field(column_name='Price', attribute='price')
#     qty = fields.Field(column_name='Qty', attribute='qty')
#     total_sales = fields.Field(column_name='Total Sales', attribute='total_sales', readonly=True)

#     class Meta:
#         model = Report
#         fields = ('bp_code', 'bp_name', 'customer_site', 'district', 'profile', 'sector', 'customer_category',
#                   'supplier', 'product', 'bw', 'item_description', 'kms_dfl_only', 'qty', 'price', 'total_sales',
#                   'billing_cycle', 'end_date', 'agreement_days', 'contract_status', 'account_manager',
#                   'contact_person', 'cp_email', 'cp_phone', 'comment')
#         import_id_fields = ('bp_code',)

#     def import_field(self, field, obj, data, is_m2m=False, **kwargs):        
#         if field.attribute == 'qty' or field.attribute == 'price':
#             value = data.get(field.column_name)
#             if value is not None and value != '':
#                 try:
#                     setattr(obj, field.attribute, field.clean(value))
#                 except:
#                     pass
#         else:
#             super().import_field(field, obj, data, is_m2m, **kwargs)


#     def before_save_instance(self, instance, using_transactions, dry_run):
#         if instance.qty is None:
#             instance.qty = 0
#         if instance.price is None:
#             instance.price = 0
#         if instance.end_date is None:
#             instance.end_date = date.today()
#         instance.total_sales = instance.price * instance.qty
#         instance.agreement_days = (instance.end_date.date() - date.today()).days