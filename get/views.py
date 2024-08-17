from django.shortcuts import render,HttpResponse
from backend.models import CustomUser
from loops.models import loops
from loops.serializers import loopsSerializer, taskSerializer
from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from django.http import JsonResponse

from robot.models import robotModel
from robot.serializers import robotSerializer
# Create your views here.
def home(request):
    return HttpResponse('home')



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getloop(request):


    try:
        auth_token = request.headers.get('Authorization').split()[1]
        user = request.user.unique_id  # Assuming TokenAuthentication is used, the user is available in request.user

        # Retrieve all robots for the authenticated user
        robots = robotModel.objects.filter(owner_id=user)
        robot_serializer = robotSerializer(robots, many=True)

        # Retrieve all loops for the authenticated user
        loops_instances = loops.objects.filter(admin_id=user)
        loops_serializer = loopsSerializer(loops_instances, many=True)
        

        # Retrieve all tasks for the authenticated user
        
        robot_data = []

        for robot in robots:
            # Retrieve loops for the current robot
            loops_instances = loops.objects.filter(roboid=robot.unique_id)
            loops_serializer = loopsSerializer(loops_instances, many=True)
            tasks_instances =loops.objects.filter(admin_id=user)
            serializer = taskSerializer(tasks_instances,many=True)
            # Create a dictionary for the current robot's data
            robot_data.append({
                'robot_unique_id': robot.unique_id,
                'loops': loops_serializer.data,
                'tasks':serializer.data
            })

        return JsonResponse({
            'message':'successfull',
            'robots': robot_data,
            'status': True
        })

    except Exception as e:
        return JsonResponse({'message': str(e), 'status': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
