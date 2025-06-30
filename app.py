from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load default CSV
csv_path = os.path.join(UPLOAD_FOLDER, 'default.csv')
df = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame(columns=["Description", "Actions", "Objects"])

@app.route('/')
def index():
    instructions = df['Description'].unique().tolist()
    return render_template('index.html', instructions=instructions)

@app.route('/get_details_json', methods=['POST'])
def get_details_json():
    if request.method == 'POST':
        instruction = request.json.get('instruction')
        
    else:
        instruction = request.args.get('instruction')  # for testing in browser

    filtered = df[df['Description'] == instruction]
    actions = filtered['Actions'].tolist()
    objects = filtered['Objects'].tolist()

    return jsonify({'actions': actions, 'objects': objects})


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    global df
    file = request.files.get('csv_file')
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'default.csv')
        file.save(filepath)
        df = pd.read_csv(filepath)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
