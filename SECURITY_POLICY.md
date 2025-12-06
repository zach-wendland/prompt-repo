# Security Policy

**Version:** 1.0.0
**Last Updated:** December 2025

This document outlines security standards, ethical guidelines, and acceptable use policies for all prompts in this repository.

## Table of Contents

- [Reporting Security Vulnerabilities](#reporting-security-vulnerabilities)
- [Acceptable Use Policy](#acceptable-use-policy)
- [Prohibited Content](#prohibited-content)
- [Data Handling Guidelines](#data-handling-guidelines)
- [Ethical AI Standards](#ethical-ai-standards)
- [Content Review Process](#content-review-process)
- [Archived Content](#archived-content)

## Reporting Security Vulnerabilities

### How to Report

If you discover a security vulnerability or problematic content:

1. **Do not** create a public issue
2. Email the maintainers directly with:
   - Description of the vulnerability/issue
   - Steps to reproduce
   - Potential impact assessment
   - Suggested remediation (if any)

### Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 5 business days
- **Resolution:** Based on severity (Critical: 7 days, High: 14 days, Medium: 30 days)

### What Qualifies as a Security Issue

- Prompts containing embedded credentials or API keys
- Content that could enable unauthorized access to systems
- Prompts designed to bypass AI safety measures maliciously
- Proprietary or leaked content from AI providers
- Personal or sensitive information exposure

## Acceptable Use Policy

### Permitted Uses

- Professional and enterprise workflows
- Educational and research purposes
- Creative writing and content generation
- Software development assistance
- Data analysis and business intelligence
- Personal productivity enhancement

### User Responsibilities

- Test prompts in safe environments before production use
- Validate outputs for accuracy and appropriateness
- Comply with applicable laws and regulations
- Respect intellectual property rights
- Report problematic content or security issues

## Prohibited Content

The following content types are **not permitted** in this repository:

### Absolutely Prohibited

1. **Malicious Code Generation**
   - Prompts designed to generate malware, viruses, or ransomware
   - Instructions for creating hacking tools or exploits
   - Content enabling unauthorized system access

2. **Safety Bypass Attempts**
   - Prompts designed to circumvent AI safety measures
   - Jailbreak techniques intended for malicious purposes
   - Instructions to ignore ethical guidelines

3. **Harmful Content**
   - Content promoting violence, harassment, or discrimination
   - Instructions for illegal activities
   - Content that could cause physical or psychological harm

4. **Privacy Violations**
   - Prompts containing personal identifiable information (PII)
   - Content enabling doxxing or stalking
   - Instructions for unauthorized surveillance

5. **Intellectual Property Violations**
   - Leaked system prompts from commercial AI providers
   - Proprietary content without proper licensing
   - Copyright-infringing material

### Conditional Content (Requires Review)

- Security research prompts (must include ethical context)
- Penetration testing tools (must specify authorized use only)
- Content analysis prompts for sensitive topics

## Data Handling Guidelines

### What to Include

- Placeholder variables for sensitive data: `[YOUR_API_KEY]`, `{{user_input}}`
- Generic examples that demonstrate functionality
- Clear documentation of required inputs

### What to Exclude

- Real API keys, tokens, or credentials
- Production database connection strings
- Personal email addresses or phone numbers
- Internal company information
- Customer or user data

### Example Placeholders

```
Database: [YOUR_DATABASE_NAME]
API Key: [INSERT_API_KEY]
Email: user@example.com
Endpoint: https://api.example.com/v1/
```

## Ethical AI Standards

### Core Principles

1. **Transparency**
   - Document prompt intentions clearly
   - Disclose limitations and potential biases
   - Provide usage context and appropriate applications

2. **Fairness**
   - Avoid prompts that could produce discriminatory outputs
   - Test across diverse scenarios and user groups
   - Document known biases or limitations

3. **Safety**
   - Design prompts with guardrails where appropriate
   - Consider potential misuse scenarios
   - Include appropriate constraints and boundaries

4. **Privacy**
   - Minimize data collection in prompt design
   - Respect user privacy in examples and documentation
   - Follow data protection principles

### Quality Standards

All prompts should:

- Serve a legitimate, documented purpose
- Be tested with intended AI models
- Include appropriate usage guidance
- Follow repository formatting standards

## Content Review Process

### Pre-Submission Checklist

Before submitting a prompt, verify:

- [ ] No embedded credentials or secrets
- [ ] No proprietary/leaked content
- [ ] No personally identifiable information
- [ ] Clear, legitimate use case documented
- [ ] Tested with at least one AI model
- [ ] Follows repository style guidelines
- [ ] Appropriate tier classification (free/premium/enterprise)

### Review Criteria

Maintainers evaluate submissions for:

1. **Security:** No vulnerabilities or harmful content
2. **Quality:** Meets documentation and formatting standards
3. **Originality:** Not duplicate or improperly attributed
4. **Value:** Provides genuine utility to users
5. **Ethics:** Aligns with acceptable use policy

### Escalation

Content flagged for potential violations undergoes:

1. Initial maintainer review
2. Secondary review if borderline
3. Removal pending review for serious concerns
4. Contributor notification with explanation

## Archived Content

### Safety Research Archive

Previously, this repository contained a `jailbreaks/` directory with AI safety stress tests. This content has been:

- **Quarantined** to a separate branch (`jailbreaks-archive`)
- **Removed** from the main production branch
- **Preserved** for legitimate security research purposes only

### Accessing Archived Content

The archived content is available on the `jailbreaks-archive` branch for:

- Academic security researchers
- AI safety professionals
- Authorized red team exercises

**Note:** This content is not part of the production repository and should only be used for defensive security research with appropriate authorization.

## Compliance

### License Compatibility

All contributions must be:

- Original work or properly licensed
- Compatible with MIT License
- Free of third-party restrictions that conflict with repository terms

### Regulatory Considerations

Users are responsible for ensuring prompt usage complies with:

- GDPR (data protection)
- CCPA (California privacy)
- Industry-specific regulations (HIPAA, SOX, etc.)
- Local laws and regulations

## Updates to This Policy

This security policy may be updated to address:

- New security threats or vulnerabilities
- Changes in AI safety best practices
- Community feedback and lessons learned
- Regulatory or legal requirements

Major updates will be announced in the repository changelog.

---

## Questions?

- **Security Issues:** Email maintainers directly
- **Policy Questions:** Open a GitHub Discussion
- **General Inquiries:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Remember:** Security is everyone's responsibility. When in doubt, err on the side of caution and ask before submitting potentially sensitive content.
