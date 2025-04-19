from django.urls import path
from report.views import TransactionReportView

urlpatterns = [
    path('report_aggs/', TransactionReportView.as_view(), name='report_aggs'),
]