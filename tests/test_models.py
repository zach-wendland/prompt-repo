"""
Tests for prompt models and genetic structures
"""
import pytest
from datetime import datetime

from promptlab.models import (
    Gene, PromptDNA, Prompt, PromptCategory, PromptTier, BreedingResult
)


class TestGene:
    """Test Gene class"""

    def test_gene_creation(self):
        """Test creating a gene"""
        gene = Gene(
            name="test_gene",
            sequence="This is a test instruction",
            gene_type="instructions",
            dominant=True
        )

        assert gene.name == "test_gene"
        assert gene.sequence == "This is a test instruction"
        assert gene.gene_type == "instructions"
        assert gene.dominant is True
        assert gene.mutations == 0

    def test_gene_mutation(self):
        """Test gene mutation"""
        gene = Gene("original", "Original sequence", "system", True)
        mutated = gene.mutate(strength=0.1)

        assert mutated.name == "original_m1"
        assert mutated.mutations == 1
        assert "VARIATION" in mutated.sequence
        assert gene.mutations == 0  # Original unchanged

    def test_multiple_mutations(self):
        """Test multiple successive mutations"""
        gene = Gene("test", "Test sequence", "context", True)

        mutant1 = gene.mutate()
        mutant2 = mutant1.mutate()
        mutant3 = mutant2.mutate()

        assert mutant1.mutations == 1
        assert mutant2.mutations == 2
        assert mutant3.mutations == 3


class TestPromptDNA:
    """Test PromptDNA class"""

    def test_dna_creation(self):
        """Test creating DNA"""
        dna = PromptDNA()

        assert dna.genes == []
        assert dna.generation == 1
        assert dna.parents == []

    def test_add_gene(self):
        """Test adding genes to DNA"""
        dna = PromptDNA()
        gene1 = Gene("gene1", "Sequence 1", "system", True)
        gene2 = Gene("gene2", "Sequence 2", "context", True)

        dna.add_gene(gene1)
        dna.add_gene(gene2)

        assert len(dna.genes) == 2
        assert dna.genes[0] == gene1
        assert dna.genes[1] == gene2

    def test_get_genes_by_type(self):
        """Test filtering genes by type"""
        dna = PromptDNA()
        dna.add_gene(Gene("g1", "seq1", "system", True))
        dna.add_gene(Gene("g2", "seq2", "context", True))
        dna.add_gene(Gene("g3", "seq3", "system", False))

        system_genes = dna.get_genes_by_type("system")
        context_genes = dna.get_genes_by_type("context")

        assert len(system_genes) == 2
        assert len(context_genes) == 1
        assert all(g.gene_type == "system" for g in system_genes)

    def test_express_dna(self):
        """Test expressing DNA as prompt text"""
        dna = PromptDNA()
        dna.add_gene(Gene("sys", "You are an AI", "system", True))
        dna.add_gene(Gene("ctx", "Context here", "context", True))
        dna.add_gene(Gene("inst", "Do this", "instructions", True))

        expressed = dna.express()

        assert "You are an AI" in expressed
        assert "Context here" in expressed
        assert "Do this" in expressed

    def test_genome_hash(self):
        """Test genome hash generation"""
        dna1 = PromptDNA()
        dna1.add_gene(Gene("g1", "sequence1", "system", True))

        dna2 = PromptDNA()
        dna2.add_gene(Gene("g2", "sequence1", "system", True))

        # Same sequence should give same hash
        assert dna1.get_genome_hash() == dna2.get_genome_hash()

    def test_genome_hash_different(self):
        """Test different sequences give different hashes"""
        dna1 = PromptDNA()
        dna1.add_gene(Gene("g1", "sequence1", "system", True))

        dna2 = PromptDNA()
        dna2.add_gene(Gene("g2", "sequence2", "system", True))

        assert dna1.get_genome_hash() != dna2.get_genome_hash()


class TestPrompt:
    """Test Prompt class"""

    def test_prompt_creation(self):
        """Test creating a prompt"""
        dna = PromptDNA()
        dna.add_gene(Gene("g1", "Test instruction", "instructions", True))

        prompt = Prompt(
            id="test_prompt",
            name="Test Prompt",
            description="A test prompt",
            category=PromptCategory.SIMPLE,
            tier=PromptTier.FREE,
            dna=dna,
            tags={"test", "sample"},
            model_compatibility=["gpt-4", "claude-3"]
        )

        assert prompt.id == "test_prompt"
        assert prompt.name == "Test Prompt"
        assert prompt.category == PromptCategory.SIMPLE
        assert prompt.tier == PromptTier.FREE
        assert len(prompt.tags) == 2
        assert "test" in prompt.tags

    def test_get_genome_id(self):
        """Test genome ID generation"""
        dna = PromptDNA()
        dna.add_gene(Gene("g1", "Sequence", "system", True))

        prompt = Prompt(
            id="test",
            name="Test",
            description="Test",
            category=PromptCategory.SIMPLE,
            tier=PromptTier.FREE,
            dna=dna
        )

        genome_id = prompt.get_genome_id()
        assert genome_id.startswith("test_")
        assert len(genome_id) > len("test_")

    def test_prompt_clone(self):
        """Test cloning a prompt"""
        dna = PromptDNA()
        dna.add_gene(Gene("g1", "Original", "system", True))

        original = Prompt(
            id="original",
            name="Original",
            description="Original prompt",
            category=PromptCategory.SIMPLE,
            tier=PromptTier.FREE,
            dna=dna
        )

        clone = original.clone()

        assert clone.id == "original_clone"
        assert clone.name == "Original (Clone)"
        assert clone.description == original.description
        assert len(clone.dna.genes) == len(original.dna.genes)
        assert clone.created > original.created

    def test_prompt_serialization(self):
        """Test prompt to_dict and from_dict"""
        dna = PromptDNA()
        dna.add_gene(Gene("g1", "Test", "system", True))

        original = Prompt(
            id="test",
            name="Test",
            description="Test prompt",
            category=PromptCategory.WORK,
            tier=PromptTier.PREMIUM,
            dna=dna,
            tags={"tag1", "tag2"}
        )

        # Serialize
        data = original.to_dict()

        assert data["id"] == "test"
        assert data["name"] == "Test"
        assert data["category"] == "work"
        assert data["tier"] == "premium"
        assert "tag1" in data["tags"]

        # Deserialize
        restored = Prompt.from_dict(data)

        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.category == original.category
        assert restored.tier == original.tier
        assert restored.tags == original.tags


class TestBreedingResult:
    """Test BreedingResult class"""

    def test_breeding_result_creation(self):
        """Test creating a breeding result"""
        dna = PromptDNA(generation=2, parents=["parent1", "parent2"])
        offspring = Prompt(
            id="offspring",
            name="Offspring",
            description="Test offspring",
            category=PromptCategory.SIMPLE,
            tier=PromptTier.FREE,
            dna=dna
        )

        result = BreedingResult(
            offspring=offspring,
            parent1_id="parent1",
            parent2_id="parent2",
            generation=2,
            inherited_traits={"system": "parent1", "context": "parent2"},
            novel_traits=["mutation1"]
        )

        assert result.offspring == offspring
        assert result.parent1_id == "parent1"
        assert result.generation == 2
        assert len(result.inherited_traits) == 2
        assert len(result.novel_traits) == 1

    def test_breeding_result_describe(self):
        """Test breeding result description"""
        dna = PromptDNA(generation=2)
        offspring = Prompt(
            id="off",
            name="Offspring",
            description="Test",
            category=PromptCategory.SIMPLE,
            tier=PromptTier.FREE,
            dna=dna
        )

        result = BreedingResult(
            offspring=offspring,
            parent1_id="p1",
            parent2_id="p2",
            generation=2,
            inherited_traits={"sys": "p1"},
            novel_traits=[]
        )

        description = result.describe()

        assert "Offspring" in description
        assert "Generation: 2" in description
        assert "p1" in description
        assert "p2" in description
