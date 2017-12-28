from app.App import App
from config import IP_PORT, DB_URL

app = App(DB_URL)

if __name__ == '__main__':
    flaskApp = app.init()
    flaskApp.run(port=IP_PORT)
