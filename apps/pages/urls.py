from django.urls import path
from .views import (
    
    authentication_signin,
    authentication_signup,
    authentication_pass_reset,
    authentication_change,
    authentication_lockscreen,
    authentication_logout,
    authentication_success_msg,
    authentication_twostep_verification,
    
    # errors
    error_404,
    error_500,
    error_503,
    error_offline,

    # pages
    pages_starter,
    pages_profile,
    pages_timeline,
    pages_faqs,
    pages_pricing,
    pages_maintenance,
    pages_coming_soon,
    pages_privacy_policy,
    pages_term_conditions,
    pages_web_apps,
)

app_name = 'pages'


urlpatterns = [
    
    # authentication
    path('authentication/signin',view=authentication_signin,name='authentication.signin'),
    path('authentication/signup',view=authentication_signup,name='authentication.signup'),
    path('authentication/pass-reset',view=authentication_pass_reset,name='authentication.pass_reset'),
    path('authentication/change',view=authentication_change,name='authentication.change'),
    path('authentication/lockscreen',view=authentication_lockscreen,name='authentication.lockscreen'),
    path('authentication/logout',view=authentication_logout,name='authentication.logout'),
    path('authentication/success-msg',view=authentication_success_msg,name='authentication.success_msg'),
    path('authentication/twostep-verification',view=authentication_twostep_verification,name='authentication.twostep_verification'),
    
    # errors
    path('errors/error_404',view=error_404,name='errors.error_404'),
    path('errors/error_500',view=error_500,name='errors.error_500'),
    path('errors/error_503',view=error_503,name='errors.error_503'),
    path('errors/offline',view=error_offline,name='errors.offline'),
   
    
    # pages
    path('starter',view=pages_starter,name='starter'),
    path('profile',view=pages_profile,name='profile'),
    path('timeline',view=pages_timeline,name='timeline'),
    path('faqs',view=pages_faqs,name='faqs'),
    path('pricing',view=pages_pricing,name='pricing'),
    path('maintenance',view=pages_maintenance,name='maintenance'),
    path('coming-soon',view=pages_coming_soon,name='coming_soon'),
    path('privacy-policy',view=pages_privacy_policy,name='privacy_policy'),
    path('term-conditions',view=pages_term_conditions,name='term_conditions'),
    path('web-apps',view=pages_web_apps,name='web_apps'),
]