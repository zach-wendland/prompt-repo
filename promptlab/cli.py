"""
PromptLab CLI - Genetic Prompt Engineering Interface
"""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box
from rich.tree import Tree

from .storage import PromptLibrary
from .genetics import GeneticLab
from .models import PromptCategory, PromptTier

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🧬 PromptLab - Genetic Prompt Engineering

    Treat prompts like DNA: breed, mutate, splice, and evolve them!
    """
    pass


@cli.command()
def init():
    """Initialize PromptLab in current directory"""
    library = PromptLibrary()
    console.print("[green]✓[/green] Loading repository prompts...")
    library.load_repository_prompts()
    console.print(f"[green]✓[/green] Loaded {len(library.prompts)} prompts")

    console.print("\n[cyan]PromptLab initialized![/cyan]")
    console.print("Try: [yellow]promptlab list[/yellow]")


@cli.command()
@click.option('--category', '-c', type=click.Choice(['simple', 'work', 'agentic', 'stocks', 'fun']), help='Filter by category')
@click.option('--tier', '-t', type=click.Choice(['free', 'premium', 'enterprise']), help='Filter by tier')
@click.option('--search', '-s', help='Search prompts')
def list(category, tier, search):
    """List all available prompts"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    # Apply filters
    cat_filter = PromptCategory(category) if category else None
    tier_filter = PromptTier(tier) if tier else None

    prompts = library.search(query=search or "", category=cat_filter, tier=tier_filter)

    if not prompts:
        console.print("[yellow]No prompts found matching criteria[/yellow]")
        return

    # Create table
    table = Table(title=f"🧬 Prompt Library ({len(prompts)} prompts)", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category", style="magenta")
    table.add_column("Tier", style="yellow")
    table.add_column("Genes", justify="right")
    table.add_column("Generation", justify="right")

    for prompt in sorted(prompts, key=lambda p: p.name):
        tier_symbol = {
            "free": "🆓",
            "premium": "⭐",
            "enterprise": "💎"
        }.get(prompt.tier.value, "")

        table.add_row(
            prompt.id[:20],
            prompt.name[:30],
            prompt.category.value,
            f"{tier_symbol} {prompt.tier.value}",
            str(len(prompt.dna.genes)),
            str(prompt.dna.generation)
        )

    console.print(table)


@cli.command()
@click.argument('prompt_id')
def inspect(prompt_id):
    """Inspect a prompt's genetic structure"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    prompt = library.get_by_id(prompt_id)
    if not prompt:
        console.print(f"[red]Error:[/red] Prompt '{prompt_id}' not found")
        return

    # Main info panel
    info = f"""
**Name:** {prompt.name}
**Category:** {prompt.category.value}
**Tier:** {prompt.tier.value}
**Version:** {prompt.version}

**Description:**
{prompt.description}

**Genome ID:** `{prompt.get_genome_id()}`
**Generation:** {prompt.dna.generation}
**Parents:** {', '.join(prompt.dna.parents) if prompt.dna.parents else 'Original'}

**Tags:** {', '.join(prompt.tags) if prompt.tags else 'None'}
**Models:** {', '.join(prompt.model_compatibility)}
    """

    console.print(Panel(Markdown(info), title=f"🧬 {prompt.name}", border_style="cyan"))

    # Genes table
    console.print("\n")
    genes_table = Table(title="Genetic Structure", box=box.SIMPLE)
    genes_table.add_column("Gene Type", style="yellow")
    genes_table.add_column("Name", style="cyan")
    genes_table.add_column("Dominant", justify="center")
    genes_table.add_column("Mutations", justify="right")
    genes_table.add_column("Length", justify="right")

    for gene in prompt.dna.genes:
        genes_table.add_row(
            gene.gene_type,
            gene.name[:30],
            "✓" if gene.dominant else "✗",
            str(gene.mutations),
            str(len(gene.sequence))
        )

    console.print(genes_table)


@cli.command()
@click.argument('prompt_id')
@click.option('--output', '-o', help='Output file (default: stdout)')
def express(prompt_id, output):
    """Express a prompt's DNA as usable text (genotype → phenotype)"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    prompt = library.get_by_id(prompt_id)
    if not prompt:
        console.print(f"[red]Error:[/red] Prompt '{prompt_id}' not found")
        return

    expressed = prompt.dna.express()

    if output:
        with open(output, 'w') as f:
            f.write(expressed)
        console.print(f"[green]✓[/green] Prompt expressed to {output}")
    else:
        console.print(Panel(expressed, title=f"🧬 {prompt.name} - Expressed", border_style="green"))


@cli.command()
@click.argument('parent1_id')
@click.argument('parent2_id')
@click.option('--name', '-n', help='Name for offspring')
@click.option('--save', '-s', is_flag=True, help='Save to personal genome')
def breed(parent1_id, parent2_id, name, save):
    """Breed two prompts to create offspring"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    parent1 = library.get_by_id(parent1_id)
    parent2 = library.get_by_id(parent2_id)

    if not parent1:
        console.print(f"[red]Error:[/red] Parent 1 '{parent1_id}' not found")
        return
    if not parent2:
        console.print(f"[red]Error:[/red] Parent 2 '{parent2_id}' not found")
        return

    # Analyze compatibility first
    lab = GeneticLab()
    compat = lab.analyze_compatibility(parent1, parent2)

    console.print("\n[cyan]Analyzing genetic compatibility...[/cyan]\n")

    compat_table = Table(box=box.SIMPLE)
    compat_table.add_column("Metric", style="yellow")
    compat_table.add_column("Value", style="green")

    compat_table.add_row("Compatibility Score", f"{compat['compatibility_score']:.2%}")
    compat_table.add_row("Shared Gene Types", str(len(compat['shared_gene_types'])))
    compat_table.add_row("Category Match", "✓" if compat['category_match'] else "✗")
    compat_table.add_row("Tier Compatible", "✓" if compat['tier_compatible'] else "✗")
    compat_table.add_row("Breeding Recommended", "✓" if compat['breeding_recommended'] else "✗")

    console.print(compat_table)

    if not compat['breeding_recommended']:
        console.print("\n[yellow]Warning:[/yellow] Low compatibility. Proceed anyway? (y/n)", end=" ")
        if not click.confirm(""):
            return

    console.print("\n[green]🧬 Breeding in progress...[/green]\n")

    result = lab.breed(parent1, parent2, name=name)

    console.print(Panel(result.describe(), title="🎉 New Prompt Created!", border_style="green"))

    # Show lineage
    console.print(lab.visualize_lineage(result.offspring))

    if save:
        library.save_prompt(result.offspring)
        console.print(f"\n[green]✓[/green] Saved to personal genome as: {result.offspring.id}")


@cli.command()
@click.argument('prompt_id')
@click.option('--strength', '-s', type=float, default=0.2, help='Mutation strength (0.0-1.0)')
@click.option('--save', is_flag=True, help='Save mutant to personal genome')
def mutate(prompt_id, strength, save):
    """Create a mutated version of a prompt"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    prompt = library.get_by_id(prompt_id)
    if not prompt:
        console.print(f"[red]Error:[/red] Prompt '{prompt_id}' not found")
        return

    lab = GeneticLab()
    mutant = lab.mutate(prompt, mutation_strength=strength)

    console.print(f"\n[green]🧬 Mutation complete![/green]\n")
    console.print(f"Original: {prompt.name}")
    console.print(f"Mutant:   {mutant.name}")
    console.print(f"Mutation strength: {strength:.1%}")
    console.print(f"Genes affected: {int(len(mutant.dna.genes) * strength)}")

    if save:
        library.save_prompt(mutant)
        console.print(f"\n[green]✓[/green] Saved to personal genome as: {mutant.id}")


@cli.command()
@click.argument('target_id')
@click.argument('donor_id')
@click.option('--genes', '-g', multiple=True, help='Gene types to splice (can specify multiple)')
@click.option('--save', is_flag=True, help='Save to personal genome')
def splice(target_id, donor_id, genes, save):
    """Splice genes from donor into target (CRISPR-like editing)"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    target = library.get_by_id(target_id)
    donor = library.get_by_id(donor_id)

    if not target:
        console.print(f"[red]Error:[/red] Target '{target_id}' not found")
        return
    if not donor:
        console.print(f"[red]Error:[/red] Donor '{donor_id}' not found")
        return

    if not genes:
        console.print("[yellow]No gene types specified. Available types:[/yellow]")
        donor_genes = set(g.gene_type for g in donor.dna.genes)
        for gt in donor_genes:
            console.print(f"  - {gt}")
        return

    lab = GeneticLab()
    spliced = lab.splice(target, donor, list(genes))

    console.print(f"\n[green]🧬 Splice complete![/green]\n")
    console.print(f"Target: {target.name}")
    console.print(f"Donor:  {donor.name}")
    console.print(f"Spliced genes: {', '.join(genes)}")

    if save:
        library.save_prompt(spliced)
        console.print(f"\n[green]✓[/green] Saved to personal genome as: {spliced.id}")


@cli.command()
def stats():
    """Show library statistics"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    stats = library.get_stats()

    console.print(Panel.fit(
        f"""
[cyan]Total Prompts:[/cyan] {stats['total_prompts']}
[cyan]Total Genes:[/cyan] {stats['total_genes']}
[cyan]Avg Genes/Prompt:[/cyan] {stats['avg_genes_per_prompt']:.1f}

[yellow]Categories:[/yellow]
{chr(10).join(f'  • {k}: {v}' for k, v in stats['categories'].items())}

[yellow]Tiers:[/yellow]
{chr(10).join(f'  • {k}: {v}' for k, v in stats['tiers'].items())}
        """,
        title="🧬 Library Statistics",
        border_style="cyan"
    ))


@cli.command()
@click.argument('prompt_id')
@click.option('--depth', '-d', type=int, default=3, help='Lineage depth')
def lineage(prompt_id, depth):
    """Show the lineage (ancestry) of a prompt"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    prompt = library.get_by_id(prompt_id)
    if not prompt:
        console.print(f"[red]Error:[/red] Prompt '{prompt_id}' not found")
        return

    lab = GeneticLab()
    lineage_viz = lab.visualize_lineage(prompt, depth=depth)

    console.print(Panel(lineage_viz, title="Genetic Lineage", border_style="cyan"))


@cli.command()
@click.argument('prompt_id')
@click.argument('output_path')
def export(prompt_id, output_path):
    """Export a prompt to a file"""
    library = PromptLibrary()
    library.load_repository_prompts()
    library.load_personal_genome()

    try:
        library.export_prompt(prompt_id, output_path)
        console.print(f"[green]✓[/green] Exported to {output_path}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
def lab():
    """Launch interactive PromptLab (coming soon)"""
    console.print(Panel(
        """
[cyan]Interactive Lab Mode[/cyan]

This feature will provide an interactive environment for:
• Visual prompt exploration
• Real-time breeding
• Mutation experiments
• Genetic analysis

[yellow]Coming in v1.1![/yellow]
        """,
        title="🧬 PromptLab Interactive",
        border_style="cyan"
    ))


if __name__ == '__main__':
    cli()
