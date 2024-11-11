import multiprocessing
import os

# Server socket
bind = "0.0.0.0:" + os.getenv("PORT", "8000")
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'quickep'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Server hooks
def on_starting(server):
    """Log when server starts"""
    server.log.info("Starting QuickEP server...")

def on_exit(server):
    """Clean up on exit"""
    server.log.info("Shutting down QuickEP server...")

def post_fork(server, worker):
    """Setup worker after fork"""
    server.log.info(f"Worker spawned (pid: {worker.pid})")
