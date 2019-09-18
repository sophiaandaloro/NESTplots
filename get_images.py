import io
from flask import Response, Flask, send_file, request
import benchmark_plots as plots
import os

#Makes all the benchmark plots from NEST library/functions
plots.makeplots()

file_path = './Images/'
directory = os.path.dirname(file_path)

app = Flask(__name__)

@app.route('/get_image')
def get_image():
    filename = request.args.get('interaction') + '_' + request.args.get('yieldtype') + '.png'
    return send_file(os.path.join(directory, filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug = True)