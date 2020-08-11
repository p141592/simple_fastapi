# Обслуживание middleware

# Загрузить все модули в этом пакете
# Обернуть их в app

class Middleware:
    BASE_PATH = 

    def get_middlewares():
                for _module in settings.COMPONENTS_PATH.iterdir():

            if str(_module).endswith('.py'):
                yield Component(_module)

    @classmethod
    def init_app(cls, app):
        pass

