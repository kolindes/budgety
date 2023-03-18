import os

from app import create_app

if __name__ == '__main__':
    app = create_app()
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app')
    app.run(debug=True, port=3000, host='0.0.0.0')
