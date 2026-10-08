bind = "0.0.0.0:{{ cookiecutter.port }}"  # Internal container port
worker_class = "gthread"  # Threaded workers for I/O-heavy tasks
workers = 2  # Number of worker processes
threads = 2  # Concurrency boost without extra processes
timeout = 60  # Request timeout (seconds)

# Logging
errorlog = "-"  # stderr -> `docker logs`
loglevel = "warning"  # Suppress verbose logs
accesslog = None  # Disable access log to reduce I/O

# Security & reliability
forwarded_allow_ips = "*"  # Accept proxy headers from any IP
max_requests = 1000  # Auto-restart workers after N requests
max_requests_jitter = 100  # Jitter to prevent simultaneous restarts
