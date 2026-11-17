from flask import Flask, render_template, jsonify, request
import time
import os

app = Flask(__name__)

# Global variables to store game state
game_state = {
    'player1_time': 0,  # Time spent by player 1
    'player2_time': 0,  # Time spent by player 2
    'global_time': 3600,  # Total game time in seconds
    'initial_global_time': 3600,  # To store the initial time setting
    'active_player': None,
    'last_tick': None,
    'game_started': False,
    'is_paused': False,
    'global_last_tick': None,
    'finished': False
}


def _advance(now):
    """Fold the time since the last tick into the active player and the game clock.

    Both move by the same amount, capped at the game time left, so the players'
    times always add up to the time used and the game ends at zero.
    """
    if not game_state['game_started'] or game_state['is_paused'] or game_state['finished']:
        return
    if game_state['last_tick'] is None:
        return
    elapsed = min(now - game_state['last_tick'], max(game_state['global_time'], 0))
    if game_state['active_player'] == 1:
        game_state['player1_time'] += elapsed
    elif game_state['active_player'] == 2:
        game_state['player2_time'] += elapsed
    game_state['global_time'] -= elapsed
    game_state['last_tick'] = now
    game_state['global_last_tick'] = now
    if game_state['global_time'] <= 0:
        game_state['global_time'] = 0
        game_state['finished'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_global_time', methods=['POST'])
def set_global_time():
    if game_state['game_started']:
        return jsonify({'error': 'Cannot change time while game is running'}), 400
    
    try:
        new_time = int(request.json.get('time'))
        if new_time <= 0:
            return jsonify({'error': 'Time must be positive'}), 400
        game_state['global_time'] = new_time
        game_state['initial_global_time'] = new_time
        return jsonify(game_state)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid time format'}), 400

@app.route('/start')
def start_game():
    # Restarting mid-game cleared the players but kept the global time used.
    if game_state['game_started']:
        return jsonify({'error': 'Game already running; reset it first'}), 400
    game_state['game_started'] = True
    game_state['active_player'] = 1
    current_time = time.time()
    game_state['last_tick'] = current_time
    game_state['global_last_tick'] = current_time
    game_state['is_paused'] = False
    game_state['player1_time'] = 0
    game_state['player2_time'] = 0
    game_state['finished'] = False
    return jsonify(game_state)

@app.route('/switch/<int:player>')
def switch_player(player):
    if not game_state['game_started'] or game_state['is_paused']:
        return jsonify({'error': 'Game not started or paused'}), 400
    if player not in (1, 2):
        return jsonify({'error': 'Player must be 1 or 2'}), 400
    
    _advance(time.time())
    if game_state['finished']:
        return jsonify({'error': 'Game time is over'}), 400

    game_state['active_player'] = player
    return jsonify(game_state)

@app.route('/pause')
def pause_game():
    if not game_state['game_started']:
        return jsonify({'error': 'Game not started'}), 400

    current_time = time.time()
    _advance(current_time)
    if game_state['finished']:
        return jsonify({'error': 'Game time is over'}), 400
    if not game_state['is_paused']:
        game_state['global_last_tick'] = None

    game_state['is_paused'] = not game_state['is_paused']
    if not game_state['is_paused']:
        game_state['last_tick'] = current_time
        game_state['global_last_tick'] = current_time
    
    return jsonify(game_state)

@app.route('/reset')
def reset_game():
    game_state['player1_time'] = 0
    game_state['player2_time'] = 0
    game_state['global_time'] = game_state['initial_global_time']
    game_state['active_player'] = None
    game_state['last_tick'] = None
    game_state['global_last_tick'] = None
    game_state['game_started'] = False
    game_state['is_paused'] = False
    game_state['finished'] = False
    return jsonify(game_state)

@app.route('/state')
def get_state():
    _advance(time.time())
    return jsonify(game_state)

if __name__ == '__main__':
    # Only enable debug mode in development
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug) 