from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, db
from .serializers import RegisteredFace

# Initialize Firebase outside the view function
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://face-recognition-system-ebb56-default-rtdb.firebaseio.com/",
                                     'storageBucket': "face-recognition-system-ebb56.appspot.com"})

# Reference to the Firebase database
ref = db.reference('/registered_faces')


def get_all_users_info(request):
    try:
        # Assuming you pass the information in the header
        request_secret_key = request.headers.get("token")
        if not request_secret_key:
            return JsonResponse({'message': 'Token not provided in the header'}, status=400)

        # Query Firebase to get all users' information
        all_users_data = ref.child(request_secret_key).get()

        if all_users_data:
            # Extract relevant information for all users
            user_list = []
            for registration_id, user_data in all_users_data.items():
                user_name = user_data.get('name', 'User')
                user_age = user_data.get('age', 'N/A')
                image_path = user_data.get('image_path')
                complete_url = f"{request.build_absolute_uri('')}{image_path}"
                user_info = {
                    'registration_id': registration_id,
                    'name': user_name,
                    'age': user_age,
                    'image': complete_url
                }
                user_list.append(user_info)

            return JsonResponse({'message':'successfull','data': user_list})

        else:
            return JsonResponse({'message': 'No users found for the provided token'}, status=404)

    except Exception as e:
        # Handle exceptions, log them, or return an appropriate error response
        return JsonResponse({'message': f'Error retrieving user data: {str(e)}'}, status=500)
