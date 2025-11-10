"""
AI-Powered Prompt Analyzer

Analyzes prompt quality, complexity, and effectiveness using various metrics.
"""
import re
from typing import Dict, List, Tuple, Any
from collections import Counter
import math


class PromptAnalyzer:
    """
    Advanced prompt analysis using NLP and heuristics.

    Analyzes:
    - Complexity
    - Clarity
    - Structure quality
    - Token efficiency
    - Semantic coherence
    """

    def __init__(self):
        # Common stop words for filtering
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }

        # Quality indicators
        self.positive_indicators = [
            'specific', 'clear', 'detailed', 'step-by-step', 'example',
            'context', 'format', 'structure', 'output', 'constraint',
            'requirement', 'criteria', 'guideline', 'instruction'
        ]

        self.negative_indicators = [
            'maybe', 'perhaps', 'somehow', 'something', 'anything', 'whatever',
            'vague', 'unclear', 'confusing', 'ambiguous'
        ]

    def analyze_comprehensive(self, prompt_text: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a prompt.

        Returns detailed metrics and recommendations.
        """
        analysis = {
            'text_stats': self._analyze_text_stats(prompt_text),
            'structure': self._analyze_structure(prompt_text),
            'clarity': self._analyze_clarity(prompt_text),
            'complexity': self._calculate_complexity(prompt_text),
            'quality_score': 0.0,
            'recommendations': [],
            'strengths': [],
            'weaknesses': []
        }

        # Calculate overall quality score
        analysis['quality_score'] = self._calculate_quality_score(analysis)

        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis, prompt_text)

        # Identify strengths
        analysis['strengths'] = self._identify_strengths(analysis, prompt_text)

        # Identify weaknesses
        analysis['weaknesses'] = self._identify_weaknesses(analysis, prompt_text)

        return analysis

    def _analyze_text_stats(self, text: str) -> Dict[str, Any]:
        """Basic text statistics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chars = len(text)
        words_count = len(words)
        sentences_count = len(sentences)

        return {
            'char_count': chars,
            'word_count': words_count,
            'sentence_count': sentences_count,
            'avg_word_length': chars / words_count if words_count > 0 else 0,
            'avg_sentence_length': words_count / sentences_count if sentences_count > 0 else 0,
            'estimated_tokens': self._estimate_tokens(text)
        }

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Rough estimate: 1 token ≈ 4 characters for English
        return len(text) // 4

    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze prompt structure"""
        structure = {
            'has_sections': False,
            'sections': [],
            'has_examples': False,
            'has_constraints': False,
            'has_output_format': False,
            'xml_tags': [],
            'markdown_headers': []
        }

        # Check for XML-style tags
        xml_tags = re.findall(r'<(\w+)>', text)
        structure['xml_tags'] = list(set(xml_tags))

        # Check for markdown headers
        markdown_headers = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
        structure['markdown_headers'] = markdown_headers

        structure['has_sections'] = len(xml_tags) > 0 or len(markdown_headers) > 0

        # Check for examples
        structure['has_examples'] = bool(re.search(r'\b(example|instance|for example|e\.g\.)\b', text, re.IGNORECASE))

        # Check for constraints
        structure['has_constraints'] = bool(re.search(r'\b(constraint|limitation|must not|should not|never)\b', text, re.IGNORECASE))

        # Check for output format
        structure['has_output_format'] = bool(re.search(r'\b(output|format|structure|response)\b', text, re.IGNORECASE))

        return structure

    def _analyze_clarity(self, text: str) -> Dict[str, Any]:
        """Analyze clarity metrics"""
        clarity = {
            'readability_score': 0.0,
            'positive_indicators': 0,
            'negative_indicators': 0,
            'imperative_verbs': 0,
            'question_density': 0.0,
            'clarity_score': 0.0
        }

        # Flesch Reading Ease approximation
        words = text.split()
        sentences = len(re.split(r'[.!?]+', text))
        syllables = sum(self._count_syllables(word) for word in words)

        if sentences > 0 and len(words) > 0:
            avg_sentence_length = len(words) / sentences
            avg_syllables_per_word = syllables / len(words)

            # Flesch Reading Ease
            clarity['readability_score'] = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word

        # Count positive/negative indicators
        text_lower = text.lower()
        clarity['positive_indicators'] = sum(1 for indicator in self.positive_indicators if indicator in text_lower)
        clarity['negative_indicators'] = sum(1 for indicator in self.negative_indicators if indicator in text_lower)

        # Count imperative verbs (action words)
        imperative_pattern = r'\b(do|use|create|write|analyze|generate|provide|ensure|include|exclude|avoid|focus|consider|remember)\b'
        clarity['imperative_verbs'] = len(re.findall(imperative_pattern, text_lower))

        # Question density
        questions = len(re.findall(r'\?', text))
        clarity['question_density'] = questions / len(words) * 100 if len(words) > 0 else 0

        # Overall clarity score (0-100)
        clarity_score = 0
        clarity_score += min(clarity['readability_score'] / 2, 30)  # Max 30 points
        clarity_score += min(clarity['positive_indicators'] * 5, 25)  # Max 25 points
        clarity_score -= clarity['negative_indicators'] * 5  # Penalty
        clarity_score += min(clarity['imperative_verbs'] * 3, 20)  # Max 20 points
        clarity_score += 15 if 0 < clarity['question_density'] < 5 else 0  # Questions are good in moderation
        clarity_score += 10  # Base score

        clarity['clarity_score'] = max(0, min(100, clarity_score))

        return clarity

    def _count_syllables(self, word: str) -> int:
        """Rough syllable count"""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e'):
            syllable_count -= 1

        return max(1, syllable_count)

    def _calculate_complexity(self, text: str) -> Dict[str, Any]:
        """Calculate prompt complexity"""
        complexity = {
            'structural_complexity': 0,
            'linguistic_complexity': 0,
            'logical_complexity': 0,
            'overall_complexity': 0
        }

        # Structural complexity (sections, nesting)
        sections = len(re.findall(r'<\w+>|^#+\s+', text, re.MULTILINE))
        nesting_depth = text.count('<')  # Simple approximation
        complexity['structural_complexity'] = min(100, (sections * 10 + nesting_depth * 5))

        # Linguistic complexity (vocabulary richness)
        words = [w.lower() for w in re.findall(r'\b\w+\b', text) if w.lower() not in self.stop_words]
        unique_words = len(set(words))
        total_words = len(words)
        lexical_diversity = unique_words / total_words if total_words > 0 else 0

        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0

        complexity['linguistic_complexity'] = min(100, (
            lexical_diversity * 50 +
            (avg_word_length - 4) * 10
        ))

        # Logical complexity (conditionals, lists, numbers)
        conditionals = len(re.findall(r'\b(if|when|unless|while|until|whether)\b', text, re.IGNORECASE))
        lists = len(re.findall(r'^\s*[-*\d]+\.?\s+', text, re.MULTILINE))
        numbers = len(re.findall(r'\b\d+\b', text))

        complexity['logical_complexity'] = min(100, (
            conditionals * 10 +
            lists * 5 +
            numbers * 3
        ))

        # Overall complexity
        complexity['overall_complexity'] = (
            complexity['structural_complexity'] * 0.3 +
            complexity['linguistic_complexity'] * 0.4 +
            complexity['logical_complexity'] * 0.3
        )

        return complexity

    def _calculate_quality_score(self, analysis: Dict) -> float:
        """Calculate overall quality score (0-100)"""
        score = 0.0

        # Clarity contribution (40%)
        score += analysis['clarity']['clarity_score'] * 0.4

        # Structure contribution (30%)
        structure = analysis['structure']
        structure_score = 0
        structure_score += 20 if structure['has_sections'] else 0
        structure_score += 15 if structure['has_examples'] else 0
        structure_score += 10 if structure['has_constraints'] else 0
        structure_score += 15 if structure['has_output_format'] else 0
        structure_score += len(structure['xml_tags']) * 5
        structure_score += len(structure['markdown_headers']) * 3

        score += min(100, structure_score) * 0.3

        # Complexity contribution (20%) - moderate complexity is best
        complexity = analysis['complexity']['overall_complexity']
        # Ideal complexity is around 50
        complexity_score = 100 - abs(complexity - 50)
        score += complexity_score * 0.2

        # Text stats contribution (10%)
        text_stats = analysis['text_stats']
        stats_score = 0
        # Ideal word count is 100-500
        if 100 <= text_stats['word_count'] <= 500:
            stats_score += 50
        # Ideal avg sentence length is 15-25 words
        if 15 <= text_stats['avg_sentence_length'] <= 25:
            stats_score += 50

        score += stats_score * 0.1

        return min(100, max(0, score))

    def _generate_recommendations(self, analysis: Dict, text: str) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []

        # Structure recommendations
        structure = analysis['structure']
        if not structure['has_sections']:
            recommendations.append("Add clear sections (using ## headers or <Tags>) to organize your prompt")

        if not structure['has_examples']:
            recommendations.append("Include examples to clarify expected outputs")

        if not structure['has_constraints']:
            recommendations.append("Define clear constraints and limitations")

        if not structure['has_output_format']:
            recommendations.append("Specify the desired output format explicitly")

        # Clarity recommendations
        clarity = analysis['clarity']
        if clarity['clarity_score'] < 60:
            recommendations.append("Improve clarity by using more specific and directive language")

        if clarity['negative_indicators'] > 2:
            recommendations.append("Remove vague or ambiguous language")

        if clarity['imperative_verbs'] < 3:
            recommendations.append("Use more action verbs to give clear instructions")

        # Complexity recommendations
        complexity = analysis['complexity']['overall_complexity']
        if complexity < 30:
            recommendations.append("Add more detail and structure to make the prompt more comprehensive")
        elif complexity > 70:
            recommendations.append("Simplify the prompt - it may be too complex")

        # Length recommendations
        word_count = analysis['text_stats']['word_count']
        if word_count < 50:
            recommendations.append("Expand the prompt with more context and details (aim for 100-500 words)")
        elif word_count > 1000:
            recommendations.append("Consider breaking this into multiple focused prompts")

        return recommendations

    def _identify_strengths(self, analysis: Dict, text: str) -> List[str]:
        """Identify prompt strengths"""
        strengths = []

        if analysis['quality_score'] >= 80:
            strengths.append("Excellent overall quality")

        if analysis['structure']['has_sections']:
            strengths.append("Well-structured with clear sections")

        if analysis['structure']['has_examples']:
            strengths.append("Includes helpful examples")

        if analysis['clarity']['clarity_score'] >= 70:
            strengths.append("Clear and easy to understand")

        if analysis['clarity']['positive_indicators'] >= 5:
            strengths.append("Uses quality indicator words effectively")

        if 40 <= analysis['complexity']['overall_complexity'] <= 60:
            strengths.append("Optimal complexity level")

        if analysis['text_stats']['word_count'] >= 100:
            strengths.append("Adequate detail and context")

        return strengths

    def _identify_weaknesses(self, analysis: Dict, text: str) -> List[str]:
        """Identify prompt weaknesses"""
        weaknesses = []

        if analysis['quality_score'] < 50:
            weaknesses.append("Low overall quality score - needs significant improvement")

        if not analysis['structure']['has_sections']:
            weaknesses.append("Lacks clear structure")

        if analysis['clarity']['negative_indicators'] > 2:
            weaknesses.append("Contains vague or ambiguous language")

        if analysis['clarity']['imperative_verbs'] == 0:
            weaknesses.append("No clear action verbs or instructions")

        if analysis['complexity']['overall_complexity'] < 20:
            weaknesses.append("Too simple - lacks necessary detail")
        elif analysis['complexity']['overall_complexity'] > 80:
            weaknesses.append("Overly complex - may confuse the AI")

        if analysis['text_stats']['word_count'] < 30:
            weaknesses.append("Too brief - needs more context")

        return weaknesses

    def compare_prompts(self, prompt1_text: str, prompt2_text: str) -> Dict[str, Any]:
        """Compare two prompts side by side"""
        analysis1 = self.analyze_comprehensive(prompt1_text)
        analysis2 = self.analyze_comprehensive(prompt2_text)

        comparison = {
            'prompt1': analysis1,
            'prompt2': analysis2,
            'winner': None,
            'differences': {},
            'recommendation': ""
        }

        # Determine winner
        if analysis1['quality_score'] > analysis2['quality_score'] * 1.1:
            comparison['winner'] = 'prompt1'
        elif analysis2['quality_score'] > analysis1['quality_score'] * 1.1:
            comparison['winner'] = 'prompt2'
        else:
            comparison['winner'] = 'tie'

        # Calculate differences
        comparison['differences'] = {
            'quality_score_diff': analysis1['quality_score'] - analysis2['quality_score'],
            'word_count_diff': analysis1['text_stats']['word_count'] - analysis2['text_stats']['word_count'],
            'complexity_diff': analysis1['complexity']['overall_complexity'] - analysis2['complexity']['overall_complexity'],
            'clarity_diff': analysis1['clarity']['clarity_score'] - analysis2['clarity']['clarity_score']
        }

        # Generate recommendation
        if comparison['winner'] == 'prompt1':
            comparison['recommendation'] = "Prompt 1 is significantly better overall"
        elif comparison['winner'] == 'prompt2':
            comparison['recommendation'] = "Prompt 2 is significantly better overall"
        else:
            comparison['recommendation'] = "Both prompts are comparable - consider combining their strengths"

        return comparison

    def suggest_improvements(self, text: str) -> List[Tuple[str, str]]:
        """Suggest specific text improvements"""
        improvements = []

        # Check for common issues
        if not re.search(r'\b(you are|act as|role)\b', text, re.IGNORECASE):
            improvements.append((
                "Add role definition",
                "Consider starting with: 'You are an expert...' or 'Act as...'"
            ))

        if not re.search(r'\b(context|background|scenario)\b', text, re.IGNORECASE):
            improvements.append((
                "Add context",
                "Provide background information with: '<Context>...</Context>'"
            ))

        if text.count('\n') < 3:
            improvements.append((
                "Add line breaks",
                "Break up the text with paragraphs for better readability"
            ))

        if not re.search(r'\b(example|instance)\b', text, re.IGNORECASE):
            improvements.append((
                "Add examples",
                "Include 1-2 examples: '<Example>...</Example>'"
            ))

        if len(re.findall(r'\?', text)) == 0 and len(text.split()) > 50:
            improvements.append((
                "Consider questions",
                "Add clarifying questions if the task is complex"
            ))

        return improvements
