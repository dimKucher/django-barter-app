from typing import Dict

from django.db.models import Q
from django.http import HttpRequest
from app_proposal.models import ExchangeProposal


def get_proposal_counter(request: HttpRequest) -> Dict[str, int]:
    """Счетчик всех входящих запросов со статусом `PENDING`"""
    proposal_counter = {"counter": None}
    if request.user.is_authenticated:
        proposal_counter["counter"] = ExchangeProposal.objects.filter(
            Q(ad_receiver=request.user) &
            Q(status=ExchangeProposal.STATUS_PENDING)
        ).count()

    return proposal_counter
