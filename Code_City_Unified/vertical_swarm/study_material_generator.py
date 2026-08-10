#!/usr/bin/env python3
"""
Vertical AI Study Material Generator
Transforms documents into learning resources
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict

class StudyMaterialGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def generate_summary(self, documents: List[str], length: str = "medium") -> str:
        """Generate executive summary of documents"""
        
        length_prompts = {
            "short": "1-2 paragraphs, key takeaways only",
            "medium": "3-5 paragraphs, main themes and supporting details",
            "long": "Comprehensive summary with examples and context"
        }
        
        prompt = f"""You are a study material expert. Create a {length_prompts[length]} summary of these documents.

Focus on:
- Main themes and arguments
- Key facts and data points
- Important concepts to understand
- Connections between ideas

Documents:
{self._format_docs(documents)}

Provide a clear, well-structured summary suitable for studying."""

        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_qa_pairs(self, documents: List[str], count: int = 20) -> List[Dict]:
        """Generate Q&A pairs for self-testing"""
        
        prompt = f"""You are creating study questions from these documents.

Generate {count} question-answer pairs that:
- Cover key concepts and facts
- Range from basic recall to deeper understanding
- Include "why" and "how" questions, not just "what"
- Are answerable from the documents provided

Format each as JSON:
{{"question": "...", "answer": "...", "difficulty": "easy|medium|hard"}}

Documents:
{self._format_docs(documents)}

Return ONLY a JSON array of Q&A pairs, no other text."""

        response = self.model.generate_content(prompt)
        
        # Parse JSON response
        try:
            qa_pairs = json.loads(response.text)
            return qa_pairs
        except:
            # Fallback if JSON parsing fails
            return self._parse_qa_fallback(response.text)
    
    def generate_concept_map(self, documents: List[str]) -> Dict:
        """Generate hierarchical concept map"""
        
        prompt = f"""Analyze these documents and create a concept map showing relationships between ideas.

Structure as JSON:
{{
  "main_topic": "...",
  "key_concepts": [
    {{
      "name": "Concept 1",
      "description": "...",
      "related_to": ["Concept 2", "Concept 3"],
      "importance": "high|medium|low"
    }}
  ],
  "connections": [
    {{"from": "Concept 1", "to": "Concept 2", "relationship": "causes/supports/contradicts"}}
  ]
}}

Documents:
{self._format_docs(documents)}

Return ONLY valid JSON."""

        response = self.model.generate_content(prompt)
        return json.loads(response.text)
    
    def generate_timeline(self, documents: List[str]) -> List[Dict]:
        """Extract chronological events/developments"""
        
        prompt = f"""Extract any chronological information from these documents into a timeline.

Format as JSON array:
[
  {{"date": "YYYY-MM-DD or description", "event": "...", "significance": "..."}},
  ...
]

If no dates are explicit, infer sequence from context (use descriptions like "early phase", "later development").

Documents:
{self._format_docs(documents)}

Return ONLY JSON array."""

        response = self.model.generate_content(prompt)
        return json.loads(response.text)
    
    def generate_flashcards(self, documents: List[str], count: int = 30) -> List[Dict]:
        """Generate Anki-style flashcards"""
        
        prompt = f"""Create {count} flashcards for spaced repetition learning.

Format as JSON:
[
  {{
    "front": "Question or prompt",
    "back": "Answer or explanation",
    "tags": ["topic1", "topic2"],
    "difficulty": 1-5
  }}
]

Make cards atomic (one concept per card) and clear.

Documents:
{self._format_docs(documents)}

Return ONLY JSON array."""

        response = self.model.generate_content(prompt)
        return json.loads(response.text)
    
    def _format_docs(self, documents: List[str]) -> str:
        """Format documents for prompt"""
        formatted = ""
        for i, doc in enumerate(documents, 1):
            formatted += f"\n--- Document {i} ---\n{doc}\n"
        return formatted
    
    def _parse_qa_fallback(self, text: str) -> List[Dict]:
        """Fallback parser if JSON fails"""
        # Simple heuristic parsing
        qa_pairs = []
        lines = text.split('\n')
        current_q = None
        
        for line in lines:
            if line.startswith('Q:') or line.startswith('Question:'):
                current_q = line.split(':', 1)[1].strip()
            elif line.startswith('A:') or line.startswith('Answer:'):
                if current_q:
                    qa_pairs.append({
                        "question": current_q,
                        "answer": line.split(':', 1)[1].strip(),
                        "difficulty": "medium"
                    })
                    current_q = None
        
        return qa_pairs


# Integration with Vertical AI
def create_study_package(documents: List[str], output_dir: str = "./study_materials"):
    """Generate complete study package from documents"""
    
    generator = StudyMaterialGenerator(api_key="YOUR_API_KEY")
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("Generating study materials...")
    
    # 1. Summary
    print("  - Creating summary...")
    summary = generator.generate_summary(documents, length="medium")
    (output_path / "summary.md").write_text(summary)
    
    # 2. Q&A pairs
    print("  - Generating Q&A pairs...")
    qa_pairs = generator.generate_qa_pairs(documents, count=25)
    (output_path / "qa_pairs.json").write_text(json.dumps(qa_pairs, indent=2))
    
    # 3. Flashcards
    print("  - Creating flashcards...")
    flashcards = generator.generate_flashcards(documents, count=40)
    (output_path / "flashcards.json").write_text(json.dumps(flashcards, indent=2))
    
    # 4. Concept map
    print("  - Building concept map...")
    concept_map = generator.generate_concept_map(documents)
    (output_path / "concept_map.json").write_text(json.dumps(concept_map, indent=2))
    
    # 5. Timeline (if applicable)
    print("  - Extracting timeline...")
    timeline = generator.generate_timeline(documents)
    (output_path / "timeline.json").write_text(json.dumps(timeline, indent=2))
    
    print(f"\n✓ Study materials created in {output_dir}/")
    return output_path