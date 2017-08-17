from __future__ import unicode_literals

from django.db import models
from login.models import EmployeeDropdown,EmployeePrimdetail
# Create your models here.

class EmployeePerdetail(models.Model):
    fname = models.CharField(db_column='FName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mname = models.CharField(db_column='MName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    bg = models.ForeignKey(EmployeeDropdown,db_column='Bg', related_name='BloodGroup', blank=True, null=True)  # Field name made lowercase.
    gender = models.ForeignKey(EmployeeDropdown,db_column='Gender', related_name='Gender', blank=True, null=True)  # Field name made lowercase.
    nationality = models.ForeignKey(EmployeeDropdown,db_column='Nationality', related_name='nationality', blank=True, null=True)  # Field name made lowercase.
    caste = models.ForeignKey(EmployeeDropdown, related_name='caste',db_column='Caste', blank=True, null=True)  # Field name made lowercase.
    marital_status = models.ForeignKey(EmployeeDropdown, related_name='marital_status',db_column='Marital_status', blank=True, null=True)  # Field name made lowercase.
    religion = models.ForeignKey(EmployeeDropdown, related_name='religion',db_column='Religion', blank=True, null=True)  # Field name made lowercase.
    image_path = models.CharField(max_length=500, blank=True, null=True)
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_per', primary_key=True, unique=True, max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'employee_perdetail'


class EmployeeAcademic(models.Model):
    pass_year_10 = models.IntegerField(db_column='Pass_Year_10', blank=True, null=True)  # Field name made lowercase.
    board_10 = models.ForeignKey(EmployeeDropdown,db_column='Board_10', related_name='board10', blank=True, null=True)  # Field name made lowercase.
    cgpa_per_10 = models.DecimalField(db_column='Cgpa_Per_10', max_digits=5, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pass_year_12 = models.IntegerField(db_column='Pass_Year_12', blank=True, null=True)  # Field name made lowercase.
    board_12 = models.ForeignKey(EmployeeDropdown,db_column='Board_12', related_name='board12', blank=True, null=True)  # Field name made lowercase.
    cgpa_per_12 = models.DecimalField(db_column='Cgpa_Per_12', max_digits=5, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pass_year_dip = models.IntegerField(db_column='Pass_Year_Dip', blank=True, null=True)  # Field name made lowercase.
    univ_dip = models.ForeignKey(EmployeeDropdown, related_name='DiplomaUniversity',db_column='Univ_Dip', blank=True, null=True)  # Field name made lowercase.
    cgpa_per_dip = models.DecimalField(db_column='Cgpa_Per_Dip', max_digits=5, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pass_year_ug = models.IntegerField(db_column='Pass_Year_Ug', blank=True, null=True)  # Field name made lowercase.
    univ_ug = models.ForeignKey(EmployeeDropdown,db_column='Univ_UG', related_name='UG_University', blank=True, null=True)  # Field name made lowercase.
    degree_ug = models.ForeignKey(EmployeeDropdown,db_column='Degree_UG', related_name='UG_Degree', blank=True, null=True)  # Field name made lowercase.
    cgpa_per_ug = models.DecimalField(db_column='Cgpa_Per_Ug', max_digits=5, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pass_year_pg = models.IntegerField(db_column='Pass_Year_Pg', blank=True, null=True)  # Field name made lowercase.
    univ_pg = models.ForeignKey(EmployeeDropdown,db_column='Univ_PG', related_name='PG_University', blank=True, null=True)  # Field name made lowercase.
    degree_pg = models.ForeignKey(EmployeeDropdown,db_column='Degree_PG', related_name='PG_Degree', blank=True, null=True)  # Field name made lowercase.
    cgpa_per_pg = models.DecimalField(db_column='Cgpa_Per_Pg', max_digits=5, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    area_spl_pg = models.IntegerField(db_column='Area_Spl_Pg', blank=True, null=True)  # Field name made lowercase.
    doctrate = models.CharField(db_column='doctrate', max_length=200, blank=True, null=True)  # Field name made lowercase.
    univ_doctrate = models.ForeignKey(EmployeeDropdown,db_column='Univ_Doctrate', related_name='DoctrateUniversity', blank=True, null=True)  # Field name made lowercase.
    date_doctrate = models.DateField(db_column='Date_Doctrate', blank=True, null=True)  # Field name made lowercase.
    stage_doctrate = models.ForeignKey(EmployeeDropdown,db_column='Stage_Doctrate', related_name='stage_doctrate', blank=True, null=True)  # Field name made lowercase.
    research_topic_doctrate = models.CharField(db_column='Research_topic_doctrate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    degree_other = models.ForeignKey(EmployeeDropdown,db_column='Degree_Other', related_name='DegreeOther', blank=True, null=True)  # Field name made lowercase.
    pass_year_other = models.IntegerField(db_column='Pass_Year_Other', blank=True, null=True)  # Field name made lowercase.
    univ_other = models.ForeignKey(EmployeeDropdown,db_column='Univ_Other', related_name='OtherUniversity', blank=True, null=True)  # Field name made lowercase.
    cgpa_per_other = models.DecimalField(db_column='Cgpa_Per_Other', max_digits=5, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    area_spl_other = models.CharField(db_column='Area_Spl_Other', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_academic', primary_key=True, unique=True, max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'employee_academic'

class EmployeeDocuments(models.Model):
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_doc', primary_key=True, unique=True, max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.
    marksheet_10 = models.CharField(db_column='Marksheet_10', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marksheet_12 = models.CharField(db_column='Marksheet_12', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marksheet_dip = models.CharField(db_column='Marksheet_Dip', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marksheet_ug = models.CharField(db_column='Marksheet_Ug', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marksheet_pg = models.CharField(db_column='Marksheet_Pg', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marksheet_doctrate = models.CharField(db_column='Marksheet_Doctrate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marksheet_other = models.CharField(db_column='Marksheet_Other', max_length=50, blank=True, null=True)  # Field name made lowercase.
    medical_fitness = models.CharField(db_column='Medical_Fitness', max_length=50, blank=True, null=True)  # Field name made lowercase.
    character_certificate = models.CharField(db_column='Character_Certificate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    experience_certificate = models.CharField(db_column='Experience_Certificate', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'employee_documents'

class EmployeeAddress(models.Model):
    p_add1 = models.CharField(db_column='P_Add1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p_add2 = models.CharField(db_column='P_Add2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p_city = models.CharField(db_column='P_City', max_length=30, blank=True, null=True)  # Field name made lowercase.
    p_district = models.CharField(db_column='P_District', max_length=30, blank=True, null=True)  # Field name made lowercase.
    p_state = models.ForeignKey(EmployeeDropdown,db_column='P_State', related_name='PermanentState', blank=True, null=True)  # Field name made lowercase.
    p_pincode = models.CharField(db_column='P_Pincode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    c_add1 = models.CharField(db_column='C_Add1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    c_add2 = models.CharField(db_column='C_Add2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    c_city = models.CharField(db_column='C_City', max_length=30, blank=True, null=True)  # Field name made lowercase.
    c_district = models.CharField(db_column='C_District', max_length=30, blank=True, null=True)  # Field name made lowercase.
    c_state = models.ForeignKey(EmployeeDropdown,db_column='C_State', related_name='CorrespondenceState', blank=True, null=True)  # Field name made lowercase.
    c_pincode = models.CharField(db_column='C_Pincode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_addr', primary_key=True, unique=True, max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'employee_address'

class EmployeeResearch(models.Model):
    research_years = models.IntegerField(db_column='Research_Years', blank=True, null=True)  # Field name made lowercase.
    research_months = models.IntegerField(db_column='Research_Months', blank=True, null=True)  # Field name made lowercase.
    industry_years = models.IntegerField(db_column='Industry_Years', blank=True, null=True)  # Field name made lowercase.
    industry_months = models.IntegerField(db_column='Industry_Months', blank=True, null=True)  # Field name made lowercase.
    teaching_years = models.IntegerField(db_column='Teaching_Years', blank=True, null=True)  # Field name made lowercase.
    teaching_months = models.IntegerField(db_column='Teaching_Months', blank=True, null=True)  # Field name made lowercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_research', primary_key=True, unique=True, max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'employee_research'

class EmployeePayroll(models.Model):
    bank_ac_no = models.CharField(db_column='Bank_Ac_No', max_length=25, blank=True, null=True)  # Field name made lowercase.
    uan_no = models.CharField(db_column='Uan_No', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pan_no = models.CharField(db_column='Pan_No', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aadhar_no = models.CharField(db_column='Aadhar_No', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pf_deduction = models.CharField(db_column='Pf_Deduction', max_length=3, blank=True, null=True)  # Field name made lowercase.
    salary_type = models.ForeignKey(EmployeeDropdown,db_column='Salary_Type', related_name='SalaryType', blank=True, null=True)  # Field name made lowercase.
    basic = models.DecimalField(db_column='Basic', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    agp = models.DecimalField(db_column='Agp', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    da = models.DecimalField(db_column='Da', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    hra = models.DecimalField(db_column='Hra', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    other_allowances = models.DecimalField(db_column='Other_Allowances', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    mediclaim = models.CharField(db_column='Mediclaim', max_length=3, blank=True, null=True)  # Field name made lowercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_payroll', primary_key=True, unique=True, max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'employee_payroll'

'''class NewEmployeeNewEmployee(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField()
    timestamp = models.DateTimeField()'''

class Reporting(models.Model):
    sno = models.AutoField(db_column='Sno', primary_key=True)  # Field name made lowercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_rep', max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.
    reporting_to = models.ForeignKey(EmployeeDropdown,db_column='Reporting_To', related_name='Designation', blank=True, null=True)  # Field name made lowercase.
    department = models.ForeignKey(EmployeeDropdown,db_column='Department', related_name='Department', blank=True, null=True)  # Field name made lowercase.
    reporting_no = models.IntegerField(db_column='Reporting_No', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'reporting'

class Roles(models.Model):
    sno = models.AutoField(db_column='Sno', primary_key=True)  # Field name made lowercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='employee_id_role', max_length=20, on_delete=models.CASCADE)  # Field name made lowercase.
    roles = models.ForeignKey(EmployeeDropdown,db_column='roles', related_name='role', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'roles'

class NoDuesHead(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase                                                                                       owercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='nodue_emp', blank=True, null=True) # Field name made lowercase                                                                                        l=True)  # Field name made lowercase.
    due_head = models.ForeignKey(EmployeeDropdown,db_column='Due_Head', related_name='nodue_head', blank=True, null=True) # Field name made lowercase 
    status = models.CharField(db_column='Status', max_length=15, blank=True, default='ACTIVE')  # Field name made lowercase
    

    class Meta:
        db_table = 'no_dues_head'

class NoDuesEmp(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase                                                                                        owercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='emp_id_due', blank=True, null=True)  # Field name made lowercase                                                                              l=True)  # Field name made lowercase.
    head_id = models.ForeignKey(NoDuesHead,db_column='Head_Id', related_name='emp_id_head', blank=True, null=True) # Field name made lowercase                                                                                       ull=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=15, blank=True, null=True)  # Field name made lowercase                                                                                      l=True)  # Field name made lowercase.

    class Meta:
        db_table = 'no_dues_employee'



class EmployeeSeparation(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    emp_id = models.ForeignKey(EmployeePrimdetail,db_column='Emp_Id', related_name='emp_id_sepration', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    type = models.ForeignKey(EmployeeDropdown,db_column='Type', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rejoin_date = models.DateField(db_column='Rejoin_Date', blank=True, null=True)  # Field name made lowercase.
    emp_remark = models.CharField(db_column='Emp_Remark', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    hod_status = models.CharField(db_column='HOD_Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    hod_remark = models.CharField(db_column='HOD_Remark', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    hr_status = models.CharField(db_column='HR_Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    hr_remark = models.CharField(db_column='HR_Remark', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    attachment = models.CharField(db_column='Attachment', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'employee_separation'

class Shifts(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
	shiftid = models.ForeignKey(EmployeeDropdown,db_column='shiftId', related_name='emp_shift', blank=True, null=True)
	intime = models.TimeField(db_column='intime',max_length=10, blank=True, null=True)
	outtime = models.TimeField(db_column='outtime',max_length=10, blank=True, null=True)
	latein = models.TimeField(db_column='lateIn', max_length=10, blank=True, null=True)  # Field name made lowercase.
	earlyexit = models.TimeField(db_column='earlyExit', max_length=10, blank=True, null=True)  # Field name made lowercase.
	fulldaytime = models.TimeField(db_column='fullDayTime', max_length=10, blank=True, null=True)  # Field name made lowercase.
	halfdaytime = models.TimeField(db_column='halfDayTime', max_length=10, blank=True, null=True)  # Field name made lowercase.
	breakstart = models.TimeField(db_column='breakStart', max_length=10, blank=True, null=True)  # Field name made lowercase.
	breakend = models.TimeField(db_column='breakEnd', max_length=10, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		db_table = 'shifts'
