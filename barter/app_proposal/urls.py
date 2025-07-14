from django.urls import path
from app_proposal import views

app_name = "app_proposal"

urlpatterns = [
    path("receiving_list", views.ProposalSendListView.as_view(), name="receiving_list"),
    path("sending_list", views.ProposalReceiveListView.as_view(), name="sending_list"),
    path("<int:pk>/create/", views.ProposalCreateView.as_view(), name="request"),
    path("<int:pk>/detail/", views.ProposalDetail.as_view(), name="detail"),
    path("<int:pk>/accept/", views.AcceptProposalView.as_view(), name="accept"),
    path("<int:pk>/reject/", views.RejectProposalView.as_view(), name="reject"),


    # path("<int:pk>/detail/", views.CartDetail.as_view(), name="cart"),
    # path("<int:pk>/detail/", views.CartDetail.as_view(), name="cart"),
]
