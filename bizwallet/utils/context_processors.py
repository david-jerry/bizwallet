from __future__ import absolute_import

from datetime import datetime as dt

from django.conf import settings
from django.db.models import Avg, Count, F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear

from bizwallet.blog.models import Post
from bizwallet.users.models import BalHistory


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {"DEBUG": settings.DEBUG}

def recent_posts(_request):
    return {"recent_posts": Post.objects.recent_posts}


        

current_year = dt.now().strftime("%Y")
current_syear = dt.now().strftime("%y")
previous_year = int(current_year) - 1
previous_syear = int(current_syear) - 1


# def current_balance(_request):
#     return {"current_balance": BalHistory.objects.filter(date__year=current_year, user=_request.user)
#             .annotate(price=F("amount"))
#             .values("price")
#             .annotate(month=ExtractMonth("date"))
#             .values("month")
#             .annotate(average=Sum("amount"))
#             .values("average")
#             .order_by("month")
#         }


# def previous_balance(_request):
#     return {"previous_balance": BalHistory.objects.filter(date__year=previous_year, user=_request.user)
#             .annotate(price=F("amount"))
#             .values("price")
#             .annotate(month=ExtractMonth("date"))
#             .values("month")
#             .annotate(average=Sum("amount"))
#             .values("average")
#             .order_by("month")
#         }
