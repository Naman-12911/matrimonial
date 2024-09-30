from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from account.models import User, PrefredGender
from .serializer import UserSerializers,SwipeSerializers
from .models import Swipe
import random
from django.http.response import Http404

# class MatchedProfilesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         user_gender = user.gender

#         # Get user's preferred gender
#         try:
#             user_preference = PrefredGender.objects.get(user=user)
#         except PrefredGender.DoesNotExist:
#             return Response({"detail": "Preferred gender not found for the user."}, status=400)

#         # If logged-in user is Male ('M'), show Female ('F') and vice versa
#         opposite_gender = 'F' if user_gender == 'M' else 'M'

#         # Initial queryset for opposite gender
#         queryset = User.objects.filter(gender=opposite_gender)

#         # Initialize an empty Q object for OR conditions
#         # query_conditions = Q()

#         # Add flexible filtering based on preferences (using OR logic for any one condition)
#         # Height: +- 5% range
#         # if user_preference.prefred_height:
#         #     height_filter = Q(height__gte=user_preference.prefred_height * 0.95,
#         #                       height__lte=user_preference.prefred_height * 1.05)
#         #     query_conditions |= height_filter

#         # # Location: partial match using __icontains
#         # if user_preference.prefred_location:
#         #     location_filter = Q(location__icontains=user_preference.prefred_location)
#         #     query_conditions |= location_filter

#         # # Religion: partial match using __icontains
#         # if user_preference.prefred_religion:
#         #     religion_filter = Q(religion__icontains=user_preference.prefred_religion)
#         #     query_conditions |= religion_filter

#         # # Income: +- 20% range
#         # if user_preference.prefred_income:
#         #     income_filter = Q(income__gte=user_preference.prefred_income * 0.8,
#         #                       income__lte=user_preference.prefred_income * 1.2)
#         #     query_conditions |= income_filter

#         # # Family Type: partial match using __icontains
#         # if user_preference.family_type:
#         #     family_type_filter = Q(family_type__icontains=user_preference.family_type)
#         #     query_conditions |= family_type_filter

#         # # Smoke: Exact match since it's boolean
#         # if user_preference.prefred_smoke is not None:
#         #     smoke_filter = Q(smoke=user_preference.prefred_smoke)
#         #     query_conditions |= smoke_filter

#         # # Drink: Exact match since it's boolean
#         # if user_preference.prefred_drink is not None:
#         #     drink_filter = Q(drink=user_preference.prefred_drink)
#         #     query_conditions |= drink_filter

#         # Apply the OR conditions
#         queryset = queryset.filter(queryset)

#         # Shuffle the results for a probabilistic approach
#         profile_list = list(queryset)
#         random.shuffle(profile_list)

#         # Serialize the results, pass the request to check for membership in the serializer
#         serializer = UserSerializers(profile_list, many=True, context={'request': request})

#         return Response(serializer.data)


class MatchedProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_gender = user.gender

        # Get user's preferred gender
        # try:
        #     user_preference = PrefredGender.objects.get(user=user)
        # except PrefredGender.DoesNotExist:
        #     return Response({"detail": "Preferred gender not found for the user."}, status=400)

        # Determine opposite gender for filtering (assuming only male 'M' and female 'F')
        opposite_gender = 'F' if user_gender == 'M' else 'M'

        # Fetch users of the opposite gender
        queryset = User.objects.filter(gender=opposite_gender)

        # Shuffle the results randomly
        profile_list = list(queryset)
        random.shuffle(profile_list)

        # Serialize the results
        serializer = UserSerializers(profile_list, many=True, context={'request': request})

        return Response(serializer.data)

class SwipeOrMatchAPIview(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk=None, format=None):
            if pk:
                data = self.get_object(pk)
                serializer = Swipe(data)
                return Response(serializer.data)

            else:
                data = Swipe.objects.all()
                serializer = SwipeSerializers(data, many=True)

                return Response(serializer.data)
            
    def post(self, request, format=None):
        current_user = request.user
        mutable_data = request.data.copy() if request.data else {}

        mutable_data['user'] = current_user.id 
                
        serializer = SwipeSerializers(data=mutable_data)

        # Check if the data passed is valid
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return Response to User
        response = Response({
            'message': 'Swipe match Created Successfully',
            'data': serializer.data
        })
        return response
    
    def patch(self, request, pk=None, format=None):
        # Get the todo to update
        swipe_to_update = Swipe.objects.get(pk=pk)

        serializer = SwipeSerializers(instance=swipe_to_update, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response()
        response.data = {
            'message': 'user updated Successfully',
            'data': serializer.data
        }

        return response