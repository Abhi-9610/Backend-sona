from django.shortcuts import get_object_or_404, render,HttpResponse
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from backend.models import CustomUser
from django.http import JsonResponse
from rest_framework import  status 
from rest_framework.response import Response
from .serializers import *
# Create your views here.
def home(request):
   return HttpResponse('home')



api='api'
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addrobot(request):
        
            name=request.data.get('name')
            image=request.data.get('image')
            ip =request.data.get('ip')
            port = request.data.get('port')
            

            auth_token=request.headers.get('Authorization').split()[1]
            # print(auth_token)
            token=Token.objects.get(key=auth_token)
            # print(token.user)
            user = CustomUser.objects.get(email=token.user.email)
            # print(user.unique_id)
            owner_id = user.unique_id
            dataObject = {
                "name":name,
                'image':image,
                'ip':ip,
                'port':port,
                
                
                "owner_id":str(owner_id)
            }
        
            if(name == None or image == None or  ip == None or port==None):
                return JsonResponse({'message':'Unsufficient Data','status':False},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = robotSerializer(data=dataObject)
            if serializer.is_valid():
                serializer.save()
                profile_image = serializer.data.get('image')
                if profile_image:
                    complete_url = f"{request.build_absolute_uri('')[:-16]}{profile_image}"
                    print(profile_image)
                    serializer.data['profile'] = complete_url
                    

                    data={
                        'name':serializer.data.get('name'),
                        'ip':serializer.data.get('ip'),
                        'port':serializer.data.get('port'),
                        'owner_id':serializer.data.get('owner_id'),
                        'profile':complete_url,
                        'unique_id':serializer.data.get('unique_id')

                        
                    }
                return JsonResponse({'message':'successfull','data':data,'status':True} ,status=status.HTTP_201_CREATED)
            return JsonResponse({'message':serializer.errors,'status':False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addgoals(request):
    name = request.data.get('name')
    random = request.data.get('random')
    audio = request.data.get('audio')
    message = request.data.get('message')

    auth_token = request.headers.get('Authorization').split()[1]
    token = Token.objects.get(key=auth_token)
    user = CustomUser.objects.get(email=token.user.email)
    owner_id = user.unique_id

    dataObject = {
        "name": name,
        'random': random,
        'audio': audio,
        'message': message,
        "owner_id": str(owner_id)
    }

    if name is None or random is None or audio is None:
        return JsonResponse({'message': 'Insufficient Data', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

    # Validate audio format
    

    serializer = goalSerializer(data=dataObject)
    if serializer.is_valid():
        serializer.save()
        audio_url = serializer.data.get('audio')
        if audio_url:
            complete_url = f"{request.build_absolute_uri('')[:-15]}{audio_url}"
            serializer.data['audio'] = complete_url

            data = {
                'name': serializer.data.get('name'),
                'random': serializer.data.get('random'),
                'message': serializer.data.get('message'),
                'owner_id': serializer.data.get('owner_id'),
                'audio': complete_url,
                'unique_id': serializer.data.get('unique_id')
            }

            return JsonResponse({'message':'successfull','data': data, 'status': True}, status=status.HTTP_201_CREATED)

    return JsonResponse({'message': serializer.errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def robot_detail(request, unique_id):
    robot = get_object_or_404(robotModel, unique_id=unique_id)

    
    print(robot)
    if request.method == 'PUT':
        serializer = robotSerializer(robot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'message':'successfull','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        robot.delete()
        return Response({'status':True,'message': 'Robot deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view([ 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def goal_detail(request, unique_id):
    goal = get_object_or_404(goalsModel, unique_id=unique_id)

 
    print(goal)
    if request.method == 'PUT':
        serializer = goalSerializer(goal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response({'status':True,'message':'successfull','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        goal.delete()
        return Response({'status':True,'message': 'Goal deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def goaldetail(request):
    # Retrieve the unique_id from the token
    unique_id = request.user.unique_id
    
    try:
        products = goalsModel.objects.filter(owner_id=unique_id)
    except goalsModel.DoesNotExist:
        return Response({'message': 'goal not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

    serializer =goalSerializer(products, many=True )
    serialized_data = serializer.data
    for product_data in serialized_data:
        image_path = product_data.get('audio')
        if image_path:
            complete_url = f"{request.build_absolute_uri('')[:-15]}{image_path}"
            product_data['audio'] = complete_url


    return Response({'message':'successfull','status': True, 'data': serialized_data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def robotdetail(request):
    # Retrieve the unique_id from the token
    unique_id = request.user.unique_id
    
    try:
        products = robotModel.objects.filter(owner_id=unique_id)
    except robotModel.DoesNotExist:
        return Response({'message': 'Robot not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

    serializer = robotSerializer(products, many=True)
    serialized_data = serializer.data
    
    for product_data in serialized_data:
        image_path = product_data.get('image')
        # api='api'+image_path
        # print(api)

        if image_path:
            api_url = ('api'+image_path)
        
        # Use build_absolute_uri to generate the full URL
            complete_url = f"{request.build_absolute_uri('')[:-18]}{api_url}"

            # Update the image path in product_data with the complete URL
            product_data['image'] = complete_url

    return Response({'message':'successfull','status': True, 'data': serialized_data}, status=status.HTTP_200_OK)



