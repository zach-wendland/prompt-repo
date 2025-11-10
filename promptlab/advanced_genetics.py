"""
Advanced Genetic Operations
Extends basic genetics with sophisticated algorithms
"""
import random
from typing import List, Tuple, Optional, Callable, Dict, Any
from datetime import datetime
import math

from .models import Prompt, PromptDNA, Gene, PromptCategory, PromptTier


class FitnessFunction:
    """
    Fitness function for evaluating prompt quality.

    Used in natural selection and optimization algorithms.
    """

    def __init__(self, weights: Optional[dict] = None):
        self.weights = weights or {
            'effectiveness_score': 0.4,
            'usage_count': 0.2,
            'gene_count': 0.1,
            'generation': -0.1,  # Prefer newer generations
            'complexity': 0.2
        }

    def calculate(self, prompt: Prompt) -> float:
        """Calculate fitness score (0-100)"""
        fitness = 0.0

        # Effectiveness score (0-100)
        fitness += prompt.effectiveness_score * self.weights['effectiveness_score']

        # Usage count (normalized)
        usage_norm = min(100, prompt.usage_count * 2)  # Cap at 50 uses = 100 score
        fitness += usage_norm * self.weights['usage_count']

        # Gene count (optimal around 5-10 genes)
        gene_count = len(prompt.dna.genes)
        gene_score = 100 - abs(gene_count - 7) * 10
        gene_score = max(0, gene_score)
        fitness += gene_score * self.weights['gene_count']

        # Generation (newer is better)
        gen_score = min(100, prompt.dna.generation * 10)
        fitness += gen_score * abs(self.weights['generation'])

        # Complexity (from analyzer)
        # This would be calculated by the analyzer
        complexity_score = 50  # Default moderate complexity
        fitness += complexity_score * self.weights['complexity']

        return min(100, max(0, fitness))


class AdvancedGeneticLab:
    """
    Advanced genetic operations beyond basic breeding.

    Implements:
    - Multi-parent breeding (3+ parents)
    - Natural selection
    - Tournament selection
    - Adaptive mutation
    - Gene pool management
    - Evolutionary strategies
    """

    def __init__(self, fitness_function: Optional[FitnessFunction] = None):
        self.fitness_function = fitness_function or FitnessFunction()
        self.generation_history = []
        self.elite_prompts = []

    def multi_parent_breeding(self,
                             parents: List[Prompt],
                             name: Optional[str] = None,
                             selection_method: str = 'best_of_each') -> Prompt:
        """
        Breed from 3 or more parents.

        Selection methods:
        - 'best_of_each': Take best gene of each type from all parents
        - 'weighted': Weight genes by parent fitness
        - 'random': Random selection from all parents
        - 'dominant_cascade': Dominant genes in order of parent fitness
        """
        if len(parents) < 2:
            raise ValueError("Need at least 2 parents")

        if name is None:
            name = f"MultiGen_{len(parents)}parents"

        # Collect all gene types
        all_gene_types = set()
        for parent in parents:
            for gene in parent.dna.genes:
                all_gene_types.add(gene.gene_type)

        offspring_genes = []

        for gene_type in all_gene_types:
            # Collect genes of this type from all parents
            candidates = []
            for parent in parents:
                parent_genes = parent.dna.get_genes_by_type(gene_type)
                if parent_genes:
                    candidates.extend([(g, parent) for g in parent_genes])

            if not candidates:
                continue

            # Select gene based on method
            if selection_method == 'best_of_each':
                # Take dominant genes first, then highest fitness parent
                dominant = [c for c in candidates if c[0].dominant]
                if dominant:
                    # Sort by parent fitness
                    dominant.sort(key=lambda x: self.fitness_function.calculate(x[1]), reverse=True)
                    selected_gene = dominant[0][0]
                else:
                    candidates.sort(key=lambda x: self.fitness_function.calculate(x[1]), reverse=True)
                    selected_gene = candidates[0][0]

            elif selection_method == 'weighted':
                # Weighted selection based on fitness
                fitnesses = [self.fitness_function.calculate(c[1]) for c in candidates]
                total_fitness = sum(fitnesses)
                if total_fitness > 0:
                    weights = [f / total_fitness for f in fitnesses]
                    selected = random.choices(candidates, weights=weights)[0]
                    selected_gene = selected[0]
                else:
                    selected_gene = random.choice(candidates)[0]

            elif selection_method == 'random':
                selected_gene = random.choice(candidates)[0]

            else:  # dominant_cascade
                # Order parents by fitness
                parents_fitness = [(p, self.fitness_function.calculate(p)) for p in parents]
                parents_fitness.sort(key=lambda x: x[1], reverse=True)

                selected_gene = None
                for parent, _ in parents_fitness:
                    parent_genes = parent.dna.get_genes_by_type(gene_type)
                    dominant_genes = [g for g in parent_genes if g.dominant]
                    if dominant_genes:
                        selected_gene = dominant_genes[0]
                        break

                if selected_gene is None:
                    selected_gene = candidates[0][0]

            offspring_genes.append(selected_gene)

        # Create offspring DNA
        max_generation = max(p.dna.generation for p in parents)
        offspring_dna = PromptDNA(
            genes=offspring_genes,
            generation=max_generation + 1,
            parents=[p.get_genome_id() for p in parents]
        )

        # Combine tags
        all_tags = set()
        for parent in parents:
            all_tags.update(parent.tags)

        # Combine model compatibility
        all_models = set()
        for parent in parents:
            all_models.update(parent.model_compatibility)

        # Create offspring
        # Determine tier (highest among parents)
        tier_order = {'free': 0, 'premium': 1, 'enterprise': 2}
        parent_tiers = [(p.tier, tier_order[p.tier.value]) for p in parents]
        best_tier = max(parent_tiers, key=lambda x: x[1])[0]

        offspring = Prompt(
            id=f"multi_{len(parents)}p_gen{offspring_dna.generation}",
            name=name,
            description=f"Multi-parent offspring from {len(parents)} parents",
            category=parents[0].category,
            tier=best_tier,
            dna=offspring_dna,
            tags=all_tags,
            model_compatibility=list(all_models),
            author="PromptLab Advanced Genetics",
            created=datetime.now()
        )

        return offspring

    def adaptive_mutation(self,
                         prompt: Prompt,
                         fitness_threshold: float = 50.0,
                         base_rate: float = 0.2) -> Prompt:
        """
        Mutation with adaptive rate based on fitness.

        High fitness prompts mutate less (already good).
        Low fitness prompts mutate more (need exploration).
        """
        fitness = self.fitness_function.calculate(prompt)

        # Calculate adaptive mutation rate
        if fitness >= fitness_threshold:
            # High fitness: lower mutation rate
            mutation_rate = base_rate * (1.0 - (fitness - fitness_threshold) / 50.0)
        else:
            # Low fitness: higher mutation rate
            mutation_rate = base_rate * (1.5 + (fitness_threshold - fitness) / 50.0)

        mutation_rate = max(0.05, min(0.8, mutation_rate))

        # Apply mutations
        mutant = prompt.clone()
        mutant.id = f"{prompt.id}_adaptive_m"
        mutant.name = f"{prompt.name} (Adaptive Mutant)"

        num_mutations = max(1, int(len(mutant.dna.genes) * mutation_rate))

        for _ in range(num_mutations):
            if mutant.dna.genes:
                gene_idx = random.randint(0, len(mutant.dna.genes) - 1)
                original_gene = mutant.dna.genes[gene_idx]
                mutated_gene = original_gene.mutate(mutation_rate)
                mutant.dna.genes[gene_idx] = mutated_gene

        mutant.dna.generation += 1
        mutant.updated = datetime.now()

        return mutant

    def tournament_selection(self,
                            population: List[Prompt],
                            tournament_size: int = 3,
                            num_winners: int = 1) -> List[Prompt]:
        """
        Select prompts using tournament selection.

        Randomly select tournament_size prompts and pick the best.
        """
        if len(population) < tournament_size:
            tournament_size = len(population)

        winners = []
        for _ in range(num_winners):
            tournament = random.sample(population, tournament_size)
            tournament_fitnesses = [(p, self.fitness_function.calculate(p)) for p in tournament]
            tournament_fitnesses.sort(key=lambda x: x[1], reverse=True)
            winners.append(tournament_fitnesses[0][0])

        return winners

    def natural_selection(self,
                         population: List[Prompt],
                         survival_rate: float = 0.3,
                         elite_count: int = 2) -> List[Prompt]:
        """
        Perform natural selection on a population.

        Keep top performers (elitism) plus random survivors.
        """
        if not population:
            return []

        # Calculate fitness for all
        pop_fitness = [(p, self.fitness_function.calculate(p)) for p in population]
        pop_fitness.sort(key=lambda x: x[1], reverse=True)

        # Elite survivors (always keep best)
        survivors = [p for p, _ in pop_fitness[:elite_count]]
        self.elite_prompts = survivors.copy()

        # Calculate how many more to keep
        remaining_slots = int(len(population) * survival_rate) - elite_count

        if remaining_slots > 0 and len(pop_fitness) > elite_count:
            # Fitness-proportional selection for remaining slots
            remaining_pop = pop_fitness[elite_count:]
            total_fitness = sum(f for _, f in remaining_pop)

            if total_fitness > 0:
                weights = [f / total_fitness for _, f in remaining_pop]
                selected = random.choices(
                    [p for p, _ in remaining_pop],
                    weights=weights,
                    k=remaining_slots
                )
                survivors.extend(selected)
            else:
                # If all fitness is 0, random selection
                survivors.extend(random.sample([p for p, _ in remaining_pop], min(remaining_slots, len(remaining_pop))))

        return survivors

    def evolve_population(self,
                         population: List[Prompt],
                         generations: int = 5,
                         mutation_rate: float = 0.2,
                         breeding_rate: float = 0.5,
                         elite_count: int = 2) -> List[Prompt]:
        """
        Evolve a population over multiple generations.

        Returns the final evolved population.
        """
        current_pop = population.copy()

        for gen in range(generations):
            # Natural selection
            survivors = self.natural_selection(current_pop, elite_count=elite_count)

            # Breeding phase
            offspring = []
            num_offspring = int(len(current_pop) * breeding_rate)

            for _ in range(num_offspring):
                # Tournament selection for parents
                parents = self.tournament_selection(survivors, tournament_size=3, num_winners=2)

                if len(parents) >= 2:
                    # Breed
                    from .genetics import GeneticLab
                    lab = GeneticLab(mutation_rate=0.0)  # We'll handle mutation separately
                    result = lab.breed(parents[0], parents[1])
                    offspring.append(result.offspring)

            # Mutation phase
            mutants = []
            num_mutants = int(len(current_pop) * mutation_rate)

            for _ in range(num_mutants):
                parent = random.choice(survivors)
                mutant = self.adaptive_mutation(parent)
                mutants.append(mutant)

            # Combine for next generation
            current_pop = survivors + offspring + mutants

            # Track generation
            self.generation_history.append({
                'generation': gen + 1,
                'population_size': len(current_pop),
                'avg_fitness': sum(self.fitness_function.calculate(p) for p in current_pop) / len(current_pop),
                'max_fitness': max(self.fitness_function.calculate(p) for p in current_pop),
                'elite': [p.id for p in self.elite_prompts]
            })

        return current_pop

    def find_optimal_prompt(self,
                           starting_prompts: List[Prompt],
                           target_fitness: float = 90.0,
                           max_generations: int = 20,
                           population_size: int = 20) -> Tuple[Prompt, int]:
        """
        Evolve prompts until target fitness is reached.

        Returns (best_prompt, generations_needed)
        """
        # Initialize population
        population = starting_prompts.copy()

        # Expand to population size if needed
        while len(population) < population_size:
            parent = random.choice(starting_prompts)
            mutant = self.adaptive_mutation(parent)
            population.append(mutant)

        for gen in range(max_generations):
            # Evolve one generation
            population = self.evolve_population(population, generations=1)

            # Check if target reached
            best_fitness = max(self.fitness_function.calculate(p) for p in population)

            if best_fitness >= target_fitness:
                # Found optimal prompt
                pop_fitness = [(p, self.fitness_function.calculate(p)) for p in population]
                pop_fitness.sort(key=lambda x: x[1], reverse=True)
                return pop_fitness[0][0], gen + 1

        # Return best after max generations
        pop_fitness = [(p, self.fitness_function.calculate(p)) for p in population]
        pop_fitness.sort(key=lambda x: x[1], reverse=True)
        return pop_fitness[0][0], max_generations

    def crossbreed_species(self,
                          species1: List[Prompt],
                          species2: List[Prompt],
                          hybrid_count: int = 5) -> List[Prompt]:
        """
        Create hybrids between two different species (categories) of prompts.

        Useful for combining domain expertise.
        """
        hybrids = []

        for _ in range(hybrid_count):
            parent1 = random.choice(species1)
            parent2 = random.choice(species2)

            # Multi-parent breeding with both
            hybrid = self.multi_parent_breeding(
                [parent1, parent2],
                name=f"{parent1.category.value}-{parent2.category.value} Hybrid",
                selection_method='weighted'
            )

            hybrids.append(hybrid)

        return hybrids

    def gene_pool_diversity(self, population: List[Prompt]) -> Dict[str, Any]:
        """
        Analyze genetic diversity of a population.

        Returns diversity metrics.
        """
        if not population:
            return {'error': 'Empty population'}

        all_genes = []
        all_gene_types = set()
        genome_hashes = set()

        for prompt in population:
            all_genes.extend(prompt.dna.genes)
            all_gene_types.update(g.gene_type for g in prompt.dna.genes)
            genome_hashes.add(prompt.dna.get_genome_hash())

        # Calculate diversity metrics
        diversity = {
            'population_size': len(population),
            'unique_genomes': len(genome_hashes),
            'total_genes': len(all_genes),
            'unique_gene_types': len(all_gene_types),
            'avg_genes_per_prompt': len(all_genes) / len(population),
            'genome_diversity_ratio': len(genome_hashes) / len(population),
            'gene_type_distribution': {}
        }

        # Gene type distribution
        from collections import Counter
        gene_type_counts = Counter(g.gene_type for g in all_genes)
        diversity['gene_type_distribution'] = dict(gene_type_counts)

        # Genetic entropy (Shannon entropy of gene types)
        total = sum(gene_type_counts.values())
        entropy = 0
        for count in gene_type_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        diversity['genetic_entropy'] = entropy

        return diversity

    def optimize_prompt_for_task(self,
                                 prompt: Prompt,
                                 task_description: str,
                                 fitness_evaluator: Optional[Callable] = None) -> Prompt:
        """
        Optimize a prompt for a specific task.

        Uses iterative mutation and selection.
        """
        current_best = prompt
        current_fitness = self.fitness_function.calculate(prompt)

        if fitness_evaluator:
            current_fitness = fitness_evaluator(prompt)

        attempts = 0
        max_attempts = 10
        no_improvement_count = 0

        while attempts < max_attempts and no_improvement_count < 3:
            # Generate variants
            variants = []
            for _ in range(5):
                variant = self.adaptive_mutation(current_best)
                variants.append(variant)

            # Evaluate variants
            for variant in variants:
                if fitness_evaluator:
                    variant_fitness = fitness_evaluator(variant)
                else:
                    variant_fitness = self.fitness_function.calculate(variant)

                if variant_fitness > current_fitness:
                    current_best = variant
                    current_fitness = variant_fitness
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1

            attempts += 1

        return current_best
