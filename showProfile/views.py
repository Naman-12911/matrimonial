from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from account.models import User, PrefredGender
from account.serializer import UserSerializers
import random

class MatchedProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_gender = user.gender

        # Get user's preferred gender
        try:
            user_preference = PrefredGender.objects.get(user=user)
        except PrefredGender.DoesNotExist:
            return Response({"detail": "Preferred gender not found for the user."}, status=400)

        # If logged-in user is Male ('M'), show Female ('F') and vice versa
        opposite_gender = 'F' if user_gender == 'M' else 'M'

        # Initial queryset for opposite gender
        queryset = User.objects.filter(gender=opposite_gender)

        # Initialize an empty Q object for OR conditions
        query_conditions = Q()

        # Add flexible filtering based on preferences (using OR logic for any one condition)
        # Height: +- 5% range
        if user_preference.prefred_height:
            height_filter = Q(height__gte=user_preference.prefred_height * 0.95,
                              height__lte=user_preference.prefred_height * 1.05)
            query_conditions |= height_filter

        # Location: partial match using __icontains
        if user_preference.prefred_location:
            location_filter = Q(location__icontains=user_preference.prefred_location)
            query_conditions |= location_filter

        # Religion: partial match using __icontains
        if user_preference.prefred_religion:
            religion_filter = Q(religion__icontains=user_preference.prefred_religion)
            query_conditions |= religion_filter

        # Income: +- 20% range
        if user_preference.prefred_income:
            income_filter = Q(income__gte=user_preference.prefred_income * 0.8,
                              income__lte=user_preference.prefred_income * 1.2)
            query_conditions |= income_filter

        # Family Type: partial match using __icontains
        if user_preference.family_type:
            family_type_filter = Q(family_type__icontains=user_preference.family_type)
            query_conditions |= family_type_filter

        # Smoke: Exact match since it's boolean
        if user_preference.prefred_smoke is not None:
            smoke_filter = Q(smoke=user_preference.prefred_smoke)
            query_conditions |= smoke_filter

        # Drink: Exact match since it's boolean
        if user_preference.prefred_drink is not None:
            drink_filter = Q(drink=user_preference.prefred_drink)
            query_conditions |= drink_filter

        # Apply the OR conditions
        queryset = queryset.filter(query_conditions)

        # Shuffle the results for a probabilistic approach
        profile_list = list(queryset)
        random.shuffle(profile_list)

        # Serialize the results, pass the request to check for membership in the serializer
        serializer = UserSerializers(profile_list, many=True, context={'request': request})

        return Response(serializer.data)
