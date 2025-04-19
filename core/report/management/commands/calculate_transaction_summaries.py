from django.core.management.base import BaseCommand
from core.mongo_client import db

class Command(BaseCommand):

    def handle(self, *args, **options):
        
       
        db.summary_transaction.delete_many({})
        
        self.calculate_daily_summaries(db)
        self.calculate_weekly_summaries(db)
        self.calculate_monthly_summaries(db)
        
        print('Successfull')

    def calculate_daily_summaries(self, db):
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'merchantId': '$merchantId',
                        'year': {'$year': '$createdAt'},
                        'month': {'$month': '$createdAt'},
                        'day': {'$dayOfMonth': '$createdAt'}
                    },
                    'totalAmount': {'$sum': '$amount'},
                    'count': {'$sum': 1},
                    'date': {'$first': '$createdAt'}
                }
            },
            {
                '$project': {
                    'merchantId': '$_id.merchantId',
                    'date': 1,
                    'totalAmount': 1,
                    'count': 1,
                    'type': 'daily',
                    '_id': 0
                }
            },
            {
                '$out': 'summary_transaction'
            }
        ]
        db.transaction.aggregate(pipeline)

    def calculate_weekly_summaries(self, db):
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'merchantId': '$merchantId',
                        'year': {'$year': '$createdAt'},
                        'week': {'$week': '$createdAt'}
                    },
                    'totalAmount': {'$sum': '$amount'},
                    'count': {'$sum': 1},
                    'date': {'$first': '$createdAt'}
                }
            },
            {
                '$project': {
                    'merchantId': '$_id.merchantId',
                    'year': '$_id.year',
                    'week': '$_id.week',
                    'totalAmount': 1,
                    'count': 1,
                    'type': 'weekly',
                    '_id': 0
                }
            },
            {
                '$merge': {
                    'into': 'summary_transaction',
                    'whenMatched': 'replace',
                    'whenNotMatched': 'insert'
                }
            }
        ]
        db.transaction.aggregate(pipeline)

    def calculate_monthly_summaries(self, db):
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'merchantId': '$merchantId',
                        'year': {'$year': '$createdAt'},
                        'month': {'$month': '$createdAt'}
                    },
                    'totalAmount': {'$sum': '$amount'},
                    'count': {'$sum': 1},
                    'date': {'$first': '$createdAt'}
                }
            },
            {
                '$project': {
                    'merchantId': '$_id.merchantId',
                    'year': '$_id.year',
                    'month': '$_id.month',
                    'totalAmount': 1,
                    'count': 1,
                    'type': 'monthly',
                    '_id': 0
                }
            },
            {
                '$merge': {
                    'into': 'summary_transaction',
                    'whenMatched': 'replace',
                    'whenNotMatched': 'insert'
                }
            }
        ]
        db.transaction.aggregate(pipeline)