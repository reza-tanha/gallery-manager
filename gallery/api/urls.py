from django.urls import path, include


urlpatterns = [
    # path('blog/', include(('gallery.blog.urls', 'blog')))
    path(
        "users/",
        include(('gallery.users.urls', "users"), namespace="users"),
    )
]
