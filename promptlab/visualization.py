"""
Visualization and Analytics for PromptLab

ASCII-based visualizations for terminal display.
"""
from typing import List, Dict, Any, Tuple
from collections import Counter
import math

from .models import Prompt


class PromptVisualizer:
    """
    Create ASCII visualizations for prompts and their relationships.
    """

    def __init__(self, width: int = 80):
        self.width = width

    def draw_family_tree(self, prompt: Prompt, ancestors: Dict[str, Prompt], depth: int = 3) -> str:
        """
        Draw an ASCII family tree showing lineage.
        """
        lines = []
        lines.append(f"{'=' * self.width}")
        lines.append(f"Family Tree: {prompt.name}")
        lines.append(f"{'=' * self.width}")
        lines.append("")

        def draw_node(pid: str, level: int, is_last: bool, prefix: str):
            if level > depth or pid not in ancestors:
                return

            p = ancestors[pid]
            connector = "└── " if is_last else "├── "

            # Node info
            node_line = f"{prefix}{connector}{p.name} (Gen {p.dna.generation})"
            lines.append(node_line)

            # Draw children (parents in our case)
            parents = p.dna.parents
            if parents and level < depth:
                new_prefix = prefix + ("    " if is_last else "│   ")
                for i, parent_id in enumerate(parents):
                    is_last_child = (i == len(parents) - 1)
                    draw_node(parent_id, level + 1, is_last_child, new_prefix)

        # Start with the root
        lines.append(f"{prompt.name} (Gen {prompt.dna.generation})")

        if prompt.dna.parents:
            for i, parent_id in enumerate(prompt.dna.parents):
                is_last = (i == len(prompt.dna.parents) - 1)
                draw_node(parent_id, 1, is_last, "")

        lines.append("")
        return "\n".join(lines)

    def draw_fitness_chart(self, prompts: List[Tuple[str, float]], title: str = "Fitness Scores") -> str:
        """
        Draw a horizontal bar chart of fitness scores.
        """
        lines = []
        lines.append(f"{'=' * self.width}")
        lines.append(f"{title}")
        lines.append(f"{'=' * self.width}")
        lines.append("")

        if not prompts:
            lines.append("No data to display")
            return "\n".join(lines)

        # Sort by fitness
        prompts = sorted(prompts, key=lambda x: x[1], reverse=True)

        # Calculate bar width
        max_name_length = max(len(name) for name, _ in prompts)
        bar_width = self.width - max_name_length - 20  # Space for name, score, and bar

        max_fitness = max(score for _, score in prompts) if prompts else 100

        for name, fitness in prompts[:20]:  # Top 20
            # Truncate name if needed
            display_name = name[:max_name_length].ljust(max_name_length)

            # Calculate bar length
            if max_fitness > 0:
                bar_length = int((fitness / max_fitness) * bar_width)
            else:
                bar_length = 0

            bar = "█" * bar_length
            score_str = f"{fitness:5.1f}"

            line = f"{display_name} │{bar} {score_str}"
            lines.append(line)

        lines.append("")
        return "\n".join(lines)

    def draw_evolution_graph(self, generation_history: List[Dict]) -> str:
        """
        Draw a graph showing fitness evolution over generations.
        """
        lines = []
        lines.append(f"{'=' * self.width}")
        lines.append("Evolution Progress")
        lines.append(f"{'=' * self.width}")
        lines.append("")

        if not generation_history:
            lines.append("No evolution data")
            return "\n".join(lines)

        # Extract data
        generations = [g['generation'] for g in generation_history]
        avg_fitnesses = [g['avg_fitness'] for g in generation_history]
        max_fitnesses = [g['max_fitness'] for g in generation_history]

        # Graph dimensions
        graph_height = 15
        graph_width = min(self.width - 20, len(generations) * 3)

        # Scale data
        min_fitness = min(min(avg_fitnesses), min(max_fitnesses))
        max_fitness = max(max(avg_fitnesses), max(max_fitnesses))
        fitness_range = max_fitness - min_fitness if max_fitness > min_fitness else 1

        # Draw graph
        for row in range(graph_height):
            line_chars = []
            fitness_level = max_fitness - (row / graph_height) * fitness_range

            for i, gen in enumerate(generations):
                avg_fit = avg_fitnesses[i]
                max_fit = max_fitnesses[i]

                # Determine character
                if abs(max_fit - fitness_level) < (fitness_range / graph_height):
                    char = "█"  # Max fitness
                elif abs(avg_fit - fitness_level) < (fitness_range / graph_height):
                    char = "▓"  # Avg fitness
                else:
                    char = "░" if row % 2 == 0 else " "

                line_chars.append(char * 2)

            # Add Y-axis label
            label = f"{fitness_level:5.1f} │"
            lines.append(label + "".join(line_chars))

        # X-axis
        lines.append("      └" + "─" * (len(generations) * 2))
        x_labels = "       " + "".join(f"{g:2d}" for g in generations)
        lines.append(x_labels)
        lines.append("")

        # Legend
        lines.append("Legend: █ Max Fitness  ▓ Avg Fitness")
        lines.append("")

        return "\n".join(lines)

    def draw_gene_distribution(self, prompts: List[Prompt]) -> str:
        """
        Draw distribution of gene types across prompts.
        """
        lines = []
        lines.append(f"{'=' * self.width}")
        lines.append("Gene Type Distribution")
        lines.append(f"{'=' * self.width}")
        lines.append("")

        # Count gene types
        gene_types = []
        for prompt in prompts:
            for gene in prompt.dna.genes:
                gene_types.append(gene.gene_type)

        if not gene_types:
            lines.append("No genes to analyze")
            return "\n".join(lines)

        type_counts = Counter(gene_types)
        total = len(gene_types)

        # Sort by count
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)

        # Draw bars
        max_count = max(count for _, count in sorted_types)
        bar_width = self.width - 30

        for gene_type, count in sorted_types:
            percentage = (count / total) * 100
            bar_length = int((count / max_count) * bar_width)
            bar = "█" * bar_length

            line = f"{gene_type:15s} │{bar} {count:4d} ({percentage:5.1f}%)"
            lines.append(line)

        lines.append("")
        lines.append(f"Total genes: {total}")
        lines.append("")

        return "\n".join(lines)

    def draw_compatibility_matrix(self, prompts: List[Prompt], max_size: int = 10) -> str:
        """
        Draw a compatibility matrix showing which prompts breed well together.
        """
        lines = []
        lines.append(f"{'=' * self.width}")
        lines.append("Compatibility Matrix")
        lines.append(f"{'=' * self.width}")
        lines.append("")

        # Limit size
        if len(prompts) > max_size:
            prompts = prompts[:max_size]
            lines.append(f"(Showing top {max_size} prompts)")
            lines.append("")

        if len(prompts) < 2:
            lines.append("Need at least 2 prompts")
            return "\n".join(lines)

        # Calculate compatibility scores
        from .genetics import GeneticLab
        lab = GeneticLab()

        # Header
        header = "   │ " + " ".join(f"{i:2d}" for i in range(len(prompts)))
        lines.append(header)
        lines.append("───┼" + "─" * (len(prompts) * 3))

        # Matrix
        for i, prompt1 in enumerate(prompts):
            row = f"{i:2d} │ "
            for j, prompt2 in enumerate(prompts):
                if i == j:
                    char = "──"
                else:
                    compat = lab.analyze_compatibility(prompt1, prompt2)
                    score = compat['compatibility_score']

                    # Convert to symbol
                    if score >= 0.8:
                        char = "██"  # Excellent
                    elif score >= 0.6:
                        char = "▓▓"  # Good
                    elif score >= 0.4:
                        char = "▒▒"  # Moderate
                    elif score >= 0.2:
                        char = "░░"  # Poor
                    else:
                        char = "  "  # Very poor

                row += char + " "
            lines.append(row)

        lines.append("")
        lines.append("Legend: ██ Excellent  ▓▓ Good  ▒▒ Moderate  ░░ Poor")
        lines.append("")

        # Prompt list
        lines.append("Prompts:")
        for i, prompt in enumerate(prompts):
            lines.append(f"{i:2d}. {prompt.name}")

        lines.append("")
        return "\n".join(lines)

    def draw_dashboard(self, stats: Dict[str, Any]) -> str:
        """
        Draw a comprehensive dashboard with key metrics.
        """
        lines = []
        width = self.width

        # Title
        lines.append("╔" + "═" * (width - 2) + "╗")
        title = "PROMPTLAB DASHBOARD"
        padding = (width - len(title) - 2) // 2
        lines.append("║" + " " * padding + title + " " * (width - padding - len(title) - 2) + "║")
        lines.append("╚" + "═" * (width - 2) + "╝")
        lines.append("")

        # Overall stats
        lines.append("┌─ Overall Statistics " + "─" * (width - 24) + "┐")
        lines.append(f"│ Total Prompts: {stats.get('total_prompts', 0):>5d}          Total Genes: {stats.get('total_genes', 0):>5d}          │")
        lines.append(f"│ Unique Tags:   {stats.get('total_tags', 0):>5d}          Avg Genes:   {stats.get('total_genes', 0) / max(stats.get('total_prompts', 1), 1):>5.1f}          │")
        lines.append("└" + "─" * (width - 2) + "┘")
        lines.append("")

        # Category breakdown
        if 'by_category' in stats:
            lines.append("┌─ By Category " + "─" * (width - 18) + "┐")
            for category, count in stats['by_category'].items():
                bar_length = min(30, count * 3)
                bar = "█" * bar_length
                lines.append(f"│ {category:12s} {bar} {count:3d}                    │")
            lines.append("└" + "─" * (width - 2) + "┘")
            lines.append("")

        # Top performers
        if 'top_performers' in stats and stats['top_performers']:
            lines.append("┌─ Top Performers " + "─" * (width - 21) + "┐")
            for perf in stats['top_performers'][:5]:
                name = perf['name'][:30].ljust(30)
                score = perf['score']
                stars = "★" * int(score / 20)  # 0-5 stars
                lines.append(f"│ {name} {stars:5s} {score:5.1f}           │")
            lines.append("└" + "─" * (width - 2) + "┘")
            lines.append("")

        # Most used
        if 'most_used' in stats and stats['most_used']:
            lines.append("┌─ Most Used " + "─" * (width - 16) + "┐")
            for used in stats['most_used'][:5]:
                name = used['name'][:30].ljust(30)
                count = used['count']
                bar_length = min(15, count)
                bar = "█" * bar_length
                lines.append(f"│ {name} {bar:15s} {count:4d}         │")
            lines.append("└" + "─" * (width - 2) + "┘")
            lines.append("")

        return "\n".join(lines)

    def draw_complexity_radar(self, prompt: Prompt, analysis: Dict) -> str:
        """
        Draw a radar chart showing prompt complexity dimensions.
        """
        lines = []
        lines.append(f"{'=' * self.width}")
        lines.append(f"Complexity Analysis: {prompt.name}")
        lines.append(f"{'=' * self.width}")
        lines.append("")

        # Extract metrics
        metrics = {
            'Structural': analysis.get('complexity', {}).get('structural_complexity', 0),
            'Linguistic': analysis.get('complexity', {}).get('linguistic_complexity', 0),
            'Logical': analysis.get('complexity', {}).get('logical_complexity', 0),
            'Quality': analysis.get('quality_score', 0),
            'Clarity': analysis.get('clarity', {}).get('clarity_score', 0)
        }

        # Draw bars
        for metric, value in metrics.items():
            bar_length = int(value / 100 * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            lines.append(f"{metric:12s} │{bar}│ {value:5.1f}")

        lines.append("")
        return "\n".join(lines)
