# Repository Guidelines

## Project Structure & Module Organization
The repo is organized by prompt purpose: `simple/` holds quick utilities, `work-prompts/` contains enterprise workflows such as `work-prompts/sap-assistant.txt`, `agentic/` stores multi-step agents, `fun/` covers creative briefs, `stocks/` captures financial research, and `jailbreaks/` houses safety stress tests. Agent scaffolds plus evaluation suites live in `agents/` (see `agents/general/claude/tests/`). Root docs (`README.md`, `CONTRIBUTING.md`, `PROMPT_GUIDELINES.md`) spell out policies; review them before editing. Keep assets near their owners and use lowercase-hyphen files like `fun/meta_prompter.txt`.

## Build, Test, and Development Commands
No compile step is required; rely on these commands:
- `git checkout -b add-prompt-{slug}` - create a focused branch for each contribution.
- `rg --files simple work-prompts agentic` - confirm where similar prompts live before adding new files.
- `rg -n "^---" work-prompts/*` - sanity-check that YAML front matter opens each prompt file.

## Coding Style & Naming Conventions
Write prompts in Markdown with the metadata block from `PROMPT_GUIDELINES.md`, preserving the heading order (`Description`, `Use Case`, `Instructions`, etc.) and fencing every example. Use a professional tone, avoid emoji, and keep lines under ~120 characters. Filenames stay lowercase and hyphenated, ending in `.md` or `.txt`. XML agents keep attribute order and two-space indenting, e.g., `agents/general/judge-gpt-5.1-20251128.xml`.

## Testing Guidelines
Verify each prompt with at least one target LLM (GPT-4, Claude 3, Gemini) and note the model/version in your PR. Re-run the documented `Example Input/Output`, updating them whenever behavior shifts. Agent prompt edits should refresh evaluation runs in `agents/general/claude/tests/` so reviewers can repeat the flow.

## Commit & Pull Request Guidelines
Follow `CONTRIBUTING.md`: `git commit -m "Add {prompt} for {use-case}"` plus a bullet list covering files, category, and tested models. Pull requests should link issues, restate the prompt's purpose, summarize testing evidence, and flag premium tiers or assumptions. Screenshots are only needed when UI assets under `agents/.../claude/tests/ui/` change; otherwise Markdown diffs suffice. Keep PRs scoped to a single prompt or doc tweak.

## Security & Configuration Tips
Never include private data, credentials, or policy-circumvention tricks. Re-run the ethical checklist in `PROMPT_GUIDELINES.md`, ensure metadata tiers (`free`, `premium`, `enterprise`) are accurate, and document safe placeholders for external tooling. Contributions ship under MIT, so submit only text you own or have rights to.
