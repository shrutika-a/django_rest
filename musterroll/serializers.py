from rest_framework import serializers
from login.models import EmployeeDropdown


class FieldListSerializer(serializers.ModelSerializer):
	id=serializers.IntegerField(source='sno') 
	field_name=serializers.CharField(source='field')   
	parent_id=serializers.CharField(source='pid')    
	val=serializers.CharField(source='value')  
	class Meta:
		model = EmployeeDropdown
		fields = ('id','parent_id','field_name','val',)


class CategorySubCategorySerializer(serializers.ModelSerializer): 
	id=serializers.IntegerField(source='sno')   
	val=serializers.CharField(source='value')    
	class Meta:
		model=EmployeeDropdown
		fields=('id','val',)
		