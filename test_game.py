"""
Tests for LastSignal game mechanics
"""

import unittest
from game import (
    GameEngine, InformationFragment, NPCFaction, Player,
    InformationType, ActionType, FactionState, WorldState
)


class TestInformationFragment(unittest.TestCase):
    """Test information fragment behavior"""
    
    def test_create_fragment(self):
        """Test creating an information fragment"""
        info = InformationFragment(
            id="test_1",
            content="Test data",
            info_type=InformationType.TRUTH
        )
        self.assertEqual(info.id, "test_1")
        self.assertEqual(info.content, "Test data")
        self.assertEqual(info.info_type, InformationType.TRUTH)
        self.assertEqual(info.spread_count, 0)
        self.assertEqual(len(info.believers), 0)
    
    def test_alter_fragment(self):
        """Test altering an information fragment"""
        original = InformationFragment(
            id="orig_1",
            content="Original content",
            info_type=InformationType.TRUTH
        )
        
        altered = original.alter("player_123")
        
        self.assertIn("ALTERED", altered.content)
        self.assertIn("player_123", altered.content)
        self.assertEqual(altered.info_type, InformationType.CORRUPTED)
        self.assertEqual(altered.source_player, "player_123")
        self.assertEqual(altered.altered_count, 1)


class TestNPCFaction(unittest.TestCase):
    """Test NPC faction behavior"""
    
    def test_create_faction(self):
        """Test creating an NPC faction"""
        faction = NPCFaction(name="Test Faction")
        self.assertEqual(faction.name, "Test Faction")
        self.assertEqual(faction.state, FactionState.PEACEFUL)
        self.assertEqual(faction.influence_score, 10.0)
        self.assertEqual(len(faction.beliefs), 0)
    
    def test_update_belief(self):
        """Test updating faction beliefs"""
        faction = NPCFaction(name="Test Faction")
        info = InformationFragment(
            id="info_1",
            content="Test",
            info_type=InformationType.TRUTH
        )
        
        faction.update_belief(info, strength=5.0)
        
        self.assertEqual(faction.beliefs["info_1"], 5.0)
        self.assertIn("Test Faction", info.believers)
    
    def test_faction_becomes_zealous(self):
        """Test faction becoming zealous with high belief"""
        faction = NPCFaction(name="Test Faction")
        info = InformationFragment(
            id="info_1",
            content="Test",
            info_type=InformationType.TRUTH
        )
        
        # Add strong belief
        faction.beliefs[info.id] = 20.0
        
        world_state = WorldState()
        result = faction.calculate_action(world_state)
        
        self.assertEqual(faction.state, FactionState.ZEALOUS)
        self.assertIsNotNone(result)
        self.assertIn("zealous", result.lower())


class TestPlayer(unittest.TestCase):
    """Test player behavior"""
    
    def test_create_player(self):
        """Test creating a player"""
        player = Player(id="p1", name="TestPlayer")
        self.assertEqual(player.id, "p1")
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player.influence_score, 0.0)
        self.assertEqual(len(player.actions_taken), 0)
    
    def test_take_action(self):
        """Test player taking an action"""
        player = Player(id="p1", name="TestPlayer")
        info = InformationFragment(
            id="info_1",
            content="Test",
            info_type=InformationType.TRUTH
        )
        
        action = player.take_action(ActionType.SPREAD, info, "TargetFaction")
        
        self.assertEqual(len(player.actions_taken), 1)
        self.assertEqual(action['action'], ActionType.SPREAD)
        self.assertEqual(action['info_id'], "info_1")
        self.assertEqual(action['target'], "TargetFaction")


class TestGameEngine(unittest.TestCase):
    """Test game engine functionality"""
    
    def test_initialize_game(self):
        """Test game initialization"""
        engine = GameEngine(num_players=2, game_duration=300.0)
        engine.initialize_game()
        
        self.assertTrue(engine.game_active)
        self.assertEqual(len(engine.world_state.factions), 5)
        self.assertGreater(len(engine.world_state.active_information), 0)
        self.assertIsNotNone(engine.start_time)
    
    def test_add_player(self):
        """Test adding a player to the game"""
        engine = GameEngine()
        engine.initialize_game()
        
        player = engine.add_player("p1", "TestPlayer")
        
        self.assertEqual(player.id, "p1")
        self.assertEqual(player.name, "TestPlayer")
        self.assertIn("p1", engine.players)
        self.assertGreater(len(player.secret_data), 0)
    
    def test_spread_action(self):
        """Test spreading information"""
        engine = GameEngine()
        engine.initialize_game()
        player = engine.add_player("p1", "TestPlayer")
        
        info_id = list(engine.world_state.active_information.keys())[0]
        faction_name = list(engine.world_state.factions.keys())[0]
        
        result = engine.process_player_action(
            "p1", ActionType.SPREAD, info_id, faction_name
        )
        
        self.assertIn("spread", result.lower())
        self.assertGreater(player.influence_score, 0)
        
        info = engine.world_state.active_information[info_id]
        self.assertEqual(info.spread_count, 1)
    
    def test_alter_action(self):
        """Test altering information"""
        engine = GameEngine()
        engine.initialize_game()
        player = engine.add_player("p1", "TestPlayer")
        
        info_id = list(engine.world_state.active_information.keys())[0]
        initial_count = len(engine.world_state.active_information)
        
        result = engine.process_player_action(
            "p1", ActionType.ALTER, info_id
        )
        
        self.assertIn("altered", result.lower())
        self.assertGreater(player.influence_score, 0)
        self.assertEqual(len(engine.world_state.active_information), initial_count + 1)
    
    def test_hide_action(self):
        """Test hiding information"""
        engine = GameEngine()
        engine.initialize_game()
        player = engine.add_player("p1", "TestPlayer")
        
        info_id = list(engine.world_state.active_information.keys())[0]
        info = engine.world_state.active_information[info_id]
        
        # First spread it so there's something to hide
        engine.process_player_action("p1", ActionType.SPREAD, info_id)
        initial_believers = len(info.believers)
        
        result = engine.process_player_action(
            "p1", ActionType.HIDE, info_id
        )
        
        self.assertIn("hid", result.lower())
        self.assertGreater(player.influence_score, 0)
    
    def test_process_round(self):
        """Test processing a game round"""
        engine = GameEngine()
        engine.initialize_game()
        
        initial_round = engine.world_state.round_number
        events = engine.process_round()
        
        self.assertEqual(engine.world_state.round_number, initial_round + 1)
        self.assertGreater(len(events), 0)
    
    def test_calculate_winner(self):
        """Test winner calculation"""
        engine = GameEngine()
        engine.initialize_game()
        
        p1 = engine.add_player("p1", "Player1")
        p2 = engine.add_player("p2", "Player2")
        
        p1.influence_score = 10.0
        p2.influence_score = 5.0
        
        winner_id = engine.calculate_winner()
        self.assertEqual(winner_id, "p1")
    
    def test_game_over_condition(self):
        """Test game over detection"""
        engine = GameEngine(game_duration=1.0)
        engine.initialize_game()
        
        # Initially not over
        self.assertFalse(engine.is_game_over())
        
        # Set time to 0
        engine.world_state.time_remaining = 0
        self.assertTrue(engine.is_game_over())


class TestWorldState(unittest.TestCase):
    """Test world state management"""
    
    def test_create_world_state(self):
        """Test creating world state"""
        world = WorldState(time_remaining=300.0)
        self.assertEqual(world.round_number, 0)
        self.assertEqual(world.time_remaining, 300.0)
        self.assertEqual(len(world.factions), 0)
        self.assertEqual(len(world.active_information), 0)
    
    def test_add_event(self):
        """Test adding events to world state"""
        world = WorldState()
        world.add_event("Test event")
        
        self.assertEqual(len(world.events_log), 1)
        self.assertIn("Test event", world.events_log[0])
        self.assertIn("Round 0", world.events_log[0])


class TestIntegration(unittest.TestCase):
    """Integration tests for full game flow"""
    
    def test_full_game_flow(self):
        """Test a complete game from start to finish"""
        # Initialize game
        engine = GameEngine(game_duration=1.0)
        engine.initialize_game()
        
        # Add players
        p1 = engine.add_player("p1", "Player1")
        p2 = engine.add_player("p2", "Player2")
        
        # Players take actions
        info_id = list(engine.world_state.active_information.keys())[0]
        engine.process_player_action("p1", ActionType.SPREAD, info_id)
        engine.process_player_action("p2", ActionType.ALTER, info_id)
        
        # Process round
        events = engine.process_round()
        
        # Check state
        self.assertGreater(p1.influence_score, 0)
        self.assertGreater(p2.influence_score, 0)
        self.assertEqual(engine.world_state.round_number, 1)
        self.assertGreater(len(events), 0)
        
        # End game
        engine.world_state.time_remaining = 0
        self.assertTrue(engine.is_game_over())
        
        # Get winner
        winner_id = engine.calculate_winner()
        self.assertIn(winner_id, ["p1", "p2"])


if __name__ == '__main__':
    unittest.main()
