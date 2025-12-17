import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import chat.routing  # import AFTER setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikewala.settings')
django.setup()  # 🔥 ensures Django apps are loaded before importing routing



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})