from flask import Flask, render_template, request, jsonify
from src.get_submittable_meeting import *
from pathlib import Path
import os
from datetime import datetime


def get_script_dir():
    """Get the directory where the current Python script is located."""
    if "__file__" in globals():
        script_path = Path(os.path.abspath(__file__)).resolve().parent
    else:
        script_path = Path.cwd()
    return script_path


def create_directory_if_not_exists(directory):
    """Check if the directory exists; create it if it doesn't."""
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    script_dir = get_script_dir()
    results_dir = script_dir / "results"
    create_directory_if_not_exists(results_dir)


app = Flask(__name__)


meeting_data_file = results_dir / "meeting_data.json"

if os.path.exists(meeting_data_file):
    with open(meeting_data_file, "r") as infile:
        output_data = json.load(infile)
else:
    output_data = get_submittable_meeting()
    with open(meeting_data_file, "w") as outfile:
        json.dump(output_data, outfile, indent=4, ensure_ascii=False)

if output_data.get("date") != datetime.now().strftime("%Y-%m-%d"):
    output_data = get_submittable_meeting()
    with open(meeting_data_file, "w") as outfile:
        json.dump(output_data, outfile, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    current_date = output_data.get("date")
    return render_template(
        "index.html",
        domestic=output_data["domestic"],
        international=output_data["international"],
        date=current_date,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
