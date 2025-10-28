"""
Tests for genetic operations
"""
import pytest
from promptlab.genetics import GeneticLab
from promptlab.models import (
    Prompt, PromptDNA, Gene, PromptCategory, PromptTier
)


@pytest.fixture
def simple_prompt1():
    """Create a simple test prompt"""
    dna = PromptDNA()
    dna.add_gene(Gene("sys1", "You are helpful", "system", True))
    dna.add_gene(Gene("ctx1", "Context A", "context", True))
    dna.add_gene(Gene("inst1", "Do task A", "instructions", True))

    return Prompt(
        id="prompt1",
        name="Prompt 1",
        description="Test prompt 1",
        category=PromptCategory.SIMPLE,
        tier=PromptTier.FREE,
        dna=dna,
        model_compatibility=["gpt-4"]
    )


@pytest.fixture
def simple_prompt2():
    """Create another simple test prompt"""
    dna = PromptDNA()
    dna.add_gene(Gene("sys2", "You are an expert", "system", True))
    dna.add_gene(Gene("ctx2", "Context B", "context", False))
    dna.add_gene(Gene("inst2", "Do task B", "instructions", True))

    return Prompt(
        id="prompt2",
        name="Prompt 2",
        description="Test prompt 2",
        category=PromptCategory.SIMPLE,
        tier=PromptTier.FREE,
        dna=dna,
        model_compatibility=["claude-3"]
    )


class TestGeneticLab:
    """Test GeneticLab class"""

    def test_lab_creation(self):
        """Test creating a genetic lab"""
        lab = GeneticLab(mutation_rate=0.2)

        assert lab.mutation_rate == 0.2
        assert lab.breeding_history == []

    def test_breed_prompts(self, simple_prompt1, simple_prompt2):
        """Test breeding two prompts"""
        lab = GeneticLab(mutation_rate=0.0)  # No mutation for predictable test

        result = lab.breed(simple_prompt1, simple_prompt2, name="Offspring")

        assert result.offspring.name == "Offspring"
        # Parent IDs should contain the prompt ID
        assert simple_prompt1.id in result.parent1_id
        assert simple_prompt2.id in result.parent2_id
        assert result.generation == 2  # Both parents are gen 1
        assert len(result.offspring.dna.genes) >= 3  # Should have genes from both

    def test_breed_dominant_genes(self, simple_prompt1, simple_prompt2):
        """Test that dominant genes are preferred"""
        lab = GeneticLab(mutation_rate=0.0)

        result = lab.breed(simple_prompt1, simple_prompt2)

        # Check that system gene (dominant in both) is present
        system_genes = result.offspring.dna.get_genes_by_type("system")
        assert len(system_genes) >= 1

    def test_breed_increases_generation(self, simple_prompt1, simple_prompt2):
        """Test that breeding increases generation"""
        lab = GeneticLab()

        result = lab.breed(simple_prompt1, simple_prompt2)

        assert result.offspring.dna.generation == 2
        assert simple_prompt1.dna.generation == 1
        assert simple_prompt2.dna.generation == 1

    def test_breed_combines_tags(self, simple_prompt1, simple_prompt2):
        """Test that breeding combines tags from parents"""
        simple_prompt1.tags = {"tag1", "tag2"}
        simple_prompt2.tags = {"tag2", "tag3"}

        lab = GeneticLab()
        result = lab.breed(simple_prompt1, simple_prompt2)

        assert "tag1" in result.offspring.tags
        assert "tag2" in result.offspring.tags
        assert "tag3" in result.offspring.tags

    def test_breed_combines_model_compatibility(self, simple_prompt1, simple_prompt2):
        """Test that breeding combines model compatibility"""
        lab = GeneticLab()
        result = lab.breed(simple_prompt1, simple_prompt2)

        assert "gpt-4" in result.offspring.model_compatibility
        assert "claude-3" in result.offspring.model_compatibility

    def test_breeding_history_tracked(self, simple_prompt1, simple_prompt2):
        """Test that breeding history is tracked"""
        lab = GeneticLab()

        assert len(lab.breeding_history) == 0

        lab.breed(simple_prompt1, simple_prompt2)

        assert len(lab.breeding_history) == 1
        assert simple_prompt1.id in lab.breeding_history[0].parent1_id

    def test_mutate_prompt(self, simple_prompt1):
        """Test mutating a prompt"""
        lab = GeneticLab()

        mutant = lab.mutate(simple_prompt1, mutation_strength=0.5)

        assert mutant.id == f"{simple_prompt1.id}_mutant"
        assert "Mutant" in mutant.name
        assert len(mutant.dna.genes) == len(simple_prompt1.dna.genes)
        assert mutant.dna.generation == 2

    def test_mutate_changes_genes(self, simple_prompt1):
        """Test that mutation actually changes genes"""
        lab = GeneticLab()

        mutant = lab.mutate(simple_prompt1, mutation_strength=0.3)

        # At least one gene should have mutations
        mutations = sum(g.mutations for g in mutant.dna.genes)
        assert mutations > 0

    def test_splice_genes(self, simple_prompt1, simple_prompt2):
        """Test splicing genes between prompts"""
        lab = GeneticLab()

        # Splice system gene from prompt2 into prompt1
        spliced = lab.splice(simple_prompt1, simple_prompt2, ["system"])

        # Should have system gene from prompt2
        system_genes = spliced.dna.get_genes_by_type("system")
        assert len(system_genes) > 0

        # Should still have other genes from prompt1
        context_genes = spliced.dna.get_genes_by_type("context")
        assert len(context_genes) > 0

    def test_splice_multiple_gene_types(self, simple_prompt1, simple_prompt2):
        """Test splicing multiple gene types"""
        lab = GeneticLab()

        spliced = lab.splice(simple_prompt1, simple_prompt2, ["system", "context"])

        # Should have replaced genes
        assert len(spliced.dna.genes) >= 2

    def test_crossover(self, simple_prompt1, simple_prompt2):
        """Test genetic crossover"""
        lab = GeneticLab()

        offspring1, offspring2 = lab.crossover(simple_prompt1, simple_prompt2, split_ratio=0.5)

        # Both offspring should exist
        assert offspring1 is not None
        assert offspring2 is not None

        # Should have genes
        assert len(offspring1.dna.genes) > 0
        assert len(offspring2.dna.genes) > 0

        # Should be generation 2
        assert offspring1.dna.generation == 2
        assert offspring2.dna.generation == 2

    def test_crossover_creates_different_offspring(self, simple_prompt1, simple_prompt2):
        """Test that crossover creates two different offspring"""
        lab = GeneticLab()

        offspring1, offspring2 = lab.crossover(simple_prompt1, simple_prompt2)

        # Should have different IDs
        assert offspring1.id != offspring2.id

        # May have different gene compositions (depending on split)
        assert offspring1.get_genome_id() != offspring2.get_genome_id()

    def test_analyze_compatibility_same_category(self, simple_prompt1, simple_prompt2):
        """Test compatibility analysis for same category"""
        lab = GeneticLab()

        compat = lab.analyze_compatibility(simple_prompt1, simple_prompt2)

        assert "compatibility_score" in compat
        assert 0 <= compat["compatibility_score"] <= 1
        assert compat["category_match"] is True  # Both SIMPLE

    def test_analyze_compatibility_different_category(self, simple_prompt1):
        """Test compatibility analysis for different categories"""
        # Create a different category prompt
        dna = PromptDNA()
        dna.add_gene(Gene("g", "Test", "system", True))

        work_prompt = Prompt(
            id="work",
            name="Work",
            description="Work prompt",
            category=PromptCategory.WORK,
            tier=PromptTier.PREMIUM,
            dna=dna
        )

        lab = GeneticLab()
        compat = lab.analyze_compatibility(simple_prompt1, work_prompt)

        assert compat["category_match"] is False

    def test_compatibility_score_calculation(self, simple_prompt1, simple_prompt2):
        """Test that compatibility score is calculated correctly"""
        lab = GeneticLab()

        compat = lab.analyze_compatibility(simple_prompt1, simple_prompt2)

        assert isinstance(compat["compatibility_score"], float)
        assert "shared_gene_types" in compat
        assert "unique_to_parent1" in compat
        assert "unique_to_parent2" in compat
        assert "breeding_recommended" in compat

    def test_visualize_lineage(self, simple_prompt1):
        """Test lineage visualization"""
        lab = GeneticLab()

        lineage = lab.visualize_lineage(simple_prompt1)

        assert "Lineage" in lineage
        assert simple_prompt1.name in lineage
        assert "Genome" in lineage
        assert "Generation" in lineage

    def test_visualize_lineage_with_parents(self, simple_prompt1, simple_prompt2):
        """Test lineage visualization for bred prompt"""
        lab = GeneticLab()

        result = lab.breed(simple_prompt1, simple_prompt2)
        lineage = lab.visualize_lineage(result.offspring)

        assert "Parents:" in lineage
        # Should show parent genome IDs

    def test_get_breeding_history(self, simple_prompt1, simple_prompt2):
        """Test retrieving breeding history"""
        lab = GeneticLab()

        lab.breed(simple_prompt1, simple_prompt2)
        lab.breed(simple_prompt1, simple_prompt2, name="Second")

        history = lab.get_breeding_history()

        assert len(history) == 2
        assert history[0].offspring.name != history[1].offspring.name


class TestBreedingEdgeCases:
    """Test edge cases in breeding"""

    def test_breed_with_no_overlapping_genes(self):
        """Test breeding prompts with completely different gene types"""
        dna1 = PromptDNA()
        dna1.add_gene(Gene("g1", "Gene 1", "system", True))

        dna2 = PromptDNA()
        dna2.add_gene(Gene("g2", "Gene 2", "context", True))

        prompt1 = Prompt(
            id="p1", name="P1", description="Test",
            category=PromptCategory.SIMPLE, tier=PromptTier.FREE, dna=dna1
        )
        prompt2 = Prompt(
            id="p2", name="P2", description="Test",
            category=PromptCategory.SIMPLE, tier=PromptTier.FREE, dna=dna2
        )

        lab = GeneticLab(mutation_rate=0.0)
        result = lab.breed(prompt1, prompt2)

        # Should have genes from both
        assert len(result.offspring.dna.genes) >= 2

    def test_breed_with_empty_dna(self):
        """Test breeding prompts with minimal DNA"""
        dna1 = PromptDNA()
        dna1.add_gene(Gene("g1", "Only gene", "system", True))

        dna2 = PromptDNA()
        dna2.add_gene(Gene("g2", "Another gene", "system", True))

        prompt1 = Prompt(
            id="p1", name="P1", description="Test",
            category=PromptCategory.SIMPLE, tier=PromptTier.FREE, dna=dna1
        )
        prompt2 = Prompt(
            id="p2", name="P2", description="Test",
            category=PromptCategory.SIMPLE, tier=PromptTier.FREE, dna=dna2
        )

        lab = GeneticLab()
        result = lab.breed(prompt1, prompt2)

        assert result.offspring is not None
        assert len(result.offspring.dna.genes) >= 1

    def test_mutation_with_zero_strength(self, simple_prompt1):
        """Test mutation with zero strength"""
        lab = GeneticLab()

        mutant = lab.mutate(simple_prompt1, mutation_strength=0.0)

        # Should still create mutant but with no actual mutations
        assert mutant.id != simple_prompt1.id

    def test_splice_nonexistent_gene_type(self, simple_prompt1, simple_prompt2):
        """Test splicing gene type that doesn't exist in donor"""
        lab = GeneticLab()

        spliced = lab.splice(simple_prompt1, simple_prompt2, ["nonexistent_type"])

        # Should still create spliced prompt
        assert spliced is not None
