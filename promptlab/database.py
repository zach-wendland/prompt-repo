"""
Enhanced Database Layer for PromptLab
Provides SQLite-backed storage with advanced querying capabilities
"""
import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import contextmanager

from .models import Prompt, PromptCategory, PromptTier


class PromptDatabase:
    """
    High-performance SQLite database for prompt storage and retrieval.

    Features:
    - Full-text search
    - Complex queries
    - Caching
    - Transaction support
    - Migration system
    """

    VERSION = 1

    def __init__(self, db_path: str = ".promptlab/prompts.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_database(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Main prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    version TEXT,
                    author TEXT,
                    genome_id TEXT UNIQUE,
                    generation INTEGER DEFAULT 1,
                    usage_count INTEGER DEFAULT 0,
                    effectiveness_score REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    dna_json TEXT NOT NULL,
                    metadata_json TEXT
                )
            """)

            # Genes table for detailed querying
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS genes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id TEXT NOT NULL,
                    gene_name TEXT NOT NULL,
                    gene_type TEXT NOT NULL,
                    sequence TEXT NOT NULL,
                    dominant INTEGER DEFAULT 1,
                    mutations INTEGER DEFAULT 0,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
                )
            """)

            # Lineage tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lineage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    offspring_id TEXT NOT NULL,
                    parent_id TEXT NOT NULL,
                    parent_order INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (offspring_id) REFERENCES prompts(id) ON DELETE CASCADE,
                    FOREIGN KEY (parent_id) REFERENCES prompts(id) ON DELETE CASCADE
                )
            """)

            # Tags table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id TEXT NOT NULL,
                    tag TEXT NOT NULL,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
                    UNIQUE(prompt_id, tag)
                )
            """)

            # Full-text search virtual table
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS prompts_fts USING fts5(
                    prompt_id UNINDEXED,
                    name,
                    description,
                    tags,
                    content
                )
            """)

            # Effectiveness tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS effectiveness_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id TEXT NOT NULL,
                    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    model TEXT,
                    score REAL,
                    latency_ms INTEGER,
                    token_count INTEGER,
                    notes TEXT,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
                )
            """)

            # Analytics events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    prompt_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_json TEXT,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE SET NULL
                )
            """)

            # Indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_prompts_category ON prompts(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_prompts_tier ON prompts(tier)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_prompts_genome ON prompts(genome_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_genes_prompt ON genes(prompt_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_genes_type ON genes(gene_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_lineage_offspring ON lineage(offspring_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_lineage_parent ON lineage(parent_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags_prompt ON tags(prompt_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_effectiveness_prompt ON effectiveness_logs(prompt_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_prompt ON events(prompt_id)")

            # Version tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("INSERT OR IGNORE INTO schema_version (version) VALUES (?)", (self.VERSION,))

    def save_prompt(self, prompt: Prompt) -> bool:
        """Save or update a prompt"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Serialize DNA
            dna_json = json.dumps({
                "genes": [
                    {
                        "name": g.name,
                        "sequence": g.sequence,
                        "gene_type": g.gene_type,
                        "dominant": g.dominant,
                        "mutations": g.mutations
                    }
                    for g in prompt.dna.genes
                ],
                "generation": prompt.dna.generation,
                "parents": prompt.dna.parents
            })

            metadata_json = json.dumps({
                "model_compatibility": prompt.model_compatibility,
                "usage_count": prompt.usage_count,
                "effectiveness_score": prompt.effectiveness_score
            })

            # Upsert prompt
            cursor.execute("""
                INSERT OR REPLACE INTO prompts
                (id, name, description, category, tier, version, author, genome_id, generation,
                 usage_count, effectiveness_score, updated_at, dna_json, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prompt.id,
                prompt.name,
                prompt.description,
                prompt.category.value,
                prompt.tier.value,
                prompt.version,
                prompt.author,
                prompt.get_genome_id(),
                prompt.dna.generation,
                prompt.usage_count,
                prompt.effectiveness_score,
                datetime.now(),
                dna_json,
                metadata_json
            ))

            # Save genes
            cursor.execute("DELETE FROM genes WHERE prompt_id = ?", (prompt.id,))
            for gene in prompt.dna.genes:
                cursor.execute("""
                    INSERT INTO genes (prompt_id, gene_name, gene_type, sequence, dominant, mutations)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (prompt.id, gene.name, gene.gene_type, gene.sequence, gene.dominant, gene.mutations))

            # Save tags
            cursor.execute("DELETE FROM tags WHERE prompt_id = ?", (prompt.id,))
            for tag in prompt.tags:
                cursor.execute("INSERT INTO tags (prompt_id, tag) VALUES (?, ?)", (prompt.id, tag))

            # Save lineage
            if prompt.dna.parents:
                cursor.execute("DELETE FROM lineage WHERE offspring_id = ?", (prompt.id,))
                for idx, parent_id in enumerate(prompt.dna.parents):
                    cursor.execute("""
                        INSERT INTO lineage (offspring_id, parent_id, parent_order)
                        VALUES (?, ?, ?)
                    """, (prompt.id, parent_id, idx))

            # Update FTS
            cursor.execute("DELETE FROM prompts_fts WHERE prompt_id = ?", (prompt.id,))
            tags_str = " ".join(prompt.tags)
            content = prompt.dna.express()
            cursor.execute("""
                INSERT INTO prompts_fts (prompt_id, name, description, tags, content)
                VALUES (?, ?, ?, ?, ?)
            """, (prompt.id, prompt.name, prompt.description, tags_str, content))

            # Log event
            self.log_event("prompt_saved", prompt.id, {"name": prompt.name})

            return True

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,)).fetchone()

            if not row:
                return None

            return self._row_to_prompt(row, cursor)

    def _row_to_prompt(self, row: sqlite3.Row, cursor: sqlite3.Cursor) -> Prompt:
        """Convert database row to Prompt object"""
        from .models import PromptDNA, Gene

        # Deserialize DNA
        dna_data = json.loads(row['dna_json'])
        metadata = json.loads(row['metadata_json'])

        genes = [
            Gene(
                name=g['name'],
                sequence=g['sequence'],
                gene_type=g['gene_type'],
                dominant=g['dominant']
            )
            for g in dna_data['genes']
        ]

        dna = PromptDNA(
            genes=genes,
            generation=dna_data['generation'],
            parents=dna_data['parents']
        )

        # Get tags
        tags = set()
        tag_rows = cursor.execute("SELECT tag FROM tags WHERE prompt_id = ?", (row['id'],)).fetchall()
        for tag_row in tag_rows:
            tags.add(tag_row['tag'])

        prompt = Prompt(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            category=PromptCategory(row['category']),
            tier=PromptTier(row['tier']),
            dna=dna,
            tags=tags,
            model_compatibility=metadata.get('model_compatibility', []),
            version=row['version'],
            author=row['author'],
            created=datetime.fromisoformat(row['created_at']) if isinstance(row['created_at'], str) else row['created_at'],
            updated=datetime.fromisoformat(row['updated_at']) if isinstance(row['updated_at'], str) else row['updated_at'],
            usage_count=row['usage_count'],
            effectiveness_score=row['effectiveness_score']
        )

        return prompt

    def search(self,
               query: Optional[str] = None,
               category: Optional[PromptCategory] = None,
               tier: Optional[PromptTier] = None,
               tags: Optional[List[str]] = None,
               min_generation: Optional[int] = None,
               min_effectiveness: Optional[float] = None,
               limit: int = 100) -> List[Prompt]:
        """Advanced search with multiple filters"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Build query
            sql_parts = ["SELECT DISTINCT p.* FROM prompts p"]
            where_clauses = []
            params = []

            # Full-text search
            if query:
                sql_parts.append("JOIN prompts_fts fts ON p.id = fts.prompt_id")
                where_clauses.append("prompts_fts MATCH ?")
                params.append(query)

            # Tag filter
            if tags:
                sql_parts.append("JOIN tags t ON p.id = t.prompt_id")
                placeholders = ",".join("?" * len(tags))
                where_clauses.append(f"t.tag IN ({placeholders})")
                params.extend(tags)

            # Category filter
            if category:
                where_clauses.append("p.category = ?")
                params.append(category.value)

            # Tier filter
            if tier:
                where_clauses.append("p.tier = ?")
                params.append(tier.value)

            # Generation filter
            if min_generation:
                where_clauses.append("p.generation >= ?")
                params.append(min_generation)

            # Effectiveness filter
            if min_effectiveness:
                where_clauses.append("p.effectiveness_score >= ?")
                params.append(min_effectiveness)

            # Combine query
            if where_clauses:
                sql_parts.append("WHERE " + " AND ".join(where_clauses))

            sql_parts.append(f"ORDER BY p.effectiveness_score DESC LIMIT {limit}")

            sql = " ".join(sql_parts)
            rows = cursor.execute(sql, params).fetchall()

            prompts = []
            for row in rows:
                prompt = self._row_to_prompt(row, cursor)
                prompts.append(prompt)

            return prompts

    def get_lineage_tree(self, prompt_id: str, depth: int = 5) -> Dict[str, Any]:
        """Get full ancestry tree"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            def get_parents(pid: str, current_depth: int) -> Dict:
                if current_depth >= depth:
                    return {"id": pid, "children": []}

                parents = cursor.execute("""
                    SELECT parent_id FROM lineage
                    WHERE offspring_id = ?
                    ORDER BY parent_order
                """, (pid,)).fetchall()

                return {
                    "id": pid,
                    "children": [get_parents(p['parent_id'], current_depth + 1) for p in parents]
                }

            return get_parents(prompt_id, 0)

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Basic counts
            stats['total_prompts'] = cursor.execute("SELECT COUNT(*) FROM prompts").fetchone()[0]
            stats['total_genes'] = cursor.execute("SELECT COUNT(*) FROM genes").fetchone()[0]
            stats['total_tags'] = cursor.execute("SELECT COUNT(DISTINCT tag) FROM tags").fetchone()[0]

            # Category breakdown
            category_rows = cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM prompts
                GROUP BY category
            """).fetchall()
            stats['by_category'] = {row['category']: row['count'] for row in category_rows}

            # Tier breakdown
            tier_rows = cursor.execute("""
                SELECT tier, COUNT(*) as count
                FROM prompts
                GROUP BY tier
            """).fetchall()
            stats['by_tier'] = {row['tier']: row['count'] for row in tier_rows}

            # Generation stats
            gen_stats = cursor.execute("""
                SELECT
                    AVG(generation) as avg_gen,
                    MAX(generation) as max_gen,
                    MIN(generation) as min_gen
                FROM prompts
            """).fetchone()
            stats['generations'] = {
                'average': gen_stats['avg_gen'],
                'max': gen_stats['max_gen'],
                'min': gen_stats['min_gen']
            }

            # Effectiveness stats
            eff_stats = cursor.execute("""
                SELECT
                    AVG(effectiveness_score) as avg_eff,
                    MAX(effectiveness_score) as max_eff
                FROM prompts
                WHERE effectiveness_score > 0
            """).fetchone()
            stats['effectiveness'] = {
                'average': eff_stats['avg_eff'] or 0,
                'max': eff_stats['max_eff'] or 0
            }

            # Most used prompts
            most_used = cursor.execute("""
                SELECT id, name, usage_count
                FROM prompts
                ORDER BY usage_count DESC
                LIMIT 5
            """).fetchall()
            stats['most_used'] = [
                {'id': row['id'], 'name': row['name'], 'count': row['usage_count']}
                for row in most_used
            ]

            # Top performers
            top_performers = cursor.execute("""
                SELECT id, name, effectiveness_score
                FROM prompts
                WHERE effectiveness_score > 0
                ORDER BY effectiveness_score DESC
                LIMIT 5
            """).fetchall()
            stats['top_performers'] = [
                {'id': row['id'], 'name': row['name'], 'score': row['effectiveness_score']}
                for row in top_performers
            ]

            return stats

    def log_event(self, event_type: str, prompt_id: Optional[str] = None, data: Optional[Dict] = None):
        """Log an analytics event"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            data_json = json.dumps(data) if data else None
            cursor.execute("""
                INSERT INTO events (event_type, prompt_id, data_json)
                VALUES (?, ?, ?)
            """, (event_type, prompt_id, data_json))

    def log_effectiveness(self, prompt_id: str, model: str, score: float,
                         latency_ms: Optional[int] = None,
                         token_count: Optional[int] = None,
                         notes: Optional[str] = None):
        """Log prompt effectiveness test results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO effectiveness_logs
                (prompt_id, model, score, latency_ms, token_count, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (prompt_id, model, score, latency_ms, token_count, notes))

            # Update prompt's average effectiveness
            avg_score = cursor.execute("""
                SELECT AVG(score) as avg_score
                FROM effectiveness_logs
                WHERE prompt_id = ?
            """, (prompt_id,)).fetchone()['avg_score']

            cursor.execute("""
                UPDATE prompts
                SET effectiveness_score = ?
                WHERE id = ?
            """, (avg_score, prompt_id))

    def increment_usage(self, prompt_id: str):
        """Increment usage counter"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE prompts
                SET usage_count = usage_count + 1
                WHERE id = ?
            """, (prompt_id,))
            self.log_event("prompt_used", prompt_id)

    def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics for the past N days"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cutoff = datetime.now().timestamp() - (days * 86400)

            # Events in period
            events = cursor.execute("""
                SELECT event_type, COUNT(*) as count
                FROM events
                WHERE timestamp >= datetime(?, 'unixepoch')
                GROUP BY event_type
            """, (cutoff,)).fetchall()

            summary = {
                'period_days': days,
                'events': {row['event_type']: row['count'] for row in events},
                'total_events': sum(row['count'] for row in events)
            }

            # Tests performed
            tests = cursor.execute("""
                SELECT COUNT(*) as count
                FROM effectiveness_logs
                WHERE test_date >= datetime(?, 'unixepoch')
            """, (cutoff,)).fetchone()
            summary['tests_performed'] = tests['count']

            return summary
