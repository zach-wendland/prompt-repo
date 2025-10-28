"""
Storage and Persistence for Prompts
"""
import json
import os
from pathlib import Path
from typing import List, Optional, Dict
import re

from .models import Prompt, PromptDNA, Gene, PromptCategory, PromptTier


class PromptLibrary:
    """
    Manages the prompt library storage and retrieval.

    Supports:
    - Loading prompts from repository files
    - Saving custom/generated prompts
    - Searching and filtering
    - Personal genome (user's saved prompts)
    """

    def __init__(self, repo_path: str = ".", lab_path: str = ".promptlab"):
        self.repo_path = Path(repo_path)
        self.lab_path = Path(lab_path)
        self.lab_path.mkdir(exist_ok=True)

        self.prompts: Dict[str, Prompt] = {}
        self.personal_genome_path = self.lab_path / "personal_genome.json"

    def load_repository_prompts(self):
        """
        Load all prompts from the repository files.

        Parses the actual prompt files and converts them to Prompt objects.
        """
        categories = {
            "simple": PromptCategory.SIMPLE,
            "work-prompts": PromptCategory.WORK,
            "agentic": PromptCategory.AGENTIC,
            "stocks": PromptCategory.STOCKS,
            "fun": PromptCategory.FUN
        }

        for dir_name, category in categories.items():
            dir_path = self.repo_path / dir_name
            if not dir_path.exists():
                continue

            for file_path in dir_path.glob("*"):
                if file_path.suffix in [".txt", ".md"] and file_path.is_file():
                    try:
                        prompt = self._parse_prompt_file(file_path, category)
                        if prompt:
                            self.prompts[prompt.id] = prompt
                    except Exception as e:
                        print(f"Warning: Failed to load {file_path}: {e}")

    def _parse_prompt_file(self, file_path: Path, category: PromptCategory) -> Optional[Prompt]:
        """Parse a prompt file and extract its genetic components"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse metadata (YAML frontmatter)
        metadata = {}
        prompt_content = content

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                metadata_text = parts[1]
                prompt_content = parts[2]

                # Simple YAML parsing
                for line in metadata_text.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()

                        # Handle lists
                        if value.startswith('[') and value.endswith(']'):
                            value = [v.strip() for v in value[1:-1].split(',')]

                        metadata[key] = value

        # Extract genes from content
        dna = PromptDNA()

        # Parse structured sections
        sections = self._parse_sections(prompt_content)

        # Convert sections to genes
        gene_type_mapping = {
            'system': 'system',
            'role': 'system',
            'context': 'context',
            'instructions': 'instructions',
            'constraints': 'constraints',
            'output format': 'output_format',
            'output_format': 'output_format',
            'reasoning': 'reasoning',
            'example': 'examples',
            'tips': 'constraints',
            'description': 'context',
            'use case': 'context'
        }

        for section_name, section_content in sections.items():
            section_lower = section_name.lower()
            gene_type = gene_type_mapping.get(section_lower, 'instructions')

            gene = Gene(
                name=f"{file_path.stem}_{section_name.replace(' ', '_')}",
                sequence=section_content.strip(),
                gene_type=gene_type,
                dominant=gene_type in ['system', 'instructions']
            )
            dna.add_gene(gene)

        # If no structured sections, treat entire content as instructions
        if not dna.genes:
            gene = Gene(
                name=f"{file_path.stem}_main",
                sequence=prompt_content.strip(),
                gene_type='instructions',
                dominant=True
            )
            dna.add_gene(gene)

        # Create prompt object
        prompt = Prompt(
            id=file_path.stem,
            name=metadata.get('name', file_path.stem.replace('-', ' ').title()),
            description=sections.get('Description', metadata.get('description', 'No description')),
            category=category,
            tier=PromptTier(metadata.get('tier', 'free')),
            dna=dna,
            tags=set(metadata.get('tags', [])),
            model_compatibility=metadata.get('model_compatibility', ['all']),
            version=metadata.get('version', '1.0.0'),
            author=metadata.get('author', 'unknown')
        )

        return prompt

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown sections from content"""
        sections = {}
        current_section = None
        current_content = []

        lines = content.split('\n')
        for line in lines:
            # Check for markdown headers
            if line.startswith('##'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip('#').strip()
                current_content = []
            elif line.startswith('<') and '>' in line:
                # XML-style tags like <System>, <Context>
                tag_match = re.match(r'<(\w+)>', line)
                if tag_match:
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = tag_match.group(1)
                    current_content = []
                    continue

            if current_section:
                current_content.append(line)

        # Add last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)

        # If no sections found, return content as Instructions
        if not sections:
            sections['Instructions'] = content

        return sections

    def save_prompt(self, prompt: Prompt):
        """Save a prompt to the personal genome"""
        self.prompts[prompt.id] = prompt

        # Load existing personal genome
        personal_genome = []
        if self.personal_genome_path.exists():
            with open(self.personal_genome_path, 'r') as f:
                personal_genome = json.load(f)

        # Add or update prompt
        prompt_dict = prompt.to_dict()
        existing_idx = None
        for i, p in enumerate(personal_genome):
            if p['id'] == prompt.id:
                existing_idx = i
                break

        if existing_idx is not None:
            personal_genome[existing_idx] = prompt_dict
        else:
            personal_genome.append(prompt_dict)

        # Save
        with open(self.personal_genome_path, 'w') as f:
            json.dump(personal_genome, f, indent=2)

    def load_personal_genome(self):
        """Load user's personal genome"""
        if not self.personal_genome_path.exists():
            return

        with open(self.personal_genome_path, 'r') as f:
            personal_genome = json.load(f)

        for prompt_data in personal_genome:
            prompt = Prompt.from_dict(prompt_data)
            self.prompts[prompt.id] = prompt

    def search(self,
               query: str = "",
               category: Optional[PromptCategory] = None,
               tier: Optional[PromptTier] = None,
               tags: Optional[List[str]] = None) -> List[Prompt]:
        """Search prompts with filters"""
        results = list(self.prompts.values())

        if query:
            query = query.lower()
            results = [
                p for p in results
                if query in p.name.lower() or
                   query in p.description.lower() or
                   any(query in tag.lower() for tag in p.tags)
            ]

        if category:
            results = [p for p in results if p.category == category]

        if tier:
            results = [p for p in results if p.tier == tier]

        if tags:
            results = [
                p for p in results
                if any(tag in p.tags for tag in tags)
            ]

        return results

    def get_by_id(self, prompt_id: str) -> Optional[Prompt]:
        """Get a specific prompt by ID"""
        return self.prompts.get(prompt_id)

    def list_all(self) -> List[Prompt]:
        """List all prompts"""
        return list(self.prompts.values())

    def get_stats(self) -> dict:
        """Get library statistics"""
        prompts = list(self.prompts.values())

        category_counts = {}
        tier_counts = {}

        for prompt in prompts:
            cat = prompt.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1

            tier = prompt.tier.value
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        return {
            "total_prompts": len(prompts),
            "categories": category_counts,
            "tiers": tier_counts,
            "total_genes": sum(len(p.dna.genes) for p in prompts),
            "avg_genes_per_prompt": sum(len(p.dna.genes) for p in prompts) / len(prompts) if prompts else 0
        }

    def export_prompt(self, prompt_id: str, output_path: str):
        """Export a prompt to a file"""
        prompt = self.get_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt {prompt_id} not found")

        output = f"""---
version: {prompt.version}
created: {prompt.created.isoformat()}
updated: {prompt.updated.isoformat()}
category: {prompt.category.value}
tier: {prompt.tier.value}
author: {prompt.author}
tags: [{', '.join(prompt.tags)}]
model_compatibility: [{', '.join(prompt.model_compatibility)}]
genome_id: {prompt.get_genome_id()}
generation: {prompt.dna.generation}
---

# {prompt.name}

## Description
{prompt.description}

## Genetic Information
- Genome ID: {prompt.get_genome_id()}
- Generation: {prompt.dna.generation}
- Genes: {len(prompt.dna.genes)}
- Parents: {', '.join(prompt.dna.parents) if prompt.dna.parents else 'Original'}

## Prompt Content

{prompt.dna.express()}

---
Generated by PromptLab 🧬
"""

        with open(output_path, 'w') as f:
            f.write(output)
