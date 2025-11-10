"""
Tests for advanced genetics
"""
import pytest
from promptlab.advanced_genetics import AdvancedGeneticLab, FitnessFunction
from promptlab.models import Prompt, PromptDNA, Gene, PromptCategory, PromptTier


@pytest.fixture
def test_prompts():
    """Create test prompts"""
    prompts = []

    for i in range(5):
        dna = PromptDNA()
        dna.add_gene(Gene(f"sys{i}", f"System {i}", "system", True))
        dna.add_gene(Gene(f"ctx{i}", f"Context {i}", "context", i < 3))

        prompt = Prompt(
            id=f"test_{i}",
            name=f"Test Prompt {i}",
            description=f"Test prompt number {i}",
            category=PromptCategory.SIMPLE,
            tier=PromptTier.FREE,
            dna=dna,
            effectiveness_score=50.0 + i * 10,
            usage_count=i * 5
        )
        prompts.append(prompt)

    return prompts


@pytest.fixture
def advanced_lab():
    """Create advanced lab"""
    return AdvancedGeneticLab()


class TestFitnessFunction:
    """Test FitnessFunction class"""

    def test_fitness_calculation(self, test_prompts):
        """Test fitness calculation"""
        fitness_fn = FitnessFunction()
        prompt = test_prompts[0]

        fitness = fitness_fn.calculate(prompt)

        assert isinstance(fitness, float)
        assert 0 <= fitness <= 100

    def test_custom_weights(self, test_prompts):
        """Test custom fitness weights"""
        fitness_fn = FitnessFunction(weights={
            'effectiveness_score': 1.0,
            'usage_count': 0.0,
            'gene_count': 0.0,
            'generation': 0.0,
            'complexity': 0.0
        })

        prompt = test_prompts[0]
        prompt.effectiveness_score = 80.0

        fitness = fitness_fn.calculate(prompt)

        # Should be heavily weighted towards effectiveness
        assert fitness > 70


class TestAdvancedGeneticLab:
    """Test AdvancedGeneticLab class"""

    def test_lab_creation(self, advanced_lab):
        """Test creating advanced lab"""
        assert advanced_lab is not None
        assert advanced_lab.fitness_function is not None

    def test_multi_parent_breeding(self, advanced_lab, test_prompts):
        """Test breeding with multiple parents"""
        parents = test_prompts[:3]

        offspring = advanced_lab.multi_parent_breeding(parents)

        assert offspring is not None
        assert offspring.dna.generation == max(p.dna.generation for p in parents) + 1
        assert len(offspring.dna.parents) == 3

    def test_multi_parent_with_two_parents(self, advanced_lab, test_prompts):
        """Test multi-parent breeding with just 2 parents"""
        parents = test_prompts[:2]

        offspring = advanced_lab.multi_parent_breeding(parents)

        assert offspring is not None

    def test_multi_parent_selection_methods(self, advanced_lab, test_prompts):
        """Test different selection methods"""
        parents = test_prompts[:3]

        methods = ['best_of_each', 'weighted', 'random', 'dominant_cascade']

        for method in methods:
            offspring = advanced_lab.multi_parent_breeding(
                parents,
                selection_method=method
            )
            assert offspring is not None

    def test_adaptive_mutation(self, advanced_lab, test_prompts):
        """Test adaptive mutation"""
        prompt = test_prompts[0]

        mutant = advanced_lab.adaptive_mutation(prompt)

        assert mutant is not None
        assert mutant.id != prompt.id
        assert "adaptive" in mutant.id.lower()

    def test_adaptive_mutation_high_fitness(self, advanced_lab, test_prompts):
        """Test adaptive mutation on high fitness prompt"""
        prompt = test_prompts[0]
        prompt.effectiveness_score = 95.0

        mutant = advanced_lab.adaptive_mutation(prompt, fitness_threshold=50.0)

        assert mutant is not None
        # High fitness should have lower mutation rate

    def test_tournament_selection(self, advanced_lab, test_prompts):
        """Test tournament selection"""
        winners = advanced_lab.tournament_selection(
            test_prompts,
            tournament_size=3,
            num_winners=2
        )

        assert len(winners) == 2
        assert all(w in test_prompts for w in winners)

    def test_natural_selection(self, advanced_lab, test_prompts):
        """Test natural selection"""
        survivors = advanced_lab.natural_selection(
            test_prompts,
            survival_rate=0.4,
            elite_count=2
        )

        assert len(survivors) > 0
        assert len(survivors) <= len(test_prompts)
        # Elite should be preserved
        assert len(advanced_lab.elite_prompts) == 2

    def test_evolve_population(self, advanced_lab, test_prompts):
        """Test evolving a population"""
        evolved = advanced_lab.evolve_population(
            test_prompts,
            generations=3,
            mutation_rate=0.2,
            breeding_rate=0.5,
            elite_count=1
        )

        assert len(evolved) > 0
        # Should have generation history
        assert len(advanced_lab.generation_history) == 3

    def test_find_optimal_prompt(self, advanced_lab, test_prompts):
        """Test finding optimal prompt"""
        best, generations = advanced_lab.find_optimal_prompt(
            test_prompts,
            target_fitness=60.0,
            max_generations=5,
            population_size=10
        )

        assert best is not None
        assert isinstance(generations, int)
        assert generations <= 5

    def test_crossbreed_species(self, advanced_lab, test_prompts):
        """Test crossbreeding different species"""
        species1 = test_prompts[:2]
        species2 = test_prompts[2:4]

        hybrids = advanced_lab.crossbreed_species(species1, species2, hybrid_count=3)

        assert len(hybrids) == 3
        assert all(h.dna.generation > 1 for h in hybrids)

    def test_gene_pool_diversity(self, advanced_lab, test_prompts):
        """Test gene pool diversity analysis"""
        diversity = advanced_lab.gene_pool_diversity(test_prompts)

        assert 'population_size' in diversity
        assert 'unique_genomes' in diversity
        assert 'genome_diversity_ratio' in diversity
        assert 'genetic_entropy' in diversity

    def test_gene_pool_diversity_empty(self, advanced_lab):
        """Test diversity analysis on empty population"""
        diversity = advanced_lab.gene_pool_diversity([])

        assert 'error' in diversity

    def test_optimize_prompt_for_task(self, advanced_lab, test_prompts):
        """Test optimizing prompt for task"""
        prompt = test_prompts[0]

        optimized = advanced_lab.optimize_prompt_for_task(
            prompt,
            task_description="Analyze data effectively"
        )

        assert optimized is not None
        # Should be same or better
        assert advanced_lab.fitness_function.calculate(optimized) >= \
               advanced_lab.fitness_function.calculate(prompt) * 0.9
