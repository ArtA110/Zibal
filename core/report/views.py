from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from core.mongo_client import db
from datetime import datetime
import jdatetime
from bson import ObjectId


class TransactionReportView(APIView):
    def get(self, request):
        _type = request.GET.get("type", None)
        mode = request.GET.get("mode", None)
        merchant_id = request.GET.get("merchant_id", None)

        if not _type or not mode:
            return Response(
                {"error": "Specify type and mode args"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if _type not in ["count", "amount"]:
            return Response(
                {"error": "Invalid type value"}, status=status.HTTP_400_BAD_REQUEST
            )

        if mode not in ["daily", "weekly", "monthly"]:
            return Response(
                {"error": "Invalid mode value"}, status=status.HTTP_400_BAD_REQUEST
            )

        query = {}
        if merchant_id:
            try:
                query["merchantId"] = ObjectId(merchant_id)
            except Exception:
                pass

        summ = {"$sum": "$amount"} if _type == "amount" else {"$sum": 1}

        pipeline = [
            {"$match": query},
            {"$sort": {"createdAt": 1}},
        ]

        if mode == "daily":
            pipeline.extend(
                [
                    {
                        "$group": {
                            "_id": {
                                "year": {"$year": "$createdAt"},
                                "month": {"$month": "$createdAt"},
                                "day": {"$dayOfMonth": "$createdAt"},
                            },
                            "value": summ,
                            "date": {"$first": "$createdAt"},
                        }
                    },
                    {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}},
                ]
            )
        elif mode == "weekly":
            pipeline.extend(
                [
                    {
                        "$group": {
                            "_id": {
                                "year": {"$year": "$createdAt"},
                                "week": {"$week": "$createdAt"},
                            },
                            "value": summ,
                            "date": {"$first": "$createdAt"},
                        }
                    },
                    {"$sort": {"_id.year": 1, "_id.week": 1}},
                ]
            )
        else:
            pipeline.extend(
                [
                    {
                        "$group": {
                            "_id": {
                                "year": {"$year": "$createdAt"},
                                "month": {"$month": "$createdAt"},
                            },
                            "value": summ,
                            "date": {"$first": "$createdAt"},
                        }
                    },
                    {"$sort": {"_id.year": 1, "_id.month": 1}},
                ]
            )

        results = list(db.transaction.aggregate(pipeline))
        results = self._convert_jalalli(results, mode=mode)
        return Response(results, status=status.HTTP_200_OK)

    def _convert_jalalli(self, results, mode):
        formatted_results = []
        persian_months = [
            "فروردین",
            "اردیبهشت",
            "خرداد",
            "تیر",
            "مرداد",
            "شهریور",
            "مهر",
            "آبان",
            "آذر",
            "دی",
            "بهمن",
            "اسفند",
        ]

        for item in results:
            gregorian_date = item["date"]
            jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)

            if mode == "daily":
                key = (
                    f"{jalali_date.year}/{jalali_date.month:02d}/{jalali_date.day:02d}"
                )
            elif mode == "weekly":
                key = f"هفته {item['_id']['week']} سال {jalali_date.year}"
            elif mode == "monthly":
                month_name = persian_months[jalali_date.month - 1]
                key = f"{month_name} {jalali_date.year}"

            formatted_results.append({"key": key, "value": item["value"]})
            return formatted_results
