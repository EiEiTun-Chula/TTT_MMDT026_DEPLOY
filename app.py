#23
#from flask import Flask, render_template
#24 update
from flask import Flask, render_template, request, jsonify
from game import TicTacToe
#25
#from agent import RandomAgent
from agent import RandomAgent, HeuristicAgent, MinimaxAgent, simulate_match

random_agent = RandomAgent(player='O')
heuristic_agent = HeuristicAgent(player='O')
minimax_agent = MinimaxAgent(player='O', use_alpha_beta=True)

# Create Flask application
app = Flask(__name__)

# Create a Tic-Tac-Toe game
game = TicTacToe()
# Create the Random AI agent
random_agent = RandomAgent(player='O')


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# API to receive a player's move
@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = data.get('position')
    

    if not isinstance(position, int) or isinstance(position, bool):
        return jsonify({
            "success": False,
            "message": "Invalid position"
        })

    if game.is_game_over():
        return jsonify({
            "success": False,
            "message": "Game is already over"
        })
    #extra 1
    # Check the game mode
    mode = data.get('mode', 'human-ai')

    # Human vs AI: only X is controlled by the human
    if mode == 'human-ai' and game.current_player != 'X':
        return jsonify({
            "success": False,
            "message": "Please wait for the AI"
        })

    success = game.make_move(position)

    return jsonify({
        "success": success,
        "board": game.board,
        "current_player": game.current_player,
        "winner": game.check_winner(),
        "game_over": game.is_game_over()
    })

# API to reset the game
@app.route('/reset', methods=['POST'])
def reset_game():
    global game

    game = TicTacToe()

    return jsonify({
        "board": game.board,
        "current_player": game.current_player
    })
#25
# API for the selected AI agent
@app.route('/ai-move', methods=['POST'])
def ai_move():

    # AI can only play on O's turn
    if game.is_game_over() or game.current_player != 'O':
        return jsonify({
            "success": False,
            "message": "AI cannot move now"
        })

    # Get the selected AI type
    data = request.get_json(silent=True) or {}
    agent_type = data.get('agent', 'random')

    # Choose the AI agent
    if agent_type == 'heuristic':
        selected_agent = heuristic_agent
    elif agent_type == 'minimax':
        selected_agent = minimax_agent
    else:
        selected_agent = random_agent

    print("Selected AI:", agent_type)
    # Calculate scores for the Minimax visualization
    move_scores = {}

    if agent_type == 'minimax':
        move_scores = selected_agent.get_move_scores(game)
    # Ask the selected AI to choose a move
    position = selected_agent.get_move(game)
    # Debug the number of nodes explored
    if agent_type == 'minimax':
        print("Nodes explored in Python:", selected_agent.nodes_explored)

    if position is None:
        return jsonify({"success": False})

    # Make the AI move
    success = game.make_move(position)

    return jsonify({
        "success": success,
        "board": game.board,
        "current_player": game.current_player,
        "winner": game.check_winner(),
        "game_over": game.is_game_over(),
        "nodes_explored": selected_agent.nodes_explored if agent_type == 'minimax' else 0,
        "move_scores": move_scores,
        "position": position
    })
# Step 32 - Interactive AI vs AI
@app.route('/ai-vs-ai-move', methods=['POST'])
def ai_vs_ai_move():
    if game.is_game_over():
        return jsonify({
            "success": False,
            "message": "Game is over"
        })

    data = request.get_json(silent=True) or {}

    # Choose the agent for the current player
    player = game.current_player

    if player == 'X':
        agent_type = data.get('agent1', 'minimax')
    else:
        agent_type = data.get('agent2', 'random')

    if agent_type == 'minimax':
        agent = MinimaxAgent(player, use_alpha_beta=True)
    elif agent_type == 'heuristic':
        agent = HeuristicAgent(player)
    else:
        agent = RandomAgent(player)

    # Calculate the AI move
    position = agent.get_move(game)

    if position is None:
        return jsonify({"success": False})

    success = game.make_move(position)

    return jsonify({
        "success": success,
        "board": game.board,
        "current_player": game.current_player,
        "winner": game.check_winner(),
        "game_over": game.is_game_over(),
        "position": position,
        "nodes_explored": agent.nodes_explored if agent_type == 'minimax' else 0
    })
# Step 27 - Bot-versus-Bot Benchmarking
@app.route('/benchmark', methods=['POST'])
def benchmark():

    # Read the selected agents from JavaScript
    data = request.get_json(silent=True) or {}

    agent1_type = data.get('agent1', 'minimax')
    agent2_type = data.get('agent2', 'random')

    # Create Player X
    if agent1_type == 'minimax':
        agent1 = MinimaxAgent('X')
    elif agent1_type == 'heuristic':
        agent1 = HeuristicAgent('X')
    else:
        agent1 = RandomAgent('X')

    # Create Player O
    if agent2_type == 'minimax':
        agent2 = MinimaxAgent('O')
    elif agent2_type == 'heuristic':
        agent2 = HeuristicAgent('O')
    else:
        agent2 = RandomAgent('O')

    # Run 50 games
    results = simulate_match(agent1, agent2, num_games=50)
    return jsonify(results)
    
# Run Flask application
if __name__ == '__main__':
    app.run(debug=True)