"""
Tests for storage and prompt library
"""
import pytest
import tempfile
import json
from pathlib import Path

from promptlab.storage import PromptLibrary
from promptlab.models import (
    Prompt, PromptDNA, Gene, PromptCategory, PromptTier
)


@pytest.fixture
def temp_lab():
    """Create a temporary lab directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield PromptLibrary(repo_path=tmpdir, lab_path=f"{tmpdir}/.promptlab")


@pytest.fixture
def sample_prompt():
    """Create a sample prompt"""
    dna = PromptDNA()
    dna.add_gene(Gene("sys", "You are helpful", "system", True))
    dna.add_gene(Gene("inst", "Do task", "instructions", True))

    return Prompt(
        id="sample",
        name="Sample Prompt",
        description="A sample prompt for testing",
        category=PromptCategory.SIMPLE,
        tier=PromptTier.FREE,
        dna=dna,
        tags={"test", "sample"},
        model_compatibility=["gpt-4"]
    )


class TestPromptLibrary:
    """Test PromptLibrary class"""

    def test_library_creation(self, temp_lab):
        """Test creating a prompt library"""
        assert temp_lab.prompts == {}
        assert temp_lab.lab_path.exists()

    def test_save_and_load_prompt(self, temp_lab, sample_prompt):
        """Test saving and loading a prompt"""
        # Save
        temp_lab.save_prompt(sample_prompt)

        # Verify file exists
        assert temp_lab.personal_genome_path.exists()

        # Create new library and load
        new_lab = PromptLibrary(
            repo_path=str(temp_lab.repo_path),
            lab_path=str(temp_lab.lab_path)
        )
        new_lab.load_personal_genome()

        # Should have the prompt
        loaded = new_lab.get_by_id("sample")
        assert loaded is not None
        assert loaded.name == sample_prompt.name
        assert loaded.description == sample_prompt.description

    def test_save_updates_existing(self, temp_lab, sample_prompt):
        """Test that saving updates existing prompt"""
        # Save once
        temp_lab.save_prompt(sample_prompt)

        # Modify and save again
        sample_prompt.description = "Updated description"
        temp_lab.save_prompt(sample_prompt)

        # Load and verify
        new_lab = PromptLibrary(
            repo_path=str(temp_lab.repo_path),
            lab_path=str(temp_lab.lab_path)
        )
        new_lab.load_personal_genome()

        loaded = new_lab.get_by_id("sample")
        assert loaded.description == "Updated description"

    def test_search_by_name(self, temp_lab, sample_prompt):
        """Test searching prompts by name"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        results = temp_lab.search(query="sample")

        assert len(results) == 1
        assert results[0].id == "sample"

    def test_search_by_description(self, temp_lab, sample_prompt):
        """Test searching prompts by description"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        results = temp_lab.search(query="sample prompt")

        assert len(results) >= 1
        assert any(r.id == "sample" for r in results)

    def test_search_by_tags(self, temp_lab, sample_prompt):
        """Test searching prompts by tags"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        results = temp_lab.search(query="test")

        assert len(results) >= 1
        assert any(r.id == "sample" for r in results)

    def test_search_with_category_filter(self, temp_lab, sample_prompt):
        """Test searching with category filter"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        # Create another prompt with different category
        dna = PromptDNA()
        dna.add_gene(Gene("g", "Test", "system", True))

        work_prompt = Prompt(
            id="work",
            name="Work Prompt",
            description="Work",
            category=PromptCategory.WORK,
            tier=PromptTier.PREMIUM,
            dna=dna
        )
        temp_lab.prompts[work_prompt.id] = work_prompt

        # Search for simple only
        results = temp_lab.search(category=PromptCategory.SIMPLE)

        assert len(results) == 1
        assert results[0].category == PromptCategory.SIMPLE

    def test_search_with_tier_filter(self, temp_lab, sample_prompt):
        """Test searching with tier filter"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        results = temp_lab.search(tier=PromptTier.FREE)

        assert len(results) >= 1
        assert all(r.tier == PromptTier.FREE for r in results)

    def test_search_with_tag_filter(self, temp_lab, sample_prompt):
        """Test searching with tag filter"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        results = temp_lab.search(tags=["test"])

        assert len(results) >= 1
        assert all("test" in r.tags for r in results)

    def test_search_no_results(self, temp_lab):
        """Test search with no results"""
        results = temp_lab.search(query="nonexistent")

        assert len(results) == 0

    def test_get_by_id(self, temp_lab, sample_prompt):
        """Test getting prompt by ID"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        prompt = temp_lab.get_by_id("sample")

        assert prompt is not None
        assert prompt.id == "sample"

    def test_get_by_id_not_found(self, temp_lab):
        """Test getting nonexistent prompt"""
        prompt = temp_lab.get_by_id("nonexistent")

        assert prompt is None

    def test_list_all(self, temp_lab, sample_prompt):
        """Test listing all prompts"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        # Add another
        dna = PromptDNA()
        dna.add_gene(Gene("g", "Test", "system", True))
        prompt2 = Prompt(
            id="second",
            name="Second",
            description="Second prompt",
            category=PromptCategory.SIMPLE,
            tier=PromptTier.FREE,
            dna=dna
        )
        temp_lab.prompts[prompt2.id] = prompt2

        all_prompts = temp_lab.list_all()

        assert len(all_prompts) == 2

    def test_get_stats(self, temp_lab, sample_prompt):
        """Test getting library statistics"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        stats = temp_lab.get_stats()

        assert stats["total_prompts"] == 1
        assert "simple" in stats["categories"]
        assert stats["categories"]["simple"] == 1
        assert "free" in stats["tiers"]
        assert stats["tiers"]["free"] == 1
        assert stats["total_genes"] == 2
        assert stats["avg_genes_per_prompt"] == 2.0

    def test_get_stats_empty(self, temp_lab):
        """Test stats with empty library"""
        stats = temp_lab.get_stats()

        assert stats["total_prompts"] == 0
        assert stats["total_genes"] == 0
        assert stats["avg_genes_per_prompt"] == 0

    def test_export_prompt(self, temp_lab, sample_prompt):
        """Test exporting a prompt to file"""
        temp_lab.prompts[sample_prompt.id] = sample_prompt

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            output_path = f.name

        try:
            temp_lab.export_prompt("sample", output_path)

            # Verify file was created
            assert Path(output_path).exists()

            # Verify content
            with open(output_path, 'r') as f:
                content = f.read()

            assert "Sample Prompt" in content
            assert "You are helpful" in content
            assert "Do task" in content
            assert "PromptLab" in content

        finally:
            Path(output_path).unlink()

    def test_export_nonexistent_prompt(self, temp_lab):
        """Test exporting nonexistent prompt raises error"""
        with pytest.raises(ValueError):
            temp_lab.export_prompt("nonexistent", "/tmp/test.md")


class TestPromptFileParsing:
    """Test parsing prompt files"""

    def test_parse_sections(self, temp_lab):
        """Test parsing markdown sections"""
        content = """
## Description
This is a description

## Instructions
Do this task

## Tips
Some tips here
        """

        sections = temp_lab._parse_sections(content)

        assert "Description" in sections
        assert "Instructions" in sections
        assert "Tips" in sections
        assert "description" in sections["Description"].lower()

    def test_parse_xml_sections(self, temp_lab):
        """Test parsing XML-style sections"""
        content = """
<System>
You are an AI
</System>

<Context>
Context here
</Context>
        """

        sections = temp_lab._parse_sections(content)

        assert "System" in sections
        assert "Context" in sections

    def test_parse_no_sections(self, temp_lab):
        """Test parsing content with no sections"""
        content = "Just plain text with no sections"

        sections = temp_lab._parse_sections(content)

        assert "Instructions" in sections
        assert "plain text" in sections["Instructions"]

    def test_parse_metadata(self, temp_lab):
        """Test parsing YAML frontmatter"""
        # Create a temp file with metadata
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("""---
version: 1.0.0
tier: free
tags: [test, sample]
---

## Description
Test prompt

## Instructions
Do something
""")
            f.flush()

            try:
                prompt = temp_lab._parse_prompt_file(
                    Path(f.name),
                    PromptCategory.SIMPLE
                )

                assert prompt is not None
                assert prompt.version == "1.0.0"
                assert prompt.tier == PromptTier.FREE
                assert "test" in prompt.tags
                assert "sample" in prompt.tags

            finally:
                Path(f.name).unlink()


class TestPersonalGenome:
    """Test personal genome persistence"""

    def test_personal_genome_file_created(self, temp_lab, sample_prompt):
        """Test that personal genome file is created"""
        temp_lab.save_prompt(sample_prompt)

        assert temp_lab.personal_genome_path.exists()

    def test_personal_genome_json_format(self, temp_lab, sample_prompt):
        """Test that personal genome is valid JSON"""
        temp_lab.save_prompt(sample_prompt)

        with open(temp_lab.personal_genome_path, 'r') as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == "sample"

    def test_personal_genome_preserves_data(self, temp_lab, sample_prompt):
        """Test that all prompt data is preserved"""
        temp_lab.save_prompt(sample_prompt)

        with open(temp_lab.personal_genome_path, 'r') as f:
            data = json.load(f)

        prompt_data = data[0]

        assert prompt_data["name"] == sample_prompt.name
        assert prompt_data["description"] == sample_prompt.description
        assert prompt_data["category"] == sample_prompt.category.value
        assert prompt_data["tier"] == sample_prompt.tier.value
        assert set(prompt_data["tags"]) == sample_prompt.tags
        assert len(prompt_data["dna"]["genes"]) == len(sample_prompt.dna.genes)


class TestRepositoryLoading:
    """Test loading prompts from repository"""

    def test_load_repository_prompts_empty_dir(self, temp_lab):
        """Test loading from empty directory"""
        temp_lab.load_repository_prompts()

        assert len(temp_lab.prompts) == 0

    def test_load_repository_prompts_with_files(self):
        """Test loading prompts from files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple directory with a prompt
            simple_dir = Path(tmpdir) / "simple"
            simple_dir.mkdir()

            # Write a simple prompt file
            prompt_file = simple_dir / "test-prompt.txt"
            prompt_file.write_text("""---
version: 1.0.0
tier: free
tags: [test]
---

## Description
Test prompt

## Instructions
Do something
""")

            # Load
            library = PromptLibrary(repo_path=tmpdir)
            library.load_repository_prompts()

            # Should have loaded the prompt
            assert len(library.prompts) >= 1
            assert "test-prompt" in library.prompts

            prompt = library.get_by_id("test-prompt")
            assert prompt is not None
            assert prompt.category == PromptCategory.SIMPLE
