import io
import random
from flask import Response, Flask, render_template, send_file
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import nr_plot as nr

app = Flask(__name__)

@app.route('/get_image')
def get_image():
    return send_file('nr_results.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug = True)

