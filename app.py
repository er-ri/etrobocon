from etrobocon.operate import control_spike_car
from logging.config import dictConfig
from flask import (
    Flask,
    Response,
    request,
    render_template
)
from etrobocon import get_frames


app = Flask(__name__)

# Set logger format
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(levelname)s] %(asctime)s: %(message)s',
    }},
    'handlers': {'etrobocon': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['etrobocon']
    }
})

# Disable flask server logging
# logging.getLogger('werkzeug').disabled = True


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(get_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/keyboard_event', methods=['POST'])
def keyboard_event():
    command = request.json
    app.logger.info(command)
    control_spike_car(command)
    return Response(status=204)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')