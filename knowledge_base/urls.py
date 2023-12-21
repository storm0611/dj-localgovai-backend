from django.urls import path, re_path
from .views import (
    KnowledgeBaseView,
    KnowledgeBaseQuestionView,
    KnowledgeBaseAllView,
    SettingView
)

urlpatterns = [
    # re_path(r'^(?P<knowledge_base_name>[\w-]+)?$', KnowledgeBaseView.as_view(), name='knowledge_base_name'),
    path('', KnowledgeBaseView.as_view(), name='knowledge_base'),   
    path('del', KnowledgeBaseView.as_view(), name='delete_knowledge_base'),   
    path('all', KnowledgeBaseAllView.as_view(), name='get_all_knowledge_bases'),   
    path('question', KnowledgeBaseQuestionView.as_view(), name='knowledge_base_question'),
    # path('setting', SettingView.as_view(), name='knowledge_base_setting'),
]
