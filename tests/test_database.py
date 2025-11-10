"""
Tests for database module
"""
import pytest
import tempfile
from pathlib import Path

from promptlab.database import PromptDatabase
from promptlab.models import Prompt, PromptDNA, Gene, PromptCategory, PromptTier


@pytest.fixture
def temp_db():
    """Create a temporary database"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = PromptDatabase(str(db_path))
        yield db


@pytest.fixture
def sample_prompt():
    """Create a sample prompt"""
    dna = PromptDNA()
    dna.add_gene(Gene("sys", "You are helpful", "system", True))
    dna.add_gene(Gene("inst", "Do task", "instructions", True))

    return Prompt(
        id="test_prompt",
        name="Test Prompt",
        description="A test prompt",
        category=PromptCategory.SIMPLE,
        tier=PromptTier.FREE,
        dna=dna,
        tags={"test", "sample"},
        model_compatibility=["gpt-4"]
    )


class TestPromptDatabase:
    """Test PromptDatabase class"""

    def test_database_initialization(self, temp_db):
        """Test database is initialized properly"""
        assert temp_db.db_path.exists()

    def test_save_prompt(self, temp_db, sample_prompt):
        """Test saving a prompt"""
        result = temp_db.save_prompt(sample_prompt)
        assert result is True

    def test_get_prompt(self, temp_db, sample_prompt):
        """Test retrieving a prompt"""
        temp_db.save_prompt(sample_prompt)
        retrieved = temp_db.get_prompt("test_prompt")

        assert retrieved is not None
        assert retrieved.id == sample_prompt.id
        assert retrieved.name == sample_prompt.name

    def test_get_nonexistent_prompt(self, temp_db):
        """Test retrieving nonexistent prompt returns None"""
        result = temp_db.get_prompt("nonexistent")
        assert result is None

    def test_search_by_category(self, temp_db, sample_prompt):
        """Test searching by category"""
        temp_db.save_prompt(sample_prompt)
        results = temp_db.search(category=PromptCategory.SIMPLE)

        assert len(results) >= 1
        assert any(p.id == "test_prompt" for p in results)

    def test_search_by_tier(self, temp_db, sample_prompt):
        """Test searching by tier"""
        temp_db.save_prompt(sample_prompt)
        results = temp_db.search(tier=PromptTier.FREE)

        assert len(results) >= 1

    def test_search_by_tags(self, temp_db, sample_prompt):
        """Test searching by tags"""
        temp_db.save_prompt(sample_prompt)
        results = temp_db.search(tags=["test"])

        assert len(results) >= 1

    def test_increment_usage(self, temp_db, sample_prompt):
        """Test incrementing usage count"""
        temp_db.save_prompt(sample_prompt)
        temp_db.increment_usage("test_prompt")

        retrieved = temp_db.get_prompt("test_prompt")
        assert retrieved.usage_count == 1

    def test_log_effectiveness(self, temp_db, sample_prompt):
        """Test logging effectiveness"""
        temp_db.save_prompt(sample_prompt)
        temp_db.log_effectiveness("test_prompt", "gpt-4", 85.5, 1500, 250, "Great results")

        # Check that effectiveness was logged
        retrieved = temp_db.get_prompt("test_prompt")
        assert retrieved.effectiveness_score > 0

    def test_get_statistics(self, temp_db, sample_prompt):
        """Test getting statistics"""
        temp_db.save_prompt(sample_prompt)
        stats = temp_db.get_statistics()

        assert stats['total_prompts'] >= 1
        assert 'by_category' in stats
        assert 'by_tier' in stats

    def test_log_event(self, temp_db):
        """Test logging events"""
        temp_db.log_event("test_event", "test_prompt", {"key": "value"})
        # If no exception, test passes

    def test_update_prompt(self, temp_db, sample_prompt):
        """Test updating an existing prompt"""
        temp_db.save_prompt(sample_prompt)

        sample_prompt.description = "Updated description"
        temp_db.save_prompt(sample_prompt)

        retrieved = temp_db.get_prompt("test_prompt")
        assert retrieved.description == "Updated description"
