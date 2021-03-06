__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"


import os

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.views.static import serve

from journal import urls as journal_urls
from core import views as core_views, plugin_loader
from utils import notify
from press import views as press_views
from cms import views as cms_views
from submission import views as submission_views
from journal import views as journal_views
from review import views as review_views

from dynamicsites.views import site_info


include('events.registration')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^submit/', include('submission.urls')),
    url(r'^', include(journal_urls)),
    url(r'^review/', include('review.urls')),
    url(r'^metrics/', include('metrics.urls')),
    url(r'^identifiers/', include('identifiers.urls')),
    url(r'^production/', include('production.urls')),
    url(r'^proofing/', include('proofing.urls')),
    url(r'^cms/', include('cms.urls')),
    url(r'^transform/', include('transform.urls')),
    url(r'^copyediting/', include('copyediting.urls')),
    url(r'^rss/', include('rss.urls')),
    url(r'^cron/', include('cron.urls')),
    url(r'^install/', include('install.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    # Root Site URLS
    url(r'^$', press_views.index, name='website_index'),
    url(r'^journals/$', press_views.journals, name='press_journals'),
    url(r'^kanban/$', core_views.kanban, name='kanban'),
    url(r'^login/$', core_views.user_login, name='core_login'),
    url(r'^login/orcid/$', core_views.user_login_orcid, name='core_login_orcid'),
    url(r'^register/step/1/$', core_views.register, name='core_register'),
    url(r'^register/step/2/(?P<token>[\w-]+)/$', core_views.activate_account, name='core_confirm_account'),
    url(r'^register/step/orcid/(?P<token>[\w-]+)/$', core_views.orcid_registration, name='core_orcid_registration'),
    url(r'^reset/step/1/$', core_views.get_reset_token, name='core_get_reset_token'),
    url(r'^reset/step/2/(?P<token>[\w-]+)/$', core_views.reset_password, name='core_reset_password'),
    url(r'^profile/$', core_views.edit_profile, name='core_edit_profile'),
    url(r'^logout/$', core_views.user_logout, name='core_logout'),
    url(r'^dashboard/$', core_views.dashboard, name='core_dashboard'),
    url(r'^cover/$', press_views.serve_press_cover, name='press_cover_download'),


    # Notes
    url(r'^article/(?P<article_id>\d+)/note/(?P<note_id>\d+)/delete/$', core_views.delete_note,
        name='kanban_delete_note'),

    # Manager URLS
    url(r'^manager/$', core_views.manager_index, name='core_manager_index'),

    # Settings Management
    url(r'^manager/settings/$', core_views.settings_index, name='core_settings_index'),
    url(r'^manager/settings/group/(?P<setting_group>[-\w.]+)/setting/(?P<setting_name>[-\w.]+)/$',
        core_views.edit_setting,
        name='core_edit_setting'),
    url(r'^manager/settings/(?P<group>[-\w.]+)/$', core_views.edit_settings_group, name='core_edit_settings_group'),
    url(r'^manager/settings/(?P<plugin>[-\w.]+)/(?P<setting_group_name>[-\w.]+)/(?P<journal>\d+)/$',
        core_views.edit_plugin_settings_groups, name='core_edit_plugin_settings_groups'),


    url(r'^manager/home/settings/$', core_views.settings_home, name='home_settings_index'),
    url(r'^manager/home/settings/order/$', core_views.journal_home_order, name='journal_home_order'),


    # Role Management
    url(r'^manager/roles/$', core_views.roles, name='core_manager_roles'),
    url(r'^manager/roles/(?P<slug>[-\w.]+)/$', core_views.role, name='core_manager_role'),
    url(r'^manager/roles/(?P<slug>[-\w.]+)/user/(?P<user_id>\d+)/(?P<action>[-\w.]+)/$', core_views.role_action,
        name='core_manager_role_action'),

    # Users
    url(r'^manager/user/$', core_views.users, name='core_manager_users'),
    url(r'^manager/user/inactive/$', core_views.inactive_users, name='core_manager_inactive_users'),
    url(r'^manager/user/authenticated/$', core_views.logged_in_users, name='core_logged_in_users'),
    url(r'^manager/user/add/$', core_views.add_user, name='core_add_user'),
    url(r'^manager/user/(?P<user_id>\d+)/edit/$', core_views.user_edit, name='core_user_edit'),

    # News
    url(r'^manager/news/$', core_views.news, name='core_manager_news'),
    url(r'^manager/news/edit/(?P<news_pk>\d+)/$', core_views.edit_news, name='core_manager_edit_news'),

    url(r'^news/$', core_views.news_list, name='core_news_list'),
    url(r'^news/(?P<news_pk>\d+)/$', core_views.news_item, name='core_news_item'),

    url(r'^news/(?P<identifier_type>.+?)/(?P<identifier>.+)/image/(?P<file_id>\d+|None)/$',
        core_views.serve_news_file, name='news_file_download'),

    # Templates
    url(r'^manager/templates/$', core_views.email_templates, name='core_email_templates'),
    url(r'^manager/templates/(?P<template_code>[-\w.]+)/$', core_views.edit_email_template,
        name='core_edit_email_template'),
    url(r'^manager/templates/(?P<template_code>[-\w.]+)/(?P<subject>[-\w.]+)/$', core_views.edit_email_template,
        name='core_edit_email_template_subject'),

    # Articles Images
    url(r'^manager/article/images/$', core_views.article_images, name='core_article_images'),
    url(r'^manager/article/images/edit/(?P<article_pk>\d+)/$', core_views.article_image_edit,
        name='core_article_image_edit'),

    # Journal Contacts
    url(r'^manager/contacts/$', core_views.contacts, name='core_journal_contacts'),
    url(r'^manager/contacts/(?P<contact_id>\d+)/$', core_views.edit_contacts, name='core_journal_contact'),
    url(r'^manager/contacts/order/$', core_views.contacts_order, name='core_journal_contacts_order'),

    # Editorial Team
    url(r'^manager/editorial/$', core_views.editorial_team, name='core_editorial_team'),
    url(r'^manager/editorial/(?P<group_id>\d+)/$', core_views.edit_editorial_group, name='core_edit_editorial_team'),
    url(r'^manager/editorial/(?P<group_id>\d+)/add/$', core_views.add_member_to_group,
        name='core_editorial_member_to_group'),
    url(r'^manager/editorial/(?P<group_id>\d+)/add/(?P<user_id>\d+)/$', core_views.add_member_to_group,
        name='core_editorial_member_to_group_user'),
    url(r'^manager/editorial/order/(?P<type_to_order>[-\w.]+)/$',
        core_views.editorial_ordering,
        name='core_editorial_ordering'),
    url(r'^manager/editorial/order/(?P<type_to_order>[-\w.]+)/group/(?P<group_id>\d+)/$',
        core_views.editorial_ordering,
        name='core_editorial_ordering_group'),

    # Review forms
    url(r'^manager/review/$',
        review_views.review_forms,
        name='review_review_forms'),
    url(r'^manager/review/form/(?P<form_id>\d+)/$',
        review_views.edit_review_form,
        name='edit_review_form'),
    url(r'^manager/review/form/(?P<form_id>\d+)/preview/$',
        review_views.preview_form,
        name='preview_form'),
    url(r'^manager/review/form/(?P<form_id>\d+)/element/(?P<element_id>\d+)/$',
        review_views.edit_review_form,
        name='edit_review_form_element'),

    # Notifications
    url(r'^manager/notifications/$',
        core_views.manage_notifications, name='core_manager_notifications'),
    url(r'^manager/notifications/(?P<notification_id>\d+)/$',
        core_views.manage_notifications, name='core_manager_edit_notifications'),

    # Plugin home
    url(r'^manager/plugins/$',
        core_views.plugin_list,
        name='core_plugin_list'),

    # Journal Sections
    url(r'^manager/sections/$',
        core_views.sections, name='core_manager_sections'),
    url(r'^manager/sections/(?P<section_id>\d+)/$',
        core_views.sections, name='core_manager_section'),

    # Pinned Articles
    url(r'^manager/articles/pinned/$',
        core_views.pinned_articles, name='core_pinned_articles'),

    # Press manager
    url(r'^manager/press/$',
        press_views.edit_press,
        name='press_edit_press'),
    url(r'^manager/press/journal_order/$',
        press_views.journal_order,
        name='press_journal_order'),

    # Workflow
    url(r'^workflow/$',
        core_views.journal_workflow,
        name='core_journal_workflow'),
    url(r'^workflow/order/$',
        core_views.order_workflow_elements,
        name='core_order_workflow_elements'),

    # Cache
    url(r'^manager/cache/flush/$', core_views.flush_cache, name='core_flush_cache'),

    # APIs
    url(r'^api/oai$', core_views.oai, name='OAI_list_records'),

    url(r'^edit/article/(?P<article_id>\d+)/metadata/$', submission_views.edit_metadata, name='edit_metadata'),
    url(r'^edit/article/(?P<article_id>\d+)/authors/order/$', submission_views.order_authors, name='order_authors'),
    url(r'^edit/article/(?P<article_id>\d+)/ident/$', submission_views.edit_identifiers, name='edit_identifiers'),
    url(r'^edit/article/(?P<article_id>\d+)/ident/(?P<identifier_id>\d+)/$', submission_views.edit_identifiers,
        name='edit_identifiers_with_ident'),
    url(r'^edit/article/(?P<article_id>\d+)/ident/(?P<identifier_id>\d+)/(?P<event>[-\w.]+)/$',
        submission_views.edit_identifiers,
        name='edit_identifiers_with_event'),

    url(r'^sitemap/$', journal_views.sitemap, name='journal_sitemap'),
]

# Allow Django to serve static content only in debug/dev mode
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^404/$', TemplateView.as_view(template_name='core/404.html')),
        url(r'^500/$', TemplateView.as_view(template_name='core/500.html')),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [
    url(r'^site-info$', site_info), ]

# Journal homepage block loading

blocks = plugin_loader.load(os.path.join('core', 'homepage_elements'), prefix='core.homepage_elements',
                            permissive=True)

if blocks:
    for block in blocks:
        try:
            urlpatterns += [
                url(r'^homepage/elements/{0}/'.format(block.name),
                    include('core.homepage_elements.{0}.urls'.format(block.name))),
            ]
        except ImportError as e:
            print("Error loading a block: {0}, {1}".format(block.name, e))
            pass

# Plugin Loading

plugins = plugin_loader.load()

if plugins:
    for plugin in plugins:
        try:
            urlpatterns += [
                url(r'^plugins/{0}/'.format(plugin.best_name()), include('plugins.{0}.urls'.format(plugin.name))),
            ]
            if settings.DEBUG:
                print("Loaded URLs for {0}".format(plugin.name))
        except ImportError as e:
            print("Error loading a plugin: {0}, {1}".format(plugin.name, e))
            pass

# load the notification plugins
if len(settings.NOTIFY_FUNCS) == 0:
    plugins = notify.load_modules()
    frameworks = []

    for key, val in plugins.items():
        if hasattr(val, 'notify_hook'):
            settings.NOTIFY_FUNCS.append(val.notify_hook)

urlpatterns += [
    url(r'^site/(?P<page_name>.*)/$', cms_views.view_page, name='cms_page'),
]
