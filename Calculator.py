def calculate_win_probability(is_home, wins, losses, avg_points_scored):
    # Start with a base probability
    probability = 0.5

    # Apply home advantage
    if is_home:
        probability *= 1.54
    
    # Calculate win percentage 
    total_games = wins + losses
    win_percentage = wins / total_games if total_games > 0 else 0

    # Apply record-based probability 
    if win_percentage >= 0.5:
        # Winning record: boost based on win percentage
        probability *= (1 + (win_percentage - 0.5))  # Slight boost for better win rates
    else:
        # Losing record: reduce probability capped at 45%
        probability *= max(0.9, win_percentage)
        probability = min(probability, 0.45)
    
    # Constrain probability between 0 and 1
    probability = min(max(probability, 0), 1)
    return probability * 100  # Return as a percentage


 # Calculate the average points scored over the last 10 games
def predict_score(points_scored_last_10, win_percentage):

    avg_points_scored = sum(points_scored_last_10) / len(points_scored_last_10)


    # Adjust predicted score based on win percentage
    if win_percentage >= 0.5:
        avg_points_scored *= (1 + (win_percentage - 0.5))  # Small boost for better win rates
    else:
        avg_points_scored *= win_percentage  # Scale down if losing record
    
    return int(avg_points_scored)

def predict_game_outcome(team1_stats, team2_stats):
    # Calculate average points for each team
    team1_avg_scored = sum(team1_stats['points_scored_last_10']) / len(team1_stats['points_scored_last_10'])
    team2_avg_scored = sum(team2_stats['points_scored_last_10']) / len(team2_stats['points_scored_last_10'])


    # Calculate win percentage for each team
    team1_win_percentage = team1_stats['wins'] / (team1_stats['wins'] + team1_stats['losses']) if (team1_stats['wins'] + team1_stats['losses']) > 0 else 0
    team2_win_percentage = team2_stats['wins'] / (team2_stats['wins'] + team2_stats['losses']) if (team2_stats['wins'] + team2_stats['losses']) > 0 else 0

    # Calculate win probability for each team
    team1_prob = calculate_win_probability(
        team1_stats['is_home'], 
        team1_stats['wins'], 
        team1_stats['losses'],
        team1_avg_scored
    )
    team2_prob = calculate_win_probability(
        team2_stats['is_home'], 
        team2_stats['wins'], 
        team2_stats['losses'],
        team2_avg_scored
    )

    # Predict scores for each team based on last 10 games and win percentage
    team1_score = predict_score(team1_stats['points_scored_last_10'], team1_win_percentage)
    team2_score = predict_score(team2_stats['points_scored_last_10'], team2_win_percentage)

    # Determine likely winner based on higher probability
    winner = "Team 1" if team1_prob > team2_prob else "Team 2"
    predicted_score = {
        "team1": team1_score,
        "team2": team2_score
    }

    return {
        "winner": winner,
        "team1_win_probability": team1_prob,
        "team2_win_probability": team2_prob,
        "predicted_score": predicted_score
    }

# Example usage
team1_stats = {
    'points_scored_last_10': [100, 102, 97, 105, 98, 110, 101, 99, 104, 107],
    'wins': 6,
    'losses': 4,
    'is_home': True
}

team2_stats = {
    'points_scored_last_10': [95, 99, 96, 100, 94, 97, 102, 98, 101, 95],
    'wins': 7,
    'losses': 3,
    'is_home': False
}

# Predict the game outcome
result = predict_game_outcome(team1_stats, team2_stats)
print(f"Predicted Winner: {result['winner']}")
print(f"Team 1 Win Probability: {result['team1_win_probability']:.2f}%")
print(f"Team 2 Win Probability: {result['team2_win_probability']:.2f}%")
print(f"Predicted Score: Team 1: {result['predicted_score']['team1']} - Team 2: {result['predicted_score']['team2']}")
