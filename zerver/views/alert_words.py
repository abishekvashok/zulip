from typing import List

from django.http import HttpRequest, HttpResponse

from zerver.lib.actions import do_add_alert_words, do_remove_alert_words
from zerver.lib.alert_words import user_alert_words
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.validator import check_capped_string, check_list, check_string
from zerver.models import UserProfile

def list_alert_words(request: HttpRequest, user_profile: UserProfile) -> HttpResponse:
    return json_success({"alert_words": user_alert_words(user_profile)})


def clean_alert_words(alert_words: List[str]) -> List[str]:
    alert_words = [w.strip() for w in alert_words]
    return [w for w in alert_words if w != ""]


@has_request_variables
def add_alert_words(
    request: HttpRequest,
    user_profile: UserProfile,
    alert_words: List[str] = REQ(json_validator=check_list(check_capped_string(100))),
) -> HttpResponse:
    do_add_alert_words(user_profile, clean_alert_words(alert_words))
    return json_success({"alert_words": user_alert_words(user_profile)})


@has_request_variables
def remove_alert_words(
    request: HttpRequest,
    user_profile: UserProfile,
    alert_words: List[str] = REQ(json_validator=check_list(check_string)),
) -> HttpResponse:
    do_remove_alert_words(user_profile, alert_words)
    return json_success({"alert_words": user_alert_words(user_profile)})
