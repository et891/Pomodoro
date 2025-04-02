from handlers.ping import router as ping_router
from handlers.tasks import router as task_router
from handlers.analytics import router as analytics_router

routers = [ping_router, task_router, analytics_router]