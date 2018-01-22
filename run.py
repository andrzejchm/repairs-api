from app.App import App
from config import IP_PORT, DB_URL

app = App(DB_URL)

if __name__ == '__main__':
    flaskApp = app.init()
    flaskApp.run(host='0.0.0.0', port=IP_PORT)
