from django.db import models


class Users(models.Model):
    user_id = models.AutoField(db_column='User_ID', primary_key=True)
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)
    role = models.CharField(db_column='Role', max_length=50, blank=True, null=True)
    profilepicture = models.CharField(db_column='ProfilePicture', max_length=255, blank=True, null=True)
    resettoken = models.CharField(db_column='ResetToken', max_length=255, blank=True, null=True)
    resettokenexpiry = models.DateTimeField(db_column='ResetTokenExpiry', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Vehicle(models.Model):
    vehicle_id = models.AutoField(db_column='Vehicle_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    vin = models.CharField(db_column='VIN', max_length=50, blank=True, null=True)
    platenumber = models.CharField(db_column='PlateNumber', max_length=20, blank=True, null=True)
    model = models.CharField(db_column='Model', max_length=50, blank=True, null=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)
    mileage = models.IntegerField(db_column='Mileage', blank=True, null=True)
    make = models.CharField(db_column='Make', max_length=50, blank=True, null=True)
    color = models.CharField(db_column='Color', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle'

    def __str__(self):
        return f"{self.make} {self.model} ({self.platenumber})"


class Appointment(models.Model):
    appointment_id = models.AutoField(db_column='Appointment_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)
    starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50)
    service_type = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'


class Invoice(models.Model):
    invoice_id = models.AutoField(db_column='Invoice_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    invoicedate = models.DateField(db_column='InvoiceDate', blank=True, null=True)
    subtotallabor = models.DecimalField(db_column='SubtotalLabor', max_digits=10, decimal_places=2, blank=True, null=True)
    subtotalparts = models.DecimalField(db_column='SubtotalParts', max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(db_column='Tax', max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(db_column='Discount', max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)
    jobcard = models.ForeignKey('Jobcard', models.DO_NOTHING, db_column='JobCard_ID', blank=True, null=True, related_name='invoice_list')
    duedate = models.DateField(db_column='DueDate', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice'


class Payment(models.Model):
    payment_id = models.AutoField(db_column='Payment_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='Invoice_ID', blank=True, null=True)
    paymentdate = models.DateField(db_column='PaymentDate', blank=True, null=True)
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, blank=True, null=True)
    method = models.CharField(db_column='Method', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'


class Jobcard(models.Model):
    jobcard_id = models.AutoField(db_column='JobCard_ID', primary_key=True)
    appointment = models.ForeignKey(Appointment, models.DO_NOTHING, db_column='Appointment_ID', blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    technician = models.ForeignKey(Users, models.DO_NOTHING, db_column='Technician_ID', blank=True, null=True, related_name='assigned_jobs')
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='Invoice_ID', blank=True, null=True, related_name='jobcard_list')
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    reportedissues = models.TextField(db_column='ReportedIssues', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)
    totallaborcost = models.DecimalField(db_column='TotalLaborCost', max_digits=10, decimal_places=2, blank=True, null=True)
    totalpartscost = models.DecimalField(db_column='TotalPartsCost', max_digits=10, decimal_places=2, blank=True, null=True)
    technician_notes = models.TextField(db_column='Technician_Notes', blank=True, null=True)
    total_hours = models.DecimalField(db_column='TotalHours', max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)

    class Meta:
        managed = False
        db_table = 'jobcard'


class Inventoryitem(models.Model):
    item_id = models.AutoField(db_column='Item_ID', primary_key=True)
    itemnumber = models.IntegerField(db_column='ItemNumber', blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)
    unitprice = models.IntegerField(db_column='UnitPrice', blank=True, null=True)
    stockqty = models.IntegerField(db_column='StockQty', blank=True, null=True)
    minstocklevel = models.IntegerField(db_column='MinStockLevel', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventoryitem'


class Jobcardparts(models.Model):
    id = models.AutoField(primary_key=True)
    jobcard = models.ForeignKey(Jobcard, models.DO_NOTHING, db_column='JobCard_ID')
    item = models.ForeignKey(Inventoryitem, models.DO_NOTHING, db_column='Item_ID')
    quantityused = models.IntegerField(db_column='QuantityUsed', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True, default='Pending')

    class Meta:
        managed = False
        db_table = 'jobcardparts'
        unique_together = (('jobcard', 'item'),)


class Inspection(models.Model):
    inspection_id = models.AutoField(db_column='Inspection_ID', primary_key=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)
    jobcard = models.ForeignKey(Jobcard, models.DO_NOTHING, db_column='JobCard_ID', blank=True, null=True)
    date = models.DateField(db_column='Date', blank=True, null=True)
    healthscore = models.IntegerField(db_column='HealthScore', blank=True, null=True)
    healthcategory = models.CharField(db_column='HealthCategory', max_length=50, blank=True, null=True)
    results = models.TextField(db_column='Results', blank=True, null=True)
    diagnosticdata = models.TextField(db_column='DiagnosticData', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inspection'


class Certification(models.Model):
    certification_id = models.AutoField(db_column='Certification_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)
    inspection = models.ForeignKey(Inspection, models.DO_NOTHING, db_column='Inspection_ID', blank=True, null=True)
    issuedate = models.DateField(db_column='IssueDate', blank=True, null=True)
    next_maint_date = models.DateField(db_column='Next_Maint_Date', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certification'


class Timelog(models.Model):
    timelog_id = models.AutoField(db_column='TimeLog_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)
    jobcard = models.ForeignKey(Jobcard, models.DO_NOTHING, db_column='JobCard_ID', blank=True, null=True)
    starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True)
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)
    totalhours = models.DecimalField(db_column='TotalHours', max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timelog'


# --- Role-specific profile tables ---

class Admin(models.Model):
    admin_id = models.AutoField(db_column='Admin_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Client(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING, db_column='User_ID', primary_key=True)
    registrationdate = models.DateField(db_column='RegistrationDate', blank=True, null=True)
    customercategory = models.CharField(db_column='CustomerCategory', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'


class Technician(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING, db_column='User_ID', primary_key=True)
    currentstatus = models.CharField(db_column='CurrentStatus', max_length=50, blank=True, null=True)
    hiredate = models.DateField(db_column='HireDate', blank=True, null=True)
    specialization = models.CharField(db_column='Specialization', max_length=100, blank=True, null=True)
    yearsofexperience = models.IntegerField(db_column='YearsOfExperience', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'technician'


class Servicemanager(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING, db_column='User_ID', primary_key=True)
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)
    shift = models.CharField(db_column='Shift', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicemanager'


class Stockkeeper(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING, db_column='User_ID', primary_key=True)

    class Meta:
        managed = False
        db_table = 'stockkeeper'


class Financemanager(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING, db_column='User_ID', primary_key=True)

    class Meta:
        managed = False
        db_table = 'financemanager'


class Dataanalyst(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING, db_column='User_ID', primary_key=True)

    class Meta:
        managed = False
        db_table = 'dataanalyst'

class Topmanager(models.Model):
    manager_id = models.AutoField(db_column='Manager_ID', primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID')

    class Meta:
        managed = False
        db_table = 'topmanager'


class Supplier(models.Model):
    supplier_id = models.AutoField(db_column='Supplier_ID', primary_key=True)
    user = models.OneToOneField(Users, models.CASCADE, db_column='User_ID')
    company_name = models.CharField(db_column='Company_Name', max_length=100, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=20, default='Active')
    
    class Meta:
        managed = False
        db_table = 'supplier'
    
    def __str__(self):
        return self.company_name if self.company_name else str(self.user)


class SupplierPart(models.Model):
    part_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='parts')
    car_model = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'supplier_part'
        
    def __str__(self):
        return f"{self.name} ({self.code}) - {self.car_model}"

class PurchaseOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    supplier_part = models.ForeignKey(SupplierPart, on_delete=models.CASCADE)
    stock_keeper = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending') # Pending, Approved, Rejected, Delivered
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'purchase_order'

    def __str__(self):
        return f"PO-{self.order_id} - {self.supplier_part.name} ({self.quantity})"
