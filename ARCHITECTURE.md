# LastSignal Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         LASTSIGNAL GAME                          │
│              Multiplayer Psychological Strategy                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        INTERFACES LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────┐         ┌─────────────────┐                │
│  │   Web UI       │         │   CLI Interface │                 │
│  │  (index.html)  │         │  (server.py)    │                 │
│  └────────┬───────┘         └────────┬────────┘                 │
│           │                          │                           │
└───────────┼──────────────────────────┼───────────────────────────┘
            │                          │
            └──────────┬───────────────┘
                       │
┌──────────────────────┼───────────────────────────────────────────┐
│                      │  SERVER LAYER                             │
├──────────────────────┼───────────────────────────────────────────┤
│                      ▼                                            │
│           ┌──────────────────┐                                   │
│           │   GameServer     │                                   │
│           │  - Sessions      │                                   │
│           │  - Connections   │                                   │
│           │  - Routing       │                                   │
│           └────────┬─────────┘                                   │
│                    │                                              │
│         ┌──────────┴──────────┐                                  │
│         │                     │                                  │
│    ┌────▼──────┐       ┌─────▼─────┐                           │
│    │ Session 1 │       │ Session 2 │  ...                       │
│    │ (2 players)│       │ (4 players)│                          │
│    └────┬──────┘       └─────┬─────┘                           │
└─────────┼────────────────────┼──────────────────────────────────┘
          │                    │
          └──────────┬─────────┘
                     │
┌────────────────────┼──────────────────────────────────────────────┐
│                    │  GAME ENGINE LAYER                           │
├────────────────────┼──────────────────────────────────────────────┤
│                    ▼                                               │
│         ┌───────────────────┐                                     │
│         │   GameEngine      │                                     │
│         │  - Game loop      │                                     │
│         │  - State mgmt     │                                     │
│         │  - Victory calc   │                                     │
│         └─────────┬─────────┘                                     │
│                   │                                                │
│    ┌──────────────┼──────────────────┐                           │
│    │              │                  │                            │
│    ▼              ▼                  ▼                            │
│ ┌────────┐  ┌─────────────┐  ┌──────────┐                       │
│ │Players │  │  WorldState │  │ Actions  │                        │
│ └────────┘  └─────────────┘  └──────────┘                        │
│                   │                                                │
│         ┌─────────┼─────────┐                                     │
│         │                   │                                     │
│         ▼                   ▼                                     │
│  ┌─────────────┐    ┌──────────────┐                            │
│  │ NPCFactions │    │ Information  │                             │
│  │  - Beliefs  │    │  Fragments   │                             │
│  │  - States   │    │  - Truth     │                             │
│  │  - Actions  │    │  - Lie       │                             │
│  └─────────────┘    │  - Corrupted │                             │
│                     └──────────────┘                              │
└───────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Game Initialization
```
GameEngine.initialize_game()
    ├─> Create 5 NPC Factions
    │   └─> Initialize beliefs, state, relationships
    ├─> Generate 8 Information Fragments
    │   └─> Mix of truths, lies, and corrupted data
    └─> Start game timer
```

### 2. Player Action Flow
```
Player Input (SPREAD/ALTER/HIDE)
    │
    ▼
GameEngine.process_player_action()
    │
    ├─> SPREAD
    │   ├─> Update faction beliefs (+1.0 or +2.0)
    │   ├─> Increment spread_count
    │   └─> Award influence (+0.5 or +1.0)
    │
    ├─> ALTER
    │   ├─> Create new corrupted fragment
    │   ├─> Add to active information
    │   └─> Award influence (+1.5)
    │
    └─> HIDE
        ├─> Remove from 2 factions' beliefs
        └─> Award influence (+0.8)
```

### 3. Round Processing
```
GameEngine.process_round()
    │
    ├─> Update timer
    │
    ├─> For each NPC Faction:
    │   ├─> Calculate strongest belief
    │   ├─> Determine state change:
    │   │   ├─> Belief > 15  → ZEALOUS (cult)
    │   │   ├─> Belief > 10  → AGGRESSIVE (war)
    │   │   └─> Belief < 2   → CRASHED (failure)
    │   └─> Generate event
    │
    └─> Process faction interactions:
        ├─> Common beliefs → Alliances
        └─> Aggressive state → Conflicts
```

## Core Concepts

### Information Warfare
- Players don't control units—they control **narratives**
- Information fragments shape faction beliefs
- Beliefs drive NPC actions (wars, alliances, crashes)

### Belief System
```
NPCFaction
    beliefs: { info_id: strength }
    
When information is spread:
    belief[info_id] += strength
    
Faction actions based on belief:
    if max_belief > 15: → Zealous (cult)
    if max_belief > 10: → Aggressive (war)
    if max_belief < 2:  → Crashed (failure)
```

### Influence Scoring
```
Player influence = sum of:
    + Spread to faction: +1.0
    + Broadcast to all:  +0.5
    + Alter information: +1.5
    + Hide information:  +0.8
    
Winner = Player with highest influence when timer expires
```

### Game States

#### Information Fragment States
- **TRUTH**: Accurate data, builds credibility
- **LIE**: False data, can mislead factions
- **CORRUPTED**: Altered data, unpredictable effects

#### Faction States
- **PEACEFUL**: Normal operation
- **AGGRESSIVE**: Attacks other factions
- **ZEALOUS**: Cult-like devotion to beliefs
- **CRASHED**: System failure from info overload
- **ALLIED**: Cooperative relationships

## File Structure

```
lastsignal/
├── game.py           # Core game engine (450 lines)
│   ├── InformationFragment
│   ├── NPCFaction
│   ├── Player
│   ├── WorldState
│   └── GameEngine
│
├── server.py         # Multiplayer server (350 lines)
│   ├── GameSession
│   ├── GameServer
│   └── CLI interface
│
├── index.html        # Web UI (600 lines)
│   ├── Game interface
│   ├── Action buttons
│   └── Live updates
│
├── test_game.py      # Test suite (280 lines)
│   └── 18 comprehensive tests
│
├── demo.py           # Demo script (200 lines)
│   └── Automated gameplay showcase
│
└── README.md         # Documentation
    └── Game rules, mechanics, examples
```

## Key Game Mechanics

### 1. Information Manipulation
Players receive 3 random data fragments each round:
- Can **SPREAD** to specific faction or broadcast to all
- Can **ALTER** to create corrupted versions
- Can **HIDE** to remove from faction beliefs

### 2. Emergent Behavior
NPC factions react autonomously:
- Form alliances when sharing beliefs
- Start wars when aggressive
- Crash from conflicting information
- Become zealous with strong convictions

### 3. Victory Conditions
- Timer-based: Game ends after set duration (60-600s)
- Score-based: Player with highest influence wins
- Influence gained through strategic information control

## Testing Strategy

### Unit Tests
- Information fragment creation and alteration
- NPC faction belief updates and state changes
- Player action processing and influence calculation
- Game engine initialization and state management

### Integration Tests
- Full game flow from start to finish
- Multi-player scenarios
- Round processing with faction interactions
- Victory calculation

### Manual Testing
- CLI interface for gameplay testing
- Demo script for automated runs
- Web UI for visual testing

## Future Enhancements

1. **Real Multiplayer Networking**
   - WebSocket support for live gameplay
   - Real-time state synchronization
   - Player-to-player interactions

2. **Advanced AI**
   - More sophisticated faction decision-making
   - Faction memory of past events
   - Dynamic relationship evolution

3. **Extended Content**
   - More faction types
   - Special information abilities
   - Scenario-based gameplay
   - Custom game modes

4. **Social Features**
   - Player alliances and betrayals
   - Chat and communication
   - Reputation system
   - Tournament mode

---

**Design Philosophy**: The game models information warfare in digital systems, where truth is subjective and the winner's narrative becomes reality. Every mechanic reinforces this theme—players are invisible, factions act on belief not fact, and victory is about shaping perception, not controlling territory.
