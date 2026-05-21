# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(db_column='Admin_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'


class Appointment(models.Model):
    appointment_id = models.AutoField(db_column='Appointment_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=11)  # Field name made lowercase.
    service_type = models.CharField(max_length=19)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'


class Certification(models.Model):
    certification_id = models.AutoField(db_column='Certification_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)  # Field name made lowercase.
    inspection = models.ForeignKey('Inspection', models.DO_NOTHING, db_column='Inspection_ID', blank=True, null=True)  # Field name made lowercase.
    issuedate = models.DateField(db_column='IssueDate', blank=True, null=True)  # Field name made lowercase.
    next_maint_date = models.DateField(db_column='Next_Maint_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'certification'


class Client(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.
    registrationdate = models.DateField(db_column='RegistrationDate', blank=True, null=True)  # Field name made lowercase.
    customercategory = models.CharField(db_column='CustomerCategory', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'client'


class Dataanalyst(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dataanalyst'


class Financemanager(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'financemanager'


class Inspection(models.Model):
    inspection_id = models.AutoField(db_column='Inspection_ID', primary_key=True)  # Field name made lowercase.
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)  # Field name made lowercase.
    jobcard = models.ForeignKey('Jobcard', models.DO_NOTHING, db_column='JobCard_ID', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    healthscore = models.IntegerField(db_column='HealthScore', blank=True, null=True)  # Field name made lowercase.
    healthcategory = models.CharField(db_column='HealthCategory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    results = models.TextField(db_column='Results', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inspection'


class Inventoryitem(models.Model):
    item_id = models.AutoField(db_column='Item_ID', primary_key=True)  # Field name made lowercase.
    itemnumber = models.IntegerField(db_column='ItemNumber', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    stockqty = models.IntegerField(db_column='StockQty', blank=True, null=True)  # Field name made lowercase.
    minstocklevel = models.IntegerField(db_column='MinStockLevel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inventoryitem'


class Invoice(models.Model):
    invoice_id = models.AutoField(db_column='Invoice_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    invoicedate = models.DateField(db_column='InvoiceDate', blank=True, null=True)  # Field name made lowercase.
    subtotallabor = models.DecimalField(db_column='SubtotalLabor', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotalparts = models.DecimalField(db_column='SubtotalParts', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    discount = models.DecimalField(db_column='Discount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice'


class Jobcard(models.Model):
    jobcard_id = models.AutoField(db_column='JobCard_ID', primary_key=True)  # Field name made lowercase.
    appointment_id = models.IntegerField(db_column='Appointment_ID', blank=True, null=True)  # Field name made lowercase.
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='Vehicle_ID', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    invoice_id = models.IntegerField(db_column='Invoice_ID', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    reportedissues = models.TextField(db_column='ReportedIssues', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totallaborcost = models.DecimalField(db_column='TotalLaborCost', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalpartscost = models.DecimalField(db_column='TotalPartsCost', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jobcard'


class Jobcardparts(models.Model):
    jobcard = models.OneToOneField(Jobcard, models.DO_NOTHING, db_column='JobCard_ID', primary_key=True)  # Field name made lowercase.
    item = models.ForeignKey(Inventoryitem, models.DO_NOTHING, db_column='Item_ID')  # Field name made lowercase.
    quantityused = models.IntegerField(db_column='QuantityUsed', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jobcardparts'
        unique_together = (('jobcard', 'item'),)


class Payment(models.Model):
    payment_id = models.AutoField(db_column='Payment_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='Invoice_ID', blank=True, null=True)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payment'


class Servicemanager(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)  # Field name made lowercase.
    shift = models.CharField(db_column='Shift', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'servicemanager'


class Stockkeeper(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stockkeeper'


class Technician(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.
    currentstatus = models.CharField(db_column='CurrentStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hiredate = models.DateField(db_column='HireDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'technician'


class Timelog(models.Model):
    timelog_id = models.AutoField(db_column='TimeLog_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    jobcard = models.ForeignKey(Jobcard, models.DO_NOTHING, db_column='JobCard_ID', blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
    totalhours = models.DecimalField(db_column='TotalHours', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'timelog'


class Users(models.Model):
    user_id = models.AutoField(db_column='User_ID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=14, blank=True, null=True)  # Field name made lowercase.
    profilepicture = models.CharField(db_column='ProfilePicture', max_length=255, blank=True, null=True)  # Field name made lowercase.
    resettoken = models.CharField(db_column='ResetToken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    resettokenexpiry = models.DateTimeField(db_column='ResetTokenExpiry', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'


class Vehicle(models.Model):
    vehicle_id = models.AutoField(db_column='Vehicle_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    vin = models.CharField(db_column='VIN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    platenumber = models.CharField(db_column='PlateNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    mileage = models.IntegerField(db_column='Mileage', blank=True, null=True)  # Field name made lowercase.
    make = models.CharField(db_column='Make', max_length=50, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vehicle'
