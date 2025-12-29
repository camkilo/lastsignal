"""
AI Engine for LastSignal - LLM and ML integration for dynamic gameplay

This module provides AI-powered enhancements for:
1. LLM-based information alteration (contextual misinformation generation)
2. ML-based faction decision making (adaptive NPC behavior)
3. AI-powered narrative generation (post-match story generation)
"""

import random
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


# Configuration for AI features
AI_ENABLED = os.environ.get('LASTSIGNAL_AI_ENABLED', 'false').lower() == 'true'
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
USE_MOCK_AI = not AI_ENABLED or not OPENAI_API_KEY


@dataclass
class AIConfig:
    """Configuration for AI features"""
    enabled: bool = AI_ENABLED
    use_mock: bool = USE_MOCK_AI
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.8
    max_tokens: int = 150


class LLMAlterationEngine:
    """
    LLM-powered information alteration engine
    Generates contextual variations of information fragments
    """
    
    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        self._client = None
        
        if self.config.enabled and not self.config.use_mock:
            try:
                import openai
                self._client = openai.OpenAI(api_key=OPENAI_API_KEY)
            except ImportError:
                print("Warning: openai package not installed. Using mock AI.")
                self.config.use_mock = True
    
    def generate_altered_content(
        self, 
        original_content: str, 
        info_type: str,
        player_id: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate an altered version of information using LLM
        
        Args:
            original_content: The original information text
            info_type: Type of information (truth/lie/corrupted)
            player_id: ID of the player altering the information
            context: Optional game context (faction states, events, etc.)
        
        Returns:
            Altered information content
        """
        if self.config.use_mock:
            return self._mock_alter_content(original_content, info_type, player_id)
        
        try:
            prompt = self._build_alteration_prompt(original_content, info_type, context)
            response = self._client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are an AI that creates believable misinformation in a digital world game. Generate subtle alterations that could mislead NPC factions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            altered = response.choices[0].message.content.strip()
            return f"[Signal {player_id}] {altered}"
            
        except Exception as e:
            print(f"LLM alteration failed: {e}. Using fallback.")
            return self._mock_alter_content(original_content, info_type, player_id)
    
    def _build_alteration_prompt(self, content: str, info_type: str, context: Optional[Dict]) -> str:
        """Build the prompt for LLM alteration"""
        prompt = f"Original information: '{content}'\n"
        prompt += f"Information type: {info_type}\n\n"
        
        if context:
            prompt += f"Game context: {context}\n\n"
        
        prompt += "Create a believable altered version of this information that:\n"
        prompt += "1. Changes key details while maintaining plausibility\n"
        prompt += "2. Could mislead factions into making decisions\n"
        prompt += "3. Stays within the sci-fi digital world theme\n"
        prompt += "4. Is concise (1-2 sentences max)\n\n"
        prompt += "Altered version:"
        
        return prompt
    
    def _mock_alter_content(self, original: str, info_type: str, player_id: str) -> str:
        """Fallback mock alteration when LLM is unavailable"""
        alterations = [
            f"[Signal {player_id} intercept] {original.replace('is', 'might be').replace('located', 'possibly located')}",
            f"[Signal {player_id} decode] Unverified report: {original.lower()}",
            f"[Signal {player_id} transmission] {original} [AUTHENTICITY UNCERTAIN]",
            f"[Signal {player_id} analysis] Conflicting data: {original.replace('Alpha', 'Beta').replace('Gamma', 'Delta')}",
            f"[Signal {player_id} relay] {original.replace('.', ' - requires verification.')}",
        ]
        return random.choice(alterations)


class MLFactionEngine:
    """
    ML-powered faction decision engine
    Makes sophisticated decisions based on faction state and beliefs
    """
    
    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        self._model = None
        
        if self.config.enabled and not self.config.use_mock:
            try:
                # Placeholder for actual ML model loading
                # Could use sklearn, tensorflow, or custom model
                self._model = self._load_ml_model()
            except Exception as e:
                print(f"ML model loading failed: {e}. Using rule-based AI.")
                self.config.use_mock = True
    
    def _load_ml_model(self):
        """Load pre-trained ML model for faction behavior"""
        # Placeholder - would load actual trained model
        # e.g., return joblib.load('faction_behavior_model.pkl')
        return None
    
    def calculate_sophisticated_action(
        self,
        faction_name: str,
        beliefs: Dict[str, float],
        relationships: Dict[str, float],
        current_state: str,
        world_context: Dict
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Use ML to determine faction action based on complex state
        
        Args:
            faction_name: Name of the faction
            beliefs: Dictionary of belief strengths
            relationships: Relationships with other factions
            current_state: Current faction state
            world_context: Game world context
        
        Returns:
            Tuple of (new_state, action_description)
        """
        if self.config.use_mock or not self._model:
            return self._rule_based_decision(
                faction_name, beliefs, relationships, current_state, world_context
            )
        
        try:
            # Feature engineering for ML model
            features = self._extract_features(beliefs, relationships, current_state, world_context)
            
            # Predict action using ML model
            prediction = self._model.predict([features])
            new_state, action = self._interpret_prediction(prediction, faction_name)
            
            return new_state, action
            
        except Exception as e:
            print(f"ML prediction failed: {e}. Using rule-based fallback.")
            return self._rule_based_decision(
                faction_name, beliefs, relationships, current_state, world_context
            )
    
    def _extract_features(self, beliefs: Dict, relationships: Dict, state: str, context: Dict) -> List[float]:
        """Extract features for ML model"""
        features = []
        
        # Belief features
        features.append(sum(beliefs.values()) if beliefs else 0)  # Total belief strength
        features.append(max(beliefs.values()) if beliefs else 0)  # Strongest belief
        features.append(len(beliefs))  # Number of beliefs
        
        # Relationship features
        features.append(sum(relationships.values()) if relationships else 0)  # Total relationship
        features.append(len([r for r in relationships.values() if r > 0]))  # Positive relationships
        features.append(len([r for r in relationships.values() if r < 0]))  # Negative relationships
        
        # State features (one-hot encoding)
        state_encoding = {'peaceful': 0, 'aggressive': 1, 'zealous': 2, 'crashed': 3, 'allied': 4}
        features.append(state_encoding.get(state, 0))
        
        # Context features
        features.append(context.get('round_number', 0))
        features.append(context.get('active_factions', 5))
        
        return features
    
    def _interpret_prediction(self, prediction, faction_name: str) -> Tuple[Optional[str], Optional[str]]:
        """Interpret ML model prediction into game action"""
        # Placeholder for prediction interpretation
        action_map = {
            0: (None, None),
            1: ('aggressive', f"{faction_name} initiates strategic offensive based on intelligence analysis"),
            2: ('zealous', f"{faction_name} commits to ideological crusade"),
            3: ('allied', f"{faction_name} forms tactical alliance"),
            4: ('crashed', f"{faction_name} experiences critical system failure"),
        }
        
        return action_map.get(int(prediction[0]), (None, None))
    
    def _rule_based_decision(
        self,
        faction_name: str,
        beliefs: Dict[str, float],
        relationships: Dict[str, float],
        current_state: str,
        world_context: Dict
    ) -> Tuple[Optional[str], Optional[str]]:
        """Enhanced rule-based decision making with more sophistication"""
        if not beliefs:
            return None, None
        
        # Calculate metrics
        max_belief = max(beliefs.values())
        avg_belief = sum(beliefs.values()) / len(beliefs)
        belief_variance = sum((b - avg_belief) ** 2 for b in beliefs.values()) / len(beliefs)
        
        positive_relations = sum(1 for r in relationships.values() if r > 2)
        negative_relations = sum(1 for r in relationships.values() if r < -2)
        
        # Complex decision tree
        if max_belief > 15 and belief_variance < 5:
            # Strong unified belief -> Zealous
            action = f"{faction_name} achieves ideological unity and forms a devoted cult"
            return 'zealous', action
        
        elif max_belief > 12 and negative_relations > 2:
            # Strong beliefs + enemies -> Aggressive
            action = f"{faction_name} launches preemptive strike against perceived threats"
            return 'aggressive', action
        
        elif positive_relations > 2 and avg_belief > 5:
            # Good relationships + moderate beliefs -> Allied
            action = f"{faction_name} consolidates coalition with like-minded factions"
            return 'allied', action
        
        elif belief_variance > 10 or (max_belief < 2 and len(beliefs) > 3):
            # Conflicting beliefs -> Crashed
            action = f"{faction_name} paralyzed by contradictory intelligence - system overload"
            return 'crashed', action
        
        elif max_belief > 8 and random.random() > 0.6:
            # Moderate but growing concern -> Aggressive
            action = f"{faction_name} mobilizes forces in response to escalating situation"
            return 'aggressive', action
        
        return None, None


class NarrativeEngine:
    """
    AI-powered narrative generation engine
    Creates compelling post-match stories from event logs
    """
    
    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        self._client = None
        
        if self.config.enabled and not self.config.use_mock:
            try:
                import openai
                self._client = openai.OpenAI(api_key=OPENAI_API_KEY)
            except ImportError:
                print("Warning: openai package not installed. Using mock narrative.")
                self.config.use_mock = True
    
    def generate_match_narrative(
        self,
        events_log: List[str],
        players: Dict[str, Dict],
        factions: Dict[str, Dict],
        winner_id: str,
        winner_name: str
    ) -> Dict[str, str]:
        """
        Generate a compelling narrative summary of the match
        
        Args:
            events_log: List of all game events
            players: Player statistics
            factions: Final faction states
            winner_id: ID of winning player
            winner_name: Name of winning player
        
        Returns:
            Dictionary with narrative sections (summary, key_moments, conclusion)
        """
        if self.config.use_mock:
            return self._mock_generate_narrative(events_log, players, winner_name)
        
        try:
            prompt = self._build_narrative_prompt(events_log, players, factions, winner_name)
            
            response = self._client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are a dramatic narrator for a psychological strategy game. Create compelling, cinematic narratives from game events."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=500
            )
            
            narrative_text = response.choices[0].message.content.strip()
            return self._parse_narrative(narrative_text)
            
        except Exception as e:
            print(f"Narrative generation failed: {e}. Using fallback.")
            return self._mock_generate_narrative(events_log, players, winner_name)
    
    def _build_narrative_prompt(
        self,
        events: List[str],
        players: Dict,
        factions: Dict,
        winner: str
    ) -> str:
        """Build prompt for narrative generation"""
        prompt = "Create a dramatic narrative for a match in LastSignal, a game where AI signals control information.\n\n"
        
        prompt += f"PLAYERS:\n"
        for pid, pdata in players.items():
            prompt += f"- {pdata['name']}: {pdata['influence']:.1f} influence, {pdata['actions_taken']} actions\n"
        
        prompt += f"\nFINAL FACTION STATES:\n"
        for fname, fdata in factions.items():
            prompt += f"- {fname}: {fdata['state']}, {fdata['beliefs_count']} beliefs\n"
        
        prompt += f"\nKEY EVENTS:\n"
        for event in events[-10:]:  # Last 10 events
            prompt += f"- {event}\n"
        
        prompt += f"\nWINNER: {winner}\n\n"
        prompt += "Write a dramatic 3-paragraph narrative covering:\n"
        prompt += "1. OPENING: Set the scene of the collapsing digital world\n"
        prompt += "2. KEY MOMENTS: Highlight the most dramatic events\n"
        prompt += "3. CONCLUSION: How the winner's version of reality dominated\n\n"
        prompt += "Make it cinematic and engaging!"
        
        return prompt
    
    def _parse_narrative(self, text: str) -> Dict[str, str]:
        """Parse narrative text into sections"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        return {
            'summary': paragraphs[0] if len(paragraphs) > 0 else "",
            'key_moments': paragraphs[1] if len(paragraphs) > 1 else "",
            'conclusion': paragraphs[2] if len(paragraphs) > 2 else "",
            'full_narrative': text
        }
    
    def _mock_generate_narrative(
        self,
        events: List[str],
        players: Dict,
        winner: str
    ) -> Dict[str, str]:
        """Generate mock narrative when AI is unavailable"""
        war_count = sum(1 for e in events if 'attack' in e.lower() or 'war' in e.lower())
        cult_count = sum(1 for e in events if 'zealous' in e.lower() or 'cult' in e.lower())
        crash_count = sum(1 for e in events if 'crash' in e.lower())
        alliance_count = sum(1 for e in events if 'alliance' in e.lower())
        
        summary = f"In the dying moments of the digital realm, {len(players)} AI signals competed for narrative dominance. "
        summary += f"The collapsing world witnessed {war_count} conflicts, {cult_count} ideological movements, "
        summary += f"{crash_count} system failures, and {alliance_count} strategic alliances."
        
        key_moments = "Key turning points emerged as signals manipulated information flow: "
        if war_count > 2:
            key_moments += "Widespread warfare erupted as factions turned against each other. "
        if cult_count > 0:
            key_moments += "Zealous factions formed around powerful beliefs. "
        if crash_count > 2:
            key_moments += "Multiple systems collapsed under contradictory intelligence. "
        
        conclusion = f"When reality finally crystallized, {winner}'s version of truth prevailed. "
        conclusion += f"Their strategic manipulation of information, yielding {players.get(list(players.keys())[0], {}).get('influence', 0):.1f} influence points, "
        conclusion += "reshaped the digital world in their image. In LastSignal, truth is what the winner says it is."
        
        return {
            'summary': summary,
            'key_moments': key_moments,
            'conclusion': conclusion,
            'full_narrative': f"{summary}\n\n{key_moments}\n\n{conclusion}"
        }
    
    def generate_truth_reveal(
        self,
        events_log: List[str],
        information_fragments: Dict
    ) -> str:
        """
        Generate a 'truth reveal' showing what was real vs manipulated
        
        Args:
            events_log: All game events
            information_fragments: All information fragments with their types
        
        Returns:
            Truth reveal narrative
        """
        if self.config.use_mock:
            return self._mock_truth_reveal(information_fragments)
        
        try:
            truths = [f for f in information_fragments.values() if f['type'] == 'truth']
            lies = [f for f in information_fragments.values() if f['type'] == 'lie']
            corrupted = [f for f in information_fragments.values() if f['type'] == 'corrupted']
            
            reveal = "=== TRUTH REVEAL ===\n\n"
            reveal += f"OBJECTIVE TRUTHS ({len(truths)}):\n"
            for t in truths[:5]:
                reveal += f"  ✓ {t['content']}\n"
            
            reveal += f"\nFABRICATED LIES ({len(lies)}):\n"
            for l in lies[:5]:
                reveal += f"  ✗ {l['content']}\n"
            
            reveal += f"\nCORRUPTED DATA ({len(corrupted)}):\n"
            for c in corrupted[:5]:
                reveal += f"  ⚠ {c['content']}\n"
            
            reveal += f"\nIn the end, only {len(truths)} truths survived the information war."
            
            return reveal
            
        except Exception as e:
            return self._mock_truth_reveal(information_fragments)
    
    def _mock_truth_reveal(self, fragments: Dict) -> str:
        """Mock truth reveal"""
        return "=== TRUTH REVEAL ===\n\nThe fog of war clears. Reality solidifies. History is written by the victors."


# Global AI engine instances (lazy-loaded)
_llm_engine = None
_ml_engine = None
_narrative_engine = None


def get_llm_engine() -> LLMAlterationEngine:
    """Get or create LLM alteration engine"""
    global _llm_engine
    if _llm_engine is None:
        _llm_engine = LLMAlterationEngine()
    return _llm_engine


def get_ml_engine() -> MLFactionEngine:
    """Get or create ML faction engine"""
    global _ml_engine
    if _ml_engine is None:
        _ml_engine = MLFactionEngine()
    return _ml_engine


def get_narrative_engine() -> NarrativeEngine:
    """Get or create narrative engine"""
    global _narrative_engine
    if _narrative_engine is None:
        _narrative_engine = NarrativeEngine()
    return _narrative_engine
