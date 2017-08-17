from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from .views import Add_Shift,view_shift_data,display_shift,field_add,add_employee,add_update_dropdown,field_addtn,delete_cat,field_update,field_delete,field_update_view,Update,update_view_id,update_view_info,update_info,fields,show_category,add_cat,update_cat,category_value,add_pay,pay_view,long_leave_type,seperate_req,employee_view,add_no_dues,separation_previous,separation_approval_admin,separation_employee_details,separation_employee_status,view_approval_status,no_dues,separation_employee,separation_approval_hod,separation_employee_details_hod,view_approval_status_hod,delete_nodues,separation_employee_status_hod,noduesApproval,approve_nodues,GetData,GetLinks
urlpatterns = [

    #url(r'^/$', admin.site.urls),
    url(r'^add/$', field_add),
	url(r'^data/$', add_employee),
    url(r'^update/values/$',Update),
    url(r'^add/values/$', category_value),
##################### MUSTERROLL SETTINGS ######################
	url(r'^add_update_dropdown/$',add_update_dropdown),
	url(r'^add_update_dropdown/add$',field_addtn),
	url(r'^add_update_dropdown/update$',field_update),
	url(r'^add_update_dropdown/delete$',field_delete),
	url(r'^add_update_dropdown/values$',field_update_view),
	############## UPDATE EMPLOYEE ####################
	url(r'^update_employee/id$',update_view_id),
	url(r'^update_employee/info$',update_view_info),
	url(r'^update_employee/update$',update_info),
	
    
################ SEPERATION ########################
	url(r'^long_leave/$',long_leave_type),
	url(r'^seperate_request/$',seperate_req),
	url(r'^nodues_approve/$',noduesApproval),
	
	url(r'^fields/$',fields),
	url(r'^approve/$',approve_nodues),
	url(r'^fields_category/$',show_category),
	url(r'^add_category/$',add_cat),
	url(r'^update_category/$',update_cat),
	url(r'^delete_category/$',delete_cat),

################### SHIFT SETTINGS ###################
	url(r'^view_shift/$',display_shift),
	url(r'^add_shift/$',Add_Shift),
	url(r'^previous_shift/$',view_shift_data),

############### PAYROLL#######################
	url(r'^add_pay/$',add_pay),
	url(r'^pay/$',pay_view),

################ NO DUES ####################
	url(r'^no_dues/$',employee_view),
	url(r'^assign/$',no_dues),
	url(r'^delete_nodues/$',delete_nodues),
	url(r'^no_dues_add/$',add_no_dues),
	url(r'^separation_prev/$',separation_previous),
############### Separation ###################
	url(r'^separation_employee/$',separation_approval_admin),
	url(r'^separation_details/$',separation_employee_details),
	url(r'^separation/$',separation_employee),
	url(r'^separation_status_hod/$',separation_employee_status_hod),
	url(r'^separation_status/$',separation_employee_status),
	url(r'^separation_table/$',view_approval_status),
	url(r'^separation_table_hod/$',view_approval_status_hod),
	url(r'^separation_employee_hod/$',separation_approval_hod),
	url(r'^separation_details_hod/$',separation_employee_details_hod),
	################### Employee RecordReport ############
	url(r'^GetData$',GetData),
	#################### Dashboard Assign Link #############
	url(r'^GetLinks/$',GetLinks)
	
]




