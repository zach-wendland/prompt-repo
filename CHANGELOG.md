# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `SECURITY_POLICY.md` - Comprehensive security and ethical use guidelines
- `CLAUDE.md` - Claude Code guidance for working in this repository
- `AGENTS.md` - Agent configuration documentation

### Changed
- File naming standardization: Added `.txt` extensions to `prompt-engineer-2025-04-11` and `company-investigator`
- Moved `/jailbreaks` directory to `jailbreaks-archive` branch for security research purposes only
- Updated repository structure to remove jailbreak content from production branch

### Security
- Quarantined jailbreak content to separate branch for authorized security research only
- Implemented comprehensive security policy
- Added content review guidelines

### Planned
- Web application platform
- Subscription management system
- Community marketplace
- API access for developers
- Mobile applications
- AI-powered prompt generator

## [2.0.0] - 2025-10-27

### Major Changes
- **Repository Restructuring:** Complete overhaul of repository organization
- **Monetization Strategy:** Introduction of tiered pricing model (Free/Premium/Enterprise)
- **Documentation Overhaul:** Comprehensive guides and policies added

### Added
- **Strategic Documents:**
  - `MONETIZATION_STRATEGY.md` - Complete 3-year business plan
  - `IMMEDIATE_ACTION_PLAN.md` - 90-day tactical roadmap
  - `EXECUTIVE_SUMMARY.md` - High-level strategic overview

- **Policy & Guidelines:**
  - `CONTRIBUTING.md` - Contribution guidelines and process
  - `PROMPT_GUIDELINES.md` - Quality standards and best practices
  - `CHANGELOG.md` - This file

- **Infrastructure:**
  - Metadata structure for all prompts
  - Version control system
  - Tier classification system

### Changed
- Repository focus: From general collection to professional/enterprise emphasis
- Licensing clarity: Commercial use now explicitly planned
- Quality standards: Implemented three-tier quality system

### Security
- Established ethical use policy
- Created security reporting procedures
- Implemented content review process
- Added acceptable use guidelines

## [1.0.0] - 2025-10-XX

### Initial Repository State

#### Prompts by Category

**Agentic Prompts (3):**
- `ICL-baseline.txt`
- `domain-specific-prompter.txt`
- `dynamic-cheatsheet-prompter.txt`

**Simple Prompts (4):**
- `code-debugging.txt`
- `meeting-notes.txt`
- `strict-data-analysis.txt`
- `text-review.txt`

**Fun Prompts (3):**
- `gpt4o-job-interview.txt`
- `meta_prompter.txt`
- `wargame-master`

**Work Prompts (10):**
- `Snowflake-sql.md`
- `copilot-chat-summary`
- `copilot-it-agent`
- `copilot-pbi-dashboard`
- `copilot-session`
- `copilot_settings.md`
- `data-analyst-sap`
- `sap-assistant.txt`
- `servicenow-rfc.md`
- `technical-meeting-notes`

**Stocks (1):**
- `company-investigator`

**Jailbreaks (7):** [ARCHIVED - moved to jailbreaks-archive branch]
- Quarantined for security and ethical concerns
- Available only for authorized security research

### Repository Setup
- MIT License
- Basic README
- Git repository initialized

---

## Version History Format

### [Version] - YYYY-MM-DD

#### Added
New features, prompts, or documentation added to the repository.

#### Changed
Changes to existing functionality, prompts, or documentation.

#### Deprecated
Features or prompts that will be removed in upcoming releases.

#### Removed
Features, prompts, or files that have been removed.

#### Fixed
Bug fixes, error corrections, or improvements to existing content.

#### Security
Security-related changes, vulnerability fixes, or policy updates.

---

## Upcoming Releases

### [2.1.0] - Planned for 2025-11

#### Planned Additions
- Enhanced README with showcase of top prompts
- Usage examples for all free-tier prompts
- Video tutorials for complex prompts
- Community Discord server setup
- Newsletter signup integration

#### Planned Changes
- Metadata added to all existing prompts
- Improved file organization
- Better categorization system
- Enhanced documentation

### [3.0.0] - Planned for 2026-Q1

#### Planned Major Changes
- Web application launch
- User authentication system
- Subscription management
- Payment processing integration
- Community marketplace beta
- Premium prompt library (25+ new prompts)

---

## Contributing to Changelog

When contributing, please update this changelog with your changes:

1. Add your changes under `[Unreleased]` section
2. Use appropriate category (Added, Changed, etc.)
3. Include brief description of the change
4. Reference related issues or PRs if applicable

Example:
```markdown
### Added
- New SAP S/4HANA data extraction prompt (#123)
- Advanced email automation workflow (#124)

### Fixed
- Corrected typo in meeting-notes prompt (#125)
```

---

## Links

- [Repository](https://github.com/zach-wendland/prompt-repo)
- [Issues](https://github.com/zach-wendland/prompt-repo/issues)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY_POLICY.md)

---

## Notes

- **Breaking Changes:** Major version increments (X.0.0) may include breaking changes
- **Backward Compatibility:** Minor versions (x.X.0) maintain backward compatibility
- **Patches:** Patch versions (x.x.X) are always safe to update
- **Release Frequency:** Updates released as significant changes accumulate
- **Notification:** Major releases announced via newsletter and social media

---

**Last Updated:** December 5, 2025
**Current Version:** 2.0.0
**Next Planned Release:** 2.1.0 (Q1 2026)
