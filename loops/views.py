from django.shortcuts import get_list_or_404, get_object_or_404, render, HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from robot.models import *
from backend.models import CustomUser
from .models import *
from .serializers import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loopsfun(request):
    goalid = request.data.get('goalid')
    roboid = request.data.get('roboid')
    name = request.data.get('name')
    time_delay_seconds = request.data.get('time_delay_seconds')

    try:
        auth_token = request.headers.get('Authorization').split()[1]
        token = Token.objects.get(key=auth_token)
        user = CustomUser.objects.get(email=token.user.email)
        owner_id = user.unique_id

        # Clean the input UUID strings by removing unwanted characters
        roboid = roboid.strip()
        goalid = goalid.strip()

        # Check if the provided roboid and goalid exist in the respective models
        robo_exists = robotModel.objects.filter(unique_id=roboid).exists()
        goal_exists = goalsModel.objects.filter(unique_id=goalid).exists()

        if robo_exists and goal_exists:
            dataObject = {
                'roboid': str(roboid),
                'goalid': str(goalid),
                'time_delay_seconds': time_delay_seconds,
                'admin_id': str(owner_id),
                'type': '1',
                'name': name
            }

            serializer = loopsSerializer(data=dataObject)
            if serializer.is_valid():
                loop_instance = serializer.save()

                data = {
                    'name': loop_instance.name,
                    'roboid': loop_instance.roboid,
                    'time_delay_seconds': loop_instance.time_delay_seconds,
                    'created_at': loop_instance.created_at,
                    'unique_id': loop_instance.unique_id,
                    'admin_id': loop_instance.admin_id,
                    'type': loop_instance.type,
                    'related_events': []  # initialize an empty list for related events
                }

                dataob = {
                    'owner_id': data.get('roboid'),
                    'goalid': goalid,
                    'type': '1'
                }

                serializer1 = loopeventSerializer(data=dataob)
                if serializer1.is_valid():
                    serializer1.save()

                    # Filter related events using owner_id
                    related_events = loopevent.objects.filter(owner_id=str(roboid))

                    # Serialize the related events
                    related_events_serializer = loopeventSerializer(related_events, many=True)

                    # Update the 'related_events' key in the 'data' dictionary
                    data['related_events'] = related_events_serializer.data

                    return JsonResponse({'message':'successfull','data': data,
                                         'status': True}, status=status.HTTP_201_CREATED)

                else:
                    return JsonResponse({'message': serializer1.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return JsonResponse({'message': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)

    except Token.DoesNotExist:
        return JsonResponse({'message': 'Invalid token', 'status': False}, status=status.HTTP_401_UNAUTHORIZED)

    except CustomUser.DoesNotExist:
        return JsonResponse({'message': 'User not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JsonResponse({'message': str(e), 'status': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'message': 'goalid and roboid not matched!!', 'status': False}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events_by_roboid(request, roboid):
    try:
        # Assuming roboid is a valid UUID, you might want to add validation here

        # Filter events based on the provided roboid
        events = loopevent.objects.filter(owner_id=roboid)

        # Serialize the events
        serializer = loopeventSerializer(events, many=True)

        return JsonResponse({'message':'successfull','events': serializer.data, 'status': True})

    except loopevent.DoesNotExist:
        return JsonResponse({'message': 'Events not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getloop(request, roboid):

        loop_instances = get_list_or_404(loops, roboid=roboid)
        # Retrieve loop details
        serializer = loopsSerializer(loop_instances, many=True)
        return Response({'message':'successfull','data': serializer.data, 'status': True})

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_loop(request, roboid):
    try:
        # Use get_list_or_404 to handle multiple objects with the same roboid
        loop_instances = get_list_or_404(loops, roboid=roboid)

        if request.method == 'PUT':
            # Partial update for loop
            if loop_instances:
                serializer = loopsSerializer(loop_instances[0], data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message':'successfull','data': serializer.data, 'status': True})
                return Response({'message': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'No loops found for the specified roboid', 'status': False}, status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'DELETE':
            # Delete all loops with the specified roboid
            for loop_instance in loop_instances:
                loop_instance.delete()
            return Response({'message': 'Loops deleted successfully', 'status': True})

    except loops.DoesNotExist:
        return Response({'message': 'Loops not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_loopevent(request, unique_id):
    try:
        event_instance = loopevent.objects.get(unique_id=unique_id)

        if request.method == 'PUT':
            # Partial update for event
            if request.data:
                serializer = loopeventSerializer(event_instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message':'successfull','data': serializer.data, 'status': True})
                return Response({'message': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'No data provided for update', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            # Delete event
            event_instance.delete()
            return Response({'message': 'Event deleted successfully', 'status': True})

    except loopevent.DoesNotExist:
        return Response({'message': 'Event not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task(request):
    try:
        name = request.data.get('name')
        roboid = request.data.get('roboid')
        
        timestring = request.data.get('timestring')

        auth_token = request.headers.get('Authorization').split()[1]
        token = Token.objects.get(key=auth_token)
        user = CustomUser.objects.get(email=token.user.email)
        owner_id = user.unique_id

        # Clean the input UUID strings by removing unwanted characters
        roboid = roboid.strip()
        

        # Check if the provided roboid and goalid exist in the respective models
        robo_exists = robotModel.objects.filter(unique_id=roboid).exists()
        # goal_exists = goalsModel.objects.filter(unique_id=goalid).exists()

        if robo_exists:
            dataObject = {
                'roboid': str(roboid),
                
                'timestring': timestring,
                'admin_id': str(owner_id),
                'type': '2',
                'name': name
            }
            
            serializer = taskSerializer(data=dataObject)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'successfull','data': serializer.data, 'status': True})
            else:
                return JsonResponse({'message': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'Error: Robo or Goal not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': str(e), 'status': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request, roboid):
    try:
        loop_instances = get_list_or_404(loops, roboid=roboid)
        # Retrieve loop details
        serializer = taskSerializer(loop_instances, many=True)
        return Response({'message':'successfull','data': serializer.data, 'status': True})
    except:
        return Response({'message': 'Task not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)




@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_task(request, unique_id):
    try:
            task_instance = loops.objects.get(unique_id=unique_id)
      

            if request.method == 'PUT':
                # Partial update for task
                serializer = taskSerializer(task_instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message':'successfull','data': serializer.data, 'status': True})
                
                return Response({'message': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)

            elif request.method == 'DELETE':
                # Delete task
                task_instance.delete()
                return Response({'message': 'Task deleted successfully', 'status': True})

    except:
        return Response({'message': 'Task not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

