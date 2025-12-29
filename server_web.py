"""
Web server for LastSignal game deployment on Render
Serves the game UI and provides API endpoints for multiplayer
"""

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import json
from server import GameServer, GameSession

app = Flask(__name__, static_folder='.')
CORS(app)

# Global game server instance
game_server = GameServer()

# Port configuration for Render
PORT = int(os.environ.get('PORT', 8080))

@app.route('/')
def index():
    """Serve the main game UI"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'LastSignal Game Server'})

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List available game sessions"""
    sessions = game_server.list_sessions()
    return jsonify({'sessions': sessions})

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Create a new game session"""
    data = request.json or {}
    max_players = data.get('max_players', 4)
    game_duration = data.get('game_duration', 300.0)
    
    session_id = game_server.create_session(max_players, game_duration)
    return jsonify({'session_id': session_id, 'success': True})

@app.route('/api/sessions/<session_id>/join', methods=['POST'])
def join_session(session_id):
    """Join a game session"""
    data = request.json or {}
    player_name = data.get('player_name', 'Anonymous')
    connection_id = data.get('connection_id', f'web_{id(request)}')
    
    player_id = game_server.join_session(session_id, connection_id, player_name)
    
    if player_id:
        return jsonify({
            'success': True,
            'player_id': player_id,
            'session_id': session_id
        })
    else:
        return jsonify({'success': False, 'error': 'Cannot join session'}), 400

@app.route('/api/sessions/<session_id>/start', methods=['POST'])
def start_session(session_id):
    """Start a game session"""
    success = game_server.start_session(session_id)
    return jsonify({'success': success})

@app.route('/api/sessions/<session_id>/state', methods=['GET'])
def get_session_state(session_id):
    """Get current state of a session"""
    player_id = request.args.get('player_id')
    state = game_server.get_session_state(session_id, player_id)
    return jsonify(state)

@app.route('/api/sessions/<session_id>/action', methods=['POST'])
def process_action(session_id):
    """Process a player action"""
    data = request.json or {}
    connection_id = data.get('connection_id')
    
    if not connection_id:
        return jsonify({'error': 'connection_id required'}), 400
    
    result = game_server.process_action(connection_id, data)
    return jsonify(result)

@app.route('/api/sessions/<session_id>/round', methods=['POST'])
def process_round(session_id):
    """Process a round for the session"""
    events = game_server.process_round(session_id)
    return jsonify({'events': events})

@app.route('/api/sessions/<session_id>/status', methods=['GET'])
def check_game_status(session_id):
    """Check if game is over and get results"""
    result = game_server.check_game_over(session_id)
    if result:
        return jsonify(result)
    return jsonify({'game_over': False})

if __name__ == '__main__':
    print(f"Starting LastSignal server on port {PORT}")
    print(f"Environment: {'Production' if os.environ.get('RENDER') else 'Development'}")
    
    if os.environ.get('RENDER'):
        # Production mode on Render
        app.run(host='0.0.0.0', port=PORT)
    else:
        # Development mode
        app.run(host='0.0.0.0', port=PORT, debug=True)
