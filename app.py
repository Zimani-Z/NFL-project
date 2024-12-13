from flask import Flask, jsonify, render_template, request
from Calculator import predict_game_outcome

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html') 


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    team1_stats = {
        'points_scored_last_10': data['team1']['points'],
        'wins': data['team1']['record'][0],
        'losses': data['team1']['record'][1],
        'is_home': data['team1']['is_home']
    }
    team2_stats = {
        'points_scored_last_10': data['team2']['points'],
        'wins': data['team2']['record'][0],
        'losses': data['team2']['record'][1],
        'is_home': data['team2']['is_home']
    }
    result = predict_game_outcome(team1_stats, team2_stats)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
