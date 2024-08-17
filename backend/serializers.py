from rest_framework import serializers
from .models import CustomUser, UserProfile,ProductsModels,LoactionModel,ReviewModel
from drf_extra_fields.fields import Base64ImageField




class CustomUserCreateSerializer(serializers.ModelSerializer):
    profile = Base64ImageField(required=True)
    class Meta:
        model = CustomUser
        fields = ['name', 'mobile', 'email', 'password', 'profile','role']
        extra_kwargs = {'password': {'write_only': True}}

    
    
   

class CustomUserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    profile = Base64ImageField(required=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()


    class Meta:
        model = CustomUser
        fields = '__all__'

   

class StaffSerializer(serializers.ModelSerializer):
    profile = Base64ImageField(required=True)
    class Meta:
        model= CustomUser
        fields=['name','mobile','email','owner_id','profile','unique_id']

    def create(self, validated_data):
        # Set the role to 3 when creating the staff user
        validated_data['role'] = 3
        staff = CustomUser.objects.create(**validated_data)
        return staff
   
    

class ProductSer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = ProductsModels
        fields = ['name', 'image', 'desc', 'owner_id','Products_id']

    
# class userSerializer(serializers.ModelSerializer):
#     image=Base64ImageField(required=True)
#     class Meta:
#         model=usermodel
#         fields="__all__"
class locationSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoactionModel
        fields="__all__"
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReviewModel
        fields="__all__"