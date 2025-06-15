from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer

class UserActivityLogView(GenericAPIView):
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserActivityLog.objects.all()

    def get_object(self):
        return UserActivityLog.objects.get(pk=self.kwargs['pk'], user=self.request.user)

    def get(self, request):
        user = request.user
        action = request.query_params.get('action')
        start = request.query_params.get('start')
        end = request.query_params.get('end')

        cache_key = f"user_logs_{user.id}_{action}_{start}_{end}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        logs = UserActivityLog.objects.filter(user=user)
        if action:
            logs = logs.filter(action=action)
        if start and end:
            logs = logs.filter(timestamp__range=[start, end])

        serializer = self.get_serializer(logs, many=True)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            cache.delete_pattern(f"user_logs_{request.user.id}*")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        try:
            log = self.get_object()
        except UserActivityLog.DoesNotExist:
            return Response({"error": "Log not found"}, status=404)

        if log.user != request.user:
            return Response({"error": "Permission denied"}, status=403)

        new_status = request.data.get('status')
        if new_status not in dict(UserActivityLog.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)

        log.status = new_status
        log.save()
        return Response({'status': 'Updated to ' + new_status})
