# Prompt Guidelines

**Version:** 1.0
**Last Updated:** October 27, 2025

This document outlines quality standards and best practices for all prompts in this repository.

## Table of Contents

- [Core Principles](#core-principles)
- [Prompt Structure](#prompt-structure)
- [Quality Criteria](#quality-criteria)
- [Category Standards](#category-standards)
- [Tier Classification](#tier-classification)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)
- [Testing Requirements](#testing-requirements)

## Core Principles

### 1. Clarity Over Cleverness
- Be explicit and clear
- Avoid ambiguous language
- Define roles and objectives precisely
- Use structured formats (XML, markdown, sections)

### 2. Effectiveness Over Length
- Concise when possible, detailed when necessary
- Every word should add value
- Remove redundant instructions
- Balance brevity with completeness

### 3. Ethical and Safe
- No harmful applications
- Respect privacy and consent
- Follow AI provider guidelines
- Consider potential misuse

### 4. Documented and Tested
- Include usage examples
- Test with multiple models when possible
- Document limitations
- Provide troubleshooting tips

## Prompt Structure

### Required Elements

All prompts should include:

```markdown
---
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
category: [category]
tier: [free|premium|enterprise]
author: username
tags: [relevant, tags]
model_compatibility: [models]
---

# Prompt Title

## Description
Brief description of purpose

## Use Case
When to use this prompt

## Instructions
[Actual prompt content]

## Example Input
Sample user input

## Example Output
Expected AI response

## Tips
- Optimization suggestions
- Common issues and solutions
```

### Optional Elements

Enhance prompts with:

```markdown
## Variations
Different versions for specific scenarios

## Advanced Usage
Power user tips and techniques

## Limitations
Known issues or constraints

## Related Prompts
Links to complementary prompts

## Version History
- v1.1: Added feature X
- v1.0: Initial release
```

## Quality Criteria

### Tier 1: Minimum Viable (Free Tier)

✅ **Must Have:**
- Clear purpose and description
- Basic usage instructions
- At least one example
- Tested with one AI model
- Proper metadata

✅ **Should Avoid:**
- Obvious errors or typos
- Vague instructions
- Missing examples
- Untested content

### Tier 2: Professional (Premium)

✅ **Must Have:**
- All Tier 1 requirements
- Multiple examples showing range
- Tested with 2+ AI models
- Advanced usage tips
- Clear limitations documented
- Optimization suggestions

✅ **Should Include:**
- Variations for different scenarios
- Troubleshooting guide
- Related prompts references
- Performance considerations

### Tier 3: Enterprise (Enterprise)

✅ **Must Have:**
- All Tier 2 requirements
- Comprehensive documentation
- Tested across major AI models
- Integration guidance
- Security considerations
- Compliance notes (if applicable)
- Support contact information

✅ **Should Include:**
- Custom modification guide
- API integration examples
- Team collaboration notes
- Usage analytics recommendations
- ROI considerations

## Category Standards

### Simple Prompts

**Characteristics:**
- Length: < 500 characters
- Complexity: Single-task
- Use case: Quick, frequent tasks

**Examples:**
- Meeting notes formatting
- Code debugging assistance
- Text proofreading
- Data formatting

**Standards:**
- Must be copy-paste ready
- No setup required
- Works with all major models
- Clear, immediate value

### Work Prompts

**Characteristics:**
- Length: 500-2000 characters
- Complexity: Professional tasks
- Use case: Enterprise, business workflows

**Examples:**
- SAP data extraction
- ServiceNow RFC creation
- Technical documentation
- Business analysis

**Standards:**
- Domain-specific terminology
- Professional tone
- Compliance-aware
- Security-conscious
- Integration-ready

### Agentic Prompts

**Characteristics:**
- Length: 1000-5000 characters
- Complexity: Multi-step workflows
- Use case: Autonomous task completion

**Examples:**
- Project management automation
- Research and analysis pipelines
- Content generation workflows
- Data processing chains

**Standards:**
- Clear step-by-step instructions
- Error handling defined
- Decision-making criteria
- Progress tracking
- Rollback procedures

### Fun Prompts

**Characteristics:**
- Length: Variable
- Complexity: Creative, educational
- Use case: Entertainment, learning

**Examples:**
- Creative writing aids
- Game masters
- Educational tutors
- Brainstorming assistants

**Standards:**
- Engaging and creative
- Still maintainable quality
- Clear value proposition
- Safe for all audiences (or clearly labeled)

## Tier Classification

### Free Tier Prompts

**Criteria:**
- Basic utility value
- Common use cases
- Minimal customization needed
- Self-explanatory

**Distribution:**
- ~30-40% of total prompts
- Entry-level quality
- Showcase repository value

### Premium Tier Prompts

**Criteria:**
- Specialized knowledge required
- Advanced techniques
- Significant time savings
- Professional applications

**Distribution:**
- ~50-60% of total prompts
- Professional quality
- Regular updates included

### Enterprise Tier Prompts

**Criteria:**
- Mission-critical applications
- Custom development required
- Ongoing support needed
- Compliance considerations

**Distribution:**
- ~10-20% of total prompts
- Enterprise quality
- Dedicated support

## Best Practices

### 1. Role Definition

❌ **Weak:**
```
Help me with data analysis
```

✅ **Strong:**
```
You are an expert data analyst with 15 years of experience in
statistical analysis and business intelligence. Your specialty is
translating complex data into actionable business insights.
```

### 2. Context Setting

❌ **Weak:**
```
Analyze this data
```

✅ **Strong:**
```
<Context>
You are analyzing Q4 sales data for a B2B SaaS company. The data
includes transaction records, customer segments, and regional
performance. Your analysis will inform the annual budget planning.
</Context>
```

### 3. Clear Instructions

❌ **Weak:**
```
Make it better
```

✅ **Strong:**
```
<Instructions>
1. Review the dataset for anomalies or outliers
2. Calculate key metrics: MRR, churn rate, CAC, LTV
3. Identify top 3 performing segments
4. Recommend 2-3 actionable strategies
5. Present findings in executive summary format
</Instructions>
```

### 4. Output Specification

❌ **Weak:**
```
Give me the results
```

✅ **Strong:**
```
<OutputFormat>
Provide results in this structure:
1. Executive Summary (3-4 sentences)
2. Key Metrics (table format)
3. Top Insights (bullet points)
4. Recommendations (numbered list)
5. Next Steps (action items)
</OutputFormat>
```

### 5. Constraints and Guardrails

✅ **Include:**
```
<Constraints>
- Focus only on quantitative data, no speculation
- Maintain confidentiality of customer names
- Use industry-standard calculations
- Highlight data quality issues if present
</Constraints>
```

### 6. Examples and Demonstrations

✅ **Provide:**
```
<Example>
Input: [Sales data CSV]
Expected Output:
## Executive Summary
Q4 sales reached $2.3M (15% YoY growth)...

## Key Metrics
| Metric | Value | Change |
|--------|-------|--------|
| MRR    | $450K | +12%   |
...
</Example>
```

## Common Pitfalls

### ❌ Avoid These Mistakes

1. **Vague Instructions**
   - "Do your best"
   - "Make it good"
   - "Help me with this"

2. **Over-specification**
   - 5000-word prompts for simple tasks
   - Unnecessary constraints
   - Redundant instructions

3. **Missing Context**
   - No background information
   - Undefined terms
   - Ambiguous references

4. **No Examples**
   - Users don't know what to expect
   - Harder to reproduce results
   - Lower adoption

5. **Ignoring Model Differences**
   - Assuming all models behave identically
   - Not testing across models
   - No model-specific notes

6. **Security Oversights**
   - Prompting for sensitive data
   - No data handling guidelines
   - Missing privacy considerations

7. **Poor Maintenance**
   - Outdated information
   - Broken examples
   - No version tracking

## Testing Requirements

### Minimum Testing (Free Tier)

Test with at least **1 model**:
- ✅ GPT-4 / ChatGPT, or
- ✅ Claude 3 (Sonnet/Opus), or
- ✅ Gemini Pro

Document:
- Model tested
- Date tested
- Results summary

### Standard Testing (Premium)

Test with at least **2 models**:
- ✅ GPT-4 / ChatGPT
- ✅ Claude 3 (Sonnet/Opus)
- Optional: Gemini, others

Document:
- All models tested
- Comparative performance notes
- Model-specific tips

### Comprehensive Testing (Enterprise)

Test with **3+ models**:
- ✅ GPT-4 / ChatGPT
- ✅ Claude 3 (Sonnet/Opus)
- ✅ Gemini Pro
- ✅ Other relevant models

Document:
- Detailed comparison
- Strengths/weaknesses per model
- Optimization guide for each
- Edge cases and limitations

### Testing Checklist

For each test:
- [ ] Prompt produces expected output
- [ ] Examples work as documented
- [ ] No errors or unexpected behavior
- [ ] Output quality meets standards
- [ ] Edge cases handled appropriately
- [ ] Performance is acceptable
- [ ] No security or ethical issues

## Versioning Guidelines

### Semantic Versioning

Use format: `MAJOR.MINOR.PATCH`

- **MAJOR (1.x.x):** Breaking changes, complete rewrites
- **MINOR (x.1.x):** New features, significant improvements
- **PATCH (x.x.1):** Bug fixes, minor tweaks, typos

### Examples

- `1.0.0` - Initial release
- `1.1.0` - Added advanced examples
- `1.1.1` - Fixed typo in instructions
- `2.0.0` - Complete restructure for new model

### When to Update Version

**PATCH update:**
- Fix typos or formatting
- Clarify existing instructions
- Update example outputs
- Minor improvements

**MINOR update:**
- Add new examples
- Add new features or options
- Improve documentation
- Add model compatibility

**MAJOR update:**
- Change core structure
- Break backward compatibility
- Complete rewrite
- New methodology

## Quality Review Checklist

Before submitting a prompt:

### Content Quality
- [ ] Clear, specific instructions
- [ ] Appropriate complexity for tier
- [ ] Proper grammar and spelling
- [ ] Professional tone (for work prompts)
- [ ] Ethical and safe applications

### Documentation
- [ ] Complete metadata
- [ ] Purpose clearly stated
- [ ] Use case explained
- [ ] Examples included
- [ ] Tips provided

### Testing
- [ ] Tested with required models
- [ ] Examples verified to work
- [ ] Edge cases considered
- [ ] Limitations documented

### Formatting
- [ ] Proper markdown formatting
- [ ] Code blocks where appropriate
- [ ] Consistent structure
- [ ] Readable layout

### Compliance
- [ ] Follows security policy
- [ ] No proprietary content
- [ ] Attribution if adapted
- [ ] License compatible

## Continuous Improvement

### Regular Updates

Prompts should be updated when:
- New AI models are released
- Better techniques are discovered
- User feedback indicates issues
- Standards or guidelines change
- Industry best practices evolve

### Community Feedback

Encourage and incorporate:
- User suggestions
- Improvement ideas
- Bug reports
- Use case expansions
- Optimization tips

### Performance Monitoring

Track:
- Usage frequency
- User ratings
- Issue reports
- Enhancement requests
- Competitor comparisons

## Resources

### Prompt Engineering References

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
- [Google Prompting Guide](https://ai.google.dev/docs/prompt_best_practices)

### Community Standards

- Review existing high-quality prompts in this repository
- Study accepted PRs for examples
- Participate in discussions
- Share learnings with community

## Questions?

If you have questions about these guidelines:

- Open a GitHub Discussion
- Reference this document in PRs
- Ask in community channels
- Contact maintainers

---

**Remember:** Quality over quantity. One excellent prompt is worth more than ten mediocre ones.
