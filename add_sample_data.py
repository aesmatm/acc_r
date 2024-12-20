import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_accounting.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import User
from projects.models import Project
from suppliers.models import Supplier, Invoice, InvoiceItem
from finance.models import AccountTree, Transaction, TransactionLine

def create_users():
    print("Creating users...")
    # Create accountants
    accountants = [
        {'username': 'accountant1', 'name': 'Mohammed Ahmed', 'email': 'accountant1@example.com'},
        {'username': 'accountant2', 'name': 'Ahmed Mohammed', 'email': 'accountant2@example.com'},
        {'username': 'accountant3', 'name': 'Omar Khalid', 'email': 'accountant3@example.com'},
    ]
    
    for acc in accountants:
        if not User.objects.filter(username=acc['username']).exists():
            first_name, last_name = acc['name'].split(' ')
            user = User.objects.create_user(
                username=acc['username'],
                password='Pass123!',
                email=acc['email'],
                first_name=first_name,
                last_name=last_name,
                role='accountant',
                is_staff=True
            )
            print(f"Created accountant: {acc['name']}")
        else:
            print(f"Accountant {acc['username']} already exists")

def create_accounts():
    print("\nCreating account tree...")
    # Main accounts
    main_accounts = [
        {'code': '1', 'name': 'Assets', 'type': 'asset'},
        {'code': '2', 'name': 'Liabilities', 'type': 'liability'},
        {'code': '3', 'name': 'Equity', 'type': 'equity'},
        {'code': '4', 'name': 'Revenue', 'type': 'revenue'},
        {'code': '5', 'name': 'Expenses', 'type': 'expense'},
    ]
    
    accounts_map = {}
    for acc in main_accounts:
        account, created = AccountTree.objects.get_or_create(
            code=acc['code'],
            defaults={
                'name': acc['name'],
                'account_type': acc['type']
            }
        )
        accounts_map[acc['code']] = account
        if created:
            print(f"Created account: {acc['name']}")
        else:
            print(f"Account {acc['name']} already exists")
    
    # Sub accounts
    sub_accounts = [
        {'code': '11', 'name': 'Cash', 'type': 'asset', 'parent': '1'},
        {'code': '12', 'name': 'Accounts Receivable', 'type': 'asset', 'parent': '1'},
        {'code': '21', 'name': 'Accounts Payable', 'type': 'liability', 'parent': '2'},
        {'code': '41', 'name': 'Project Revenue', 'type': 'revenue', 'parent': '4'},
        {'code': '51', 'name': 'Project Expenses', 'type': 'expense', 'parent': '5'},
    ]
    
    for acc in sub_accounts:
        account, created = AccountTree.objects.get_or_create(
            code=acc['code'],
            defaults={
                'name': acc['name'],
                'account_type': acc['type'],
                'parent': accounts_map[acc['parent']]
            }
        )
        if created:
            print(f"Created sub-account: {acc['name']}")
        else:
            print(f"Sub-account {acc['name']} already exists")

def create_projects():
    print("\nCreating projects...")
    projects_data = [
        {
            'name': 'Residential Tower Project',
            'code': 'PRJ001',
            'description': 'Construction of 20-floor residential tower',
            'client_name': 'Real Estate Development Co.',
            'status': 'in_progress',
            'start_date': datetime.now().date(),
            'expected_end_date': (datetime.now() + timedelta(days=365)).date(),
            'total_budget': Decimal('5000000.00'),
        },
        {
            'name': 'Commercial Complex Project',
            'code': 'PRJ002',
            'description': 'Construction of commercial complex on 10000 square meters',
            'client_name': 'Development Corporation',
            'status': 'in_progress',
            'start_date': datetime.now().date(),
            'expected_end_date': (datetime.now() + timedelta(days=540)).date(),
            'total_budget': Decimal('8000000.00'),
        },
    ]
    
    accountants = User.objects.filter(role='accountant')
    
    for proj in projects_data:
        if not Project.objects.filter(code=proj['code']).exists():
            project = Project.objects.create(
                name=proj['name'],
                code=proj['code'],
                description=proj['description'],
                client_name=proj['client_name'],
                status=proj['status'],
                start_date=proj['start_date'],
                expected_end_date=proj['expected_end_date'],
                total_budget=proj['total_budget'],
                accountant=random.choice(accountants)
            )
            print(f"Created project: {proj['name']}")
        else:
            print(f"Project {proj['code']} already exists")

def create_suppliers():
    print("\nCreating suppliers...")
    suppliers_data = [
        {
            'name': 'United Building Materials Co.',
            'code': 'SUP001',
            'contact_person': 'Khalid Mohammed',
            'phone': '0555555555',
            'email': 'supplier1@example.com',
            'address': 'Industrial Area',
            'tax_number': '123456789',
        },
        {
            'name': 'Construction Supplies Est.',
            'code': 'SUP002',
            'contact_person': 'Abdullah Ahmed',
            'phone': '0566666666',
            'email': 'supplier2@example.com',
            'address': 'Industry Street',
            'tax_number': '987654321',
        },
    ]
    
    for sup in suppliers_data:
        if not Supplier.objects.filter(code=sup['code']).exists():
            supplier = Supplier.objects.create(**sup)
            print(f"Created supplier: {sup['name']}")
        else:
            print(f"Supplier {sup['code']} already exists")

def create_invoices():
    print("\nCreating invoices...")
    suppliers = Supplier.objects.all()
    projects = Project.objects.all()
    accountants = User.objects.filter(role='accountant')
    
    if not accountants.exists():
        print("No accountants found. Cannot create invoices.")
        return
        
    for supplier in suppliers:
        for _ in range(2):  # Create 2 invoices per supplier
            invoice_number = f'INV{random.randint(1000, 9999)}'
            if not Invoice.objects.filter(invoice_number=invoice_number).exists():
                invoice = Invoice.objects.create(
                    supplier=supplier,
                    project=random.choice(projects),
                    invoice_number=invoice_number,
                    invoice_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                    due_date=datetime.now() + timedelta(days=30),
                    total_amount=Decimal(random.randint(10000, 50000)),
                    tax_amount=Decimal(random.randint(500, 2500)),
                    status='draft',
                    description='Supply of construction materials',
                    created_by=random.choice(accountants)
                )
                
                # Create invoice items
                items = [
                    {'description': 'Cement Supply', 'quantity': Decimal('5.00'), 'unit_price': Decimal('300.00')},
                    {'description': 'Steel Supply', 'quantity': Decimal('3.00'), 'unit_price': Decimal('2500.00')},
                    {'description': 'Sand Supply', 'quantity': Decimal('10.00'), 'unit_price': Decimal('100.00')},
                ]
                
                for item in items:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=item['description'],
                        quantity=item['quantity'],
                        unit_price=item['unit_price']
                    )
                
                print(f"Created invoice: {invoice.invoice_number}")
            else:
                print(f"Invoice {invoice_number} already exists")

def main():
    print("Starting to add sample data...")
    create_users()
    create_accounts()
    create_projects()
    create_suppliers()
    create_invoices()
    print("\nAll sample data has been added successfully!")

if __name__ == '__main__':
    main()
