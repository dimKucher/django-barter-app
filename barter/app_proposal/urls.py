from django.urls import path
from app_proposal import views

app_name = "app_proposal"

urlpatterns = [
    path("list/", views.ProposalListView.as_view(), name="list"),
    path("<int:pk>/create/", views.ProposalCreateView.as_view(), name="request"),
    path("<int:pk>/detail/", views.ProposalDetail.as_view(), name="detail"),
    path("<int:pk>/accept/", views.AcceptProposalView.as_view(), name="accept"),
    path("<int:pk>/reject/", views.RejectProposalView.as_view(), name="reject"),
]
