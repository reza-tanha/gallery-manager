from django.urls import path, include


urlpatterns = [
    # path('blog/', include(('gallery.blog.urls', 'blog')))
    path(
        "users/",
        include(('gallery.users.urls', "users"), namespace="users"),
    ),

    path(
        'auth/',
        include(("gallery.authentication.urls", "authentication"), namespace="authentication")
    ),
    path(
        'media/',
        include(("gallery.mediahub.urls", "media"), namespace="media")
    ),
]
