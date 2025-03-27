from flask import Flask, request, jsonify
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

app = Flask(__name__)

with open('DInner prediction.pkl', 'rb') as modelFine:
    model = pickle.load(modelFine)

@app.route("/sampleGet")
def sample_endpoint():
    return "Yes, Server Received!"
 
@app.route('/predict_location', methods=['POST'])
def predict_location():
    data = request.json
    new_data = [[data['avg_money'], data['dinner_time'], data['variety']]]
    predicted_location = model.predict(new_data)
    return jsonify({"predicted_location": predicted_location[0]})

@app.route('/get_info', methods=['POST'])
def get_info():
    data = request.json
    register_number = data['register_number']
    date = data['date']
    filtered_df = df[(df['Register Number'] == register_number) & (df['Date'] == date)]

    if filtered_df.empty:
        return jsonify({"message": "No information found for the given register number and date."}), 404

    where_ate = filtered_df.iloc[0]['Where in College ?']
    avg_spent = filtered_df['Avg money (Normalized)'].mean()
    what_ate = filtered_df.iloc[0]['Variety']

    return jsonify({
        "where_ate": where_ate,
        "avg_spent": avg_spent,
        "what_ate": what_ate
    })

if __name__ == '__main__':
    app.run(debug=True)
