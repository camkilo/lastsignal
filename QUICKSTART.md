# LastSignal - Quick Start Guide

Get started with LastSignal in under 5 minutes!

## Installation

No installation required! LastSignal uses only Python standard library.

**Requirements:**
- Python 3.7 or higher

## Run the Game

### Option 1: Web Interface (Recommended)

1. Open `index.html` in your browser:
   ```bash
   # macOS
   open index.html
   
   # Linux
   xdg-open index.html
   
   # Windows
   start index.html
   ```

2. Or use Python's built-in web server:
   ```bash
   python3 -m http.server 8000
   # Then open http://localhost:8000 in your browser
   ```

3. Enter your signal name and click **[INITIALIZE]**

4. Play the game!

### Option 2: Command-Line Interface

```bash
python3 server.py
```

Follow the prompts to set up your game.

### Option 3: Watch a Demo

```bash
python3 demo.py
```

This runs an automated 3-round game showing all mechanics.

## How to Play

### Your Goal
Be the signal with the highest **influence score** when time runs out.

### Each Round

1. **View Your Secret Data** - You have 3 information fragments
   - 🟢 **TRUTH** = Accurate information
   - 🔴 **LIE** = False information  
   - 🟣 **CORRUPTED** = Altered data

2. **Choose an Action** for each fragment:
   - **[SPREAD]** 📡 - Send info to factions (+1.0 influence)
   - **[ALTER]** 🔧 - Create corrupted version (+1.5 influence)
   - **[HIDE]** 🔒 - Remove from factions (+0.8 influence)

3. **[PROCESS ROUND]** - Watch factions react:
   - 🔥 Wars start
   - 🤝 Alliances form
   - 💥 Systems crash
   - ⚡ Cults emerge

4. **Repeat** until timer expires

### Example Turn

```
Your Secret Data:
  1. [TRUTH] System core located in sector Alpha
  2. [LIE] Digital Nomads planning attack
  3. [CORRUPTED] Emergency protocol activated

Action: Click [SPREAD] on fragment #1
Target: Choose "The Archivists" faction
Result: Archivists now believe the truth (+1.0 influence)

Action: Click [ALTER] on fragment #2
Result: Creates new corrupted lie (+1.5 influence)

Action: Click [HIDE] on fragment #3
Result: Hidden from 2 factions (+0.8 influence)

Total influence gained: 3.3 points
```

### Faction Reactions

After you act, factions react based on their beliefs:

- **High belief** (>15) → 🔥 Becomes **ZEALOUS** (forms cult)
- **Moderate belief** (>10) → ⚔️ Becomes **AGGRESSIVE** (starts wars)
- **Low belief** (<2) → 💥 **CRASHES** (system failure)
- **Shared beliefs** → 🤝 Forms **ALLIANCES**

## Strategy Tips

### Early Game (0-60s)
- Spread truths to build credibility
- Target specific factions for focused influence
- Watch which factions are receptive

### Mid Game (60-120s)
- Alter information to create chaos
- Hide damaging information
- Exploit faction conflicts

### Late Game (120-180s)
- Maximize influence with every action
- Spread widely to reach all factions
- Create dramatic events for bonus influence

### Pro Tips
1. **Target weak factions** - Those with few beliefs crash easily
2. **Create conflicts** - Wars between factions score you influence
3. **Balance actions** - Mix spread/alter/hide for varied effects
4. **Watch the clock** - Take bold actions when time is short
5. **Remember**: Truth is subjective - lies can be as powerful as truth!

## Understanding Influence

```
Action          | Influence Gain
----------------|---------------
Spread (target) | +1.0
Spread (all)    | +0.5
Alter           | +1.5
Hide            | +0.8
```

**Winning score**: Usually 10-20 influence in a 3-minute game

## Common Questions

**Q: Can I play single-player?**  
A: Yes! The web interface is single-player. You compete against the timer and try to maximize influence.

**Q: How many players can play?**  
A: 1-4 players. Use `server.py` for multiplayer CLI games.

**Q: How long is a game?**  
A: Default is 180 seconds (3 minutes). Customizable from 60-600 seconds.

**Q: What if I don't act in a round?**  
A: You gain no influence, but the game continues. Factions still react.

**Q: Can factions recover from CRASHED state?**  
A: Yes! Spread new information to revive crashed factions.

**Q: Do lies work better than truths?**  
A: All information types affect factions equally. The strategy is in how you use them.

## Running Tests

Verify everything works:

```bash
python3 test_game.py -v
```

Should show: `Ran 18 tests in 0.002s - OK`

## Next Steps

- Read [README.md](README.md) for full game rules
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand the code
- Experiment with different strategies
- Try different game durations
- Compete with friends using `server.py`

---

**Remember**: In LastSignal, you don't control characters—you control reality itself. Your version of truth becomes THE truth. Make it count. 🎮⚡
