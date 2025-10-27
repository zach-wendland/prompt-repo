# Contributing to Prompt Repository

Thank you for your interest in contributing! This repository aims to be the highest-quality collection of AI prompts for professional and personal use.

## Table of Contents

- [How to Contribute](#how-to-contribute)
- [Contribution Types](#contribution-types)
- [Quality Standards](#quality-standards)
- [Submission Process](#submission-process)
- [Prompt Template](#prompt-template)
- [Review Process](#review-process)
- [Community Guidelines](#community-guidelines)

## How to Contribute

There are several ways to contribute:

1. **Submit New Prompts:** Share your original, high-quality prompts
2. **Improve Existing Prompts:** Enhance documentation, add examples, fix issues
3. **Report Issues:** Identify bugs, errors, or problematic content
4. **Suggest Features:** Propose new categories or improvements
5. **Documentation:** Improve guides, tutorials, and examples

## Contribution Types

### New Prompts

**Requirements:**
- Must be original content or properly licensed
- Clear, documented purpose and use case
- Examples of expected input/output
- Follows our [Prompt Guidelines](PROMPT_GUIDELINES.md)
- Adheres to our [Security Policy](SECURITY_POLICY.md)

**Categories:**
- **Simple:** Quick utility prompts (< 200 characters)
- **Work:** Enterprise and professional use cases
- **Agentic:** Complex, multi-step autonomous workflows
- **Fun:** Creative, educational, or entertainment prompts
- **Specialized:** Domain-specific (finance, data, code, etc.)

### Improvements to Existing Prompts

**What to improve:**
- Clarity and readability
- Usage examples
- Error handling
- Documentation
- Performance optimization
- Model-specific variations

### Bug Reports

**Include:**
- Prompt file name and location
- Description of the issue
- Expected behavior
- Actual behavior
- AI model used (GPT-4, Claude, etc.)
- Steps to reproduce

## Quality Standards

### All Prompts Must:

1. **Be Original:** No proprietary or leaked content from AI providers
2. **Be Ethical:** Follow our acceptable use policy
3. **Be Clear:** Well-documented with purpose and usage
4. **Be Tested:** Verified to work as intended
5. **Be Formatted:** Proper structure and metadata
6. **Add Value:** Solve real problems or provide genuine utility

### Prompts Should NOT:

- Bypass AI safety measures maliciously
- Generate harmful, illegal, or unethical content
- Contain personal or sensitive information
- Include proprietary content from other sources
- Encourage misuse or harmful applications
- Be duplicate of existing prompts without significant improvement

## Submission Process

### Step 1: Fork the Repository

```bash
# Fork via GitHub UI, then clone your fork
git clone https://github.com/YOUR-USERNAME/prompt-repo.git
cd prompt-repo
```

### Step 2: Create a Feature Branch

```bash
git checkout -b add-prompt-[prompt-name]
# Example: git checkout -b add-prompt-email-analyzer
```

### Step 3: Add Your Prompt

1. Choose the appropriate directory:
   - `simple/` - Quick utility prompts
   - `work-prompts/` - Professional/enterprise
   - `agentic/` - Complex workflows
   - `fun/` - Creative/educational
   - `stocks/` or create new category if needed

2. Create your prompt file with proper naming:
   - Use lowercase with hyphens: `my-prompt-name.txt` or `.md`
   - Be descriptive: `sap-data-extractor.txt` not `sap.txt`

3. Include required metadata (see template below)

### Step 4: Follow the Prompt Template

```markdown
---
version: 1.0.0
created: 2025-10-27
updated: 2025-10-27
category: [work|simple|agentic|fun|specialized]
tier: [free|premium|enterprise]
author: your-github-username
tags: [tag1, tag2, tag3]
model_compatibility: [gpt-4, claude-3, gemini, all]
---

# Prompt Title

## Description
Brief description of what this prompt does and its use case.

## Use Case
When and why to use this prompt.

## Instructions
[Your actual prompt content here]

## Example Input
```
Sample input the user would provide
```

## Example Output
```
Expected output from the AI
```

## Tips
- Pro tip 1
- Pro tip 2

## Variations
Optional: Different versions for specific models or use cases

## Credits
If adapted from elsewhere (with permission) or inspired by others
```

### Step 5: Test Your Prompt

Test with at least one AI model:
- ✅ GPT-4 / ChatGPT
- ✅ Claude 3 (Sonnet/Opus)
- ✅ Gemini Pro
- ✅ Other models (specify)

Document which models you've tested.

### Step 6: Commit Your Changes

```bash
git add .
git commit -m "Add [prompt-name] for [use-case]

- Added new prompt for [specific purpose]
- Tested with [AI models]
- Category: [category]
- Tier: [free/premium]"
```

### Step 7: Push and Create Pull Request

```bash
git push origin add-prompt-[prompt-name]
```

Then create a Pull Request on GitHub with:
- Clear title describing the contribution
- Description of what the prompt does
- Testing notes
- Any special considerations

## Review Process

### Timeline
- Initial review: 2-5 business days
- Feedback/revisions: As needed
- Final approval: 1-3 days after revisions

### Criteria

Reviewers will check:
1. **Quality:** Does it meet our standards?
2. **Originality:** Is it unique or significantly improved?
3. **Safety:** Does it comply with security policy?
4. **Documentation:** Is it well-documented?
5. **Testing:** Has it been tested adequately?
6. **Value:** Does it add value to the repository?

### Possible Outcomes

- ✅ **Approved:** Merged into main branch
- 🔄 **Needs Changes:** Feedback provided for improvement
- ❌ **Declined:** Does not meet standards or violates policies

## Prompt Template

Save this template as `_TEMPLATE.md` for reference:

```markdown
---
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
category: [category-name]
tier: [free|premium|enterprise]
author: your-github-username
tags: [tag1, tag2, tag3]
model_compatibility: [gpt-4, claude-3, all]
---

# [Prompt Name]

## Description
What this prompt does in 1-2 sentences.

## Use Case
When and why to use this.

## Instructions
[Actual prompt content]

## Example Input
```
Sample input
```

## Example Output
```
Expected output
```

## Tips
- Helpful tips for best results

## Variations
Optional variations for different scenarios
```

## Community Guidelines

### Be Respectful
- Treat all contributors with respect
- Provide constructive feedback
- Welcome newcomers and help them learn

### Be Collaborative
- Work together to improve prompts
- Share knowledge and best practices
- Credit others for their contributions

### Be Professional
- Maintain high standards
- Follow guidelines and policies
- Communicate clearly and professionally

### Be Ethical
- Only submit ethical, legal content
- Report violations of policies
- Help maintain community trust

## Recognition

### Contributor Levels

Based on accepted contributions:

- **Contributor:** 1-4 accepted prompts
- **Active Contributor:** 5-9 accepted prompts
- **Core Contributor:** 10+ accepted prompts
- **Maintainer:** Invited by project owner

### Benefits

- **All Contributors:**
  - Listed in CONTRIBUTORS.md
  - GitHub badge
  - Satisfaction of helping others

- **Active Contributors:**
  - Free access to premium prompts
  - Early access to new features
  - Input on roadmap decisions

- **Core Contributors:**
  - All premium content free
  - Revenue sharing for marketplace contributions
  - Co-author credit in publications

## Questions?

- **GitHub Issues:** Use [Question] label
- **Discussions:** Use GitHub Discussions
- **Email:** [Contact email]

## Code of Conduct

By contributing, you agree to:

1. Follow our [Security Policy](SECURITY_POLICY.md)
2. Adhere to [Prompt Guidelines](PROMPT_GUIDELINES.md)
3. Maintain professional conduct
4. Respect intellectual property
5. Use ethical practices

## License

By contributing, you agree that your contributions will be licensed under the MIT License, with the understanding that they may be used in both free and commercial offerings of this platform.

You retain copyright of your contributions but grant us an irrevocable license to use, modify, and distribute them.

## Getting Help

Need help contributing?

- Read our [Prompt Guidelines](PROMPT_GUIDELINES.md)
- Check existing prompts for examples
- Ask in GitHub Discussions
- Review closed PRs for examples

## Thank You!

Every contribution makes this repository better for everyone. We appreciate your time and effort in helping build the best prompt collection available.

---

**Happy Contributing! 🚀**
