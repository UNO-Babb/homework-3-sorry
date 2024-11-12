#Example Flask App for a hexaganal tile game
#Logic is in this python file

from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


# Define the outer ring path for a linear progression around the board
board_path = [
    (0, 3), (0, 4), (0, 5), (0, 6), (1, 7),  # Top edge
    (2, 8), (3, 8), (4, 8), (5, 8), (6, 7),  # Right edge
    (7, 6), (7, 5), (7, 4), (7, 3), (7, 2),  # Bottom edge
    (6, 1), (5, 0), (4, 0), (3, 0), (2, 0),  # Left edge
    (1, 1)                                   # Top-left side
]

# Define unique home positions for each player
home_positions = {
    "player1": 0,  # (0, 3)
    "player2": 11  # (7, 6)
}

# Initialize game state with starting positions
game_state = {
    "players": {
        "player1": {"position_index": home_positions["player1"], "home": False},
        "player2": {"position_index": home_positions["player2"], "home": False},
    },
    "turn": "player1",
    "winner": None
}

@app.route('/state', methods=['GET'])
def get_state():
    # Convert position indexes to coordinates before sending
    response_state = {
        "players": {
            "player1": {
                "position": board_path[game_state["players"]["player1"]["position_index"]],
                "home": game_state["players"]["player1"]["home"]
            },
            "player2": {
                "position": board_path[game_state["players"]["player2"]["position_index"]],
                "home": game_state["players"]["player2"]["home"]
            }
        },
        "turn": game_state["turn"],
        "winner": game_state["winner"]
    }
    return jsonify(response_state)

@app.route('/roll', methods=['POST'])
def roll_dice():
    if game_state["winner"]:
        return jsonify({"message": f"{game_state['winner']} already won!"})

    # Current player
    player = game_state["turn"]
    current_index = game_state["players"][player]["position_index"]

    # Roll a dice (1-6)
    steps = random.randint(1, 6)

    # Ensure move is within dice constraints
    steps = min(steps, 6)

    # Move to the next position along the path
    new_index = (current_index + steps) % len(board_path)
    game_state["players"][player]["position_index"] = new_index

    # Check for victory only if player is at their designated home position
    if new_index == home_positions[player]:
        game_state["players"][player]["home"] = True
        game_state["winner"] = player

    # Switch turns
    game_state["turn"] = "player2" if player == "player1" else "player1"

    # Respond with the new position in coordinates
    return jsonify({
        "player": player,
        "steps": steps,
        "position": board_path[new_index]
    })

if __name__ == '__main__':
    app.run(debug=True)