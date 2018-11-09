from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.sessions import SessionMiddlewareStack
from django.conf.urls import url
from consultation.consumers import *

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            URLRouter(
                [
                    url(r"^consultation/(?P<username>[\w.@+-]+)/$", ChatConsumer)
                ]
            )
        )
    )
})
