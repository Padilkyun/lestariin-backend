from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
import requests
import os
import json
import logging
from PIL import Image
import google.generativeai as genai
from .models import User, Profile, Report
from .serializers import SignupSerializer, LoginSerializer, AdminLoginSerializer, UserLoginSerializer, ProfileSerializer, ChatbotSerializer, UserSerializer, ReportSerializer, LeaderboardSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': SignupSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': SignupSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatbotSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            # Integrate with Gemini API
            import google.generativeai as genai
            from django.conf import settings

            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-2.0-flash')
                # Prompt to restrict responses to environmental issues only
                prompt = f"You are Beyonder, an AI chatbot focused on environmental issues. You are an expert in environmental science, sustainability, climate change, pollution, conservation, and related topics. Always provide helpful, accurate, and informative responses about environmental matters. If the question is not related to the environment, politely redirect the conversation to environmental topics. User message: {message}"
                response = model.generate_content(prompt)
                return Response({'response': response.text})
            except Exception as e:
                return Response({'error': 'Failed to generate response', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ReportSerializer(data=request.data)
            if serializer.is_valid():
                # Save the report initially without classifications
                report = serializer.save(user=request.user, verified=False)

                # Analyze description with Gemini API
                try:
                    genai.configure(api_key=settings.GEMINI_API_KEY)
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    prompt = f"""
Analyze this description and classify it for the following environmental issues. Respond only with a JSON object in this exact format, no additional text:
{{
  "water_turbidity": "Air_bersih" or "Air_kotor" or null,
  "forest_fire": "fire" or "non_fire" or null,
  "public_fire": "fire" or "no_fire" or null,
  "trash": "banyak_sampah" or "sedikit_sampah" or null,
  "illegal_logging": "penebangan_liar" or "tidak_penebangan_liar" or null
}}
Focus on detecting signs of water turbidity (kekeruhan air), forest fires (kebakaran hutan), public fires (kebakaran di tempat publik), lots of trash (banyak sampah), and illegal logging (penebangan liar) from the description. If an issue is not detected, set the value to null.

Description: {report.description}
"""
                    response = model.generate_content(prompt)
                    response_text = response.text.strip()
                    logging.info(f"Gemini response text: {response_text}")
                    # Try to parse JSON, if it fails, extract JSON from text
                    try:
                        classifications = json.loads(response_text)
                    except json.JSONDecodeError:
                        # Extract JSON from response if there's extra text
                        import re
                        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                        if json_match:
                            classifications = json.loads(json_match.group())
                        else:
                            # If no JSON found, set to None
                            classifications = {
                                'water_turbidity': None,
                                'forest_fire': None,
                                'public_fire': None,
                                'trash': None,
                                'illegal_logging': None
                            }
                except Exception as e:
                    logging.error(f"Gemini API error: {str(e)}")
                    # If Gemini fails, set classifications to None
                    classifications = {
                        'water_turbidity': None,
                        'forest_fire': None,
                        'public_fire': None,
                        'trash': None,
                        'illegal_logging': None
                    }

                # Update report with classifications
                report.water_classification = classifications.get('water_turbidity', None)
                report.forest_classification = classifications.get('forest_fire', None)
                report.public_fire_classification = classifications.get('public_fire', None)
                report.trash_classification = classifications.get('trash', None)
                report.illegal_logging_classification = classifications.get('illegal_logging', None)
                report.save()

                # Build image URL
                if report.image and report.image.name:
                    image_url = request.build_absolute_uri(report.image.url)
                else:
                    image_url = None

                return Response({
                    'id': report.id,
                    'image_url': image_url,
                    'description': report.description,
                    'latitude': report.latitude,
                    'longitude': report.longitude,
                    'water_classification': report.water_classification,
                    'forest_classification': report.forest_classification,
                    'public_fire_classification': report.public_fire_classification,
                    'trash_classification': report.trash_classification,
                    'illegal_logging_classification': report.illegal_logging_classification,
                    'verified': report.verified,
                    'created_at': report.created_at,
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(f"Unexpected error in ReportView: {str(e)}")
            return Response({'error': 'Internal server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllReportsView(ListAPIView):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class UserReportsView(ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class VerifyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({'error': 'Only admins can verify reports.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response({'error': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)

        if report.verified:
            return Response({'error': 'Report is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the report and award points
        report.verified = True
        report.save()
        report.user.points += 15
        report.user.save()

        return Response({'message': 'Report verified successfully. User awarded 15 points.', 'user_points': report.user.points}, status=status.HTTP_200_OK)

class LeaderboardView(ListAPIView):
    queryset = User.objects.all().order_by('-points')
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
