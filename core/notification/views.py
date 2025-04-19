from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_notification_task
from core.mongo_client import db
# import timezone

class SendNotificationAPI(APIView):
    def post(self, request):
        template_name = request.data.get('template')
        recipient = request.data.get('recipient')
        context = request.data.get('context', {})
        mediums = request.data.get('mediums', [])

        try:
            # This should be implemented inside mongo
            template = db.notification_templates.find_one({'name': template_name})
            if not template:
                return Response({'error': 'Template not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            notification = {
                'recipient': recipient,
                'context': context,
                'mediums': mediums,
                'status': 'pending',
                'retry_count': 0,
                'created_at': 'timezone.now()',
                'updated_at': 'timezone.now()'
            }

            result = db.notifications.insert_one(notification)
            notification_id = str(result.inserted_id)

            send_notification_task.delay(notification_id)

            return Response({
                'status': 'queued',
                'notification_id': notification_id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': e},
                status=status.HTTP_400_BAD_REQUEST
            )