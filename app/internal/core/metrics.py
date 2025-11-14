from prometheus_fastapi_instrumentator import Instrumentator


def metrics_initialize(app):
    instrumentator = Instrumentator().instrument(app)
    instrumentator.expose(app)
