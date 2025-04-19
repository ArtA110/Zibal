from enum import Enum

# Only for better understanding of the concept because we do not use RDBMS here
class NotificationStatus(Enum):
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'
    RETRYING = 'retrying'

class NotificationMedium(Enum):
    SMS = 'sms'
    EMAIL = 'email'
    TELEGRAM = 'telegram'
