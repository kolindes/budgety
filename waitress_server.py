# --- WINDOWS ---
# The waitress web server is used to serve the Flask application,
# which is configured to listen on all available network interfaces
# as default (0.0.0.0) on port 5000.

from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
