"""
Tests for prompt analyzer
"""
import pytest
from promptlab.analyzer import PromptAnalyzer


@pytest.fixture
def analyzer():
    """Create analyzer instance"""
    return PromptAnalyzer()


@pytest.fixture
def simple_prompt_text():
    """Simple prompt text"""
    return "You are a helpful assistant. Please answer the question."


@pytest.fixture
def complex_prompt_text():
    """Complex structured prompt"""
    return """
<System>
You are an expert data analyst with 10 years of experience in statistical analysis.
</System>

<Context>
The user needs help analyzing sales data for Q4 2024. The data includes transaction records,
customer segments, and regional performance metrics.
</Context>

<Instructions>
1. Review the dataset for any anomalies or outliers
2. Calculate key metrics: revenue, growth rate, customer acquisition cost
3. Identify the top 3 performing segments
4. Provide 2-3 actionable recommendations

Ensure your analysis is data-driven and specific.
</Instructions>

<Constraints>
- Do not speculate beyond what the data shows
- Maintain customer confidentiality
- Use industry-standard calculation methods
</Constraints>

<OutputFormat>
Provide results in this structure:
1. Executive Summary
2. Key Metrics (table format)
3. Top Insights (bullet points)
4. Recommendations
</OutputFormat>

<Example>
Input: Sales data for October
Output:
## Executive Summary
Q4 sales reached $2.3M, representing 15% YoY growth...
</Example>
    """


class TestPromptAnalyzer:
    """Test PromptAnalyzer class"""

    def test_analyzer_creation(self, analyzer):
        """Test analyzer can be created"""
        assert analyzer is not None

    def test_analyze_simple_prompt(self, analyzer, simple_prompt_text):
        """Test analyzing a simple prompt"""
        analysis = analyzer.analyze_comprehensive(simple_prompt_text)

        assert 'text_stats' in analysis
        assert 'structure' in analysis
        assert 'clarity' in analysis
        assert 'complexity' in analysis
        assert 'quality_score' in analysis

    def test_analyze_complex_prompt(self, analyzer, complex_prompt_text):
        """Test analyzing a complex prompt"""
        analysis = analyzer.analyze_comprehensive(complex_prompt_text)

        assert analysis['quality_score'] > 0
        assert analysis['structure']['has_sections']
        assert len(analysis['structure']['xml_tags']) > 0

    def test_text_stats(self, analyzer, simple_prompt_text):
        """Test text statistics"""
        analysis = analyzer.analyze_comprehensive(simple_prompt_text)
        stats = analysis['text_stats']

        assert stats['word_count'] > 0
        assert stats['sentence_count'] > 0
        assert stats['char_count'] > 0

    def test_structure_detection(self, analyzer, complex_prompt_text):
        """Test structure detection"""
        analysis = analyzer.analyze_comprehensive(complex_prompt_text)
        structure = analysis['structure']

        assert structure['has_sections']
        assert 'System' in structure['xml_tags']
        assert 'Context' in structure['xml_tags']
        assert structure['has_examples']
        assert structure['has_constraints']

    def test_clarity_analysis(self, analyzer, complex_prompt_text):
        """Test clarity analysis"""
        analysis = analyzer.analyze_comprehensive(complex_prompt_text)
        clarity = analysis['clarity']

        assert 'clarity_score' in clarity
        assert 'readability_score' in clarity
        assert 'positive_indicators' in clarity

    def test_complexity_calculation(self, analyzer, complex_prompt_text):
        """Test complexity calculation"""
        analysis = analyzer.analyze_comprehensive(complex_prompt_text)
        complexity = analysis['complexity']

        assert 'structural_complexity' in complexity
        assert 'linguistic_complexity' in complexity
        assert 'overall_complexity' in complexity

    def test_recommendations_generated(self, analyzer, simple_prompt_text):
        """Test that recommendations are generated"""
        analysis = analyzer.analyze_comprehensive(simple_prompt_text)

        assert 'recommendations' in analysis
        assert isinstance(analysis['recommendations'], list)

    def test_strengths_identified(self, analyzer, complex_prompt_text):
        """Test strength identification"""
        analysis = analyzer.analyze_comprehensive(complex_prompt_text)

        assert 'strengths' in analysis
        assert len(analysis['strengths']) > 0

    def test_weaknesses_identified(self, analyzer, simple_prompt_text):
        """Test weakness identification"""
        analysis = analyzer.analyze_comprehensive(simple_prompt_text)

        assert 'weaknesses' in analysis

    def test_compare_prompts(self, analyzer, simple_prompt_text, complex_prompt_text):
        """Test comparing two prompts"""
        comparison = analyzer.compare_prompts(simple_prompt_text, complex_prompt_text)

        assert 'prompt1' in comparison
        assert 'prompt2' in comparison
        assert 'winner' in comparison
        assert 'differences' in comparison

    def test_suggest_improvements(self, analyzer, simple_prompt_text):
        """Test improvement suggestions"""
        improvements = analyzer.suggest_improvements(simple_prompt_text)

        assert isinstance(improvements, list)
        # Simple prompt should have suggestions
        assert len(improvements) > 0

    def test_quality_score_range(self, analyzer, simple_prompt_text):
        """Test quality score is in valid range"""
        analysis = analyzer.analyze_comprehensive(simple_prompt_text)

        assert 0 <= analysis['quality_score'] <= 100

    def test_high_quality_prompt_score(self, analyzer, complex_prompt_text):
        """Test that well-structured prompt gets high score"""
        analysis = analyzer.analyze_comprehensive(complex_prompt_text)

        # Complex structured prompt should score reasonably high
        assert analysis['quality_score'] >= 50
