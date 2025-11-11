"""
Passenger WSGI Entry Point for cPanel Python Application
This file is required by cPanel's Passenger to run Flask app
"""

import sys
import os

# Get the virtualenv interpreter path
project_home = os.path.dirname(__file__)
virtualenv_path = os.path.join(os.environ.get('HOME', '/home/virtuali'), 'virtualenv', 'furnilayout', '3.9')
INTERP = os.path.join(virtualenv_path, 'bin', 'python3')

# Only execute if not already using the virtualenv Python
if sys.executable != INTERP and os.path.exists(INTERP):
    os.execl(INTERP, INTERP, *sys.argv)

# Add the application's directory to the PYTHONPATH
sys.path.insert(0, project_home)

# Set environment variables
os.environ.setdefault('FLASK_ENV', 'production')

try:
    # Import Flask application
    from app import app as application
    
    # Log successful startup
    print("Flask application loaded successfully", file=sys.stderr)
except Exception as e:
    # Log any import errors
    print(f"Error loading Flask application: {str(e)}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    
    # Create a simple error application
    def application(environ, start_response):
        status = '500 Internal Server Error'
        output = f'Error loading Flask app: {str(e)}'.encode('utf-8')
        response_headers = [('Content-type', 'text/plain'),
                          ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]

# This is what Passenger will use
# DO NOT change the variable name 'application'
