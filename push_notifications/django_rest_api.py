from rest_framework import serializers, mixins, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_404_NOT_FOUND, \
    HTTP_202_ACCEPTED, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK

from .models import APNSDevice, GCMDevice, Device



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to see it.
    """

    def has_object_permission(self, request, view, obj):
        # Only allow the user to see their own devices
        return obj.user == request.user


class DeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Device
		fields = ('name', 'user', 'active', 'date_created')


class APNSDeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = APNSDevice
		fields = ('name', 'user', 'active', 'date_created', 'device_id', 'registration_id')


class GCMDeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = GCMDevice
		fields = ('name', 'user', 'active', 'date_created', 'device_id', 'registration_id')


class DeviceViewSetMixin(object):
	queryset = APNSDevice.objects.all()
	serializer_class = APNSDeviceSerializer
	permission_classes = (permissions.IsAuthenticated,
	                      IsOwner,)

	def pre_save(self, obj):
		# Set the requesting user as the device user
		obj.user = self.request.user


class APNSDeviceViewSet(DeviceViewSetMixin, viewsets.ModelViewSet):
	queryset = APNSDevice.objects.all()
	serializer_class = APNSDeviceSerializer


class GCMDeviceViewSet(DeviceViewSetMixin, viewsets.ModelViewSet):
	queryset = GCMDevice.objects.all()
	serializer_class = GCMDeviceSerializer


apns_list = APNSDeviceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

apns_detail = APNSDeviceViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

gcm_list = GCMDeviceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

gcm_detail = GCMDeviceViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})
