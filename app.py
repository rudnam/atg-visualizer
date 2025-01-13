from flask import Flask, render_template, request
from graph import create_and_draw_graph

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    graph_file = None
    if request.method == "POST":
        sequence = request.form["sequence"]
        graph_file = create_and_draw_graph(sequence)
    return render_template("index.html", graph_file=graph_file)


if __name__ == "__main__":
    app.run(debug=True)
