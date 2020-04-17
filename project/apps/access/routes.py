from .user.views import router as user

routes = (
    (user, dict(prefix="/access/user", tags=["access"])),
)
