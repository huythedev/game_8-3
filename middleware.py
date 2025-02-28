"""
Middleware for handling requests behind a proxy
"""

class ProxyFix:
    def __init__(self, app, proxy_headers=None):
        self.app = app
        self.proxy_headers = proxy_headers or ['X-Forwarded-For', 'X-Real-IP']

    def __call__(self, environ, start_response):
        # Store the original REMOTE_ADDR
        original_remote_addr = environ.get('REMOTE_ADDR', '')
        
        # Check for proxy headers
        for header in self.proxy_headers:
            http_header = 'HTTP_' + header.replace('-', '_').upper()
            if http_header in environ:
                # Get the first value in the X-Forwarded-For chain (client's real IP)
                ip_value = environ[http_header].split(',')[0].strip()
                if ip_value:
                    environ['REAL_REMOTE_ADDR'] = ip_value
                    break
        
        # If no proxy headers found, use the original IP
        if 'REAL_REMOTE_ADDR' not in environ:
            environ['REAL_REMOTE_ADDR'] = original_remote_addr
        
        return self.app(environ, start_response)

def get_real_ip(request):
    """
    Get the real client IP address from request environment.
    This works with either a direct connection or through a proxy.
    """
    if hasattr(request, 'environ') and 'REAL_REMOTE_ADDR' in request.environ:
        return request.environ['REAL_REMOTE_ADDR']
    return request.remote_addr
