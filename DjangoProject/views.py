from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from  all_models_app.models import User
# Custom Serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id  # ✅ User ID যুক্ত করছি
        # data['user_type'] = self.user.user_type
        # data['is_present'] = self.user.is_present
        # data['attendance_id'] = self.user.attendance_id
        # data['username'] = self.user.username  # ✅ Username পাঠাচ্ছি (চাইলে বাদ দিতে পারো)
        return data

# Custom View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



