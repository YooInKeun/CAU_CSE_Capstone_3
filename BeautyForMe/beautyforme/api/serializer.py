from accounts.models import *
from cosmetic.models import *
from makeup.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BigCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Big_Category
        fields = '__all__'

class SmallCategorySerializer(serializers.ModelSerializer):
    big_category = BigCategorySerializer()
    class Meta:
        model = Small_Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = SmallCategorySerializer()
    tag_names = TagSerializer(many=True)
    # cosmetics = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class CosmeticSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cosmetic
        fields = '__all__'

class UserCosmeticSerializer(serializers.ModelSerializer):
    cosmetic = CosmeticSerializer()

    class Meta:
        model = User_Cosmetic
        fields = '__all__'

class UserInterestedCosmeticSerializer(serializers.ModelSerializer):
    cosmetic = CosmeticSerializer()

    class Meta:
        model = User_Interested_Cosmetic
        fields = '__all__'

class CosmeticImportanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cosmetic_Importance
        fields = '__all__'

class BigCateroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Big_Category
        fields = '__all__'

class SmallCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Small_Category
        fields = '__all__'

class CosmeticImportanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cosmetic_Importance
        fields = '__all__'

class YoutuberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtuber
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    youtuber = YoutuberSerializer()
    
    class Meta:
        model = Video
        fields = '__all__'

class VideoBookmarkSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    
    class Meta:
        model = Video_Bookmark
        fields = '__all__'