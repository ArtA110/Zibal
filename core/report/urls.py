from django.urls import path
from report.views import TransactionReportView, TransactionSummaryAPI

urlpatterns = [
    path('report_aggs/', TransactionReportView.as_view(), name='report_aggs'),
    path('report_aggs_cache/', TransactionSummaryAPI.as_view(), 
         name='report_aggs_cache'),
]