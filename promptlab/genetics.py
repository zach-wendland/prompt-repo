"""
Genetic Operations - Breed, mutate, and splice prompts
"""
import random
from typing import List, Tuple, Optional
from datetime import datetime

from .models import Prompt, PromptDNA, Gene, BreedingResult, PromptCategory, PromptTier


class GeneticLab:
    """
    The Genetic Lab handles all prompt genetic operations.

    Operations:
    - Breeding: Combine two prompts to create offspring
    - Mutation: Random variations of prompts
    - Splicing: Targeted gene insertion/deletion
    - Crossover: Exchange gene sequences between prompts
    """

    def __init__(self, mutation_rate: float = 0.1):
        self.mutation_rate = mutation_rate
        self.breeding_history = []

    def breed(self,
              parent1: Prompt,
              parent2: Prompt,
              name: Optional[str] = None,
              crossover_points: int = 1) -> BreedingResult:
        """
        Breed two prompts to create offspring.

        Uses genetic crossover to combine genes from both parents.
        Dominant genes have priority.
        """
        if name is None:
            name = f"{parent1.name[:10]}×{parent2.name[:10]}"

        # Create offspring DNA
        offspring_dna = PromptDNA(
            generation=max(parent1.dna.generation, parent2.dna.generation) + 1,
            parents=[parent1.get_genome_id(), parent2.get_genome_id()]
        )

        # Track inheritance
        inherited_traits = {}
        novel_traits = []

        # Perform crossover
        all_gene_types = set()
        for gene in parent1.dna.genes + parent2.dna.genes:
            all_gene_types.add(gene.gene_type)

        for gene_type in all_gene_types:
            p1_genes = parent1.dna.get_genes_by_type(gene_type)
            p2_genes = parent2.dna.get_genes_by_type(gene_type)

            # Mendelian genetics: dominant genes from both parents
            p1_dominant = [g for g in p1_genes if g.dominant]
            p2_dominant = [g for g in p2_genes if g.dominant]

            # If both have dominant genes, randomly choose
            if p1_dominant and p2_dominant:
                if random.random() > 0.5:
                    chosen_genes = p1_dominant
                    inherited_traits[gene_type] = parent1.id
                else:
                    chosen_genes = p2_dominant
                    inherited_traits[gene_type] = parent2.id
            elif p1_dominant:
                chosen_genes = p1_dominant
                inherited_traits[gene_type] = parent1.id
            elif p2_dominant:
                chosen_genes = p2_dominant
                inherited_traits[gene_type] = parent2.id
            else:
                # Both recessive, take from random parent
                if p1_genes and p2_genes:
                    chosen_genes = random.choice([p1_genes, p2_genes])
                    inherited_traits[gene_type] = random.choice([parent1.id, parent2.id])
                elif p1_genes:
                    chosen_genes = p1_genes
                    inherited_traits[gene_type] = parent1.id
                else:
                    chosen_genes = p2_genes
                    inherited_traits[gene_type] = parent2.id

            for gene in chosen_genes:
                offspring_dna.add_gene(gene)

        # Apply mutation
        if random.random() < self.mutation_rate:
            mutation_gene = random.choice(offspring_dna.genes)
            mutated = mutation_gene.mutate()
            offspring_dna.genes.append(mutated)
            novel_traits.append(f"Mutation: {mutated.name}")

        # Create offspring prompt
        offspring = Prompt(
            id=f"{parent1.id}_{parent2.id}_f{offspring_dna.generation}",
            name=name,
            description=f"Hybrid of {parent1.name} and {parent2.name}",
            category=parent1.category,  # Inherit from parent1
            tier=max(parent1.tier, parent2.tier, key=lambda t: ["free", "premium", "enterprise"].index(t.value)),
            dna=offspring_dna,
            tags=parent1.tags.union(parent2.tags),
            model_compatibility=list(set(parent1.model_compatibility + parent2.model_compatibility)),
            author="PromptLab Genetics",
            created=datetime.now()
        )

        result = BreedingResult(
            offspring=offspring,
            parent1_id=parent1.id,
            parent2_id=parent2.id,
            generation=offspring_dna.generation,
            inherited_traits=inherited_traits,
            novel_traits=novel_traits
        )

        self.breeding_history.append(result)
        return result

    def mutate(self, prompt: Prompt, mutation_strength: float = 0.2) -> Prompt:
        """
        Create a mutated version of a prompt.

        Mutations can:
        - Modify existing genes
        - Add random variations
        - Change gene dominance
        """
        mutant = prompt.clone()
        mutant.id = f"{prompt.id}_mutant"
        mutant.name = f"{prompt.name} (Mutant)"

        # Mutate random genes
        num_mutations = max(1, int(len(mutant.dna.genes) * mutation_strength))

        for _ in range(num_mutations):
            gene_idx = random.randint(0, len(mutant.dna.genes) - 1)
            original_gene = mutant.dna.genes[gene_idx]
            mutated_gene = original_gene.mutate(mutation_strength)
            mutant.dna.genes[gene_idx] = mutated_gene

        mutant.dna.generation += 1
        mutant.updated = datetime.now()

        return mutant

    def splice(self,
               target: Prompt,
               donor: Prompt,
               gene_types: List[str]) -> Prompt:
        """
        Splice specific genes from donor into target.

        This is like CRISPR gene editing - precise insertion.
        """
        spliced = target.clone()
        spliced.id = f"{target.id}_spliced"
        spliced.name = f"{target.name} (Enhanced)"

        # Remove target genes of specified types
        spliced.dna.genes = [
            g for g in spliced.dna.genes
            if g.gene_type not in gene_types
        ]

        # Add donor genes
        for gene_type in gene_types:
            donor_genes = donor.dna.get_genes_by_type(gene_type)
            for gene in donor_genes:
                spliced.dna.add_gene(gene)

        spliced.description = f"Spliced {target.name} with genes from {donor.name}"
        spliced.dna.parents.append(donor.get_genome_id())
        spliced.updated = datetime.now()

        return spliced

    def crossover(self,
                  parent1: Prompt,
                  parent2: Prompt,
                  split_ratio: float = 0.5) -> Tuple[Prompt, Prompt]:
        """
        Perform genetic crossover between two prompts.

        Creates two offspring by swapping gene sequences.
        """
        split_point = int(len(parent1.dna.genes) * split_ratio)

        # Offspring 1: First part from parent1, second from parent2
        off1_genes = parent1.dna.genes[:split_point] + parent2.dna.genes[split_point:]
        off1_dna = PromptDNA(
            genes=off1_genes,
            generation=max(parent1.dna.generation, parent2.dna.generation) + 1,
            parents=[parent1.get_genome_id(), parent2.get_genome_id()]
        )

        offspring1 = Prompt(
            id=f"{parent1.id}_x{parent2.id}_a",
            name=f"{parent1.name}↔{parent2.name} A",
            description=f"Crossover variant A",
            category=parent1.category,
            tier=parent1.tier,
            dna=off1_dna,
            tags=parent1.tags.union(parent2.tags),
            model_compatibility=list(set(parent1.model_compatibility + parent2.model_compatibility)),
            author="PromptLab Genetics"
        )

        # Offspring 2: First part from parent2, second from parent1
        off2_genes = parent2.dna.genes[:split_point] + parent1.dna.genes[split_point:]
        off2_dna = PromptDNA(
            genes=off2_genes,
            generation=max(parent1.dna.generation, parent2.dna.generation) + 1,
            parents=[parent1.get_genome_id(), parent2.get_genome_id()]
        )

        offspring2 = Prompt(
            id=f"{parent1.id}_x{parent2.id}_b",
            name=f"{parent1.name}↔{parent2.name} B",
            description=f"Crossover variant B",
            category=parent2.category,
            tier=parent2.tier,
            dna=off2_dna,
            tags=parent1.tags.union(parent2.tags),
            model_compatibility=list(set(parent1.model_compatibility + parent2.model_compatibility)),
            author="PromptLab Genetics"
        )

        return offspring1, offspring2

    def analyze_compatibility(self, prompt1: Prompt, prompt2: Prompt) -> dict:
        """
        Analyze genetic compatibility between two prompts.

        Returns compatibility score and shared traits.
        """
        # Check gene type overlap
        p1_gene_types = set(g.gene_type for g in prompt1.dna.genes)
        p2_gene_types = set(g.gene_type for g in prompt2.dna.genes)

        shared_types = p1_gene_types.intersection(p2_gene_types)
        unique_p1 = p1_gene_types - p2_gene_types
        unique_p2 = p2_gene_types - p1_gene_types

        # Calculate compatibility score
        total_types = len(p1_gene_types.union(p2_gene_types))
        shared_ratio = len(shared_types) / total_types if total_types > 0 else 0

        # Category and tier compatibility
        category_match = prompt1.category == prompt2.category
        tier_compatible = abs(
            ["free", "premium", "enterprise"].index(prompt1.tier.value) -
            ["free", "premium", "enterprise"].index(prompt2.tier.value)
        ) <= 1

        compatibility_score = (
            shared_ratio * 0.5 +
            (0.3 if category_match else 0) +
            (0.2 if tier_compatible else 0)
        )

        return {
            "compatibility_score": compatibility_score,
            "shared_gene_types": list(shared_types),
            "unique_to_parent1": list(unique_p1),
            "unique_to_parent2": list(unique_p2),
            "category_match": category_match,
            "tier_compatible": tier_compatible,
            "breeding_recommended": compatibility_score > 0.4
        }

    def get_breeding_history(self) -> List[BreedingResult]:
        """Get the full breeding history"""
        return self.breeding_history

    def visualize_lineage(self, prompt: Prompt, depth: int = 3) -> str:
        """
        Create an ASCII visualization of prompt lineage.
        """
        lines = [f"🧬 Lineage of: {prompt.name}"]
        lines.append(f"   Genome: {prompt.get_genome_id()}")
        lines.append(f"   Generation: {prompt.dna.generation}")
        lines.append("")

        if prompt.dna.parents:
            lines.append("   Parents:")
            for i, parent_id in enumerate(prompt.dna.parents, 1):
                lines.append(f"   {'├' if i < len(prompt.dna.parents) else '└'}── {parent_id}")

        lines.append("")
        lines.append(f"   Genes: {len(prompt.dna.genes)}")
        gene_types = {}
        for gene in prompt.dna.genes:
            gene_types[gene.gene_type] = gene_types.get(gene.gene_type, 0) + 1

        for gtype, count in gene_types.items():
            lines.append(f"   • {gtype}: {count}")

        return "\n".join(lines)
