from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'journals'

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='journals/login.html'), name='login'),
    url(r'^logout/$',auth_views.LogoutView.as_view(), name='logout'),
    url(r"^signup/$", views.SignUp.as_view(), name="signup"),
    url(r"^test/$", views.TestPage.as_view(), name="test"),
    url(r"^thanks/$", views.ThanksPage.as_view(), name="thanks"),
    url(r"^new/$", views.CreateJournal.as_view(), name="create"),
    url(r"^journal/in/(?P<slug>[-\w]+)/$",views.JournalDetail.as_view(),name="single"),
    url(r"^journal/edit/(?P<pk>\d+)/$", views.EditJournal.as_view(), name="edit"),
    url(r"^journal/delete/(?P<pk>\d+)/$",views.DeleteJournal.as_view(),name="delete"),
    url(r"^journal/all/$", views.JournalList.as_view(), name="all"),
    url(r"^journal/entry/list/(?P<pk>\d+)/$", views.JournalEntryList.as_view(), name="entry_list"),
    url(r"^journal/entry/list/(?P<pk>\d+)/all/$", views.JournalEntryListAll.as_view(), name="entry_list_all"),
    url(r"^journal/entry/create/(?P<pk>\d+)/$", views.JournalEntryCreate.as_view(), name="entry_create"),
    url(r"^journal/entry/(?P<entryname>[-\w]+)/(?P<pk>\d+)/$",views.JournalEntryDetail.as_view(),name="entry_detail"),
    url(r'^journal/entry/(?P<pk>\d+)/edit/$', views.JournalEntryUpdate.as_view(), name='entry_update'),
    url(r'^journal/entry/(?P<pk>\d+)/remove/$', views.entry_remove, name='entry_remove'),
    url(r'^journal/entry/(?P<orginal_entry>\d+)/log/$', views.JournalEntryLog.as_view(), name='entry_log'),
    url(r'^journal/entry/(?P<pk>\d+)/hide/$', views.entry_hide, name='entry_hide'),
    url(r'^journal/entry/(?P<pk>\d+)/replace/(?P<orginal_entry_index>\d+)/$', views.entry_replace, name='entry_replace'),
    url(r'^journal/entry/search/$', views.JournalEntrySearchList.as_view(), name='entry_search'),
    # url(r'^admin/', admin.site.urls),
    #www.web.com
    # url(r'^$', views.index, name='index'),
    
    # # www.web.com/journals
    # url(r'^journals/$', views.journals, name='journals'),
    # # www.web.com/journals/login
    # url(r'^login/$', views.journal_login, name='journal_login'),
    # # www.web.com/journals/login/confirm
    # url(r'^login/confirm/$', views.journal_login_confirm, name='journal_login_confirm'),
    #
    # # www.web.com/journals/register
    # url(r'^register/$', views.journal_register, name='journal_register'),
    # # www.web.com/journals/register/confirm
    # url(r'^register/confirm/$', views.journal_register_confirm, name='journal_register_confirm'),
    #
    #
    # #www.web.com/create
    # url(r'^create/$', views.journal_create, name='journal_create'),
    # url(r'^create/confirm/$', views.journal_create_confirm, name="journals_create_confirm"),
    #
    # #www.web.com/journal/1234
    # url(r'^journal/(?P<journal_id>[0-9]+)/$', views.journal_view, name='journal_view'),
    #
    # # www.web.com/journal/search
    # url(r'^journal/search/$', views.journal_search, name='journal_search'),
    #
    # #www.web.com/journal/1234/create
    # url(r'^journal/(?P<journal_id>[0-9]+)/create/$', views.entry_create, name='entry_create'),
    # url(r'^journal/(?P<journal_id>[0-9]+)/create/confirm/$', views.entry_create_confirm, name='entry_create_confirm'),
    #
    # #www.web.com/journal/1234/entry/1234
    # url(r'^journal/(?P<journal_id>[0-9]+)/entry/(?P<entry_id>[0-9]+)/$', views.entry_view, name='entry_view'),
    #
    # #www.web.com/journal/1234/edit/1234
    # url(r'^journal/(?P<journal_id>[0-9]+)/edit/(?P<entry_id>[0-9]+)/$', views.entry_edit, name='entry_edit'),
    #
    # #www.web.com/journal/1234/edit/1234
    # url(r'^journal/(?P<journal_id>[0-9]+)/edit/confirm/(?P<entry_id>[0-9]+)/$', views.entry_edit_confirm, name='entry_edit_confirm'),
    #
    # #www.web.com/journal/1234/history/1234
    # url(r'^journal/(?P<journal_id>[0-9]+)/history/(?P<entry_id>[0-9]+)/$', views.entry_history, name='entry_history'),
]

