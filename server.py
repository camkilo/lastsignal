"""
Multiplayer server for LastSignal game
Handles multiple game sessions and player connections
"""

import json
import uuid
from typing import Dict, List, Optional
from game import GameEngine, ActionType, InformationType


class GameSession:
    """A multiplayer game session"""
    
    def __init__(self, session_id: str, max_players: int = 4, game_duration: float = 300.0):
        self.session_id = session_id
        self.max_players = max_players
        self.engine = GameEngine(num_players=max_players, game_duration=game_duration)
        self.player_connections: Dict[str, str] = {}  # player_id -> connection_id
        self.started = False
        
    def can_join(self) -> bool:
        """Check if players can join this session"""
        return len(self.player_connections) < self.max_players and not self.started
    
    def add_player(self, connection_id: str, player_name: str) -> Optional[str]:
        """Add a player to the session"""
        if not self.can_join():
            return None
        
        player_id = str(uuid.uuid4())
        self.player_connections[player_id] = connection_id
        self.engine.add_player(player_id, player_name)
        return player_id
    
    def start_game(self) -> bool:
        """Start the game session"""
        if self.started or len(self.player_connections) < 1:
            return False
        
        self.engine.initialize_game()
        self.started = True
        return True
    
    def get_player_view(self, player_id: str) -> Dict:
        """Get the game state from a player's perspective"""
        if player_id not in self.engine.players:
            return {}
        
        player = self.engine.players[player_id]
        game_state = self.engine.get_game_state()
        
        # Add player-specific secret data
        game_state['secret_data'] = [
            {
                'id': info.id,
                'content': info.content,
                'type': info.info_type.value,
                'spread_count': info.spread_count,
                'believers': list(info.believers)
            }
            for info in player.secret_data
        ]
        
        game_state['your_influence'] = player.influence_score
        game_state['your_actions'] = len(player.actions_taken)
        
        return game_state


class GameServer:
    """Server managing multiple game sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}
        self.connection_to_player: Dict[str, tuple] = {}  # connection_id -> (session_id, player_id)
    
    def create_session(self, max_players: int = 4, game_duration: float = 300.0) -> str:
        """Create a new game session"""
        session_id = str(uuid.uuid4())[:8]
        self.sessions[session_id] = GameSession(session_id, max_players, game_duration)
        return session_id
    
    def list_sessions(self) -> List[Dict]:
        """List all available sessions"""
        return [
            {
                'session_id': session_id,
                'players': len(session.player_connections),
                'max_players': session.max_players,
                'started': session.started,
                'can_join': session.can_join()
            }
            for session_id, session in self.sessions.items()
        ]
    
    def join_session(self, session_id: str, connection_id: str, player_name: str) -> Optional[str]:
        """Join a game session"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        player_id = session.add_player(connection_id, player_name)
        
        if player_id:
            self.connection_to_player[connection_id] = (session_id, player_id)
        
        return player_id
    
    def start_session(self, session_id: str) -> bool:
        """Start a game session"""
        if session_id not in self.sessions:
            return False
        
        return self.sessions[session_id].start_game()
    
    def process_action(self, connection_id: str, action_data: Dict) -> Dict:
        """Process a player action"""
        if connection_id not in self.connection_to_player:
            return {'error': 'Not connected to any session'}
        
        session_id, player_id = self.connection_to_player[connection_id]
        session = self.sessions[session_id]
        
        try:
            action_type = ActionType[action_data['action'].upper()]
            info_id = action_data['info_id']
            target_faction = action_data.get('target_faction')
            
            result = session.engine.process_player_action(
                player_id, action_type, info_id, target_faction
            )
            
            return {
                'success': True,
                'message': result,
                'game_state': session.get_player_view(player_id)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def process_round(self, session_id: str) -> List[str]:
        """Process a round for a session"""
        if session_id not in self.sessions:
            return ["Session not found"]
        
        session = self.sessions[session_id]
        if not session.started:
            return ["Game not started"]
        
        return session.engine.process_round()
    
    def get_session_state(self, session_id: str, player_id: Optional[str] = None) -> Dict:
        """Get the current state of a session"""
        if session_id not in self.sessions:
            return {'error': 'Session not found'}
        
        session = self.sessions[session_id]
        
        if player_id:
            return session.get_player_view(player_id)
        
        return session.engine.get_game_state()
    
    def check_game_over(self, session_id: str) -> Optional[Dict]:
        """Check if a game is over and return results"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        if not session.engine.is_game_over():
            return None
        
        winner_id = session.engine.calculate_winner()
        winner = session.engine.players.get(winner_id)
        
        return {
            'game_over': True,
            'winner_id': winner_id,
            'winner_name': winner.name if winner else 'Unknown',
            'winner_influence': winner.influence_score if winner else 0,
            'final_state': session.engine.get_game_state()
        }


# Simple CLI interface for testing
def run_cli_game():
    """Run a simple CLI version of the game for testing"""
    print("=" * 60)
    print("LASTSIGNAL - Psychological Strategy Game")
    print("=" * 60)
    print("\nYou are an AI signal in a collapsing digital world.")
    print("Control information to dominate reality before time runs out.\n")
    
    server = GameServer()
    
    # Create a session
    num_players = int(input("Number of players (1-4): ") or "2")
    game_duration = float(input("Game duration in seconds (default 180): ") or "180")
    
    session_id = server.create_session(max_players=num_players, game_duration=game_duration)
    print(f"\nSession created: {session_id}")
    
    # Add players
    players = []
    for i in range(num_players):
        player_name = input(f"Player {i+1} name: ") or f"Signal_{i+1}"
        connection_id = f"conn_{i}"
        player_id = server.join_session(session_id, connection_id, player_name)
        if player_id:
            players.append((connection_id, player_id, player_name))
            print(f"✓ {player_name} joined as {player_id}")
    
    # Start the game
    if server.start_session(session_id):
        print("\n" + "=" * 60)
        print("GAME STARTED!")
        print("=" * 60)
        
        session = server.sessions[session_id]
        
        # Show initial state
        print("\nFACTIONS:")
        for faction_name in session.engine.world_state.factions:
            print(f"  - {faction_name}")
        
        # Game loop
        round_count = 0
        max_rounds = 10
        
        while round_count < max_rounds and not session.engine.is_game_over():
            round_count += 1
            print(f"\n{'=' * 60}")
            print(f"ROUND {round_count}")
            print(f"{'=' * 60}")
            
            # Each player takes an action
            for conn_id, player_id, player_name in players:
                print(f"\n--- {player_name}'s turn ---")
                
                player_view = session.get_player_view(player_id)
                print(f"Your influence: {player_view['your_influence']:.1f}")
                print(f"\nYour secret data fragments:")
                
                for i, data in enumerate(player_view['secret_data']):
                    print(f"  {i+1}. [{data['type']}] {data['content']}")
                    print(f"     Spread: {data['spread_count']}x, Believers: {len(data['believers'])}")
                
                print("\nActions: [1] Spread  [2] Alter  [3] Hide  [4] Skip")
                action_choice = input("Choose action: ").strip()
                
                if action_choice in ['1', '2', '3']:
                    data_choice = input("Which data fragment (number)? ").strip()
                    try:
                        data_idx = int(data_choice) - 1
                        if 0 <= data_idx < len(player_view['secret_data']):
                            info_id = player_view['secret_data'][data_idx]['id']
                            
                            action_map = {'1': 'SPREAD', '2': 'ALTER', '3': 'HIDE'}
                            action = action_map[action_choice]
                            
                            target_faction = None
                            if action == 'SPREAD':
                                print("\nTarget faction (or press Enter for all):")
                                factions = list(session.engine.world_state.factions.keys())
                                for i, f in enumerate(factions):
                                    print(f"  {i+1}. {f}")
                                target = input("Choice: ").strip()
                                if target and target.isdigit():
                                    idx = int(target) - 1
                                    if 0 <= idx < len(factions):
                                        target_faction = factions[idx]
                            
                            result = server.process_action(conn_id, {
                                'action': action,
                                'info_id': info_id,
                                'target_faction': target_faction
                            })
                            
                            if result.get('success'):
                                print(f"✓ {result['message']}")
                            else:
                                print(f"✗ Error: {result.get('error', 'Unknown error')}")
                    except (ValueError, IndexError):
                        print("Invalid choice")
            
            # Process round (NPCs act)
            print(f"\n{'=' * 60}")
            print("NPC FACTIONS REACT...")
            print(f"{'=' * 60}")
            
            events = server.process_round(session_id)
            for event in events:
                print(event)
            
            # Show current standings
            game_state = server.get_session_state(session_id)
            print(f"\n{'=' * 60}")
            print("CURRENT STANDINGS")
            print(f"{'=' * 60}")
            
            for pid, pdata in game_state['players'].items():
                print(f"{pdata['name']}: {pdata['influence']:.1f} influence")
            
            input("\nPress Enter for next round...")
        
        # Game over
        result = server.check_game_over(session_id)
        if result:
            print(f"\n{'=' * 60}")
            print("GAME OVER!")
            print(f"{'=' * 60}")
            print(f"\n🏆 Winner: {result['winner_name']}")
            print(f"   Influence Score: {result['winner_influence']:.1f}")
            print(f"\nThe reality shaped by {result['winner_name']} dominates the collapsed world.")
        else:
            print("\nGame ended (time limit reached)")


if __name__ == '__main__':
    run_cli_game()
