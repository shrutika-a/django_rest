from rest_framework.response import Response
from rest_framework import serializers,generics
from login.models import EmployeeDropdown
from .serializers import FieldListSerializer,CategorySubCategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters,status,mixins
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from login_rest.permissions import CsrfExemptSessionAuthentication,AuthHROnlyRole,AuthEmployeeOnlyRole
from rest_framework.authentication import BasicAuthentication



class FieldList(APIView):
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,AuthHROnlyRole,AuthEmployeeOnlyRole)

	def get(self, request, format=None):
		fieldlist = EmployeeDropdown.objects.filter(value__isnull = False,pid=0)
		serializer = FieldListSerializer(fieldlist, many=True)
		payload={
			"message":"all fields",
			"data" : serializer.data
		}
		return Response(payload)

	def post(self, request, format=None):
		request.data['pid'] = request.data.pop('id')
		request.data['field'] = request.data.pop('field1')
		request.data['value'] = request.data.pop('val1')
		serializer = FieldListSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			payload={
				"message":"field created",
				
			}
			return Response(payload, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorySubCategoryDetail(APIView):
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,AuthEmployeeOnlyRole,AuthHROnlyRole)

	def delete_objects(self, pk):
		try:
			main=EmployeeDropdown.objects.get(pk=pk)
			main.delete()
			subcat=EmployeeDropdown.objects.filter(pid=pk)
			for i in subcat:
				subcategory=EmployeeDropdown.objects.get(sno=i.sno)
				self.delete_objects(i.sno)
			
			return True
		except EmployeeDropdown.DoesNotExist:
			raise Http404
			
	def update_object(self, pk):
		try:

			return EmployeeDropdown.objects.get(pk=pk).extra()
			
		except EmployeeDropdown.DoesNotExist:
			raise Http404
			
	def subcat_objects(self,pk):
			category = EmployeeDropdown.objects.filter(pid=pk)
			serializedcatdata = CategorySubCategorySerializer(category,many=True)
			for i in serializedcatdata.data:
			 	subcat = EmployeeDropdown.objects.filter(pid=i['id'])
			 	serializedsubcatdata=CategorySubCategorySerializer(subcat,many=True)
			 	i['subcat']=serializedsubcatdata.data 
			return serializedcatdata.data

	def cat_objects(self,pk):
		category = EmployeeDropdown.objects.filter(pk=pk).extra(select={'id':'sno','val':'value'})
		serializedcatdata = CategorySubCategorySerializer(category,many=True)		
		serializedcatdata.data[0]['subcat']=self.subcat_objects(pk)
		return serializedcatdata.data

	def get(self, request, pk, format=None):
		
		serializeddata=self.cat_objects(pk)
		payload={
			"message" : "subcategory list",
			"data" : serializeddata
		}
		return Response(payload)

	def put(self, request, pk, format=None):
		category = self.update_object(pk)
		serializer = CategorySubCategorySerializer(category, data=request.data)
		if serializer.is_valid():
			serializer.save()
			payload={
				"message":"field updated",
				
			}
			return Response(payload)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		category=self.delete_objects(pk)
		if(category):
			payload={"message":"deleted successfully!"}
			return Response(payload)
		return Response(status=status.HTTP_204_NO_CONTENT)

