# Prompt Repository

> **Enterprise-Grade AI Prompts for Professional & Personal Use**

A curated collection of high-quality, production-ready prompts for ChatGPT, Claude, and other AI models. Designed for professionals who value their time and need reliable, effective prompts that deliver results.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](CHANGELOG.md)
[![Prompts](https://img.shields.io/badge/prompts-21+-green.svg)](#prompt-catalog)
[![Security](https://img.shields.io/badge/security-policy-green.svg)](SECURITY_POLICY.md)

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Prompt Catalog](#prompt-catalog)
  - [Simple Prompts](#simple-prompts)
  - [Work Prompts](#work-prompts)
  - [Agentic Prompts](#agentic-prompts)
  - [Fun Prompts](#fun-prompts)
  - [Specialized Prompts](#specialized-prompts)
- [Usage](#usage)
- [Contributing](#contributing)
- [Tier System](#tier-system)
- [Security](#security)
- [License](#license)

---

## Features

- **Production-Ready**: All prompts tested with multiple AI models
- **Comprehensive Metadata**: Version tracking, compatibility tags, and categorization
- **Quality Assured**: Automated validation via GitHub Actions
- **Security First**: No credentials, secrets, or proprietary content
- **Well-Documented**: Clear usage instructions and examples
- **Multiple Tiers**: Free, premium, and enterprise offerings

---

## Quick Start

1. **Browse the catalog** below to find a prompt matching your needs
2. **Check compatibility** with your AI model (GPT-4, Claude, Gemini, etc.)
3. **Copy the prompt** from the corresponding file
4. **Customize** placeholders like `[YOUR_API_KEY]` or `{{variable}}`
5. **Use with your AI** and adjust as needed

---

## Prompt Catalog

### Simple Prompts
*Quick, single-task utilities (<500 characters)*

| Prompt | Description | Tier | Models |
|--------|-------------|------|--------|
| [Code Debugging](simple/code-debugging.txt) | Direct, no-nonsense code debugging | Free | All |
| [Meeting Notes](simple/meeting-notes.txt) | Extract decisions, responsibilities, and open questions | Free | All |
| [Strict Data Analysis](simple/strict-data-analysis.txt) | Ultra-factual analysis with explicit uncertainty marking | Free | All |
| [Text Review](simple/text-review.txt) | Line-by-line critique with specific fixes | Free | All |

### Work Prompts
*Professional and enterprise workflows*

| Prompt | Description | Tier | Models |
|--------|-------------|------|--------|
| [Data Anomaly Resolution](work-prompts/data-errors.txt) | Clean and normalize datasets with JSON output | Free | All |
| [Unresolved Action Items](work-prompts/unresolved-action-items.txt) | Surface unreplied emails and Teams messages | Free | GPT-4, Claude |
| [Snowflake SQL Assistant](work-prompts/Snowflake-sql.md) | Auto-discovering SQL query builder for Snowflake | Premium | GPT-4, Claude |
| [ServiceNow RFC Generator](work-prompts/servicenow-rfc.md) | ITIL-certified change management documentation | Premium | GPT-4, Claude, Gemini |
| [SAP S/4HANA Assistant](work-prompts/sap-assistant.txt) | Multi-agent data architect for SAP systems | Enterprise | GPT-4, Claude, Gemini |
| [Copilot Settings](work-prompts/copilot_settings.md) | Framework for effective Microsoft Copilot usage | Free | GPT-4+ |

### Agentic Prompts
*Multi-step autonomous workflows*

| Prompt | Description | Tier | Models |
|--------|-------------|------|--------|
| [ICL Baseline Agent](agentic/ICL-baseline.txt) | Foundation for autonomous API-integrated agents | Enterprise | GPT-4, Claude |
| [Domain-Specific Agent](agentic/domain-specific-prompter.txt) | Agent with proven strategies for common tasks | Enterprise | GPT-4, Claude |
| [Dynamic Cheatsheet Agent](agentic/dynamic-cheatsheet-prompter.txt) | Agent that learns from documented patterns | Enterprise | GPT-4, Claude |
| [Prompt Engineering Framework](agentic/prompt-engineer-2025-04-11.txt) | Design robust, modular prompt systems | Premium | All |

### Fun Prompts
*Creative and educational*

| Prompt | Description | Tier | Models |
|--------|-------------|------|--------|
| [InterviewPrep AI](fun/gpt4o-job-interview.txt) | Voice-enabled mock interviewer with psychological mirroring | Premium | GPT-4, Claude |
| [Meta Prompt Engineer](fun/meta_prompter.txt) | World-class prompt analysis and enhancement trainer | Premium | GPT-4, Claude, Gemini |

### Specialized Prompts

| Prompt | Description | Tier | Models |
|--------|-------------|------|--------|
| [Corporate Intelligence](stocks/company-investigator.txt) | Comprehensive company research and analysis | Premium | GPT-4, Claude |

---

## Usage

### Basic Usage

1. Open the prompt file from the catalog
2. Copy the content under `## Instructions` section
3. Replace placeholders:
   - `[YOUR_API_KEY]` → your actual API key
   - `{{variable}}` → your specific value
   - `<placeholder>` → context-specific information

### With Frontmatter

Each prompt includes YAML frontmatter with metadata:

```yaml
---
version: 1.0.0
created: 2025-10-27
updated: 2025-12-05
category: work
tier: free
author: zach-wendland
tags: [data-cleaning, json]
model_compatibility: [all]
---
```

Use this to:
- Check compatibility with your AI model
- Track versions and updates
- Understand the intended category and tier

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to submit new prompts
- Quality standards and requirements
- PR submission process
- Testing guidelines

### Quick Contribution Checklist

- [ ] Prompt includes complete YAML frontmatter
- [ ] Tested with at least one AI model
- [ ] No credentials or secrets
- [ ] Follows [Prompt Guidelines](PROMPT_GUIDELINES.md)
- [ ] Complies with [Security Policy](SECURITY_POLICY.md)

---

## Tier System

| Tier | Access | Use Cases |
|------|--------|-----------|
| **Free** | Open to all | General productivity, learning, basic workflows |
| **Premium** | Planned subscription | Advanced features, specialized domains, optimization |
| **Enterprise** | Planned enterprise license | Autonomous agents, complex integrations, custom solutions |

*Current Status*: All prompts freely available during development phase.

---

## Security

This repository maintains strict security standards:

- ✅ No embedded credentials or API keys
- ✅ No proprietary or leaked AI provider content
- ✅ Automated security scanning via GitHub Actions
- ✅ Content review process for all submissions

**Safety Research**: Jailbreak content has been quarantined to the `jailbreaks-archive` branch for authorized security research only.

See [SECURITY_POLICY.md](SECURITY_POLICY.md) for:
- Vulnerability reporting
- Acceptable use policy
- Ethical AI standards

---

## Automation & CI/CD

This repository includes automated quality checks:

- **Frontmatter Validation**: Ensures all prompts have complete metadata
- **Security Scanning**: Detects secrets and sensitive information
- **Link Checking**: Validates internal documentation references
- **PR Templates**: Standardized submission checklist

---

## Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [PROMPT_GUIDELINES.md](PROMPT_GUIDELINES.md) - Quality standards and best practices
- [SECURITY_POLICY.md](SECURITY_POLICY.md) - Security and ethical use policy
- [CHANGELOG.md](CHANGELOG.md) - Version history and updates
- [CLAUDE.md](CLAUDE.md) - Claude Code integration guide
- [AGENTS.md](AGENTS.md) - Agent configuration reference

---

## Roadmap

### Current (v2.0)
- ✅ Repository restructuring
- ✅ Security policy implementation
- ✅ Automated validation
- ✅ Comprehensive documentation

### Planned (v2.1)
- Enhanced prompt examples
- Video tutorials
- Community Discord
- Newsletter integration

### Future (v3.0)
- Web application platform
- User authentication
- Subscription management
- Premium marketplace

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Contributors retain copyright but grant an irrevocable license for use in both free and commercial offerings.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/zach-wendland/prompt-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/zach-wendland/prompt-repo/discussions)
- **Security**: See [SECURITY_POLICY.md](SECURITY_POLICY.md)

---

**⭐ Star this repo** if you find these prompts useful!

**🤝 Contribute** to help build the best prompt collection available.

---

*Built with care for the AI community*
