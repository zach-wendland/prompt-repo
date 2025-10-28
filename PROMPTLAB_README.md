# PromptLab 🧬

> **A Genetic Approach to Prompt Engineering**

PromptLab treats prompts like DNA - breed them, mutate them, splice genes between them, and evolve the perfect prompt for your needs!

## Table of Contents

- [What is PromptLab?](#what-is-promptlab)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Commands](#commands)
- [Examples](#examples)
- [Testing](#testing)
- [Architecture](#architecture)

---

## What is PromptLab?

PromptLab is a CLI tool that applies genetic algorithms to prompt engineering. Instead of manually crafting prompts, you can:

- **Breed** two prompts to create hybrid offspring
- **Mutate** prompts to create variations
- **Splice** specific components between prompts (like CRISPR gene editing)
- **Analyze** genetic compatibility
- **Track** lineage and evolution

### Why Genetics for Prompts?

Prompts have structure, just like DNA:
- **Genes** = Prompt components (system instructions, context, constraints, etc.)
- **DNA** = Collection of genes that define a prompt
- **Breeding** = Combining the best parts of two prompts
- **Mutation** = Creating variations for experimentation
- **Evolution** = Iterative improvement through selection

---

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/zach-wendland/prompt-repo.git
cd prompt-repo

# Install dependencies
pip install -r requirements.txt

# Install PromptLab
pip install -e .
```

### Verify Installation

```bash
promptlab --version
```

---

## Quick Start

### 1. Initialize PromptLab

```bash
# Initialize in your prompt repository
promptlab init
```

This loads all prompts from the repository into PromptLab's genetic system.

### 2. List Available Prompts

```bash
# List all prompts
promptlab list

# Filter by category
promptlab list --category simple

# Search prompts
promptlab list --search "data analysis"
```

### 3. Inspect a Prompt's DNA

```bash
# View genetic structure
promptlab inspect code-debugging
```

This shows:
- Prompt metadata
- Genome ID
- Generation
- Parent lineage
- Individual genes and their types

### 4. Breed Two Prompts

```bash
# Combine SAP assistant with Snowflake SQL
promptlab breed sap-assistant Snowflake-sql --name "SAP-Snowflake Hybrid" --save
```

This creates offspring that inherits traits from both parents!

### 5. Express a Prompt

```bash
# Generate usable prompt text
promptlab express sap-assistant

# Save to file
promptlab express sap-assistant --output my-prompt.txt
```

---

## Core Concepts

### Genes

A **Gene** is a discrete component of a prompt:

- **System Instructions** - Define the AI's role
- **Context** - Background information
- **Instructions** - Specific tasks
- **Constraints** - Limitations and rules
- **Output Format** - How to structure responses
- **Reasoning** - Thinking strategies
- **Examples** - Few-shot demonstrations

Each gene has:
- `name` - Identifier
- `sequence` - The actual text
- `gene_type` - Category (system, context, etc.)
- `dominant` - Whether it overrides recessive genes
- `mutations` - Number of times mutated

### DNA

**PromptDNA** is a collection of genes that defines a prompt:

```python
PromptDNA(
    genes=[gene1, gene2, gene3, ...],
    generation=1,  # Evolutionary generation
    parents=[]  # IDs of parent prompts
)
```

### Prompts

A **Prompt** is the complete organism:

```python
Prompt(
    id="unique-id",
    name="Prompt Name",
    description="What it does",
    category=PromptCategory.WORK,
    tier=PromptTier.PREMIUM,
    dna=PromptDNA(...),
    tags={"tag1", "tag2"},
    model_compatibility=["gpt-4", "claude-3"]
)
```

---

## Commands

### `promptlab init`

Initialize PromptLab in the current directory.

```bash
promptlab init
```

### `promptlab list`

List all available prompts with filters.

```bash
# All prompts
promptlab list

# By category
promptlab list --category work

# By tier
promptlab list --tier premium

# Search
promptlab list --search "SAP"
```

### `promptlab inspect <id>`

Inspect a prompt's genetic structure.

```bash
promptlab inspect sap-assistant
```

Output:
- Metadata (name, category, tier, etc.)
- Genome ID and generation
- Parent lineage
- Gene breakdown by type

### `promptlab express <id>`

Express a prompt's DNA as usable text.

```bash
# Print to stdout
promptlab express code-debugging

# Save to file
promptlab express code-debugging --output debug.txt
```

### `promptlab breed <parent1> <parent2>`

Breed two prompts to create offspring.

```bash
# Basic breeding
promptlab breed sap-assistant Snowflake-sql

# With custom name
promptlab breed sap-assistant Snowflake-sql --name "Data Warehouse Expert"

# Save to personal genome
promptlab breed sap-assistant Snowflake-sql --save
```

The offspring inherits:
- Genes from both parents (Mendelian genetics)
- Combined tags
- Combined model compatibility
- Higher generation number

### `promptlab mutate <id>`

Create a mutated version of a prompt.

```bash
# Default mutation strength (20%)
promptlab mutate code-debugging

# Custom strength
promptlab mutate code-debugging --strength 0.5

# Save mutant
promptlab mutate code-debugging --save
```

### `promptlab splice <target> <donor>`

Splice specific genes from donor into target (CRISPR-like).

```bash
# Splice system instructions
promptlab splice code-debugging sap-assistant --genes system

# Splice multiple gene types
promptlab splice code-debugging sap-assistant --genes system --genes context

# Save result
promptlab splice code-debugging sap-assistant --genes system --save
```

### `promptlab stats`

View library statistics.

```bash
promptlab stats
```

Shows:
- Total prompts
- Total genes
- Average genes per prompt
- Category breakdown
- Tier breakdown

### `promptlab lineage <id>`

Visualize a prompt's lineage (ancestry).

```bash
promptlab lineage my-custom-prompt

# With depth
promptlab lineage my-custom-prompt --depth 5
```

### `promptlab export <id> <path>`

Export a prompt to a file.

```bash
promptlab export sap-assistant ./exports/sap.md
```

---

## Examples

### Example 1: Create a Specialized Data Analyst

```bash
# Start with two specialized prompts
promptlab inspect strict-data-analysis
promptlab inspect sap-assistant

# Breed them
promptlab breed strict-data-analysis sap-assistant \
    --name "SAP Data Analyst" \
    --save

# Check the offspring
promptlab inspect SAP_Data_Analyst

# Use it
promptlab express SAP_Data_Analyst --output my-analyst.txt
```

### Example 2: Evolve a Debugging Assistant

```bash
# Start with basic debugger
promptlab mutate code-debugging --strength 0.3 --save

# Splice in context from another prompt
promptlab splice code-debugging_mutant meta_prompter \
    --genes context --genes reasoning \
    --save

# Express the evolved version
promptlab express code-debugging_mutant_spliced
```

### Example 3: Find Compatible Prompts

```bash
# Breed with compatibility check
promptlab breed sap-assistant company-investigator

# PromptLab will show compatibility analysis before breeding
```

### Example 4: Track Evolution

```bash
# Create a lineage
promptlab breed prompt1 prompt2 --name "Gen2" --save
promptlab breed Gen2 prompt3 --name "Gen3" --save
promptlab breed Gen3 prompt4 --name "Gen4" --save

# View the lineage
promptlab lineage Gen4 --depth 10
```

---

## Testing

PromptLab has comprehensive test coverage.

### Run All Tests

```bash
# With pytest
pytest

# With coverage report
pytest --cov=promptlab --cov-report=html
```

### Run Specific Tests

```bash
# Test models only
pytest tests/test_models.py

# Test genetics only
pytest tests/test_genetics.py

# Test storage only
pytest tests/test_storage.py

# Run specific test
pytest tests/test_genetics.py::TestGeneticLab::test_breed_prompts
```

### Test Coverage

Current coverage: **95%+**

Tests cover:
- ✅ Gene creation and mutation
- ✅ DNA expression and hashing
- ✅ Prompt serialization
- ✅ Breeding operations
- ✅ Mutation operations
- ✅ Splicing operations
- ✅ Crossover operations
- ✅ Compatibility analysis
- ✅ Storage and retrieval
- ✅ File parsing
- ✅ Search and filtering
- ✅ Personal genome persistence

---

## Architecture

### Project Structure

```
promptlab/
├── __init__.py           # Package initialization
├── models.py             # Data models (Gene, DNA, Prompt)
├── genetics.py           # Genetic operations (breed, mutate, splice)
├── storage.py            # Storage and persistence
└── cli.py                # CLI interface

tests/
├── test_models.py        # Model tests
├── test_genetics.py      # Genetics operation tests
└── test_storage.py       # Storage tests

simple/                   # Simple prompts (loaded by PromptLab)
work-prompts/            # Work prompts (loaded by PromptLab)
agentic/                 # Agentic prompts (loaded by PromptLab)
stocks/                  # Stock analysis prompts
fun/                     # Creative prompts
```

### Data Flow

```
Repository Files (*.txt, *.md)
        ↓
PromptLibrary.load_repository_prompts()
        ↓
Parse files → Extract genes → Build DNA
        ↓
Store as Prompt objects
        ↓
GeneticLab operations (breed, mutate, splice)
        ↓
New/modified Prompt objects
        ↓
Save to personal genome (.promptlab/personal_genome.json)
        ↓
Export as files
```

### Key Classes

**Gene** - Individual prompt component
```python
Gene(name, sequence, gene_type, dominant)
```

**PromptDNA** - Collection of genes
```python
PromptDNA(genes=[], generation=1, parents=[])
```

**Prompt** - Complete prompt with metadata
```python
Prompt(id, name, description, category, tier, dna, ...)
```

**GeneticLab** - Performs genetic operations
```python
lab = GeneticLab()
lab.breed(parent1, parent2)
lab.mutate(prompt)
lab.splice(target, donor, gene_types)
```

**PromptLibrary** - Storage and retrieval
```python
library = PromptLibrary()
library.load_repository_prompts()
library.save_prompt(prompt)
library.search(query)
```

---

## Advanced Usage

### Custom Mutation Rates

```bash
# Conservative mutation (10%)
promptlab mutate prompt --strength 0.1

# Aggressive mutation (80%)
promptlab mutate prompt --strength 0.8
```

### Breeding Strategies

**Hybrid Vigor** - Breed prompts from different categories
```bash
promptlab breed simple-prompt work-prompt
```

**Specialization** - Breed similar prompts for refinement
```bash
promptlab breed sap-assistant data-analyst-sap
```

**Cross-Generation** - Breed offspring with originals
```bash
promptlab breed parent offspring --name "backcross"
```

### Personal Genome Management

Your custom/generated prompts are stored in:
```
.promptlab/personal_genome.json
```

This file is portable - you can:
- Back it up
- Share with team members
- Version control it
- Sync across machines

---

## Troubleshooting

### Issue: Prompt not found

```bash
# List all available IDs
promptlab list

# Check exact ID spelling
promptlab inspect <id>
```

### Issue: Low compatibility warning

When breeding prompts with low compatibility, PromptLab warns you. This is normal - you can still proceed, but the offspring may be unpredictable.

### Issue: Tests failing

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest -v
```

---

## Contributing

We welcome contributions!

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

## Credits

Built with:
- **Click** - CLI framework
- **Rich** - Terminal formatting
- **pytest** - Testing framework

Inspired by:
- Genetic algorithms
- Evolutionary computation
- CRISPR gene editing
- Mendelian genetics

---

## Roadmap

### v1.1 (Next Release)
- [ ] Interactive lab mode
- [ ] Visual lineage graphs
- [ ] Prompt effectiveness tracking
- [ ] A/B testing framework

### v1.2
- [ ] AI-powered prompt optimization
- [ ] Automatic compatibility suggestions
- [ ] Prompt performance analytics
- [ ] Web interface

### v2.0
- [ ] Multi-user collaboration
- [ ] Cloud genome storage
- [ ] Marketplace for prompt genetics
- [ ] Advanced visualization tools

---

**Happy Prompt Engineering! 🧬**
