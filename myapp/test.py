import csv
from datetime import datetime
import pandas as pd
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
import django
django.setup()
from myapp.models import Report

def populate_db():
    csv_file = 'Book1.csv'  # Replace with the actual path to your CSV file

    # Read the CSV file using pandas
    df = pd.read_csv(csv_file)
    current_date = datetime.now().date()
    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        report = Report()

        # Set values for the Report object based on the CSV columns
        report.bp_code = row['BP code']
        report.bp_name = row['BP name']
        report.customer_site = row['Customer site']
        report.district = row['District']
        report.profile = row['Profile']
        report.sector = row['Sector']
        report.customer_category = row['Customer category']
        report.supplier = row['Supplier']
        report.product = row['Product']
        report.bw = row['BW']
        report.item_description = row['Item description']
        report.kms_dfl_only = row['Kms dfl only']
        report.qty = int(row['Qty'])
        report.price = float(row['Price'])
        report.total_sales = report.qty * report.price
        report.billing_cycle = row['Billing cycle']
        report.end_date = datetime.strptime(row['End Date'], '%d/%m/%Y').date()
        report.agreement_days = (report.end_date - datetime.now().date()).days
        if report.agreement_days == 0:
            report.contract_status = "Expired"
        elif report.agreement_days <= 30:
            report.contract_status = "Expires in <30 days"
        elif report.agreement_days <= 60:
            report.contract_status = "Expires in <60 days"
        else:
            report.contract_status = "Valid contract"
        report.account_manager = row['Account manager']
        report.contact_person = row['Contact person']
        report.cp_email = row['CP email']
        report.cp_phone = row['Cp phone']
        report.comment = row['Comment']

        # Save the Report object to the database
        report.save()

    print('Database population complete.')

if __name__ == '__main__':
    populate_db()
