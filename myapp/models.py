from django.db import models
from datetime import date

# Create your models here.

class Target(models.Model):
    product = models.CharField(max_length=100)
    total_targets = models.DecimalField(max_digits=20, decimal_places=2, editable=False)
    account_manager = models.CharField(max_length=100)
    sales_month = models.CharField(max_length=20)

class Report(models.Model):
    # DISTRICT_CHOICES = [
    #     ('Bugesera', 'Bugesera'),
    #     ('Burera', 'Burera'),
    #     ('Gakenke', 'Gakenke'),
    #     ('Gasabo', 'Gasabo'),
    #     ('Gatsibo', 'Gatsibo'),
    #     ('Gicumbi', 'Gicumbi'),
    #     ('Gisagara', 'Gisagara'),
    #     ('Huye', 'Huye'),
    #     ('Kamonyi', 'Kamonyi'),
    #     ('Karongi', 'Karongi'),
    #     ('Kayonza', 'Kayonza'),
    #     ('Kicukiro', 'Kicukiro'),
    #     ('Kirehe', 'Kirehe'),
    #     ('Muhanga', 'Muhanga'),
    #     ('Musanze', 'Musanze'),
    #     ('Ngoma', 'Ngoma'),
    #     ('Ngororero', 'Ngororero'),
    #     ('Nyabihu', 'Nyabihu'),
    #     ('Nyagatare', 'Nyagatare'),
    #     ('Nyamagabe', 'Nyamagabe'),
    #     ('Nyamasheke', 'Nyamasheke'),
    #     ('Nyanza', 'Nyanza'),
    #     ('Nyarugenge', 'Nyarugenge'),
    #     ('Nyaruguru', 'Nyaruguru'),
    #     ('Rubavu', 'Rubavu'),
    #     ('Ruhango', 'Ruhango'),
    #     ('Rulindo', 'Rulindo'),
    #     ('Rusizi', 'Rusizi'),
    #     ('Rutsiro', 'Rutsiro'),
    #     ('Rwamagana', 'Rwamagana'),
    #     ('Kenya', 'Kenya'),
    #     ('Tanzania', 'Tanzania'),
    # ]
    # PROFILE_CHOICES = [
    #     ('Government', 'Government'),
    #     ('Private', 'Private'),
    # ]
    # SECTOR_CHOICES = [
    #     ('CENTRAL GOV', 'CENTRAL GOV'),
    #     ('TECH', 'TECH'),
    # ]

    # district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
    # profile = models.CharField(max_length=20, choices=PROFILE_CHOICES)
    # sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)

    bp_code = models.CharField(max_length=10)
    bp_name = models.CharField(max_length=100)
    customer_site = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    profile = models.CharField(max_length=20)
    sector = models.CharField(max_length=20)
    customer_category = models.CharField(max_length=100)
    supplier = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    bw = models.IntegerField(null=True, blank=True)
    item_description = models.CharField(max_length=100)
    kms_dfl_only = models.IntegerField(null=True, blank=True)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    total_sales = models.DecimalField(max_digits=20, decimal_places=2, editable=False)
    sales_month = models.CharField(max_length=20, blank=True)
    billing_cycle = models.CharField(max_length=20)
    end_date = models.DateField()
    agreement_days = models.IntegerField(editable=False)
    contract_status = models.CharField(max_length=100, editable=False)
    account_manager = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    cp_email = models.EmailField(max_length=254)
    cp_phone = models.CharField(max_length=15, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price is not None and self.qty is not None:
            self.total_sales = self.price * self.qty
        else:
            self.total_sales = 0
        self.agreement_days = (self.end_date - date.today()).days
        if self.agreement_days <= 0:
            self.contract_status = "Expired"
        elif self.agreement_days <= 30:
            self.contract_status = "Expires in <30 days"
        elif self.agreement_days <= 60:
            self.contract_status = "Expires in <60 days"
        else:
            self.contract_status = "Valid contract"
        super().save(*args, **kwargs)


