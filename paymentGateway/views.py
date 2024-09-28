from django.shortcuts import render
from rest_framework import status
from account.models import User
from .models import SubscriptionModel
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import SubscriptionModelSerializers
from django.http.response import Http404


class SubscriptionModelAPIview(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return SubscriptionModel.objects.get(pk=pk)
        except SubscriptionModel.DoesNotExist:
            raise Http404
        
    def get(self, request, pk=None, format=None):
            if pk:
                data = self.get_object(pk)
                serializer = SubscriptionModelSerializers(data)
                return Response(serializer.data)

            else:
                data = SubscriptionModel.objects.all()
                serializer = SubscriptionModelSerializers(data, many=True)

                return Response(serializer.data)
            
    def post(self, request, format=None):
        current_user = request.user
        mutable_data = request.data.copy() if request.data else {}

        mutable_data['user'] = current_user.id 
                
        serializer = SubscriptionModelSerializers(data=mutable_data)

        # Check if the data passed is valid
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return Response to User
        response = Response({
            'message': 'Subscription Model Created Successfully',
            'data': serializer.data
        })
        return response
    
    def patch(self, request, pk=None, format=None):
        # Get the todo to update
        SubscriptionModel_to_update = SubscriptionModel.objects.get(pk=pk)

        serializer = SubscriptionModelSerializers(instance=SubscriptionModel_to_update, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response()
        response.data = {
            'message': 'Subscription Model updated Successfully',
            'data': serializer.data
        }

        return response