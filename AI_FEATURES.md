# AI Features Guide for LastSignal

This guide explains the AI-powered enhancements that make LastSignal a dynamic, emergent gameplay experience.

## Overview

LastSignal integrates three AI-powered systems:

1. **LLM-Based Information Alteration** - Generates contextual misinformation variants
2. **ML-Based Faction Decision Making** - Sophisticated NPC behavior based on complex state
3. **AI-Powered Narrative Generation** - Post-match story generation and truth reveals

## Quick Start

### Mock Mode (Default)
By default, AI features run in **mock mode** using template-based generation. This requires no API keys and works out of the box.

```bash
python3 demo.py
```

### Full AI Mode (Requires OpenAI API Key)
To enable full LLM-powered features:

```bash
export LASTSIGNAL_AI_ENABLED=true
export OPENAI_API_KEY=your_openai_api_key_here
python3 demo.py
```

Or set it programmatically:

```python
import os
os.environ['LASTSIGNAL_AI_ENABLED'] = 'true'
os.environ['OPENAI_API_KEY'] = 'your_key_here'

from game import GameEngine
engine = GameEngine()
# AI features will automatically use OpenAI
```

## Feature Details

### 1. LLM-Based Information Alteration

**Purpose**: Generate believable, contextual alterations of information fragments that can mislead NPC factions.

**How It Works**:
- When a player uses the ALTER action, the system can use an LLM to generate variations
- The LLM receives context about the game state (round number, faction states, etc.)
- Generates subtle modifications that maintain plausibility while changing key details

**Example**:

```python
from game import InformationFragment, InformationType

info = InformationFragment(
    id="info_1",
    content="The system core is located in sector Alpha",
    info_type=InformationType.TRUTH
)

# With AI enabled
context = {
    'round': 3,
    'factions': ['The Archivists', 'Digital Nomads'],
    'faction_states': {'The Archivists': 'aggressive'}
}

altered = info.alter("player_123", use_ai=True, context=context)
print(altered.content)
# Example output: "[Signal player_123] Intelligence suggests the system core 
# may have been relocated to sector Beta following recent conflicts"
```

**Mock Mode Output**:
```
"[Signal player_123 intercept] The system core might be located in sector Alpha"
```

**Configuration**:
```python
from ai_engine import AIConfig, LLMAlterationEngine

config = AIConfig(
    enabled=True,
    model="gpt-3.5-turbo",  # or "gpt-4" for better results
    temperature=0.8,        # Higher = more creative
    max_tokens=150
)

llm_engine = LLMAlterationEngine(config)
```

---

### 2. ML-Based Faction Decision Making

**Purpose**: Make sophisticated, context-aware decisions for NPC factions based on complex game state.

**How It Works**:
- Analyzes multiple factors: belief strength, belief variance, relationships, current state
- Uses enhanced rule-based AI (or can be extended with actual ML models)
- Makes nuanced decisions considering the broader game context

**Enhanced Decision Factors**:
- **Belief Strength**: How strongly factions believe information
- **Belief Variance**: How unified vs conflicted faction beliefs are
- **Relationships**: Positive and negative connections with other factions
- **Game Context**: Round number, number of active factions, world state

**Example**:

```python
from game import NPCFaction, WorldState

faction = NPCFaction(name="The Archivists")
faction.beliefs = {
    'info_1': 12.0,
    'info_2': 8.0,
    'info_3': 10.0
}
faction.relationships = {
    'Digital Nomads': -3.0,
    'System Maintainers': 4.0
}

world_state = WorldState(round_number=5)

# With AI enabled - considers all factors
action = faction.calculate_action(world_state, use_ai=True)
print(action)
# "The Archivists launches preemptive strike against perceived threats"
```

**Mock Mode Behavior**:
Uses enhanced rule-based system with sophisticated decision trees:
- Unified strong beliefs → Zealous (cult formation)
- Strong beliefs + enemies → Aggressive (preemptive strike)
- Good relationships + moderate beliefs → Allied (coalition)
- High belief variance → Crashed (paralysis)

**Extending with Real ML**:
```python
from ai_engine import MLFactionEngine
import joblib

# Train your own model
# features: [total_belief, max_belief, num_beliefs, total_relationships, 
#            positive_rels, negative_rels, state_encoding, round, active_factions]

ml_engine = MLFactionEngine()
ml_engine._model = joblib.load('faction_behavior_model.pkl')

# Now factions will use your trained model
```

---

### 3. AI-Powered Narrative Generation

**Purpose**: Create compelling post-match narratives and truth reveals.

**Features**:
- **Match Narrative**: Dramatic 3-act story of what happened
- **Truth Reveal**: Shows what was real vs manipulated

**How It Works**:
- Collects all game events, player actions, and faction states
- Uses LLM to generate cinematic narrative
- Creates "truth reveal" showing objective facts vs lies

**Example**:

```python
from game import GameEngine

engine = GameEngine()
engine.initialize_game()

# ... play the game ...

# After game ends
narrative = engine.get_match_narrative()

print(narrative['summary'])
# "In the collapsing digital realm, two AI signals waged war for narrative 
# dominance. As systems crashed and alliances formed..."

print(narrative['key_moments'])
# "The turning point came when Signal_Alpha spread conflicting intelligence..."

print(narrative['conclusion'])
# "Signal_Beta's version of reality prevailed, reshaping the world..."

# Truth reveal
truth_reveal = engine.get_truth_reveal()
print(truth_reveal)
# Shows: Objective Truths (3), Fabricated Lies (2), Corrupted Data (4)
```

**Mock Mode Output**:
Generates template-based narratives using game statistics:
- Counts wars, cults, crashes, alliances
- Creates coherent story from event patterns
- Basic truth reveal showing fragment types

**Full AI Output**:
With OpenAI enabled, generates:
- Cinematic, dramatic prose
- Contextual references to specific events
- Character-driven narratives
- Thematic conclusions about truth and perception

---

## API Reference

### `InformationFragment.alter(player_id, use_ai=True, context=None)`

Generate an altered version of information.

**Parameters**:
- `player_id` (str): ID of player altering the information
- `use_ai` (bool): Whether to use LLM (default: True)
- `context` (dict, optional): Game context for better alterations

**Returns**: New `InformationFragment` with altered content

---

### `NPCFaction.calculate_action(world_state, use_ai=True)`

Determine faction action based on beliefs and relationships.

**Parameters**:
- `world_state` (WorldState): Current game state
- `use_ai` (bool): Whether to use ML engine (default: True)

**Returns**: Action description string or None

---

### `WorldState.generate_narrative(players, winner_id, winner_name)`

Generate match narrative summary.

**Parameters**:
- `players` (dict): All players in the game
- `winner_id` (str): ID of winning player
- `winner_name` (str): Name of winning player

**Returns**: Dict with keys: 'summary', 'key_moments', 'conclusion', 'full_narrative'

---

### `WorldState.generate_truth_reveal()`

Generate truth reveal showing real vs manipulated information.

**Returns**: String with formatted truth reveal

---

### `GameEngine.get_match_narrative()`

Convenience method to generate narrative for completed match.

**Returns**: Dict with narrative sections

---

### `GameEngine.get_truth_reveal()`

Convenience method to generate truth reveal.

**Returns**: String with truth reveal

---

## Configuration

### Environment Variables

```bash
# Enable AI features
export LASTSIGNAL_AI_ENABLED=true

# OpenAI API key (required for LLM features)
export OPENAI_API_KEY=your_api_key_here
```

### Programmatic Configuration

```python
from ai_engine import AIConfig

config = AIConfig(
    enabled=True,              # Enable AI features
    use_mock=False,            # Use real AI (not mock)
    model="gpt-3.5-turbo",     # OpenAI model to use
    temperature=0.8,           # Creativity (0.0-1.0)
    max_tokens=150             # Max response length
)

# Pass to engines
from ai_engine import LLMAlterationEngine, NarrativeEngine

llm_engine = LLMAlterationEngine(config)
narrative_engine = NarrativeEngine(config)
```

---

## Performance Considerations

### API Calls

With AI enabled, the game makes API calls to OpenAI:
- **Information Alteration**: 1 call per ALTER action
- **Narrative Generation**: 1 call per match end
- **Truth Reveal**: 1 call per match end

**Typical Match**:
- 10-20 ALTER actions = 10-20 API calls
- 1 narrative + 1 truth reveal = 2 API calls
- **Total**: ~12-22 API calls per match

### Cost Estimation

Using GPT-3.5-turbo (as of 2024):
- Input: $0.0015 per 1K tokens
- Output: $0.002 per 1K tokens
- Average match: ~$0.05 - $0.15

### Rate Limiting

The AI engine includes automatic fallback:
- If API call fails, uses mock generation
- No game interruption if AI unavailable
- Graceful degradation to template-based output

---

## Best Practices

### 1. Development
Use mock mode for rapid iteration:
```python
# No API key needed
python3 demo.py
python3 server.py
```

### 2. Production
Enable AI for richer experience:
```bash
export LASTSIGNAL_AI_ENABLED=true
export OPENAI_API_KEY=$YOUR_KEY
python3 server.py
```

### 3. Testing
Disable AI for deterministic tests:
```python
info.alter(player_id, use_ai=False)
faction.calculate_action(world_state, use_ai=False)
```

### 4. Custom Models
Train your own ML models:
```python
from ai_engine import MLFactionEngine
import joblib

ml_engine = MLFactionEngine()
ml_engine._model = joblib.load('your_model.pkl')
```

---

## Extending AI Features

### Adding New AI Capabilities

1. **Create new engine in `ai_engine.py`**:
```python
class CustomAIFeature:
    def __init__(self, config: AIConfig):
        self.config = config
    
    def process(self, input_data):
        if self.config.use_mock:
            return self._mock_process(input_data)
        # Real AI logic here
```

2. **Integrate into game logic**:
```python
from ai_engine import CustomAIFeature

def your_game_method(self):
    ai_feature = CustomAIFeature()
    result = ai_feature.process(self.data)
    return result
```

3. **Add tests**:
```python
def test_custom_ai_feature(self):
    feature = CustomAIFeature()
    result = feature.process(test_data)
    self.assertIsNotNone(result)
```

---

## Troubleshooting

### "openai package not installed"
```bash
pip install openai
```

### "API key not found"
```bash
export OPENAI_API_KEY=your_key_here
```

### AI features not working
Check configuration:
```python
from ai_engine import get_llm_engine

engine = get_llm_engine()
print(f"AI Enabled: {engine.config.enabled}")
print(f"Using Mock: {engine.config.use_mock}")
```

### Slow performance
Reduce AI calls:
- Use mock mode for development
- Cache common alterations
- Limit narrative generation to match end

---

## Future Enhancements

### Planned Features
- [ ] Voice-based information (audio alterations)
- [ ] Visual misinformation (image manipulation)
- [ ] Player-specific AI personalities
- [ ] Dynamic difficulty adjustment
- [ ] Real-time event prediction
- [ ] Collaborative AI writing for events

### Community Contributions
See `CONTRIBUTING.md` for guidelines on adding AI features.

---

## Examples

See complete examples in:
- `demo.py` - Shows all AI features
- `test_game.py` - Unit tests for AI components
- `examples/` - Additional gameplay scenarios (coming soon)

---

## Credits

AI integration by LastSignal development team.
Powered by OpenAI GPT models (optional).
Mock mode uses template-based generation (no external dependencies).

---

**Remember**: In LastSignal, AI doesn't just power the game—it shapes reality itself. Every alteration, every decision, every narrative is part of the emergent story. The winner's truth becomes THE truth. 🤖⚡
