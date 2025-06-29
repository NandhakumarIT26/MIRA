from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('cookery_dataset.csv')

@app.route('/')
def index():
    instructions = df['Description'].unique().tolist()
    return render_template('index.html', instructions=instructions)

@app.route('/get_details_json', methods=['POST'])
def get_details_json():
    instruction = request.json.get('instruction')
    filtered = df[df['Description'] == instruction]

    actions = filtered['Actions'].tolist()
    objects = filtered['Objects'].tolist()

    return jsonify({
        'actions': actions,
        'objects': objects
    })

if __name__ == '__main__':
    app.run(debug=True)
