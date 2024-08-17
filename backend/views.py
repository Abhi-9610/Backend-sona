from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from rest_framework import  status
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .models import CustomUser, ProductsModels,LoactionModel,ReviewModel
from .serializers import CustomUserCreateSerializer, StaffSerializer,ProductSer,locationSerializer,ReviewSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from sona.settings import SECRET_KEY



api="/api"


@api_view(['POST'])
@permission_classes([AllowAny])
def create_subuser(request):
   
    mutable_data = request.data.copy()
    
    # Extracting the password from the request data
    password = mutable_data.get('password')
    # Hashing the password
    hashed_password = make_password(password)
    # Adding the hashed password to the mutable data
    mutable_data['password'] = hashed_password
    mutable_data['role']=2

    serializer = CustomUserCreateSerializer(data=mutable_data)
    if serializer.is_valid():
        serializer.save()
        profile_image = serializer.data.get('profile')
        if profile_image:
            complete_url = f"{request.build_absolute_uri(api)}{profile_image}"
            print(profile_image)
            serializer.data['profile'] = complete_url
            

            data={
                'name':serializer.data.get('name'),
                'mobile':serializer.data.get('mobile'),
                'email':serializer.data.get('email'),
                'role':serializer.data.get('role'),
                'profile':complete_url

                
            }
       

        # print(user.__dict__)
        return JsonResponse({'message':'successfull','status':True,'data':data},status=status.HTTP_201_CREATED)
    return JsonResponse({'message':serializer.errors,'status':False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])

@permission_classes([AllowAny])
def subuser_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    serializer = CustomUserCreateSerializer(data=request.data)
    serializer.is_valid()
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return JsonResponse({'message':"Loggin Successfully!!",
                             "token":token.key,
                             'data':serializer.data,
                             'status':True}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'status':False,'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_staff(request):

    
    # nae,mobile,email,profile,owner_id
    name = request.data.get("name")
    mobile = request.data.get("mobile")
    email = request.data.get("email")
    profile=request.data.get('profile')
   
    auth_token=request.headers.get('Authorization').split()[1]
    # print(auth_token)
    token=Token.objects.get(key=auth_token)
    # print(token.user)
    user = CustomUser.objects.get(email=token.user.email)
    # print(user.unique_id)
    owner_id = user.unique_id
    dataObject = {
        "name":name,
        
        "email":email,
        "profile":profile,
        "owner_id":str(owner_id)
    }
   
    if(name == None or mobile == None or email == None):
        return JsonResponse({'message':'Unsufficient Data','status':False},status=status.HTTP_400_BAD_REQUEST)
    
    serializer = StaffSerializer(data=dataObject)
    if serializer.is_valid():
        serializer.save()
        profile_image = serializer.data.get('profile')
        if profile_image:
            complete_url = f"{request.build_absolute_uri(api)}{profile_image}"
            print(profile_image)
            serializer.data['profile'] = complete_url
            

            data={
                'name':serializer.data.get('name'),
                'mobile':serializer.data.get('mobile'),
                'email':serializer.data.get('email'),
                'owner_id':serializer.data.get('owner_id'),
                'profile':complete_url,
                'unique_id':serializer.data.get('unique_id')

                
            }
        return JsonResponse({'message':'successfull','data':data,'status':True} ,status=status.HTTP_201_CREATED)
    return JsonResponse({'message':serializer.errors,'status':False}, status=status.HTTP_400_BAD_REQUEST)



# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_products(request):
        
            name=request.data.get('name')
            image=request.data.get('image')
            desc=request.data.get('desc')
            

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
                'desc':desc,
                "owner_id":str(owner_id)
            }
            # arr=[name,image,desc,owner_id]
        
            if(name == None or desc == None or image == None):
                return JsonResponse({'message':'Unsufficient Data','status':False},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = ProductSer(data=dataObject)
            

            
            if serializer.is_valid():
                serializer.save()
                profile_image = serializer.data.get('image')
                if profile_image:
                    complete_url = f"{request.build_absolute_uri(api)}{profile_image}"
                    print(profile_image)
                    serializer.data['profile'] = complete_url
                    

                    dataP={
                        'name':serializer.data.get('name'),
                        
                        'desc':serializer.data.get('desc'),
                        'image':complete_url,
                        'owner_id':serializer.data.get('owner_id'),
                        'products_id':serializer.data.get('Products_id'),

                        
                    }
                
           

                
                return JsonResponse({'message':'successfull','data':dataP,'status':True}, status=status.HTTP_201_CREATED)
            return JsonResponse({'message':serializer.errors,'status':False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subuser_detail(request):
    try:
        subuser = CustomUser.objects.get(unique_id=request.user.unique_id)
        serializer = CustomUserCreateSerializer(subuser)

       
        profile_image = serializer.data.get('profile')
        if profile_image:
            complete_url = f"{request.build_absolute_uri(api)}{profile_image}"
            print(profile_image)
            serializer.data['profile'] = complete_url
            

            data={
                'name':serializer.data.get('name'),
                'mobile':serializer.data.get('mobile'),
                'email':serializer.data.get('email'),
                'role':serializer.data.get('role'),
                'profile':complete_url

                
            }
            
           

        return Response({'message':'successfull','status': True, 'data':data,
                         }, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({'message': 'Subuser not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e), 'status': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_detail(request):
    # Retrieve the unique_id from the token
    unique_id = request.user.unique_id
    
    staff_members = CustomUser.objects.filter(owner_id=unique_id)

    if staff_members.exists():
        serializer = StaffSerializer(staff_members, many=True)
        for product_data in serializer.data:
            image_path = product_data.get('profile', '')
            if image_path:
                complete_url = f"{request.build_absolute_uri(api)}{image_path}"
                print(product_data['profile'])
                product_data['profile'] = complete_url
                print(product_data['profile'])
                


        return JsonResponse({'message':'successfull','status':True,'data':serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'message': 'Staff not found','status':False}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_detail(request):
    # Retrieve the unique_id from the token
    unique_id = request.user.unique_id
    
    try:
        products = ProductsModels.objects.filter(owner_id=unique_id)
    except ProductsModels.DoesNotExist:
        return Response({'message': 'Products not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSer(products, many=True )
    serialized_data = serializer.data
    for product_data in serialized_data:
        image_path = product_data.get('image', '')
        if image_path:
            complete_url = f"{request.build_absolute_uri(api)}{image_path}"
            product_data['image'] = complete_url


    return Response({'message':'successfull','status': True, 'data': serialized_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signout(request):
    try:
        auth_token = request.headers.get('Authorization').split()[1]
        user = request.user
        token = Token.objects.get(user=user)

        if token.key == auth_token:
            token.delete()
            return JsonResponse({'status': True, 'message': 'Successfully signed out'})
        else:
            return JsonResponse({'status': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    except Token.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateuser(request):
    unique_id = request.user.unique_id
    try:
        subadmin = CustomUser.objects.get(unique_id=unique_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Subuser not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserCreateSerializer(subadmin, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        profile_image = serializer.data.get('profile')
        if profile_image:
            complete_url = f"{request.build_absolute_uri(api)}{profile_image}"
            print(profile_image)
            serializer.data['profile'] = complete_url
            

            data={
                'name':serializer.data.get('name'),
                'mobile':serializer.data.get('mobile'),
                'email':serializer.data.get('email'),
                'role':serializer.data.get('role'),
                'profile':complete_url

                
            }
            
           

        return Response({'message':'successfull','status': True, 'data':data,
                         }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatestaff(request, unique_id):
    try:
        # Retrieve the staff member by unique ID
        staff_member = CustomUser.objects.get(unique_id=unique_id, owner_id=request.user.unique_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)

    # Update the staff member's details with the request data
    serializer = CustomUserCreateSerializer(staff_member, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        profile_image = serializer.data.get('profile')
        if profile_image:
            complete_url = f"{request.build_absolute_uri(api)}{profile_image}"
            print(profile_image)
            serializer.data['profile'] = complete_url
            

            data={
                'name':serializer.data.get('name'),
                'mobile':serializer.data.get('mobile'),
                'email':serializer.data.get('email'),
               
                'profile':complete_url

                
            }


        return JsonResponse({'message':'successfull','status':True,'data':data}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, Products_id):
    # Retrieve the unique_id from the token
    unique_id = request.user.unique_id
    
    try:
        product = ProductsModels.objects.get(Products_id=Products_id, owner_id=unique_id)
    except ProductsModels.DoesNotExist:
        return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        profile_image = serializer.data.get('image')
        if profile_image:
                    complete_url = f"{request.build_absolute_uri(api)}{profile_image}"
                    print(profile_image)
                    serializer.data['profile'] = complete_url
                    

                    dataP={
                        'name':serializer.data.get('name'),
                        
                        'desc':serializer.data.get('desc'),
                        'image':complete_url,
                        'owner_id':serializer.data.get('owner_id'),
                        'products_id':serializer.data.get('Products_id'),

                        
                    }
                
           

                
        return JsonResponse({'message':'successfull','data':dataP,'status':True}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def create_user(request):
#     name=request.data.get('name')
#     age=request.data.get('age')
#     image=request.data.get('image')
    
#     data={
#         "name":name,
#         'age':age,
#         "image":image
#     }


#     if(name == None or age == None or image == None):
#                 return JsonResponse({'message':'Unsufficient Data','status':False},status=status.HTTP_400_BAD_REQUEST)
#     serial


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addlocation(request):
        
            name=request.data.get('name')
            
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
               
                'ip':ip,
                'port':port,
                
                
                "owner_id":str(owner_id)
            }
        
            if(name == None  or  ip == None or port==None):
                return JsonResponse({'message':'Unsufficient Data','status':False},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = locationSerializer(data=dataObject)
            if serializer.is_valid():
                serializer.save()
                data={
                    'name':serializer.data.get('name'),
                    'ip':serializer.data.get('ip'),
                    'port':serializer.data.get('port'),
                    'unique_id':serializer.data.get('unique_id')
                
                }
                
                    

                    
                return JsonResponse({'message':'successfull','data':data,'status':True} ,status=status.HTTP_201_CREATED)
            return JsonResponse({'message':serializer.errors,'status':False}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getlocation(request):
    # Retrieve the unique_id from the token
    unique_id = request.user.unique_id
    
    try:
        products = LoactionModel.objects.filter(owner_id=unique_id)
    except LoactionModel.DoesNotExist:
        return Response({'message': 'Location not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

    serializer = locationSerializer(products, many=True)
    serialized_data = serializer.data
    print(serialized_data)
    
    

    return Response({'message':'successfull','status': True, 'data': serialized_data}, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def locationdetails(request, unique_id):
    robot = get_object_or_404(LoactionModel, unique_id=unique_id)

    
    print(robot)
    if request.method == 'PUT':
        serializer = locationSerializer(robot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data={
                    'name':serializer.data.get('name'),
                    'ip':serializer.data.get('ip'),
                    'port':serializer.data.get('port'),
                    'unique_id':serializer.data.get('unique_id')
                
                }
            return Response({'status':True,'message':'successfull','data':data},status=status.HTTP_200_OK)
        return Response({'status':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        robot.delete()
        return Response({'status':True,'message': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addReview(request):
            rating=request.data.get('rating')
            
            comment =request.data.get('comment')
            
            

            auth_token=request.headers.get('Authorization').split()[1]
            # print(auth_token)
            token=Token.objects.get(key=auth_token)
            # print(token.user)
            user = CustomUser.objects.get(email=token.user.email)
            # print(user.unique_id)
            owner_id = user.unique_id
            dataObject = {
                "rating":rating,
                'comment':comment,
               
                
                
                "owner_id":str(owner_id)
            }
        
            if(rating == None ):
                return JsonResponse({'message':'Unsufficient Data','status':False},status=status.HTTP_400_BAD_REQUEST)

            elif(comment==None):
                data={
                    'rating':rating,
                    
                
                }
                return JsonResponse({'message':'successfull','data':data,'status':True} ,status=status.HTTP_201_CREATED)
                
                



            serializer = ReviewSerializer(data=dataObject)
            if serializer.is_valid():
                serializer.save()
                
                newdata={
                    'rating':serializer.data.get('rating'),
                    'comment':serializer.data.get('comment'),

                }
                
                    

                    
                return JsonResponse({'message':'successfull','data':newdata,'status':True} ,status=status.HTTP_201_CREATED)
            return JsonResponse({'message':serializer.errors,'status':False}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getallReview(request):
    # Retrieve the unique_id from the token
    unique_id = request.user.unique_id
    
    try:
        products = ReviewModel.objects.filter(owner_id=unique_id)
    except ReviewModel.DoesNotExist:
        return Response({'message': 'No Review Found', 'status': False}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(products, many=True)
    serialized_data = serializer.data
    # print(serialized_data)
    
    

    return Response({'message':'successfull','status': True, 'data': serialized_data}, status=status.HTTP_200_OK)