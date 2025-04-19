from django.core.mail import send_mail


class MediumHandler:
    def render_template(self, notification, medium):
        template_content = getattr(notification.template, f'{medium}_template')
        return template_content.format(**notification.context)

    def send(self, notification):
        raise NotImplementedError

class SMSHandler(MediumHandler):
    def send(self, notification):
        message = self.render_template(notification, 'sms')
        response = f"some req to server with {message}"
        return response.json()

class EmailHandler(MediumHandler):
    def send(self, notification):
        subject = "Notification"
        message = self.render_template(notification, 'email')
        send_mail(
            subject,
            message,
            'noreply@zibal.ir',
            [notification.recipient],
            fail_silently=False,
        )

class TelegramHandler(MediumHandler):
    def send(self, notification):
        message = self.render_template(notification, 'telegram')
        response = response = f"some req to server with {message}"
        return response.json()


def get_handler(medium):
    handlers = {
        'sms': SMSHandler(),
        'email': EmailHandler(),
        'telegram': TelegramHandler(),
    }
    return handlers.get(medium)