# LastSignal

> A multiplayer psychological strategy game where players are invisible AI signals inside a collapsing digital world.

## 🎮 Game Concept

You don't control characters—you control **information**. 

As an invisible AI signal in a dying digital realm, you receive secret data fragments each round: truths, lies, and corrupted logs. Your goal is to spread, alter, or hide this information to influence NPC factions. These factions act only on belief, not facts, causing wars, cults, system crashes, and alliances based on what they believe to be true.

The world ends after a timer runs out. **Whoever's version of reality dominates wins.**

## 🌟 Key Features

- **Information Warfare**: Control data, not units. Every piece of information shapes reality.
- **Belief-Based AI**: NPC factions make decisions based on what they believe, not objective truth.
- **Psychological Strategy**: Manipulate perceptions to create chaos or alliances.
- **Multiplayer**: Compete against other signals to dominate the narrative.
- **Time Pressure**: The world is collapsing—make your moves count before time runs out.
- **Dynamic Events**: Wars, cults, crashes, and alliances emerge from faction beliefs.
- **🤖 AI-Powered Enhancements**: 
  - LLM-generated information alterations for infinite misinformation variants
  - ML-based faction decision making for sophisticated NPC behavior
  - AI-powered narrative generation for post-match storytelling and truth reveals

## 🚀 Quick Start

### Web Interface (Recommended)

Open `index.html` in your web browser for an interactive single-player experience:

```bash
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

Or use Python's built-in web server:

```bash
python3 -m http.server 8000
# Then open http://localhost:8000 in your browser
```

### CLI Game

Run the command-line version for testing:

```bash
python3 server.py
```

Follow the prompts to:
1. Set number of players (1-4)
2. Set game duration
3. Enter player names
4. Take actions each round

## 📖 How to Play

### Game Flow

1. **Setup**: Choose your signal name and game duration
2. **Each Round**:
   - View your secret data fragments
   - Choose actions: SPREAD, ALTER, or HIDE
   - Watch NPC factions react to information
   - See events unfold (wars, alliances, crashes, cults)
3. **Victory**: Highest influence score when time runs out wins

### Actions

- **SPREAD** 📡: Broadcast information to factions (increases their belief)
  - Target specific faction: +1.0 influence, +2.0 belief strength
  - Broadcast to all: +0.5 influence, +1.0 belief strength each
  
- **ALTER** 🔧: Modify information to create corrupted data
  - Creates new corrupted fragment
  - +1.5 influence
  
- **HIDE** 🔒: Conceal information from factions
  - Removes from 2 factions' beliefs
  - +0.8 influence

### Information Types

- **TRUTH** (Green): Accurate information
- **LIE** (Red): False information
- **CORRUPTED** (Purple): Altered or damaged data

### Faction States

- **Peaceful**: Normal operation
- **Aggressive**: Attacking other factions
- **Zealous**: Cult-like devotion to beliefs
- **Crashed**: System failure from information overload
- **Allied**: Cooperative with other factions

## 🏗️ Architecture

### Core Components

- **`game.py`**: Core game engine
  - `GameEngine`: Main game loop and state management
  - `InformationFragment`: Data pieces that players manipulate
  - `NPCFaction`: AI factions that react to beliefs
  - `Player`: Player (AI signal) representation
  - `WorldState`: Global game state tracker

- **`server.py`**: Multiplayer server
  - `GameServer`: Manages multiple game sessions
  - `GameSession`: Individual game instance
  - CLI interface for testing

- **`index.html`**: Web-based UI
  - Interactive single-player interface
  - Real-time game state updates
  - Visual representation of factions and information

## 🎯 Game Mechanics

### Belief System

NPC factions maintain belief scores for each information fragment:
- Higher belief → stronger conviction
- Belief > 15 → Faction becomes **Zealous** (cult formation)
- Belief > 10 → Faction may become **Aggressive** (starts conflicts)
- Belief < 2 → Risk of **Crash** (system failure)

### Faction Interactions

- **Common Beliefs**: Factions with shared beliefs form alliances
- **Aggressive State**: Factions attack others, reducing their influence
- **Crashed State**: Faction becomes inactive temporarily
- **Zealous State**: Extreme devotion, unpredictable behavior

### Victory Conditions

Player with highest **influence score** when timer expires wins. Influence gained through:
- Spreading information effectively
- Altering data to create new narratives
- Strategically hiding damaging information
- Causing faction reactions and events

## 🤖 AI Features

LastSignal includes powerful AI enhancements that create dynamic, emergent gameplay:

### LLM-Based Information Alteration
Generate contextual, believable misinformation when players use the ALTER action. Works in mock mode by default, or connect to OpenAI for sophisticated variations.

### ML-Based Faction Decisions
NPC factions make sophisticated decisions based on belief strength, variance, relationships, and game context. Enhanced rule-based AI with support for custom ML models.

### AI-Powered Narratives
After each match, get:
- **Match Narrative**: Dramatic 3-act story of what happened
- **Truth Reveal**: Shows what was real vs manipulated

### Enable Full AI Features
```bash
export LASTSIGNAL_AI_ENABLED=true
export OPENAI_API_KEY=your_openai_api_key
python3 demo.py
```

**See [AI_FEATURES.md](AI_FEATURES.md) for complete documentation.**

## 🧪 Testing

Run the CLI version to test game mechanics:

```bash
python3 server.py
```

Test scenarios:
1. **Single Player**: Test basic mechanics and NPC behavior
2. **Multi-Player**: Test competitive information warfare
3. **Short Games**: 60-second games for quick testing
4. **Long Games**: 5+ minute games for strategic depth
5. **AI Features**: Run `python3 demo.py` to see AI-powered narratives

## 🎨 Game Strategy Tips

1. **Early Game**: Spread truths to establish credibility
2. **Mid Game**: Alter information to create chaos
3. **Late Game**: Hide damaging info and consolidate influence
4. **Target Wisely**: Focus on specific factions for maximum impact
5. **Watch Faction States**: Predict and exploit faction behaviors
6. **Balance Actions**: Mix spread/alter/hide for varied influence
7. **Use AI Wisely**: Enable AI features for richer, more unpredictable gameplay

## 🔮 Future Enhancements

- [x] LLM-based information alteration (infinite misinformation variants)
- [x] ML-based NPC decision making (adaptive faction behavior)
- [x] AI-powered narrative generation (post-match storytelling)
- [ ] Real multiplayer networking (WebSocket support)
- [ ] More faction types and behaviors
- [ ] Information decay over time
- [ ] Player alliances and betrayals
- [ ] Replay system for strategy analysis
- [ ] Tournament mode
- [ ] Custom scenario editor
- [ ] Voice-based information fragments
- [ ] Visual misinformation generation

## 📝 License

Open source - feel free to modify and extend!

## 🤝 Contributing

This is a game about information warfare and psychological strategy. Ideas for new mechanics, faction behaviors, or game modes are welcome!

---

**Remember**: In LastSignal, truth is subjective. The winner's version of reality becomes the only reality. 🎮
