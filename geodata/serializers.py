from rest_framework import serializers

from .models import District, Region, Ward


class RegionSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Region
        fields = ["id", "name", "slug", "post_code"]


class DistrictSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = District
        fields = ["id", "name", "slug"]

    def create(self, validated_data):
        region_slug = self.context["region_slug"]
        region = Region.objects.get(slug=region_slug)
        return District.objects.create(region=region, **validated_data)
    

class WardSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Ward
        fields = ["id", "name", "post_code", "slug", "region", "district"]

    def create(self, validated_data):
        district_slug = self.context["district_slug"]
        district = District.objects.get(slug=district_slug)
        return Ward.objects.create(district=district, **validated_data)
