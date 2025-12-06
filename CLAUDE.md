# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a curated collection of AI prompts for ChatGPT, Claude, and other models. There is no build system or runtime—all content is Markdown/text.

## Directory Structure

- `simple/` - Quick utility prompts (<500 chars, single-task)
- `work-prompts/` - Enterprise/professional workflows
- `agentic/` - Multi-step autonomous workflows
- `fun/` - Creative and educational prompts
- `stocks/` - Financial research prompts
- `jailbreaks/` - Safety stress tests
- `agents/` - Agent scaffolds and evaluation suites
  - `agents/general/` - General-purpose agents (XML for GPT, MD for Claude)
  - `agents/general/claude/tests/` - Claude agent test suites
  - `agents/general/claude/research/` - Research-focused agents

## Prompt File Format

All prompts require YAML front matter:

```markdown
---
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
category: [simple|work|agentic|fun|specialized]
tier: [free|premium|enterprise]
author: github-username
tags: [tag1, tag2]
model_compatibility: [gpt-4, claude-3, all]
---

# Prompt Title

## Description
## Use Case
## Instructions
## Example Input
## Example Output
## Tips
```

## Naming Conventions

- Filenames: lowercase with hyphens (`sap-data-extractor.txt`, not `SAPExtractor.txt`)
- Extensions: `.md` or `.txt` for prompts, `.xml` for GPT agents
- XML agents include model/version: `judge-gpt-5.1-20251128.xml`

## Commands

```bash
# Find prompts by content
rg -n "pattern" simple/ work-prompts/ agentic/

# Check YAML front matter exists
rg -n "^---" work-prompts/*

# Create contribution branch
git checkout -b add-prompt-{slug}
```

## Contribution Workflow

1. Branch: `git checkout -b add-prompt-{name}`
2. Add prompt with required metadata (see format above)
3. Test with at least one LLM (GPT-4, Claude 3, or Gemini)
4. Commit: `git commit -m "Add {prompt} for {use-case}"`
5. PR should include: tested models, category, tier

## Key Guidelines

- Keep lines under ~120 characters
- Use professional tone, avoid emoji
- XML agents use two-space indentation
- Preserve heading order from PROMPT_GUIDELINES.md
- Never include credentials or private data
- Document model-specific behavior when relevant
