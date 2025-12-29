"""
Demo script for LastSignal game - shows the game mechanics in action
"""

from game import GameEngine, ActionType
import time


def print_separator():
    print("\n" + "=" * 70 + "\n")


def demo_game():
    """Run a demonstration of the game"""
    print_separator()
    print("🎮 LASTSIGNAL - Game Demonstration 🎮")
    print("A multiplayer psychological strategy game")
    print_separator()
    
    print("INITIALIZING DIGITAL WORLD...")
    engine = GameEngine(num_players=2, game_duration=180.0)
    engine.initialize_game()
    
    print(f"✓ Game initialized with {len(engine.world_state.factions)} NPC factions")
    print(f"✓ {len(engine.world_state.active_information)} information fragments generated")
    print(f"✓ Game duration: {engine.game_duration}s")
    
    print_separator()
    print("FACTIONS IN THE DIGITAL WORLD:")
    for name, faction in engine.world_state.factions.items():
        print(f"  • {name:25} - State: {faction.state.value:10} - Influence: {faction.influence_score:.1f}")
    
    print_separator()
    print("ADDING AI SIGNALS (PLAYERS)...")
    player1 = engine.add_player("signal_alpha", "Signal_Alpha")
    player2 = engine.add_player("signal_beta", "Signal_Beta")
    
    print(f"✓ {player1.name} connected with {len(player1.secret_data)} secret data fragments")
    print(f"✓ {player2.name} connected with {len(player2.secret_data)} secret data fragments")
    
    print_separator()
    print("PLAYER 1 SECRET DATA:")
    for i, info in enumerate(player1.secret_data, 1):
        print(f"  {i}. [{info.info_type.value.upper()}] {info.content}")
    
    print("\nPLAYER 2 SECRET DATA:")
    for i, info in enumerate(player2.secret_data, 1):
        print(f"  {i}. [{info.info_type.value.upper()}] {info.content}")
    
    # Round 1
    print_separator()
    print("ROUND 1 - PLAYERS TAKE ACTION")
    print_separator()
    
    # Player 1 spreads information to a specific faction
    info1 = player1.secret_data[0]
    target_faction = list(engine.world_state.factions.keys())[0]
    result1 = engine.process_player_action(
        "signal_alpha", 
        ActionType.SPREAD, 
        info1.id, 
        target_faction
    )
    print(f"Player 1 Action: {result1}")
    print(f"  → Influence gained: +1.0 (total: {player1.influence_score:.1f})")
    
    # Player 2 alters information
    info2 = player2.secret_data[0]
    result2 = engine.process_player_action(
        "signal_beta",
        ActionType.ALTER,
        info2.id
    )
    print(f"\nPlayer 2 Action: {result2}")
    print(f"  → Influence gained: +1.5 (total: {player2.influence_score:.1f})")
    print(f"  → New corrupted data fragment created!")
    
    # Process round
    print_separator()
    print("PROCESSING ROUND - NPC FACTIONS REACT...")
    print_separator()
    
    events = engine.process_round()
    for event in events[2:]:  # Skip round header and timer
        if event.strip():
            print(f"  🔥 {event}")
    
    # Show faction beliefs
    print_separator()
    print("FACTION BELIEF STATES:")
    for name, faction in engine.world_state.factions.items():
        beliefs_str = f"{len(faction.beliefs)} beliefs" if faction.beliefs else "No beliefs yet"
        print(f"  • {name:25} - {faction.state.value:10} - {beliefs_str}")
    
    # Round 2
    print_separator()
    print("ROUND 2 - MORE ACTIONS")
    print_separator()
    
    # Player 1 broadcasts to all factions
    info1_2 = player1.secret_data[1] if len(player1.secret_data) > 1 else player1.secret_data[0]
    result1_2 = engine.process_player_action(
        "signal_alpha",
        ActionType.SPREAD,
        info1_2.id,
        None  # Broadcast to all
    )
    print(f"Player 1 Action: {result1_2}")
    print(f"  → Influence: {player1.influence_score:.1f}")
    
    # Player 2 hides information
    result2_2 = engine.process_player_action(
        "signal_beta",
        ActionType.HIDE,
        info2.id
    )
    print(f"\nPlayer 2 Action: {result2_2}")
    print(f"  → Influence: {player2.influence_score:.1f}")
    
    # Process round 2
    print_separator()
    print("PROCESSING ROUND 2...")
    print_separator()
    
    events2 = engine.process_round()
    for event in events2[2:]:
        if event.strip():
            print(f"  🔥 {event}")
    
    # Round 3
    print_separator()
    print("ROUND 3 - ESCALATION")
    print_separator()
    
    # Both players spread more info
    for player_id, player in [("signal_alpha", player1), ("signal_beta", player2)]:
        if len(player.secret_data) > 2:
            info = player.secret_data[2]
            result = engine.process_player_action(
                player_id,
                ActionType.SPREAD,
                info.id
            )
            print(f"{player.name}: {result} (Influence: {player.influence_score:.1f})")
    
    # Process round 3
    print_separator()
    print("PROCESSING ROUND 3...")
    print_separator()
    
    events3 = engine.process_round()
    for event in events3[2:]:
        if event.strip():
            print(f"  🔥 {event}")
    
    # Final state
    print_separator()
    print("CURRENT GAME STATE")
    print_separator()
    
    game_state = engine.get_game_state()
    
    print("PLAYERS:")
    for pid, pdata in game_state['players'].items():
        player = engine.players[pid]
        print(f"  {pdata['name']:15} - Influence: {pdata['influence']:6.1f} - Actions: {pdata['actions_taken']}")
    
    print("\nFACTIONS:")
    for name, fdata in game_state['factions'].items():
        print(f"  {name:25} - {fdata['state']:10} - Influence: {fdata['influence']:5.1f} - Beliefs: {fdata['beliefs_count']}")
    
    print("\nRECENT EVENTS:")
    for event in game_state['events'][-5:]:
        print(f"  • {event}")
    
    # Determine winner
    print_separator()
    print("SIMULATION COMPLETE")
    print_separator()
    
    winner_id = engine.calculate_winner()
    winner = engine.players[winner_id]
    
    print(f"🏆 DOMINANT REALITY: {winner.name}")
    print(f"   Final Influence Score: {winner.influence_score:.1f}")
    print(f"   Total Actions Taken: {len(winner.actions_taken)}")
    print(f"\nThe version of reality shaped by {winner.name} has dominated the collapsed world.")
    
    print_separator()
    print("KEY METRICS:")
    print(f"  • Total Rounds Played: {game_state['round']}")
    print(f"  • Active Information Fragments: {game_state['active_info_count']}")
    print(f"  • Total Events Generated: {len(engine.world_state.events_log)}")
    
    # Show information spread
    print("\nINFORMATION SPREAD ANALYSIS:")
    for info_id, info in list(engine.world_state.active_information.items())[:5]:
        if info.spread_count > 0 or len(info.believers) > 0:
            print(f"  • {info.content[:50]:50}")
            print(f"    Type: {info.info_type.value:10} | Spread: {info.spread_count}x | Believers: {len(info.believers)}")
    
    print_separator()
    
    return engine


if __name__ == '__main__':
    demo_game()
