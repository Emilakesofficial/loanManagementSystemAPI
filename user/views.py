from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken

from loan.models import Loan
from .models import UserProfile
from .serializers import RegisterSerializer, UserProfileSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.tokens import AccessToken

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful!",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "image": request.build_absolute_uri(user.profile.image.url)
                        if user.profile.image
                        else None,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            # token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_profile = request.user.profile
        user_profile.update_loan_balance()  # Ensure balance is up-to-date

        return Response({
            "username": request.user.username,
            "loan_balance": user_profile.loan_balance,
        }, status=status.HTTP_200_OK)
    def put(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanApprovalView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id)

        if loan.status != "pending":
            return Response({"error": "Loan is already processed."}, status=status.HTTP_400_BAD_REQUEST)

        action = request.data.get("action")  # Approve or Reject
        if action == "approve":
            loan.status = "approved"
            loan.save()
            loan.user.update_loan_balance()  # Update user's loan balance
            return Response({"message": "Loan approved successfully."}, status=status.HTTP_200_OK)

        elif action == "reject":
            loan.status = "rejected"
            loan.save()
            return Response({"message": "Loan rejected."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action. Use 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)