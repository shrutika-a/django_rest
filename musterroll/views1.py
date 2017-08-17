from django.shortcuts import render
from .models import EmployeeAcademic,EmployeeDocuments,EmployeeSeparation,EmployeeAddress,EmployeeResearch,Roles,Reporting,EmployeePerdetail,NoDuesEmp,NoDuesHead,Shifts,EmployeePayroll
from dashboard.models import LeftPanel
from django.http import JsonResponse
from django.db.models import F
import json
import time
from django.contrib.auth.models import User
from login.views import check
from login.models import EmployeePrimdetail,EmployeeDropdown,AuthUser


# Create your views here.

################################################## VIEWS FOR ADD EMPLOYEE ##################################################

def category_value(request):
	error=True
	field=""
	msg=""
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			data=json.loads(request.body)
			field_id=data['emp_category']	
			j=0
			field = EmployeeDropdown.objects.filter(pid=field_id).exclude(value__isnull=True).extra(select={'category_id':'sno','category_name':'value'}).values('category_id','category_name')
			for x in range(0,len(field)):
				test=EmployeeDropdown.objects.filter(pid=field[x]['category_id']).exclude(value__isnull=True).extra(select={'subid': 'sno','subvalue':'value'}).values('subid','subvalue')
				field[x]['subcategory']=list(test)
				
			error=False
			
		else:
			msg="not authenticated"
	else:
		msg="invalid session"
	a={'error':error,'msg':msg,'data':list(field)}
	return JsonResponse(a,safe=False)

def fields(request):
	error=True
	field=""
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			#print(request.session['roles'])
			if 'HR' in request.session['roles']:
				field = EmployeeDropdown.objects.extra(select={'valueid': 'sno','value':'field'}).exclude(value__isnull=False).values('valueid','value')
				msg="Success"
				error=False
			else:
				msg="not authorised"
		else:
			msg="not authenticated"
	else:
		msg="invalid session"
	a={'error':error,'msg':msg,'data':list(field)}
	return JsonResponse(a, safe=False)	
	
def show_category(request):
	error=True
	cat=""
	msg=""
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if 'HR' in request.session['roles']:
				body=json.loads(request.body)
				sno=body['Sno']
				names=EmployeeDropdown.objects.filter(sno=sno).values('field')
				name=names[0]['field']
				cat=EmployeeDropdown.objects.filter(field=name).exclude(value__isnull=True).extra(select={'valueid': 'sno','parentId':'pid','cat':'field','text1':'value'}).values('valueid', 'parentId', 'cat', 'text1')
				for x in range(0,len(cat)):
					test=EmployeeDropdown.objects.filter(pid=cat[x]['valueid']).exclude(value__isnull=True).extra(select={'subid': 'sno','subvalue':'value'}).values('subid','subvalue')
					cat[x]['subcategory']=list(test)
				error=False
			else:
				msg="not authorized"
		else:
			msg="not authenticated"
	else:
		msg="invalid session"
	a={'error':error,'msg':msg,'data':list(cat)}
	return JsonResponse(a,safe=False)
	
def add_cat(request):
	error=True
	msg=""
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if 'HR' in request.session['roles']:
				body1 = json.loads(request.body)
				for body in body1:
					#print(body['parentid'])
					pid = body['parentid']
					value=body['val'].upper()
					field_id=body['cat']
					field_qry=EmployeeDropdown.objects.filter(sno=field_id).values('field')
					field=field_qry[0]['field']
					if pid != 0:
						field_qry=EmployeeDropdown.objects.filter(sno=field_id).values('value')
						field=field_qry[0]['value']
						cnt=EmployeeDropdown.objects.filter(field=field).values('sno')
						if len(cnt)==0:
							add=EmployeeDropdown.objects.create(pid=pid,field=field)
					add=EmployeeDropdown.objects.create(pid=pid,field=field,value=value)
				error=False
				msg="Successfully Inserted"
			else:
				msg="not authorized"
		else:
			msg="not authenticated"
	else:
		msg="invalid session"
	a={'msg':msg,'error':error}
	return JsonResponse(a, safe=False)
	
def update_cat(request):
	error=True
	msg=""
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if 'HR' in request.session['roles']:
				body = json.loads(request.body)
				sno = body['sno1']
				val=body['val'].upper()
				field_qry=EmployeeDropdown.objects.filter(sno=sno).values('pid','value')
				#print(field_qry[0])
				pid=field_qry[0]['pid']
				value=field_qry[0]['value']
				add=EmployeeDropdown.objects.filter(pid=pid,field=value).update(field=val)
				add=EmployeeDropdown.objects.filter(sno=sno).update(value=val)
				error=False
				msg="Successfully Updated"
			else:
				msg="not authorized"
		else:
			msg="not authenticated"
	else:
		msg="invalid session"
	a={'msg':msg,'error':error}
	return JsonResponse(a, safe=False)
	
def delete_cat(request):
	error=True
	msg=""
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if 'HR' in request.session['roles']:
				body = json.loads(request.body)
				sno = body['sno']
				deletec(sno)
				error=False
				msg="Successfully Deleted"
			else:
				msg="not authorized"
		else:
			msg="not authenticated"
	else:
		msg="invalid session"
	a={'msg':msg,'error':error}
	return JsonResponse(a, safe=False)
	
def deletec(pid):
	qry=EmployeeDropdown.objects.filter(pid=pid).values('sno')
	if len(qry)>0:
		for x in qry:
			deletec(x['sno'])
	qry=EmployeeDropdown.objects.filter(sno=pid).delete()
	
def add_employee(request):
	error=True
	data_values=""
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():

			#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
			qry1=EmployeeDropdown.objects.filter(field="TYPE OF EMPLOYMENT").exclude(value__isnull=True).extra(select={'v':'value','s':'sno'}).values('v','s')
			
			qry2=EmployeeDropdown.objects.filter(field="CATEGORY OF EMPLOYEE").exclude(value__isnull=True).extra(select={'ev':'value','es':'sno'}).values('ev','es')
			#qry3=EmployeeDropdown.objects.filter(field="DESIGNATION").exclude(value__isnull=True).extra(select={'dv':'value','ds':'sno'}).values('dv','ds')
			
			qry2_a=EmployeeDropdown.objects.filter(field='STATE').exclude(value__isnull=True).extra(select={'state_id':'sno','state_name':'value'}).values('state_id','state_name')

			qry3=EmployeeDropdown.objects.filter(value="DESIGNATION").exclude(value__isnull=True).extra(select={'id':'sno','field':'field'}).values('id','field')
			qry_len=len(qry3)
			for x in range(0,qry_len):
				qry3_a=EmployeeDropdown.objects.filter(pid=qry3[x]['id']).exclude(value__isnull=True).extra(select={'desg_id':'sno','desg_name':'value'}).values('desg_id','desg_name')
				qry3[x]['designation']=list(qry3_a)
			qry4=EmployeeDropdown.objects.filter(field="SHIFT SETTINGS").exclude(value__isnull=True).extra(select={'sv':'value','ss':'sno'}).values('sv','ss')
			#print(qry4)
			#l=0
			arr=[]
			arr1=[]
			#print(qry3)

###################################################################################################################################################################

# THE FOLLOWING COMMENTED CODE IS FOR THE CASE IF ANY NEW CATEGORY IS ADDED IN SHIFT SETTINGS IN EMPLOYEE EmployeeDropdown OTHER THAN FIX AND FLEXIBLE

####################################################################################################################################################################

			'''	if qry4.count()>0:
				for i in qry4:
					#print(i)
					sub_value_id=i['ss']
					print(sub_value_id)
					qry4_a=EmployeeDropdown.objects.filter(pid=sub_value_id).exclude(value__isnull=True).extra(select={'subvalue_id':'sno','subvalue':'value'}).values('subvalue_id','subvalue')
					#print(qry4_a)
					k=0
					for j in qry4_a:
						arr.append(qry4_a[k]['subvalue'])
						arr1.append(qry4_a[k]['subvalue_id'])
						#print("hi")
						k=k+1
					
					qry4[l]['sub_field']=arr
					arr=[]
					qry4[l]['sub_value_id']=arr1
					arr1=[]
					#print("Hi")#
					#qry4[a]['sub_value_id']=qry4[0]['subvalue_id']
					l=l+1
			print(qry4)'''
			
			qry5=EmployeeDropdown.objects.filter(field="TITLE").exclude(value__isnull=True).extra(select={'tv':'value','ts':'sno'}).values('tv','ts')
			
			qry6=EmployeeDropdown.objects.filter(field="POSITION").exclude(value__isnull=True).extra(select={'pv':'value','ps':'sno'}).values('pv','ps')
			qry7=EmployeeDropdown.objects.filter(field="ROLES").exclude(value__isnull=True).extra(select={'av':'value','as':'sno'}).values('av','as')
			qry8=EmployeeDropdown.objects.filter(field="BLOOD GROUP").exclude(value__isnull=True).extra(select={'bv':'value','bs':'sno'}).values('bv','bs')
			qry9=EmployeeDropdown.objects.filter(field="GENDER").exclude(value__isnull=True).extra(select={'gv':'value','gs':'sno'}).values('gv','gs')
			qry10=EmployeeDropdown.objects.filter(field="NATIONALITY").exclude(value__isnull=True).extra(select={'nv':'value','ns':'sno'}).values('nv','ns')
			qry11=EmployeeDropdown.objects.filter(field="CASTE").exclude(value__isnull=True).extra(select={'cv':'value','cs':'sno'}).values('cv','cs')
			qry12=EmployeeDropdown.objects.filter(field="MARITAL STATUS").exclude(value__isnull=True).extra(select={'mv':'value','ms':'sno'}).values('mv','ms')
			qry13=EmployeeDropdown.objects.filter(field="RELIGION").exclude(value__isnull=True).extra(select={'rv':'value','rs':'sno'}).values('rv','rs')
			qry14=EmployeeDropdown.objects.filter(field="DEPARTMENT").exclude(value__isnull=True).extra(select={'dev':'value','des':'sno'}).values('dev','des')
			qry15=EmployeeDropdown.objects.filter(field="REGULAR").exclude(value__isnull=True).extra(select={'rev':'value','rs':'sno'}).values('rs','rev')
			qry16=EmployeeDropdown.objects.filter(field="FIX").exclude(value__isnull=True).extra(select={'fiv':'value','fis':'sno'}).values('fis','fiv')
			qry17=EmployeeDropdown.objects.filter(field="FLEXIBLE").exclude(value__isnull=True).extra(select={'flv':'value','fls':'sno'}).values('fls','flv')
			
			qry19=EmployeeDropdown.objects.filter(field="UNIVERSITY").exclude(value__isnull=True).extra(select={'uv':'value','us':'sno'}).values('uv','us')
			qry20=EmployeeDropdown.objects.filter(field="BOARD").exclude(value__isnull=True).extra(select={'bov':'value','bos':'sno'}).values('bov','bos')
			qry21=EmployeeDropdown.objects.filter(field="DEGREE").exclude(value__isnull=True).extra(select={'dgv':'value','dgs':'sno'}).values('dgv','dgs')
			qry22=EmployeeDropdown.objects.filter(field="P.HD. STAGE").exclude(value__isnull=True).extra(select={'stv':'value','sts':'sno'}).values('stv','sts')
			#qry23=EmployeeDropdown.objects.filter(field="DOCTRATE").exclude(value__isnull=True).extra(select={'doc_val':'value','doc_id':'sno'}).values('doc_val','doc_id')
			qry23=EmployeeDropdown.objects.filter(field="ORGANIZATION").exclude(value__isnull=True).extra(select={'org_id':'sno','org_name':'value'}).values('org_id','org_name')

			#print(qry16)
			#print(qry17)
			msg="Success"
			error=False
			#else:
				#msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"

	data_to_be_sent={'error':error,'msg':msg,'data':{'toe':list(qry1),'coe':list(qry2),'state':list(qry2_a),'desg':list(qry3),'shift':list(qry4),'title':list(qry5),'cp':list(qry6),'ar':list(qry7),'bg':list(qry8),'gender':list(qry9),'nationality':list(qry10),'caste':list(qry11),'ms':list(qry12),'re':list(qry13),'dept':list(qry14),'regular':list(qry15),'fix':list(qry16),'flexible':list(qry17),'uni':list(qry19),'board':list(qry20),'degree':list(qry21),'stage':list(qry22),'organization':list(qry23)}}
	#return HttpResponse(msg)
	return JsonResponse(data_to_be_sent,safe=False)

###########################################################ADD PAYROLL###################################################################	

def add_pay(request):
	error="true"
	data_values=""
	if 'HTTP_COOKIE' in request.META:
		
		#if request.user.is_authenticated():
		#	if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
		data = json.loads(request.body.decode('utf-8'))
		#print(data)
		emp_pay={}
		if 'bank_ac_no' in data:
			emp_pay['bank_ac_no'] = data['bank_ac_no']
		else:
			emp_pay['bank_ac_no'] = None
		if 'uan_no' in data:
			emp_pay['uan_no'] = data['uan_no']
		else:
			emp_pay['uan_no'] = None
		if 'pan_no' in data:
			emp_pay['pan_no'] = data['pan_no']
		else:
			emp_pay['pan_no'] = None
		if 'aadhar_no' in data:
			emp_pay['aadhar_no'] = data['aadhar_no']
		else:
			emp_pay['aadhar_no'] = None
		if 'pf_deduction' in data:
			emp_pay['pf_deduction'] = data['pf_deduction']
		else:
			emp_pay['pf_deduction'] = None
		if 'salary_type' in data:
			emp_pay['salary_type'] = EmployeeDropdown.objects.get(sno=data['salary_type'])
		else:
			emp_pay['salary_type'] = None
		if 'basic' in data:
			emp_pay['basic'] = data['basic']
		else:
			emp_pay['basic'] = None
		if 'agp' in data:
			emp_pay['agp'] = data['agp']
		else:
			emp_pay['agp'] = None
		if 'da' in data:
			emp_pay['da'] = data['da']
		else:
			emp_pay['da'] = None
		if 'hra' in data:
			emp_pay['hra'] = data['hra']
		else:
			emp_pay['hra'] = None
		if 'other_allowances' in data:
			emp_pay['other_allowances'] = data['other_allowances']
		else:
			emp_pay['other_allowances'] = None
		if 'mediclaim' in data:
			emp_pay['mediclaim'] = data['mediclaim']
		else:
			emp_pay['mediclaim'] = None
		if 'emp_id' in data:
			emp_pay['emp_id'] = EmployeePrimdetail.objects.get(emp_id=data['emp_id'])
		else:
			emp_pay['emp_id'] = None
		if emp_pay:
			if EmployeePayroll.objects.filter(emp_id=emp_pay['emp_id']).count() < 1:
				qry = EmployeePayroll.objects.create(**emp_pay)
			
				msg="Data Successfully Added..."
				error=False
			else:
				msg="Data Already Exists..."
			#else:
			#	msg="Not Permitted!!"
		#else:
		#	msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"

	res={'msg':msg,'error':error}
	return JsonResponse(res,safe=False)

############################################################ADD EMPLOYEE##############################################
def field_add(request):
	data_values=""	
	error=True
	#print(request.META)
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
				data = json.loads(request.body)
				emp_per={}
				emp_prim={}
				address={}
				reporting={}
				role={}
				emp_acad={}
				emp_research={}
				emp_doc={}
				emp=AuthUser.objects.extra({'user':"CAST(username as UNSIGNED)"}).order_by('-user').values('user')
				emp_id=int(emp[0]['user'])+1
				if 'email' in data:
					email=data['email']
				else:
					email='kiet.'+emp_id+'@kiet.edu'
				na=data['name']
				name=na.split()
				ln=''
				fn=''
				size=len(name)
				if size>1:
					fn=na.rsplit(' ', 1)[0]
					ln=name[len(name)-1]
				else:
					fn=na
					ln=''
				user = User.objects.create_user(emp_id, email, 'ERP@123')
				user.first_name = fn
				user.last_name = ln
				user.user_type = 'Employee'
				user.save()
				#print(data['diploma_degree_path'])
				emp_prim['emp_id']=AuthUser.objects.get(username=emp_id)
				if 'organization' in data:
					emp_prim['organization']=EmployeeDropdown.objects.get(sno=data['organization'])
				else:
					emp_prim['organization']=None
				if 'category_cadre' in data:
					emp_prim['cadre']=EmployeeDropdown.objects.get(sno=data['category_cadre'])
				else:
					emp_prim['cadre']=None
				if 'category_lader' in data:
					emp_prim['ladder']=EmployeeDropdown.objects.get(sno=data['category_lader'])
				else:
					emp_prim['ladder']=None
				if 'name' in data:
					emp_prim['name']=data['name']
				else:
					emp_prim['name']=None
				if 'fname' in data:
					emp_per['fname']=data['fname']
				else:
					emp_per['fname']=None
				if 'image' in data:
					emp_per['image_path']=data['image']
				else:
					emp_per['image_path']=None
				if 'mname' in data:
					emp_per['mname']=data['mname']
				else:
					emp_per['mname']=None
				if 'dob' in data:
					emp_per['dob']=data['dob']
				else:
					emp_per['dob']=None
				if 'title' in data:
					emp_prim['title']=EmployeeDropdown.objects.get(sno=data['title'])
				else:
					emp_prim['title']=None
				if 'shift' in data:
					emp_prim['shift'] =EmployeeDropdown.objects.get(sno=data['shift'])
				else:
					emp_prim['shift']=None
				if 'emp_category' in data:
					emp_prim['emp_category']=EmployeeDropdown.objects.get(sno=data['emp_category'])
				else:
					emp_prim['emp_category']=None
				if 'desg' in data:
					emp_prim['desg']=EmployeeDropdown.objects.get(sno=data['desg'])
				else:
					emp_prim['desg']=None
				if 'emp_type' in data:
					emp_prim['emp_type']=EmployeeDropdown.objects.get(sno=data['emp_type'])
				else:
					emp_prim['emp_type']=None
				
				if 'dept' in data:
					emp_prim['dept']=EmployeeDropdown.objects.get(sno=data['dept'])
				else:
					emp_prim['dept']=None
				if 'bg' in data:
					emp_per['bg']=EmployeeDropdown.objects.get(sno=data['bg'])
				else:
					emp_per['bg']=None
				if 'gender' in data:
					emp_per['gender']=EmployeeDropdown.objects.get(sno=data['gender'])
				else:
					emp_per['gender']=None
				if 'current_pos' in data:
					emp_prim['current_pos']=EmployeeDropdown.objects.get(sno=data['current_pos'])
				else:
					emp_prim['current_pos']=None
				if 'reporting_no' in data :
					reporting['reporting_no']=data['reporting_no']
				else:
					reporting['reporting_no']=None
				if 'department' in data :
					reporting['department']=data['department']
				else:
					reporting['department']=None
				if 'designation' in data :
					reporting['reporting_to']=sno=data['designation']
				else:
					reporting['reporting_to']=None
				if 'nationality' in data:
					emp_per['nationality']=EmployeeDropdown.objects.get(sno=data['nationality'])
				else:
					emp_per['nationality']=None
				if 'caste' in data:
					emp_per['caste']=EmployeeDropdown.objects.get(sno=data['caste'])
				else:
					emp_per['caste']=None
				if 'marital_status' in data:
					emp_per['marital_status']=EmployeeDropdown.objects.get(sno=data['marital_status'])
				else:
					emp_per['marital_status']=None
				if 'religion' in data:
					emp_per['religion']=EmployeeDropdown.objects.get(sno=data['religion'])
				else:
					emp_per['religion']=None
				if 'roles' in data:
					role['roles']=data['roles']
				else:
					role['roles']=None
				if 'p_add1' in data:
					address['p_add1']=data['p_add1']
				else:
					address['p_add1']=None
				if 'p_add2' in data:
					address['p_add2']=data['p_add2']
				else:
					address['p_add2']=None
				if 'p_city' in data:
					address['p_city']=data['p_city']
				else:
					address['p_city']=None
				if 'p_district' in data:
					address['p_district']=data['p_district']
				else:
					address['p_district']=None
				if 'p_state' in data and data['p_state']!=None:
					address['p_state']=EmployeeDropdown.objects.get(sno=data['p_state'])
				else:
					address['p_state']=None
				if 'p_pincode' in data:
					address['p_pincode']=data['p_pincode']
				else:
					address['p_pincode']=None
				if 'c_add1' in data:
					address['c_add1']=data['c_add1']
				else:
					address['c_add1']=None
				if 'c_add2' in data:
					address['c_add2']=data['c_add2']
				else:
					address['c_add2']=None
				if 'c_city' in data:
					address['c_city']=data['c_city']
				else:
					address['c_city']=None
				if 'c_district' in data:
					address['c_district']=data['c_district']
				else:
					address['c_district']=None
				if 'c_state' in data and data['c_state']!=None:
					address['c_state']=EmployeeDropdown.objects.get(sno=data['c_state'])
				else:
					address['c_state']=None
				if 'c_pincode' in data:
					address['c_pincode']=data['c_pincode']
				else:
					address['c_pincode']=None
				if 'mob' in data:
					emp_prim['mob']=data['mob']
				else:
					emp_prim['mob']=None
				if 'join_date' in data:
					emp_prim['doj']=data['join_date']
				else:
					emp_prim['doj']=None
				if 'mob1' in data:
					emp_prim['mob1']=data['mob1']
				else:
					emp_prim['mob1']=None
				if 'email' in data:
					emp_prim['email']=data['email']
				else:
					emp_prim['email']=None
				if 'pass_year_10' in data:
					emp_acad['pass_year_10'] =data['pass_year_10']
				else:
					emp_acad['pass_year_10']=None
				if 'board_10' in data and data['board_10']!=None:
					emp_acad['board_10'] = EmployeeDropdown.objects.get(sno=data['board_10'])
				else:
					emp_acad['board_10']=None
				if 'cgpa_per_10' in data:
					emp_acad['cgpa_per_10'] = data['cgpa_per_10']
				else:
					emp_acad['cgpa_per_10']=None
				if '10th_marksheet_path' in data:
					emp_doc['marksheet_10'] = data['10th_marksheet_path']
				else:
					emp_doc['marksheet_10']=None
				if 'pass_year_12' in data:
					emp_acad['pass_year_12'] = data['pass_year_12']
				else:
					emp_acad['pass_year_12']=None
				if 'board_12' in data and data['board_12']!=None:
					emp_acad['board_12'] = EmployeeDropdown.objects.get(sno=data['board_12'])
				else:
					emp_acad['board_12']=None
				if 'cgpa_per_12' in data:
					emp_acad['cgpa_per_12'] = data['cgpa_per_12']
					print(emp_acad['cgpa_per_12'])
				else:
					emp_acad['cgpa_per_12']=None
					print('Hii')
				if '12th_marksheet_path' in data:
					emp_doc['marksheet_12'] = data['12th_marksheet_path']
				else:
					emp_doc['marksheet_12']=None
				if 'pass_year_dip' in data:
					emp_acad['pass_year_dip'] = data['pass_year_dip']
				else:
					emp_acad['pass_year_dip']=None
				if 'univ_dip' in data and data['univ_dip']!=None:
					emp_acad['univ_dip'] = EmployeeDropdown.objects.get(sno=data['univ_dip'])
				else:
					emp_acad['univ_dip']=None
				if 'cgpa_per_dip' in data:
					emp_acad['cgpa_per_dip'] = data['cgpa_per_dip']
				else:
					emp_acad['cgpa_per_dip']=None
				if 'diploma_degree_path' in data:
					emp_doc['marksheet_dip'] = data['diploma_degree_path']
				else:
					emp_doc['marksheet_dip']=None
				if 'pass_year_ug' in data:
					emp_acad['pass_year_ug'] = data['pass_year_ug']
				else:
					emp_acad['pass_year_ug']=None
				if 'univ_ug' in data and data['univ_ug']!=None:
					emp_acad['univ_ug'] = EmployeeDropdown.objects.get(sno=data['univ_ug'])
				else:
					emp_acad['univ_ug']=None
				if 'degree_ug' in data and data['degree_ug']!=None:
					emp_acad['degree_ug'] = EmployeeDropdown.objects.get(sno=data['degree_ug'])
				else:
					emp_acad['degree_ug']=None
				if 'cgpa_per_ug' in data:
					emp_acad['cgpa_per_ug'] = data['cgpa_per_ug']
				else:
					emp_acad['cgpa_per_ug']=None
				if 'ug_degree_path' in data:
					emp_doc['marksheet_ug'] = data['ug_degree_path']
				else:
					emp_doc['marksheet_ug']=None
				if 'pass_year_pg' in data:
					emp_acad['pass_year_pg'] = data['pass_year_pg']
				else:
					emp_acad['pass_year_pg']=None
				if 'univ_pg' in data and data['univ_pg']!=None:
					emp_acad['univ_pg'] = EmployeeDropdown.objects.get(sno=data['univ_pg'])
				else:
					emp_acad['univ_pg']=None
				if 'degree_pg' in data and data['degree_pg']!=None:
					emp_acad['degree_pg'] = EmployeeDropdown.objects.get(sno=data['degree_pg'])
				else:
					emp_acad['degree_pg']=None
				if 'cgpa_per_pg' in data:
					emp_acad['cgpa_per_pg'] = data['cgpa_per_pg']
				else:
					emp_acad['cgpa_per_pg']=None
				if 'pg_degree_path' in data:
					emp_doc['marksheet_pg'] = data['pg_degree_path']
				else:
					emp_doc['marksheet_pg']=None
				if 'doctrate' in data:
					emp_acad['doctrate'] = data['doctrate']
				else:
					emp_acad['doctrate']=None
				if 'univ_doctrate' in data and data['univ_doctrate']!=None:
					emp_acad['univ_doctrate'] = EmployeeDropdown.objects.get(sno=data['univ_doctrate'])
				else:
					emp_acad['univ_doctrate']=None
				if 'stage_doctrate' in data and data['stage_doctrate']!=None:
					emp_acad['stage_doctrate'] = EmployeeDropdown.objects.get(sno=data['stage_doctrate'])
				else:
					emp_acad['stage_doctrate']=None
				if 'date_doctrate' in data:
					try:
						valid_date = time.strptime(data['date_doctrate'], '%Y-%m-%d')
						emp_acad['date_doctrate'] = data['date_doctrate']
					except ValueError:
						emp_acad['date_doctrate']=None
				else:
					emp_acad['date_doctrate'] = None
				if 'research_topic_doctrate' in data:
					emp_acad['research_topic_doctrate'] = data['research_topic_doctrate']
				else:
					emp_acad['research_topic_doctrate']=None
				if 'doctrate_degree_path' in data:
					emp_doc['marksheet_doctrate'] = data['doctrate_degree_path']
				else:
					emp_doc['marksheet_doctrate']=None
				if 'pass_year_other' in data:
					emp_acad['pass_year_other'] = data['pass_year_other']
				else:
					emp_acad['pass_year_other']=None
				if 'degree_other' in data and data['degree_other']!=None:
					emp_acad['degree_other'] = EmployeeDropdown.objects.get(sno=data['degree_other'])
				else:
					emp_acad['degree_other']=None
				if 'univ_other' in data and data['univ_other']!=None:
					emp_acad['univ_other'] = EmployeeDropdown.objects.get(sno=data['univ_other'])
				else:
					emp_acad['univ_other']=None
				if 'cgpa_per_other' in data:
					emp_acad['cgpa_per_other'] = data['cgpa_per_other']
				else:
					emp_acad['cgpa_per_other']=None
				if 'area_spl_other' in data:
					emp_acad['area_spl_other'] = data['area_spl_other']
				else:
					emp_acad['area_spl_other']=None
				if 'other_doc_path' in data:
					emp_doc['marksheet_other'] = data['other_doc_path']
				else:
					emp_doc['marksheet_other']=None
				if 'cc' in data:
					emp_doc['character_certificate'] = data['cc']
				else:
					emp_doc['character_certificate']=None
				if 'medical' in data:
					emp_doc['medical_fitness'] = data['medical']
				else:
					emp_doc['medical_fitness']=None
				if 'emp_experience' in data:
					emp_doc['experience_certificate'] = data['emp_experience']
				else:
					emp_doc['experience_certificate']=None
				if 'research_years' in data:
					emp_research['research_years'] = data['research_years']
				else:
					emp_research['research_years']=None
				if 'research_months' in data:
					emp_research['research_months'] = data['research_months']
				else:
					emp_research['research_months']=None
				if 'industry_years' in data:
					emp_research['industry_years'] = data['industry_years']
				else:
					emp_research['industry_years']=None
				if 'industry_months' in data:
					emp_research['industry_months'] = data['industry_months']
				else:
					emp_research['industry_months']=None
				if 'teaching_years' in data:
					emp_research['teaching_years'] = data['teaching_years']
				else:
					emp_research['teaching_years']=None
				if 'teaching_months' in data:
					emp_research['teaching_months'] = data['teaching_months']
				else:
					emp_research['teaching_months']=None
				if emp_prim:
					qry_b = EmployeePrimdetail.objects.create(**emp_prim)

				#qry=EmployeePrimdetail.objects.extra(select={'id':'emp_id'}).values('id').order_by('-emp_id')
				last_id=emp_prim['emp_id']
				l_id=emp_doc['emp_id']=reporting_emp_id=address['emp_id']=emp_acad['emp_id']=emp_research['emp_id']=emp_per['emp_id']=EmployeePrimdetail.objects.get(emp_id=last_id)
				if emp_per:
					#print("Hi")
					qry_a = EmployeePerdetail.objects.create(**emp_per)
				#print(address)
				if address:

					qry_c = EmployeeAddress.objects.create(**address)

				#print(role)
				if role:
					for i in role['roles']:
						if i!='':
							qry_e = Roles.objects.create(roles=EmployeeDropdown.objects.get(sno=i),emp_id=l_id)
				if reporting:
					#print("Hi")
					a=1
					if(reporting['department'] and reporting['reporting_to']):
						for i,y in enumerate(reporting['department']) and enumerate(reporting['reporting_to']):
							#print(reporting['department'][i])
							#print("Hi")
							qry1=Reporting.objects.create(emp_id=reporting_emp_id,reporting_to=EmployeeDropdown.objects.get(sno=y),department=EmployeeDropdown.objects.get(sno=reporting['department'][i]),reporting_no=a)
							a=a+1
						
					else:
						qry1=""

				#print(emp_acad)
				if emp_acad:
					qry_f = EmployeeAcademic.objects.create(**emp_acad)
				if emp_research:
					qry_g = EmployeeResearch.objects.create(**emp_research)
				if emp_doc:
					qryh=EmployeeDocuments.objects.create(**emp_doc)
				if qry_a and qry_b and qry_c and qry_e and qry_f and qry_g and qryh:
					msg="Data Successfully Added..."
					error=False

			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	#print(qry)
	
	res={'msg':msg,'error':error,'id':emp_id}

	return JsonResponse(res,safe=False)



################################## MUSTERROLL UPDATE EmployeeDropdown ########################################### 


def Update(request):	# This API is for sending onload values to update employee form
#data=json.loads(request.body) #use data instead of non JSON data
	#print(request)
	error=True
	data_values=""
	#print(request)
		
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
			data = json.loads(request.body)
			Emp_Id=data['emp_id']
			Emp_Type=data['emp_type']
			Emp_Category=data['emp_category']
			Desg=data['desg']
			Shift=data['shift']

			####################################### DATA FOR PRIMARY INFO ###############################################

			qry1=EmployeePrimdetail.objects.extra(select={'id':'emp_id','nm':'name'}).values('id','nm')
			qry1=list(qry1)

			qry2=EmployeeDropdown.objects.filter(field='TYPE OF EMPLOYMENT').extra(select={'toe':'value'}).values('toe')
			qry2=list(qry2)
			qry3=EmployeeDropdown.objects.filter(field='CATEGORY OF EMPLOYEE').extra(select={'coe':'value'}).values('coe')
			qry3=list(qry3)

			qry4=EmployeeDropdown.objects.filter(field='DESIGNATION').extra(select={'desg':'value'}).values('desg')
			qry4=list(qry4)

			qry5=EmployeeDropdown.objects.filter(field='SHIFT').extra(select={'sft':'value'}).values('sft')
			qry5=list(qry5)

			data1={'toe_d': qry2,'coe_d': qry3,'desg_d': qry4, 'sft_d':qry5}      #sft_d = shift to be displayed

			################################### DATA CORRESPONDENDING TO RECIEVED ID ##########################################

			qry2_a=EmployeePrimdetail.objects.filter(field='emp_type').filter(emp_id=Emp_Id).extra(select={'toe':'value'}).values('toe')
			qry2_a=list(qry2_a)

			qry3_a=EmployeePrimdetail.objects.filter(field='emp_catergory').filter(emp_id=Emp_Id).extra(select={'coe':'value'}).values('coe')
			qry3_a=list(qry3_a)

			qry4_a=EmployeePrimdetail.objects.filter(field='desg').filter(emp_id=Emp_Id).extra(select={'desg':'value'}).values('desg')
			qry4_a=list(qry4_a)

			qry5_a=EmployeePrimdetail.objects.filter(field='shift').filter(emp_id=Emp_Id).extra(select={'sft':'value'}).values('sft')
			qry5_a=list(qry5_a)

			data2={'toe':qry2_a,'coe':qry3_a,'desg':qry4_a,'sft':qry5_a}
			
			data_values={'data1':data1,'data2':data2}
		  	#####################################################################################################################
			msg="Success"
				
			#else:
			#msg="Not Permitted!!"
		else:
			msg="Not Loggedin"
	else:
		msg="Technical Error: wrong parameters"

	data_to_be_sent={'data':data_values,'error':error,'msg':msg}
	#return HttpResponse(msg)
	return JsonResponse(data_to_be_sent,safe=False)

	

##################### VIEWS FOR EMPLOYEE EmployeeDropdown ########################

def add_update_dropdown(request):
	error=True
	qry1=""
	if 'HTTP_COOKIE' in request.META:

		if request.user.is_authenticated():
			#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:	
			qry1=EmployeeDropdown.objects.filter(pid=0).extra(select={'fd':'field'}).values('fd').distinct()				
				
			msg="Success"
			error=False
			if not qry1:
				msg="No Data Found!!"
				error=False
			#else:
			#	msg="not logged in"
		else:
			msg="Authentication failed!!"
	else:
		msg="Technical Error: Wrong Parameters"
				
	data={'msg':msg,'data':list(qry1),'error':error}	
	
	return JsonResponse(data,safe=False)
	
	
def field_delete(request):
	error=True	

	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
	
			data=json.loads(request.body)	
			#print(request.POST["name"]["pid"])
			qry=EmployeeDropdown.objects.filter(sno=data['del_id']).values('sno')
			if(qry.count()==0):
				msg="Sorry No data to delete"
			else:
				qry2 = EmployeeDropdown.objects.filter(sno=data['del_id']).delete()
				msg="Data Successfully Deleted..."
				error=False
			#else:
				#msg="Not Logged In!!"
		else:
			msg="Authentification Failed!"
	else:
		msg="Technical Error: Wrong Parameters"

	data={'error':error,'msg':msg}
	return JsonResponse(data,safe=False)


def field_addtn(request):
	error=True
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
			data=json.loads(request.body)
			Field=data['field']
			Value=data['value'].upper()
			if EmployeeDropdown.objects.filter(value=Value).exists():
			
				msg="Entry Already Exists!"
				error=False
			else:
				qry=EmployeeDropdown.objects.filter(value=Field).values('sno')
				if(qry):
					Pid=qry[0]['sno']
					qry = EmployeeDropdown.objects.create(field=Field,value=Value,pid=Pid)
					msg="Data Successfully Added..."
					error=False
				else:
					qry = EmployeeDropdown.objects.create(field=str(Field),value=str(Value),pid=int(0))
					msg="Data Successfully Added..."
					error=False
							
			#else:
				#msg="Not Logged In!!"
		else:
			msg="Authentification Failed!"
	else:
		msg="Technical Error: Wrong Parameters"

	data={'error':error,'msg':msg}

	return JsonResponse(data,safe=False)


def field_update_view(request):
	error=True
	qry=""	
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
	
			data=json.loads(request.body)
			qry=EmployeeDropdown.objects.filter(field=data['field']).extra(select={'fld':'field','val':'value','no':'sno'}).values(
				'fld','val','no')
			
			msg="Success!!"
			error=False
			if not qry:
				msg="No Data Found!!"
				error=True
					
			#else:
				#msg="Not Logged In!!"
		else:
			msg="Authentification Failed!"
	else:
		msg="Technical Error: Wrong Parameters"
				
	data_to_be_sent={'data':list(qry),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)   

def field_update(request):		
	error=True
		
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
			data=json.loads(request.body)
			
			Field = data['field'].upper()
			Sno=data['id']
			Value=data['value']
			qry_t=EmployeeDropdown.objects.filter(value=Value,sno=Sno,field=Field).values('value')
			
			if qry_t:
				msg="Entry Already exists!"
				error=False
			else:
				qry=EmployeeDropdown.objects.filter(field=Field).filter(sno=Sno).update(value=Value)
				msg="Data Successfully Updated..."
				error=False
			#else:
				#msg="Not Logged In!!"
		else:
			msg="Authentification Failed!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'error':error,'msg':msg}
	
	return JsonResponse(data,safe=False)


 
 
################################################### VIEWS FOR UPDATE EMPLOYEE ##############################################

def update_view_id(request):
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
					qry1=EmployeePrimdetail.objects.filter(emp_status='Active').extra(select={'id':'emp_id','nm':'name'}).values('id','nm')
						
					error=False
					msg="Success"
				#else:
				#msg="not logged in"
			else:
				msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
	
	data_to_be_sent={'data_d':list(qry1),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)

###################################### update form mein values yahan se aa ri hain ################################

####################################################### SEPARATION ################################################
def long_leave_type(request):
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				if request.session['hash3']=='Employee':
					qry1=EmployeeDropdown.objects.filter(field='LONG LEAVE').exclude(value__isnull=True).extra(select={'id':'sno','nm':'value'}).values('id','nm')	
					error=False
					msg="Success"
				else:
					msg="not logged in"
			else:
				msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
	
	data_to_be_sent={'data_d':list(qry1),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)

def seperate_req(request):
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				if request.session['hash3']=='Employee':
					data = json.loads(request.body)
					
					
					emp_id=EmployeePrimdetail.objects.get(emp_id=request.session['hash1'])
					if 'HOD' in request.session['roles']:
						if data["status"]=="Leave":
							if EmployeeSeparation.objects.filter(emp_id=emp_id).count() < 1 :
								qry1=EmployeeSeparation.objects.create(emp_id=emp_id,status=data['status'],type=EmployeeDropdown.objects.get(sno=data['type']),rejoin_date=data['rejoin_date'],emp_remark=data['reason'],hod_status='APPROVED',hr_status='PENDING',attachment=data['attachment'])
								error=False
								msg="Success"
							else:
								msg="Duplicate Entry.."
						else:
							if EmployeeSeparation.objects.filter(emp_id=emp_id).count() < 1 :
								qry1=EmployeeSeparation.objects.create(emp_id=emp_id,status=data['status'],emp_remark=data['reason'],hod_status='APPROVED',hr_status='PENDING',attachment=data['attachment'])
								error=False
								msg="Success"
							else:
								msg="Duplicate Entry.."
					else:
						if data["status"]=="Leave":
							if EmployeeSeparation.objects.filter(emp_id=emp_id).count() < 1 :
								qry1=EmployeeSeparation.objects.create(emp_id=emp_id,status=data['status'],type=EmployeeDropdown.objects.get(sno=data['type']),rejoin_date=data['rejoin_date'],emp_remark=data['reason'],hod_status='PENDING',hr_status='PENDING',attachment=data['attachment'])
								error=False
								msg="Success"
							else:
								msg="Duplicate Entry.."
						else:
							if EmployeeSeparation.objects.filter(emp_id=emp_id).count() < 1 :
								qry1=EmployeeSeparation.objects.create(emp_id=emp_id,status=data['status'],emp_remark=data['reason'],hod_status='PENDING',hr_status='PENDING',attachment=data['attachment'])
								error=False
								msg="Success"
							else:
								msg="Duplicate Entry.."
				else:
					msg="not logged in"

			else:
				msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
	
	data_to_be_sent={'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)

def update_view_info(request):
	error=True
	data1=""
	names=""
	Id=""
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				data = json.loads(request.body)
				Emp_Id=data['emp_id']
				#print(request.session['hash1'])
			####################################################### ALL DATA ##################################################################
				
				qry2=EmployeeDropdown.objects.filter(field='TYPE OF EMPLOYMENT').exclude(value__isnull=True).extra(select={'toe_id':'sno','toe':'value'}).values('toe','toe_id')
				#print(qry2.query)
				

				qry3=EmployeeDropdown.objects.filter(field='CATEGORY OF EMPLOYEE').exclude(value__isnull=True).extra(select={'coe_id':'sno','coe':'value'}).values('coe','coe_id')
				
				qry4=EmployeeDropdown.objects.filter(value="DESIGNATION").exclude(value__isnull=True).extra(select={'id':'sno','field':'field'}).values('id','field')
				qry_len=len(qry4)
				for x in range(0,qry_len):
					qry4_a=EmployeeDropdown.objects.filter(pid=qry4[x]['id']).exclude(value__isnull=True).extra(select={'desg_id':'sno','desg_name':'value'}).values('desg_id','desg_name')
					qry4[x]['designation']=list(qry4_a)
				#print(qry4)

				qry4_b=EmployeeDropdown.objects.filter(value="CADRE").exclude(value__isnull=True).extra(select={'id':'sno','field':'field'}).values('id','field')
				qry_len=len(qry4_b)
				for x in range(0,qry_len):
					qry4_b1=EmployeeDropdown.objects.filter(pid=qry4_b[x]['id']).exclude(value__isnull=True).extra(select={'cadre_id':'sno','cadre_name':'value'}).values('cadre_id','cadre_name')
					
					qry4_b[x]['cadre']=list(qry4_b1)
					#print(qry4_b)
				
				
				qry4_c=EmployeeDropdown.objects.filter(value="LADDER").exclude(value__isnull=True).extra(select={'id':'sno','field':'field'}).values('id','field')
				qry_len=len(qry4_c)
				for x in range(0,qry_len):
					qry4_c1=EmployeeDropdown.objects.filter(pid=qry4_c[x]['id']).exclude(value__isnull=True).extra(select={'ladre_id':'sno','ladre_name':'value'}).values('ladre_id','ladre_name')
					
					qry4_c[x]['ladre']=list(qry4_c1)
				
				
				qry5=EmployeeDropdown.objects.filter(field='SHIFT SETTINGS').exclude(value__isnull=True).extra(select={'sft_id':'sno','sft':'value'}).values('sft','sft_id')
				#print(qry5)
				qry_len=len(qry5)
				for x in range(0,qry_len):
					qry4_b1=EmployeeDropdown.objects.filter(pid=qry5[x]['sft_id']).exclude(value__isnull=True).extra(select={'shift_id':'sno','shift_name':'value'}).values('shift_id','shift_name')
					
					qry5[x]['shift']=list(qry4_b1)
				
				#print(qry5)
				qry6=EmployeeDropdown.objects.filter(field='TITLE').exclude(value__isnull=True).extra(select={'title_id':'sno','title':'value'}).values('title','title_id')
				

				qry7=EmployeeDropdown.objects.filter(field='DEPARTMENT').exclude(value__isnull=True).extra(select={'dept_id':'sno','dept':'value'}).values('dept','dept_id')
				

				qry8=EmployeeDropdown.objects.filter(field='POSITION').exclude(value__isnull=True).extra(select={'pos_id':'sno','pos':'value'}).values('pos','pos_id')
				

				qry9=EmployeeDropdown.objects.filter(field='ROLES').exclude(value__isnull=True).extra(select={'role_id':'sno','role':'value'}).values('role_id','role').distinct()
				

				qry10=EmployeeDropdown.objects.filter(field='BLOOD GROUP').exclude(value__isnull=True).extra(select={'bg_id':'sno','bg':'value'}).values('bg','bg_id')
				

				qry11=EmployeeDropdown.objects.filter(field='GENDER').exclude(value__isnull=True).extra(select={'gender_id':'sno','gender':'value'}).values('gender','gender_id')
				
				qry12=EmployeeDropdown.objects.filter(field='NATIONALITY').exclude(value__isnull=True).extra(select={'nation_id':'sno','nation':'value'}).values('nation','nation_id')
				

				qry13=EmployeeDropdown.objects.filter(field='CASTE').exclude(value__isnull=True).extra(select={'caste_id':'sno','caste':'value'}).values('caste','caste_id')
				

				qry14=EmployeeDropdown.objects.filter(field='MARITAL STATUS').exclude(value__isnull=True).extra(select={'marriage_id':'sno','marriage':'value'}).values('marriage','marriage_id')
				

				qry15=EmployeeDropdown.objects.filter(field='RELIGION').exclude(value__isnull=True).extra(select={'rel_id':'sno','rel':'value'}).values('rel','rel_id')
				

				qry16=EmployeeDropdown.objects.filter(field='BOARD').exclude(value__isnull=True).extra(select={'board_id':'sno','board':'value'}).values('board','board_id')
				

				qry17=EmployeeDropdown.objects.filter(field='UNIVERSITY').exclude(value__isnull=True).extra(select={'uni_id':'sno','uni':'value'}).values('uni','uni_id')
				

				qry18=EmployeeDropdown.objects.filter(field='DEGREE').exclude(value__isnull=True).extra(select={'deg_id':'sno','deg':'value'}).values('deg','deg_id')
				

				qry19=EmployeeDropdown.objects.filter(field='P.HD. STAGE').exclude(value__isnull=True).extra(select={'stage_id':'sno','stage':'value'}).values('stage','stage_id')
				qry20=EmployeeDropdown.objects.filter(field='ORGANIZATION').exclude(value__isnull=True).extra(select={'org_id':'sno','org_name':'value'}).values('org_id','org_name')
				qry21=EmployeeDropdown.objects.filter(field='STATE').exclude(value__isnull=True).extra(select={'state_id':'sno','state_name':'value'}).values('state_id','state_name')

				data1={'toe_d': list(qry2),'coe_d': list(qry3),'desg_d': list(qry4),'cadre_d':list(qry4_b),'ladre':list(qry4_c) ,'sft_d':list(qry5), 'title_d' : list(qry6) ,'dept_d':list(qry7) ,'pos_d':list(qry8) , 'roles_d':list(qry9) , 'bg_d':list(qry10), 'gender_d':list(qry11), 'nationality_d':list(qry12), 'caste_d':list(qry13), 'marital_status_d':list(qry14), 'rel_d':list(qry15),'board_d':list(qry16),'uni_d':list(qry17),'deg_d':list(qry18),'stage_d':list(qry19),'organization':list(qry20),'state':list(qry21)}

			########################################## DATA CORRESPONDENDING TO RECIEVED ID ##########################################

				qry2_a=EmployeePrimdetail.objects.filter(emp_id=Emp_Id).extra(select={'dep':'dept','title':'title','toe':'emp_type','coe':'emp_category','dsgn':'desg','sft':'shift','current_pos':'current_pos','cadre':'cadre','ladder':'ladder','organization':'organization'}).values('dep','title','toe','coe','dsgn','sft','current_pos','cadre','ladder','organization')
				#print(qry2_a[0]['coe'])
				########### VARIABLES HOLDING IDS ####################

				dept_id=qry2_a[0]['dep']
				title_id=qry2_a[0]['title']
				coe_id=qry2_a[0]['coe']
				toe_id=qry2_a[0]['toe']
				dsgn_id=qry2_a[0]['dsgn']
				sft_id=qry2_a[0]['sft']

				######################################################

				
				qry2_b=EmployeeDropdown.objects.filter(sno=coe_id).extra(select={'coe_name':'value'}).values('coe_name')
				
				qry2_c=EmployeeDropdown.objects.filter(sno=toe_id).extra(select={'toe_name':'value'}).values('toe_name')
				
				qry2_d=EmployeeDropdown.objects.filter(sno=dsgn_id).extra(select={'dsgn_name':'value'}).values('dsgn_name')
				
				qry2_e=EmployeeDropdown.objects.filter(sno=sft_id).extra(select={'sft_name':'value'}).values('sft_name')
				#print(qry2_e)
				
				qry2_f=EmployeeDropdown.objects.filter(sno=dept_id).extra(select={'dept_name':'value'}).values('dept_name')
				
				qry2_g=EmployeeDropdown.objects.filter(sno=title_id).extra(select={'title_name':'value'}).values('title_name')
				
				qry2_h=EmployeePrimdetail.objects.filter(emp_id=Emp_Id).extra(select={'nme':'name','date_joining':'doj','primary_mobile':'mob','secondary_mobile':'mob1','mail':'email'}).values('nme','date_joining','primary_mobile','secondary_mobile','mail')
				

				qry2_j=Roles.objects.filter(emp_id=Emp_Id).extra(select={'role':'roles'}).values('role')
				#print(qry2_j[0]['role'])
				#qry_b=EmployeeDropdown.objects.filter(sno__in=qry_a.values('holiday')).extra(select={'ht_val':'value'}).values('ht_val')
				qry_b=EmployeeDropdown.objects.filter(sno__in=qry2_j.values('role')).exclude(value__isnull=True).extra(select={'role':'sno'}).values('role')
				
				
				
				qry2_k=EmployeePerdetail.objects.filter(emp_id=Emp_Id).extra(select={'father':'fname','mother':'mname','birth_date':'dob','gndr':'gender','blood_group':'bg','nation':'nationality','caste':'caste','marry':'marital_status','rel':'religion','image':'image_path'}).values('father','mother','birth_date','gndr','blood_group','nation','caste','marry','rel','image')
				

				qry2_m=EmployeeAddress.objects.filter(emp_id=Emp_Id).extra(select={'permanent_add_1':'p_add1','permanent_add_2':'p_add2','place':'p_city','district':'p_district','state':'p_state',
					'pin':'p_pincode','corresp_add_1':'c_add1','corresp_add_2':'c_add2','corresp_place':'c_city','corresp_district':'c_district','corresp_state':'c_state','corresp_pin':'c_pincode'}).values(
					'permanent_add_1','permanent_add_2','place','district','state','pin','corresp_add_1','corresp_add_2','corresp_place','corresp_district','corresp_state','corresp_pin')
				

				qry2_n=Reporting.objects.filter(emp_id=Emp_Id).extra(select={'reporting_level':'reporting_no','reporting_designation_id':'reporting_to','reporting_official_dept_id':'department'}).values('reporting_level','reporting_designation_id','reporting_official_dept_id')
				reporting_designation_id={}
				department_id={}
				department_name={}
				reporting_designation_name={}
				#print(qry2[0])

				reporting_designation_id={}
				department_id={}
				department_name={}
				designation_name={}
				
				#print(qry2_n[0]['reporting_level'])
				j=0
			
				'''for i in qry2_n:
					qry2_n1=EmployeeDropdown.objects.filter(sno=qry2_n[j]['reporting_designation_id']).extra(select={'official_designation':'value'}).values('official_designation')
					#print(qry2_n1[0]['official_designation'])
					designation_name[j]=(qry2_n1[0]['official_designation'])
					qry2_n2=EmployeeDropdown.objects.filter(sno=qry2_n[j]['reporting_official_dept_id']).extra(select={'official_department':'value'}).values('official_department')
					#print(qry2_n[j]['reporting_official_dept_id'])
					department_name[j]=qry2_n2[0]['official_department']
					j=j+1

				reporting_info={'reporting_levels':qry2_n.count(),'designation':designation_name,'department':department_name,'ids':list(qry2_n)}
				#print(reporting_info)'''
				try:
					for i in qry2_n:
						qry2_n1=EmployeeDropdown.objects.filter(sno=qry2_n[j]['reporting_designation_id']).extra(select={'official_designation':'value'}).values('official_designation')
						########################## DYNAMIC DICTIONARY ###############################
						qry2_n[j]['designation']=qry2_n1[0]['official_designation']
						##############################################################################
						qry2_n2=EmployeeDropdown.objects.filter(sno=qry2_n[j]['reporting_official_dept_id']).extra(select={'official_department':'value'}).values('official_department')
						#print(qry2_n[j]['reporting_official_dept_id'])
						qry2_n[j]['department']=qry2_n2[0]['official_department']
						j=j+1
					#print(qry2_n)
					reporting_info={'reporting_levels':qry2_n.count(),'designation':designation_name,'department':department_name,'ids':list(qry2_n)}
				except:
					reporting_info=""

					#print(reporting_info)

				qry2_o=EmployeePrimdetail.objects.filter(emp_id=Emp_Id).extra(select={'pos':'current_pos'}).values('pos')
				pos_id=qry2_o[0]['pos']
				
				qry2_p=EmployeeDropdown.objects.filter(sno=pos_id).extra(select={'pos_value':'value'}).values('pos_value')
				
				position={'id':list(qry2_o),'val':list(qry2_p)}

				a=EmployeeAcademic.objects.filter(emp_id=Emp_Id).extra(select={'x_pass_yr':'pass_year_10','x_board':'board_10','x_cgpa':'cgpa_per_10','xii_pass_yr':'pass_year_12','xii_board':'board_12','xii_cgpa':'cgpa_per_12','diploma_pass_yr':'pass_year_dip','diploma_uni':'univ_dip','diploma_cgpa':'cgpa_per_dip','ug_pass_yr':'pass_year_ug','ug_uni':'univ_ug','ug_degree':'degree_ug','ug_cgpa':'cgpa_per_ug','pg_pass_yr':'pass_year_pg','pg_uni':'univ_pg','pg_cgpa':'cgpa_per_pg','pg_degree':'degree_pg','pg_area_specialization':'area_spl_pg','doc_research_topic':'research_topic_doctrate','doc_dropdown':'doctrate','doc_uni':'univ_doctrate','doc_date':'date_doctrate','doc_stage':'stage_doctrate','other_degree':'degree_other','other_pass_yr':'pass_year_other','other_uni':'univ_other','other_cgpa':'cgpa_per_other','other_area_specialization':'area_spl_other'}).values('x_pass_yr','x_board','x_cgpa','xii_pass_yr','xii_board','xii_cgpa','doc_date','diploma_pass_yr','diploma_uni','diploma_cgpa','ug_pass_yr','ug_uni','ug_degree','ug_cgpa','pg_pass_yr','pg_uni','pg_cgpa','pg_degree','pg_area_specialization','doc_dropdown','doc_uni','doc_stage','doc_research_topic','other_degree','other_pass_yr','other_uni','other_cgpa','other_area_specialization')
				#print(qry2_q)

				qry2_r=EmployeeDocuments.objects.filter(emp_id=Emp_Id).extra(select={'x_marksheet':'marksheet_10','xii_marksheet':'marksheet_12','diploma_marksheet':'marksheet_dip','ug_marksheet':'marksheet_ug','pg_marksheet':'marksheet_pg','doctrate_marksheet':'marksheet_doctrate','other_marksheet':'marksheet_other','medical':'medical_fitness','cc':'character_certificate','exp':'experience_certificate'}).values('x_marksheet','xii_marksheet','diploma_marksheet','ug_marksheet','pg_marksheet','doctrate_marksheet','other_marksheet','medical','cc','exp')
				
				if qry2_r:
					print("Hi")
					qry2_q=a[0]
	################################### DYNAMIC INDEXING IN DICTIONARY ###################################

					qry2_q['x_marksheet']=qry2_r[0]['x_marksheet']
					#print(a['x_marksheet'])
					qry2_q['xii_marksheet']=qry2_r[0]['xii_marksheet']
					qry2_q['diploma_marksheet']=qry2_r[0]['diploma_marksheet']
					qry2_q['ug_marksheet']=qry2_r[0]['ug_marksheet']
					qry2_q['pg_marksheet']=qry2_r[0]['pg_marksheet']
					qry2_q['doctrate_marksheet']=qry2_r[0]['doctrate_marksheet']
					qry2_q['other_marksheet']=qry2_r[0]['other_marksheet']
					qry2_q['medical']=qry2_r[0]['medical']
					qry2_q['cc']=qry2_r[0]['cc']
					qry2_q['exp']=qry2_r[0]['exp']
#########################################################################################################
				else:
					qry2_q=""

				qry_r=EmployeeAcademic.objects.filter(emp_id=Emp_Id).extra(select={'doc_id':'doctrate'}).values('doc_id')
				qry_s=EmployeeDropdown.objects.filter(sno__in=qry_r.values('doc_id')).extra(select={'doc_val':'value','doc_id':'sno'}).values('doc_val','doc_id')

				qry_t=EmployeeResearch.objects.filter(emp_id=Emp_Id).extra(select={'years_r':'research_years','months_r':'research_months','years_i':'industry_years','months_i':'industry_months','years_t':'teaching_years','months_t':'teaching_months'}).values('years_r','months_r','years_i','months_i','years_t','months_t')

				#doc_info={'doc_no':list(qry_r),'doc_name':list(qry_s)}
				#qry_s=EmployeeDropdown.objects.select_related('sno')
				#qry_s=EmployeeDropdown.join(EmployeeAcademic)
				#print(list(qry_s))

				names={'coe_value':list(qry2_b),'toe_value':list(qry2_c),'dsgn_value':list(qry2_d),'sft_value':list(qry2_e),'dept_value':list(qry2_f),'title_value':list(qry2_g),'name_n_join_date_contact':list(qry2_h),'add_role':list(qry_b),
					'personal_details':list(qry2_k),'residential_details':list(qry2_m),'reporting_level':reporting_info,'pos':position,'academic_details':qry2_q,'doc_info':list(qry_s),'research_info':list(qry_t)}
				msg="logged in"
				error=False
			#else:
			#msg="not logged in"
			else:
				msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
				
				
	data_to_be_sent={'data_d':data1,'id':list(qry2_a),'names':names,'error':error,'msg':msg}
	#return HttpResponse(msg)
	return JsonResponse(data_to_be_sent,safe=False)



def update_info(request):
	error=True
	data_values=""
	
	#print(request.body)
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():

			if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
				data=json.loads(request.body)	
				#print(data['image'])
				Emp_Id=data['emp_id']
				
				empType_id=data['toe']
				empCategory_id=data['coe']
				empDesg_id=data['desg']
				empImg=data['image']
				empShift_id=data['shift']
				empTitle_id=data['title']
				empName=data['name']
				empDept_id=data['dep']
				empDOJ_id=data['date_join']
				pos=data['pos']
				role=data['role']
				if 'department' in data:
					DepartmentId=data['department']
				else:
					DepartmentId=None
				if 'designation' in data:
					reportingTo=data['designation']
				else:
					reportingTo=None
				if 'father' in data:
					fName=data['father']
				else:
					fName=None
				if 'mother' in data:
					mName=data['mother']
				else:
					mName=None
				DOB=data['birthday']
				blood_group=data['b_grp']
				gender=data['gender']
				nationality=data['nation']
				caste=data['caste']
				marital_status=data['marriage']
				religion=data['rel']
				mob=data['mob_p']
				if 'mob_s' in data:
					mob1=data['mob_s']
				else:
					mob1=No
				email=data['mail']

				p_add1=data['add_p1']
				p_add2=data['add_p2']
				p_city=data['city_p']
				p_district=data['dis_p']
				p_pincode=data['pin_p']
				p_state=data['state_p']
				c_add1=data['add_c1']
				c_add2=data['add_c2']
				c_city=data['city_c']
				c_district=data['dis_c']
				c_state=data['state_c']
				c_pincode=data['pin_c']

				pass_year_10 =data['10_yr']
				board_10 = data['10_board']
				cgpa_per_10 = data['10_cgpa']
				x_marksheet=data['x_marksheet']
				pass_year_12 = data['12_yr']
				board_12 = data['12_board']
				cgpa_per_12 = data['12_cgpa']
				xii_marksheet=data['xii_marksheet']
				pass_year_dip = data['dip_yr']
				univ_dip = data['dip_uni']
				cgpa_per_dip = data['dip_cgpa']
				diploma_marksheet=data['diploma_marksheet']
				pass_year_ug = data['ug_yr']
				univ_ug = data['ug_uni']
				degree_ug = data['ug_degree']
				cgpa_per_ug = data['ug_cgpa']
				ug_marksheet=data['ug_marksheet']
				pass_year_pg = data['pg_yr']
				univ_pg = data['pg_uni']
				degree_pg = data['pg_degree']
				cgpa_per_pg = data['pg_cgpa']
				area_spl_pg=data['pg_area']
				pg_marksheet=data['pg_marksheet']

				doctrate = data['doc']
				univ_doctrate = data['doc_uni']
				stage_doctrate = data['doc_stage']
				doctrate_marksheet=data['doctrate_marksheet']

				reasearchYears=data['yrs_research']
				reasearchMonths=data['mon_research']
				industryYears=data['yrs_industry']
				industryMonths=data['mon_industry']
				teachingYears=data['yrs_teach']
				teachingMonths=data['mon_teach']
				date_doctrate=data['doc_date']
				research_topic_doctrate=data['doc_research']
				degree_other = data['other_degree']
				pass_year_other=data['other_yr']
				univ_other = data['other_uni']
				cgpa_per_other = data['other_cgpa']
				area_spl_other = data['other_area']
				other_marksheet=data['other_marksheet']
				organization=data['organization']
				cadre=data['cadre']
				ladder=data['ladder']
				emp_exp=data['emp_experience']
				cc=data['cc']
				medical=data['medical']
				update={'emp_type':empType_id,'emp_category':empCategory_id,'desg':empDesg_id,'shift':empShift_id,'title':empTitle_id,
				'name':empName,'dept':empDept_id,'current_pos':pos,'mob':mob,'mob1':mob1,'email':email,'doj':empDOJ_id,'organization':organization,'cadre':cadre,'ladder':ladder}
				qry1=EmployeePrimdetail.objects.filter(emp_id=Emp_Id).update(**update)
				a=0
				qry3=Reporting.objects.filter(emp_id=Emp_Id).delete()
				#print(DepartmentId)
				#print(reportingTo)
				try:
					#for i in zip(len(DepartmentId),len(reportingTo)):
					length_dept = len(DepartmentId)
					for i in range(0,length_dept):

						qry2=Reporting.objects.filter(emp_id=Emp_Id).create(emp_id=EmployeePrimdetail.objects.get(emp_id=Emp_Id),reporting_to=EmployeeDropdown.objects.get(sno=reportingTo[a]),department=EmployeeDropdown.objects.get(sno=DepartmentId[a]),reporting_no=a+1)
						a=a+1
					#print(a)
				except:
					qry2=Reporting.objects.filter(emp_id=Emp_Id).create(emp_id=EmployeePrimdetail.objects.get(emp_id=Emp_Id),reporting_to=None,department=None,reporting_no=0)

				qry3=Roles.objects.filter(emp_id=EmployeePrimdetail.objects.get(emp_id=Emp_Id)).delete()
				
				for i in role:
					qrya=Roles.objects.filter(emp_id=Emp_Id).create(emp_id=EmployeePrimdetail.objects.get(emp_id=Emp_Id),roles=EmployeeDropdown.objects.get(sno=i))

				update1={'fname':fName,'mname':mName,'bg':blood_group,'gender':gender,'nationality':nationality,'caste':caste,
				'marital_status':marital_status,'religion':religion,'dob':DOB,'image_path':empImg}
				qry4=EmployeePerdetail.objects.filter(emp_id=Emp_Id).update(**update1)

				update2={'p_add1':p_add1,'p_add2':p_add2,'p_city':p_city,'p_district':p_district,'p_state':p_state,'p_pincode':p_pincode,
				'c_add1':c_add1,'c_add2':c_add2,'c_city':c_city,'c_district':c_district,'c_state':c_state,'c_pincode':c_pincode}
				qry5=EmployeeAddress.objects.filter(emp_id=Emp_Id).update(**update2)

				update3={'pass_year_10':pass_year_10,'board_10':board_10,'cgpa_per_10':cgpa_per_10,'pass_year_12':pass_year_12,'board_12':board_12,'cgpa_per_12':cgpa_per_12,'pass_year_dip':pass_year_dip,'univ_dip':univ_dip,'cgpa_per_dip':cgpa_per_dip,'pass_year_ug':pass_year_ug,'univ_ug':univ_ug,'degree_ug':degree_ug,'cgpa_per_ug':cgpa_per_ug,'pass_year_pg':pass_year_pg,'univ_pg':univ_pg,'degree_pg':degree_pg,'cgpa_per_pg':cgpa_per_pg,'area_spl_pg':area_spl_pg,'doctrate':doctrate,'univ_doctrate':univ_doctrate,'stage_doctrate':stage_doctrate,'date_doctrate':date_doctrate,'stage_doctrate':stage_doctrate,'research_topic_doctrate':research_topic_doctrate,'degree_other':degree_other,'pass_year_other':pass_year_other,'univ_other':univ_other,'cgpa_per_other':cgpa_per_other,'area_spl_other':area_spl_other}
				#print(cgpa_per_12)
				qry6=EmployeeAcademic.objects.filter(emp_id=Emp_Id).update(**update3)
				
				update4={'research_years':reasearchYears,'research_months':reasearchMonths,'industry_years':industryYears,'industry_months':industryMonths,'teaching_years':teachingYears,'teaching_months':teachingMonths}
				qry7=EmployeeResearch.objects.filter(emp_id=Emp_Id).update(**update4)
				
				update5={'marksheet_10':x_marksheet,'marksheet_12':xii_marksheet,'marksheet_dip':diploma_marksheet,'marksheet_ug':ug_marksheet,'marksheet_pg':pg_marksheet,'marksheet_doctrate':doctrate_marksheet,'marksheet_other':other_marksheet,'medical_fitness':medical,'character_certificate':cc,'experience_certificate':emp_exp}
				qryx=EmployeeDocuments.objects.filter(emp_id=Emp_Id).update(**update5)
				error=False
				msg="Data Updated Successfully!"
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"

				
	data_values={'error':error,'msg':msg}
	return JsonResponse(data_values,safe=False)

##################################################### SHIFT SETTINGS ##################################################

def display_shift(request):
	error=True
	qry=""
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				#print("Hi")
				qry=EmployeeDropdown.objects.filter(field='SHIFT SETTINGS').exclude(value__isnull=True).extra(select={'sft_id':'sno','sft':'value'}).values('sft','sft_id')
				#print("hello")
				#print(qry)
				qry_len=len(qry)
				for x in range(0,qry_len):
					qrya=EmployeeDropdown.objects.filter(pid=qry[x]['sft_id']).exclude(value__isnull=True).extra(select={'shift_id':'sno','shift_name':'value'}).values('shift_id','shift_name')
				
					qry[x]['shift']=list(qrya)
				print(qry)
				error=False
				msg="Success"
				#print(qry)
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'error':error,'msg':msg,'values':list(qry)}
	return JsonResponse(data,safe=False)


def view_shift_data(request):
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				error=False
				data=json.loads(request.body)
				sId=data['sft']
				qry=Shifts.objects.filter(shiftid=sId).extra(select={'time_in':'intime','time_out':'outtime','in_late':'latein','exit_early':'earlyexit','fdtime':'fulldaytime','hdtime':'halfdaytime','brk_strt':'breakstart','brk_end':'breakend'}).values('time_in','time_out','in_late','exit_early','fdtime','hdtime','brk_strt','brk_end')
				msg="Success"
				if qry.count()==0:
					qry=""
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'msg':msg,'error':error,'values':list(qry)}
	return JsonResponse(data,safe=False)

def Add_Shift(request):
	error=True
	data_values=""
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				data=json.loads(request.body)
				sId=data['shift']

				iTime=data['intime']
				oTime=data['outtime']
				lIn=data['latein']
				eExit=data['earlyexit']
				fdTime=data['fulldaytime']
				hdTime=data['halfdaytime']
				bStart=data['breakstart']
				bEnd=data['breakend']
				# qry=Shifts.objects.filter(shiftid=sId,intime=iTime,outtime=oTime,latein=lIn,earlyexit=eExit,
				# 	fulldaytime=fdTime,halfdaytime=hdTime,breakstart=bStart,breakend=bEnd).count()
				qry=Shifts.objects.filter(shiftid=sId).count()
				if qry>0:
					
					sId=EmployeeDropdown.objects.get(sno=data['shift'])

					qry=Shifts.objects.filter(shiftid=sId).update(intime=iTime,outtime=oTime,latein=lIn,earlyexit=eExit,
						fulldaytime=fdTime,halfdaytime=hdTime,breakstart=bStart,breakend=bEnd)
					msg="Shifts Updated Successfully !!"
					error=False

					
				else:
					sId=EmployeeDropdown.objects.get(sno=data['shift'])

					qry=Shifts.objects.create(shiftid=sId,intime=iTime,outtime=oTime,latein=lIn,earlyexit=eExit,
						fulldaytime=fdTime,halfdaytime=hdTime,breakstart=bStart,breakend=bEnd)
					msg="Shifts Added Successfully !!"
					error=False
			else:
				msg="Authentification Failed!"
		else:
			msg="Wrong Parameters!!"
	else:
		msg="Invalid Request.."
 				
	data_values={'error':error,'msg':msg}
	
	return JsonResponse(data_values,safe=False)

################################################################ OD Category ###########################################################


def pay_view(request):
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			#if request.user.is_authenticated():
				#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
			
			qry2=EmployeeDropdown.objects.filter(field='Salary Type').exclude(value__isnull=True).extra(select={'id':'sno','nm':'value'}).values('id','nm')
			error=False
			msg="Success"
				#else:
				#msg="not logged in"
			#else:
			#	msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
	
	data_to_be_sent={'data_d':list(qry2),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)



###################################################NO DUES#########################################################

def employee_view(request):
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			#if request.user.is_authenticated():
				#if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
			
			qry2=EmployeeDropdown.objects.filter(field='No Dues Category').exclude(value__isnull=True).extra(select={'id':'sno','nm':'value'}).values('id','nm')
			error=False
			msg="Success"
				#else:
				#msg="not logged in"
			#else:
			#	msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
	
	data_to_be_sent={'data_d':list(qry2),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)

##################################### ADMIN NO DUES #########################################
def add_no_dues(request):
	error=True
	data_values=""
	if 'HTTP_COOKIE' in request.META:
		
		if request.user.is_authenticated():
			if request.session['hash3']=='Employee':
				data = json.loads(request.body.decode('utf-8'))
				print(data)
				#print(data)
				no_dues = {}
				if 'emp_id' in data:
					no_dues['emp_id'] = EmployeePrimdetail.objects.get(emp_id=data['emp_id'])
				if 'due_head' in data:
					no_dues['due_head'] = EmployeeDropdown.objects.get(sno=data['due_head'])

				if no_dues:
					
					qry = NoDuesHead.objects.create(**no_dues)
					msg = "Data Successfully Added..."
					error = False
					
			else:
				"Not LoggedIn!!!"
		else:
			"Authentication Failed!!"
	else:
		msg="Technical Error: Wrong Parameters"

	res={'msg':msg,'error':error}
	return JsonResponse(res,safe=False)

######################################PREVIOUS SEPARATION##################################
def separation_previous(request):
	error=True
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']=='Employee':
				qry=NoDuesHead.objects.filter(status='ACTIVE').values('emp_id','due_head','due_head__value','emp_id__name')
			else:
				msg="Not Logged In!!"
		else:
			msg="Authentification Failed!"
	else:
		msg="Wrong Parameters!!"
	error=False
	msg=""

	data_to_be_sent={'data_d':list(qry),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)
############################################################################################
def separation_approval_admin(request):
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
				qry=EmployeeSeparation.objects.filter(hod_status='APPROVED',hr_status='PENDING').values('emp_id','emp_id__name')
				error=False
				msg="Success"
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'data_value':list(qry),'error':error,'msg':msg}
	return JsonResponse(data,safe=False)

def separation_employee_details(request):
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']== 'Employee' and 'HR' in request.session['roles']:
				data=json.loads(request.body)

				Emp_id=data['emp_id']
				
				qryq=EmployeeSeparation.objects.filter(emp_id=Emp_id,hod_status='APPROVED',hr_status='PENDING').extra(select={'type':'type'}).values('type')
				
				qryb=EmployeeDropdown.objects.filter(sno=qryq[0]['type']).extra(select={'type_name':'value'}).values('type_name')
				qry=EmployeeSeparation.objects.filter(emp_id=Emp_id).extra(select={'separation_id':'id','emp_Id':'emp_id','status':'status','type':'type','rejoin_date':'rejoin_date','emp_remark':'emp_remark','hod_status':'hod_status','hod_remark':'hod_remark','hr_status':'hr_status','hr_remark':'hr_remark'}).values('separation_id','emp_Id','status','type','rejoin_date','emp_remark','hod_status','hod_remark','hr_status','hr_remark')
				error=False
				msg="Success"
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'data_value':list(qry),'type_name':list(qryb),'error':error,'msg':msg}
	return JsonResponse(data,safe=False)

def separation_employee_status(request):
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']== 'Employee' and 'HR' in request.session['roles']:
				data=json.loads(request.body)
				Emp_id=EmployeePrimdetail.objects.get(emp_id=data['Emp_Id'])
				Hr_Status=data['hr_status']
				ID=data['separation_id']
				Hr_Remark=data['hr_remark']
				
				qry=EmployeeSeparation.objects.filter(id=ID,emp_id=Emp_id).update(hr_status=Hr_Status,hr_remark=Hr_Remark)
				
				qry_head=NoDuesHead.objects.filter(status='ACTIVE').extra(select={'head_id':'id'}).values('head_id')
				print(qry_head)
				for i in qry_head:
					qrt_e=NoDuesEmp.objects.create(emp_id=Emp_id,status='PENDING',head_id=NoDuesHead.objects.get(id=i['head_id']))
				msg="Sucsess"
				error=False
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'error':error,'msg':msg}
	return JsonResponse(data,safe=False)

############################################ EMPLOYEE SEPARATION ###################################

##############################################################################################3


#################################################################################################
def view_approval_status(request):  ######################### SUYASH ############################
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
					
					
					qry1=EmployeeSeparation.objects.values('id','status','type__value','rejoin_date','emp_remark','hod_status','hod_remark','hr_status','hr_remark','emp_id__name')
					
					error=False
					msg="Success"
				else:
					msg="not logged in"
			else:
				msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
	
	data_to_be_sent={'data_d':list(qry1),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)
########################################################################################
def separation_employee(request):  ########TANYA #########
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']=='Employee':
				
				qry1=EmployeeSeparation.objects.filter(status='Resign',emp_id=request.session['hash1']).values('id','status','type__value','rejoin_date','emp_remark','hod_status','hod_remark','hr_status','hr_remark')
				qry2=EmployeeSeparation.objects.filter(status='Leave',emp_id=request.session['hash1']).values('id','status','type__value','rejoin_date','emp_remark','hod_status','hod_remark','hr_status','hr_remark')
				error=False
				msg="Success"
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'data_value':list(qry1),'data':list(qry2),'error':error,'msg':msg}
	return JsonResponse(data,safe=False)

#########################################################################################################################
def no_dues(request):
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				if request.session['hash3']=='Employee' and 'HR' in request.session['roles']:
					qry=EmployeeDropdown.objects.filter(field="CATEGORY OF EMPLOYEE").exclude(value__isnull=True).values('value','sno')
					msg="success"
					error=False
				else:
					msg="Not Permitted!!"
			else:
				msg="Not Loggedin!!"
		else:
			msg="Technical Error: Wrong Parameters"
	else:
		msg="Wrong Credentials!!"

	data={'data_values':list(qry),'error':error,'msg':msg}
	return JsonResponse(data,safe=False)
#############################################SEPARATION HOD##########################################

def separation_approval_hod(request):
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']=='Employee' and 'HOD' in request.session['roles']:
				user=request.session['hash1']
				qr=EmployeePrimdetail.objects.filter(emp_id=AuthUser.objects.get(username=user)).values('dept')

				if qr:
					qry_a=EmployeeSeparation.objects.filter(emp_id__dept=qr[0]['dept'],hod_status='PENDING').exclude(emp_id=request.session['hash1']).values('emp_id','emp_id__name')

					error=False
					msg="Success"
				else:
					msg="Department not found.."
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'data_value':list(qry_a),'error':error,'msg':msg}
	return JsonResponse(data,safe=False)

def separation_employee_details_hod(request):
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']== 'Employee' and 'HOD' in request.session['roles']:
				data=json.loads(request.body)
				print(data)
				Emp_id=data['emp_id']
				#print(Emp_id)
				qryq=EmployeeSeparation.objects.filter(emp_id=Emp_id,hod_status='PENDING').extra(select={'type':'type'}).values('type')
				#print(qryq[0]['type'])
				qryb=EmployeeDropdown.objects.filter(sno=qryq[0]['type']).extra(select={'type_name':'value'}).values('type_name')
				#print(qryb.query)
				

				qry=EmployeeSeparation.objects.filter(emp_id=Emp_id).values('id','emp_id','status','type__value','rejoin_date','emp_remark','hod_status','hod_remark','hr_status','hr_remark')
				#print(qry.query)
				error=False
				msg="Success"
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'data_value':list(qry),'type_name':list(qryb),'error':error,'msg':msg}
	return JsonResponse(data,safe=False)

def view_approval_status_hod(request):  
	error=True
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				if request.session['hash3']=='Employee' and 'HOD' in request.session['roles']:
					
					
					qry1=EmployeeSeparation.objects.filter(emp_id__dept__value=request.session['dept']).values('id','status','type__value','rejoin_date','emp_remark','hod_status','hod_remark','emp_id__name','hr_status','hr_remark').exclude(emp_id__desg__value='HOD')
					
					error=False
					msg="Success"
				else:
					msg="not logged in"
			else:
				msg="Authentication failed!!"
		else:
			msg="Technical error: Wrong Parameters!!!"
	else:
		msg="Invalid Request"
	
	data_to_be_sent={'data_d':list(qry1),'error':error,'msg':msg}
	return JsonResponse(data_to_be_sent,safe=False)

##########################################################################################################################
def delete_nodues(request):
	error=True
	if 'HTTP_COOKIE' in request.META:			
		if request.user.is_authenticated():	
			if request.session['hash3'] == 'Employee':
				if request.body:
					inp = json.loads(request.body.decode('utf-8'))
					emp_id=inp['Emp']
					due_head=inp['NoDues']
					qry=NoDuesHead.objects.filter(emp_id=emp_id,due_head=due_head).update(status='DELETE')
					msg="Leave Deleted Successfully..!!"
					error=False
				else:
					msg="Invalid Input"
			else:
				msg="not permitted"
		else:
			msg="not logged in"
	else:
		msg="Technical Error:wrong parameters"
	values={'error':error,'msg':msg}
	return JsonResponse(values,safe=False)
def separation_employee_status_hod(request):
	#print("kala")
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated():
			if request.session['hash3']== 'Employee' and 'HOD' in request.session['roles']:
				data=json.loads(request.body)
				Emp_id=data['Emp_Id']
				Hod_Status=data['hod_status']
				ID=data['separation_id']
				Hod_Remark=data['hod_remark']
				if Hod_Status == 'REJECTED':
					qryt=EmployeeSeparation.objects.filter(id=ID,emp_id=Emp_id).update(hr_status='REJECTED',hod_status='REJECTED',hod_remark=Hod_Remark)
				else:
					qry=EmployeeSeparation.objects.filter(id=ID,emp_id=Emp_id).update(hod_status=Hod_Status,hod_remark=Hod_Remark)
				
				msg="Sucsess"
				error=False
			else:
				msg="Not Permitted!!"
		else:
			msg="Not Loggedin!!"
	else:
		msg="Technical Error: Wrong Parameters"
	data={'error':error,'msg':msg}
	return JsonResponse(data,safe=False)

def noduesApproval(request):
	error=True
	msg=''
	if 'HTTP_COOKIE' in request.META:
		if request.user.is_authenticated(): 
			if request.session['hash3']== 'Employee':
				#print(request.session)
				#Id=NoDuesHead.objects.get(id=Id)
				qry1=NoDuesHead.objects.filter(emp_id=request.session['hash1']).values('id')
				#print(qry1)
				qry1_count=NoDuesHead.objects.filter(emp_id=request.session['hash1']).values('id').count()
				#print(qry1_count)
				dic=[]
				#dic2=[]
				for x in range(qry1_count):
					dic1={}
					#dic2.append(qry1[x]['id'])
					qry2=NoDuesEmp.objects.filter(head_id=qry1[x]['id'],status='PENDING').values('emp_id','emp_id__name')
					print(qry2)
					qry2_count=NoDuesEmp.objects.filter(head_id=qry1[x]['id'],status='PENDING').values('emp_id','emp_id__name').count()
					#print(qry2_count)
					#print(qry2_count)
					# if (qry2_count==0):
					# 	dic1['Name']=None
					# 	dic1['NoDuesDept']=None
					# 	dic.append(dic1)
					# else:
					for y in range(qry2_count):
						dic1['Name']=qry2[y]['emp_id__name']
						qry3=NoDuesHead.objects.filter(emp_id=qry2[y]['emp_id'],id=qry1[x]['id']).values('id','due_head__value')
						#print(qry3)
						qry3_count=NoDuesHead.objects.filter(emp_id=qry2[y]['emp_id'],id=qry1[x]['id']).values('id','due_head__value').count()
						#print(qry3_count)
						for z in range(qry3_count):
							dic1={}
							dic1['EmpId']=qry2[y]['emp_id']
							dic1['Name']=qry2[y]['emp_id__name']
							dic1['NoDuesDept']=qry3[z]['due_head__value']
							dic1['NoDuesId']=qry3[z]['id']
							dic.append(dic1)
					#print(dic1)
				#print(dic)
				#qry3=EmployeeDropdown.objects.filter(field="No Dues Category").exclude(value__isnull=True).extra(select={'tv':'value','ts':'sno'}).values('tv','ts')
				error=False
				msg='Success...'
			else:
				msg="Not Loggedin!!"
		else:
			msg="not permitted"
	else:
		msg="Technical Error:Wrong Parameters"
	data={'data':dic,'error':error,'msg':msg}
	return JsonResponse(data,safe=False)



def approve_nodues(request):
	error=True
	if 'HTTP_COOKIE' in request.META:			
		if request.user.is_authenticated():	
			if request.session['hash3'] == 'Employee':
				if request.body:
					inp = json.loads(request.body.decode('utf-8'))
					#print(inp)
					emp_id=inp['Emp_Id']
					#print(emp_id)
					head_id=inp['NoDuesId']
					# qry1=NoDuesHead.objects.filter(emp_id=emp_id).values('id','due_head__value','emp_id')
					# qry1_count=NoDuesHead.objects.filter(emp_id=emp_id).values('id','due_head__value','emp_id').count()
					# for b in range(qry1_count):
					qry=NoDuesEmp.objects.filter(emp_id=emp_id,head_id=head_id).update(status='APPROVED')
					qry2=NoDuesEmp.objects.filter(emp_id=emp_id).values('emp_id','status')
						
					qry2_count=qry2.count()
					flag=0
					for a in range(qry2_count):
					#	print(a)
						
						if qry2[a]['status']=="APPROVED":
							flag=1
						else:
							flag=0
							break
					
								
					if(flag==1):
						qry3=EmployeePrimdetail.objects.filter(emp_id=emp_id).update(emp_status='SEPARATE')
					else:
						qry3=EmployeePrimdetail.objects.filter(emp_id=emp_id).update(emp_status='ACTIVE')
					msg="Approved"
					error=False
				else:
				 	msg="Invalid Input"
			else:
				msg="not permitted"
		else:
			msg="not logged in"
	else:
		msg="Technical Error:wrong parameters"
	values={'error':error,'msg':msg}
	return JsonResponse(values,safe=False)


def GetData(request):
	error=True
	msg=""
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				data = json.loads(request.body)
				EmpId = data['emp_id']
				QryGetEmp = EmployeePrimdetail.objects.filter(emp_id = EmpId).values()
				if QryGetEmp.count():
					msg = "Success"
					error = False
				else:
					msg = "No data Found"
					error = True	
			else:
				msg="User not authenticated"	
		else:
			msg="No cookie"		
	else:
		msg="No request"	
	
	data_to_be_sent={'data':list(QryGetEmp),'msg':msg,'error':error}
	
	return JsonResponse(data_to_be_sent,safe=False)	

###################################### Assign Links Dashboard ###############################

def GetLinks(request):
	error=True
	
	if request.META:
		if 'HTTP_COOKIE' in request.META:
			if request.user.is_authenticated():
				sub_links=[]
				link_qry=LeftPanel.objects.filter(parent_id=0).values('menu_id','link_name')
				#print(link_qry)
				x=0
				for i in link_qry:
					print(i['menu_id'])
					sub_link=LeftPanel.objects.filter(parent_id=i['menu_id']).values('menu_id','link_name')
					print(sub_link)
					#print(list(sub_link))
					a=link_qry[x]['link_name']
					#print(a)
					sub_links.append(list(sub_link))
					#
					x+=1
				print(sub_links)
				role_qry=LeftPanel.objects.exclude(role__value=True).values('role__value','role').distinct()
				#print(role_qry)
				error=False
				msg="Success"
				data={'roles':list(role_qry),'main_links':list(link_qry),'msg':msg,'error':error}	 

			else:
				msg="User not authenticated"	
		else:
			msg="No cookie"		
	else:
		msg="No request"	
	return JsonResponse(data,safe=False)