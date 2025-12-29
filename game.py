"""
LastSignal - A multiplayer psychological strategy game

Players are invisible AI signals inside a collapsing digital world.
Control information, not characters. Spread truths, lies, and corrupted data
to influence NPC factions and dominate reality before the world ends.
"""

import random
import time
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from enum import Enum


# Game configuration constants
SECTOR_NAMES = ["Alpha", "Beta", "Gamma", "Delta", "Omega"]
DEFAULT_FACTION_NAMES = [
    "The Archivists",
    "Digital Nomads",
    "Encryption Zealots",
    "System Maintainers",
    "Data Miners"
]


class InformationType(Enum):
    """Types of information fragments"""
    TRUTH = "truth"
    LIE = "lie"
    CORRUPTED = "corrupted"


class ActionType(Enum):
    """Actions players can take with information"""
    SPREAD = "spread"
    ALTER = "alter"
    HIDE = "hide"


class FactionState(Enum):
    """Possible states for NPC factions"""
    PEACEFUL = "peaceful"
    AGGRESSIVE = "aggressive"
    ZEALOUS = "zealous"
    CRASHED = "crashed"
    ALLIED = "allied"


@dataclass
class InformationFragment:
    """A piece of information in the game world"""
    id: str
    content: str
    info_type: InformationType
    source_player: Optional[str] = None
    spread_count: int = 0
    altered_count: int = 0
    believers: Set[str] = field(default_factory=set)
    
    def alter(self, player_id: str, use_ai: bool = True, context: Optional[Dict] = None) -> 'InformationFragment':
        """
        Create an altered version of this information
        
        Args:
            player_id: ID of the player altering the information
            use_ai: Whether to use LLM for generating contextual variations
            context: Optional game context for more sophisticated alterations
        
        Returns:
            New InformationFragment with altered content
        """
        # Try to use AI engine for sophisticated alteration
        if use_ai:
            try:
                from ai_engine import get_llm_engine
                llm = get_llm_engine()
                altered_content = llm.generate_altered_content(
                    self.content,
                    self.info_type.value,
                    player_id,
                    context
                )
            except Exception as e:
                # Fallback to simple alteration if AI fails
                altered_content = f"[ALTERED by {player_id}] {self.content}"
        else:
            altered_content = f"[ALTERED by {player_id}] {self.content}"
        
        return InformationFragment(
            id=f"{self.id}_altered_{player_id}",
            content=altered_content,
            info_type=InformationType.CORRUPTED,
            source_player=player_id,
            altered_count=self.altered_count + 1
        )


@dataclass
class NPCFaction:
    """An NPC faction that acts on beliefs"""
    name: str
    state: FactionState = FactionState.PEACEFUL
    beliefs: Dict[str, float] = field(default_factory=dict)  # info_id -> belief strength
    influence_score: float = 10.0
    relationships: Dict[str, float] = field(default_factory=dict)  # faction_name -> relationship
    
    def update_belief(self, info_fragment: InformationFragment, strength: float = 1.0):
        """Update faction's belief in a piece of information"""
        self.beliefs[info_fragment.id] = self.beliefs.get(info_fragment.id, 0) + strength
        info_fragment.believers.add(self.name)
    
    def calculate_action(self, world_state: 'WorldState', use_ai: bool = True) -> Optional[str]:
        """
        Decide what action to take based on beliefs
        
        Args:
            world_state: Current world state for context
            use_ai: Whether to use ML engine for sophisticated decision-making
        
        Returns:
            Action description string or None
        """
        if not self.beliefs:
            return None
        
        # Try to use ML engine for sophisticated decision-making
        if use_ai:
            try:
                from ai_engine import get_ml_engine
                ml_engine = get_ml_engine()
                
                world_context = {
                    'round_number': world_state.round_number,
                    'active_factions': len(world_state.factions),
                    'total_information': len(world_state.active_information),
                }
                
                new_state, action = ml_engine.calculate_sophisticated_action(
                    self.name,
                    self.beliefs,
                    self.relationships,
                    self.state.value,
                    world_context
                )
                
                if new_state and action:
                    self.state = FactionState(new_state)
                    return action
                    
            except Exception as e:
                # Fallback to rule-based if AI fails
                pass
        
        # Original rule-based logic as fallback
        strongest_belief = max(self.beliefs.items(), key=lambda x: x[1])
        belief_strength = strongest_belief[1]
        
        if belief_strength > 15:
            self.state = FactionState.ZEALOUS
            return f"{self.name} has become zealous! Forms a cult around their beliefs."
        elif belief_strength > 10 and random.random() > 0.5:
            self.state = FactionState.AGGRESSIVE
            return f"{self.name} starts a conflict with neighboring factions!"
        elif belief_strength < 2:
            self.state = FactionState.CRASHED
            return f"{self.name} experiences a system crash from conflicting information!"
        
        return None


@dataclass
class Player:
    """A player (AI signal) in the game"""
    id: str
    name: str
    secret_data: List[InformationFragment] = field(default_factory=list)
    actions_taken: List[Dict] = field(default_factory=list)
    influence_score: float = 0.0
    
    def take_action(self, action: ActionType, info: InformationFragment, 
                   target_faction: Optional[str] = None) -> Dict:
        """Take an action with information"""
        action_record = {
            'action': action,
            'info_id': info.id,
            'target': target_faction,
            'timestamp': time.time()
        }
        self.actions_taken.append(action_record)
        return action_record


@dataclass
class WorldState:
    """The state of the collapsing digital world"""
    round_number: int = 0
    time_remaining: float = 300.0  # 5 minutes in seconds
    factions: Dict[str, NPCFaction] = field(default_factory=dict)
    active_information: Dict[str, InformationFragment] = field(default_factory=dict)
    events_log: List[str] = field(default_factory=list)
    
    def add_event(self, event: str):
        """Log an event in the world"""
        self.events_log.append(f"[Round {self.round_number}] {event}")
    
    def generate_narrative(self, players: Dict[str, 'Player'], winner_id: str, winner_name: str) -> Dict[str, str]:
        """
        Generate AI-powered narrative summary of the match
        
        Args:
            players: Dictionary of all players
            winner_id: ID of the winning player
            winner_name: Name of the winning player
        
        Returns:
            Dictionary containing narrative sections
        """
        try:
            from ai_engine import get_narrative_engine
            narrative_engine = get_narrative_engine()
            
            # Prepare player data
            player_data = {
                pid: {
                    'name': p.name,
                    'influence': p.influence_score,
                    'actions_taken': len(p.actions_taken)
                }
                for pid, p in players.items()
            }
            
            # Prepare faction data
            faction_data = {
                fname: {
                    'state': faction.state.value,
                    'influence': faction.influence_score,
                    'beliefs_count': len(faction.beliefs)
                }
                for fname, faction in self.factions.items()
            }
            
            return narrative_engine.generate_match_narrative(
                self.events_log,
                player_data,
                faction_data,
                winner_id,
                winner_name
            )
            
        except Exception as e:
            # Fallback narrative if AI fails
            return {
                'summary': f"In a battle for narrative dominance, {winner_name} emerged victorious.",
                'key_moments': f"The match featured {len(self.events_log)} critical events.",
                'conclusion': f"{winner_name}'s version of reality now defines the collapsed world.",
                'full_narrative': f"Match concluded. Winner: {winner_name}"
            }
    
    def generate_truth_reveal(self) -> str:
        """
        Generate AI-powered 'truth reveal' showing what was real vs manipulated
        
        Returns:
            Truth reveal narrative
        """
        try:
            from ai_engine import get_narrative_engine
            narrative_engine = get_narrative_engine()
            
            # Prepare information fragment data
            fragment_data = {
                info_id: {
                    'content': info.content,
                    'type': info.info_type.value,
                    'spread_count': info.spread_count,
                    'believers': len(info.believers)
                }
                for info_id, info in self.active_information.items()
            }
            
            return narrative_engine.generate_truth_reveal(self.events_log, fragment_data)
            
        except Exception as e:
            return "=== TRUTH REVEAL ===\n\nThe fog of information warfare clears. Reality solidifies."



class GameEngine:
    """Core game engine for LastSignal"""
    
    def __init__(self, num_players: int = 2, game_duration: float = 300.0):
        self.players: Dict[str, Player] = {}
        self.world_state = WorldState(time_remaining=game_duration)
        self.game_duration = game_duration
        self.game_active = False
        self.start_time: Optional[float] = None
        
    def initialize_game(self):
        """Set up the initial game state"""
        # Create NPC factions
        for name in DEFAULT_FACTION_NAMES:
            self.world_state.factions[name] = NPCFaction(
                name=name,
                relationships={other: 0.0 for other in DEFAULT_FACTION_NAMES if other != name}
            )
        
        # Generate initial information fragments
        self.generate_information_fragments()
        
        self.world_state.add_event("The digital world begins to collapse...")
        self.game_active = True
        self.start_time = time.time()
    
    def generate_information_fragments(self):
        """Generate secret information fragments for distribution"""
        templates = [
            ("The system core is located in sector {}", InformationType.TRUTH),
            ("Faction {} is planning an attack", InformationType.LIE),
            ("Emergency protocol {} activated", InformationType.CORRUPTED),
            ("Resource cache found at coordinates {}", InformationType.TRUTH),
            ("Security breach in {} subsystem", InformationType.LIE),
            ("Ancient data suggests {} holds the key", InformationType.CORRUPTED),
            ("Coalition forming between {} factions", InformationType.TRUTH),
            ("Virus detected in {} network", InformationType.LIE),
        ]
        
        for i, (template, info_type) in enumerate(templates):
            content = template.format(random.choice(SECTOR_NAMES))
            fragment = InformationFragment(
                id=f"info_{i}",
                content=content,
                info_type=info_type
            )
            self.world_state.active_information[fragment.id] = fragment
    
    def add_player(self, player_id: str, player_name: str) -> Player:
        """Add a player to the game"""
        player = Player(id=player_id, name=player_name)
        self.players[player_id] = player
        
        # Give player some secret data
        available_info = list(self.world_state.active_information.values())
        if available_info:
            player.secret_data = random.sample(
                available_info, 
                min(3, len(available_info))
            )
        
        return player
    
    def process_player_action(self, player_id: str, action_type: ActionType, 
                             info_id: str, target_faction: Optional[str] = None) -> str:
        """Process a player's action"""
        if player_id not in self.players:
            return "Error: Player not found"
        
        if info_id not in self.world_state.active_information:
            return "Error: Information fragment not found"
        
        player = self.players[player_id]
        info = self.world_state.active_information[info_id]
        
        # Execute the action
        if action_type == ActionType.SPREAD:
            return self._spread_information(player, info, target_faction)
        elif action_type == ActionType.ALTER:
            return self._alter_information(player, info)
        elif action_type == ActionType.HIDE:
            return self._hide_information(player, info)
        
        return "Error: Unknown action"
    
    def _spread_information(self, player: Player, info: InformationFragment, 
                           target_faction: Optional[str]) -> str:
        """Spread information to faction(s)"""
        player.take_action(ActionType.SPREAD, info, target_faction)
        info.spread_count += 1
        
        if target_faction and target_faction in self.world_state.factions:
            # Spread to specific faction
            faction = self.world_state.factions[target_faction]
            faction.update_belief(info, strength=2.0)
            player.influence_score += 1.0
            return f"{player.name} spread information to {target_faction}"
        else:
            # Spread to all factions
            for faction in self.world_state.factions.values():
                faction.update_belief(info, strength=1.0)
            player.influence_score += 0.5
            return f"{player.name} broadcast information to all factions"
    
    def _alter_information(self, player: Player, info: InformationFragment) -> str:
        """Alter information to create a new version"""
        player.take_action(ActionType.ALTER, info)
        
        # Prepare context for AI alteration
        context = {
            'round': self.world_state.round_number,
            'factions': [f.name for f in self.world_state.factions.values()],
            'faction_states': {f.name: f.state.value for f in self.world_state.factions.values()},
        }
        
        altered_info = info.alter(player.id, use_ai=True, context=context)
        self.world_state.active_information[altered_info.id] = altered_info
        player.influence_score += 1.5
        return f"{player.name} altered information, creating {altered_info.id}"
    
    def _hide_information(self, player: Player, info: InformationFragment) -> str:
        """Hide information from factions"""
        player.take_action(ActionType.HIDE, info)
        
        # Remove from some factions' beliefs
        factions_affected = random.sample(
            list(self.world_state.factions.keys()),
            k=min(2, len(self.world_state.factions))
        )
        
        for faction_name in factions_affected:
            faction = self.world_state.factions[faction_name]
            if info.id in faction.beliefs:
                del faction.beliefs[info.id]
                info.believers.discard(faction_name)
        
        player.influence_score += 0.8
        return f"{player.name} hid information from {len(factions_affected)} factions"
    
    def process_round(self) -> List[str]:
        """Process a game round - NPCs act on their beliefs"""
        self.world_state.round_number += 1
        events = []
        
        # Update time
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.world_state.time_remaining = max(0, self.game_duration - elapsed)
        
        events.append(f"=== Round {self.world_state.round_number} ===")
        events.append(f"Time remaining: {self.world_state.time_remaining:.1f}s")
        
        # Each faction acts based on their beliefs
        for faction in self.world_state.factions.values():
            action_result = faction.calculate_action(self.world_state)
            if action_result:
                events.append(action_result)
                self.world_state.add_event(action_result)
        
        # Check for faction interactions
        interaction_events = self._process_faction_interactions()
        events.extend(interaction_events)
        
        return events
    
    def _process_faction_interactions(self) -> List[str]:
        """Process interactions between factions"""
        events = []
        faction_list = list(self.world_state.factions.values())
        
        for i, faction1 in enumerate(faction_list):
            for faction2 in faction_list[i+1:]:
                # Check for common beliefs
                common_beliefs = set(faction1.beliefs.keys()) & set(faction2.beliefs.keys())
                
                if len(common_beliefs) > 2:
                    # Form alliance
                    faction1.relationships[faction2.name] = faction1.relationships.get(faction2.name, 0) + 1
                    faction2.relationships[faction1.name] = faction2.relationships.get(faction1.name, 0) + 1
                    
                    if faction1.relationships[faction2.name] > 3:
                        events.append(f"⚔ {faction1.name} and {faction2.name} form an alliance!")
                        self.world_state.add_event(f"{faction1.name} and {faction2.name} allied")
                
                # Check for conflicts
                if faction1.state == FactionState.AGGRESSIVE and random.random() > 0.6:
                    events.append(f"⚔ {faction1.name} attacks {faction2.name}!")
                    faction2.influence_score *= 0.8
                    self.world_state.add_event(f"War between {faction1.name} and {faction2.name}")
        
        return events
    
    def calculate_winner(self) -> Optional[str]:
        """Calculate which player's version of reality dominates"""
        if not self.players:
            return None
        
        # Player with highest influence score wins
        winner = max(self.players.values(), key=lambda p: p.influence_score)
        return winner.id
    
    def is_game_over(self) -> bool:
        """Check if the game has ended"""
        return self.world_state.time_remaining <= 0 or not self.game_active
    
    def get_game_state(self) -> Dict:
        """Get current game state for display"""
        return {
            'round': self.world_state.round_number,
            'time_remaining': self.world_state.time_remaining,
            'factions': {
                name: {
                    'state': faction.state.value,
                    'influence': faction.influence_score,
                    'beliefs_count': len(faction.beliefs)
                }
                for name, faction in self.world_state.factions.items()
            },
            'players': {
                pid: {
                    'name': player.name,
                    'influence': player.influence_score,
                    'actions_taken': len(player.actions_taken)
                }
                for pid, player in self.players.items()
            },
            'active_info_count': len(self.world_state.active_information),
            'events': self.world_state.events_log[-5:]  # Last 5 events
        }
    
    def get_match_narrative(self) -> Dict[str, str]:
        """
        Generate AI-powered narrative summary of the completed match
        
        Returns:
            Dictionary with narrative sections (summary, key_moments, conclusion, full_narrative)
        """
        winner_id = self.calculate_winner()
        winner = self.players.get(winner_id)
        winner_name = winner.name if winner else "Unknown"
        
        return self.world_state.generate_narrative(self.players, winner_id, winner_name)
    
    def get_truth_reveal(self) -> str:
        """
        Generate AI-powered truth reveal showing what was real vs manipulated
        
        Returns:
            Truth reveal narrative string
        """
        return self.world_state.generate_truth_reveal()
