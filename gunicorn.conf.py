import multiprocessing

import os

e = os.environ.get
CPU_COUNT = int(multiprocessing.cpu_count())

workers = e("WORKERS_COUNT", CPU_COUNT)
worker_class = "uvicorn.workers.UvicornWorker"
preload_app = True
graceful_timeout = 0

