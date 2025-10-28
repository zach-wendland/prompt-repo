"""
Prompt Models - Define the structure of genetic prompts
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
from enum import Enum
import hashlib
import json


class PromptTier(Enum):
    """Prompt access tiers"""
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class PromptCategory(Enum):
    """Prompt categories"""
    SIMPLE = "simple"
    WORK = "work"
    AGENTIC = "agentic"
    STOCKS = "stocks"
    FUN = "fun"


class Gene:
    """
    A Gene represents a distinct component of a prompt.

    Genes can be:
    - System instructions
    - Context blocks
    - Constraints
    - Output formats
    - Reasoning strategies
    """

    def __init__(self,
                 name: str,
                 sequence: str,
                 gene_type: str,
                 dominant: bool = True):
        self.name = name
        self.sequence = sequence  # The actual text
        self.gene_type = gene_type  # system, context, instruction, etc.
        self.dominant = dominant  # Dominant genes override recessive ones
        self.mutations = 0

    def mutate(self, strength: float = 0.1) -> 'Gene':
        """Create a mutated version of this gene"""
        # Simple mutation: add variation markers
        mutated_sequence = f"{self.sequence}\n\n[VARIATION {self.mutations + 1}]"
        mutated = Gene(
            name=f"{self.name}_m{self.mutations + 1}",
            sequence=mutated_sequence,
            gene_type=self.gene_type,
            dominant=self.dominant
        )
        mutated.mutations = self.mutations + 1
        return mutated

    def __repr__(self):
        return f"Gene({self.name}, type={self.gene_type}, dominant={self.dominant})"


@dataclass
class PromptDNA:
    """
    The genetic code of a prompt.

    DNA consists of multiple genes that define the prompt's behavior.
    """
    genes: List[Gene] = field(default_factory=list)
    generation: int = 1
    parents: List[str] = field(default_factory=list)  # Parent DNA IDs

    def add_gene(self, gene: Gene):
        """Add a gene to the DNA strand"""
        self.genes.append(gene)

    def get_genes_by_type(self, gene_type: str) -> List[Gene]:
        """Get all genes of a specific type"""
        return [g for g in self.genes if g.gene_type == gene_type]

    def express(self) -> str:
        """Express the DNA as a complete prompt (genotype -> phenotype)"""
        # Group genes by type and assemble in order
        gene_order = ["system", "context", "instructions", "constraints",
                     "output_format", "reasoning", "examples"]

        expressed = []
        for gene_type in gene_order:
            genes = self.get_genes_by_type(gene_type)
            if genes:
                # Dominant genes take precedence
                dominant_genes = [g for g in genes if g.dominant]
                active_genes = dominant_genes if dominant_genes else genes

                for gene in active_genes:
                    expressed.append(gene.sequence)

        return "\n\n".join(expressed)

    def get_genome_hash(self) -> str:
        """Get unique hash of this DNA (for tracking lineage)"""
        genome_str = "".join([g.sequence for g in self.genes])
        return hashlib.md5(genome_str.encode()).hexdigest()[:8]


@dataclass
class Prompt:
    """
    A Prompt is the full organism with metadata and DNA.
    """
    id: str
    name: str
    description: str
    category: PromptCategory
    tier: PromptTier
    dna: PromptDNA
    tags: Set[str] = field(default_factory=set)
    model_compatibility: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    created: datetime = field(default_factory=datetime.now)
    updated: datetime = field(default_factory=datetime.now)
    author: str = "unknown"
    usage_count: int = 0
    effectiveness_score: float = 0.0

    def get_genome_id(self) -> str:
        """Get the genetic identifier"""
        return f"{self.id}_{self.dna.get_genome_hash()}"

    def get_lineage(self) -> List[str]:
        """Get the full lineage (ancestry) of this prompt"""
        return self.dna.parents

    def clone(self) -> 'Prompt':
        """Create an exact clone of this prompt"""
        import copy
        clone = copy.deepcopy(self)
        clone.id = f"{self.id}_clone"
        clone.name = f"{self.name} (Clone)"
        clone.created = datetime.now()
        return clone

    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "tier": self.tier.value,
            "dna": {
                "genes": [
                    {
                        "name": g.name,
                        "sequence": g.sequence,
                        "gene_type": g.gene_type,
                        "dominant": g.dominant,
                        "mutations": g.mutations
                    }
                    for g in self.dna.genes
                ],
                "generation": self.dna.generation,
                "parents": self.dna.parents
            },
            "tags": list(self.tags),
            "model_compatibility": self.model_compatibility,
            "version": self.version,
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat(),
            "author": self.author,
            "usage_count": self.usage_count,
            "effectiveness_score": self.effectiveness_score
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Prompt':
        """Deserialize from dictionary"""
        dna = PromptDNA(
            genes=[
                Gene(
                    name=g["name"],
                    sequence=g["sequence"],
                    gene_type=g["gene_type"],
                    dominant=g["dominant"]
                )
                for g in data["dna"]["genes"]
            ],
            generation=data["dna"]["generation"],
            parents=data["dna"]["parents"]
        )

        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            category=PromptCategory(data["category"]),
            tier=PromptTier(data["tier"]),
            dna=dna,
            tags=set(data["tags"]),
            model_compatibility=data["model_compatibility"],
            version=data["version"],
            created=datetime.fromisoformat(data["created"]),
            updated=datetime.fromisoformat(data["updated"]),
            author=data["author"],
            usage_count=data["usage_count"],
            effectiveness_score=data["effectiveness_score"]
        )


@dataclass
class BreedingResult:
    """Result of breeding two prompts"""
    offspring: Prompt
    parent1_id: str
    parent2_id: str
    generation: int
    inherited_traits: Dict[str, str]  # trait_name -> parent_id
    novel_traits: List[str]  # New emergent traits

    def describe(self) -> str:
        """Describe the breeding outcome"""
        return f"""
🧬 New Prompt Generated!

Name: {self.offspring.name}
Generation: {self.generation}
Genome ID: {self.offspring.get_genome_id()}

Parents:
  - {self.parent1_id}
  - {self.parent2_id}

Inherited Traits: {len(self.inherited_traits)}
Novel Traits: {len(self.novel_traits)}

DNA Composition: {len(self.offspring.dna.genes)} genes
"""
