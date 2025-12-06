# Pull Request

## Description

Brief description of the changes in this PR.

## Type of Change

- [ ] New prompt
- [ ] Enhancement to existing prompt
- [ ] Bug fix
- [ ] Documentation update
- [ ] Repository infrastructure/tooling

## Prompt Information (if applicable)

- **Category:** [simple/work/agentic/fun/specialized]
- **Tier:** [free/premium/enterprise]
- **Tested Models:** [e.g., GPT-4, Claude 3 Opus, Gemini Pro]

## Pre-Submission Checklist

### Required for ALL PRs

- [ ] I have read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] I have read [SECURITY_POLICY.md](../SECURITY_POLICY.md)
- [ ] My changes follow the repository style guidelines
- [ ] I have tested my changes locally

### Required for Prompt Submissions

- [ ] Prompt includes complete YAML frontmatter with all required fields:
  - [ ] `version` (semver format: X.Y.Z)
  - [ ] `created` (YYYY-MM-DD)
  - [ ] `updated` (YYYY-MM-DD)
  - [ ] `category`
  - [ ] `tier`
  - [ ] `author`
  - [ ] `tags` (array)
  - [ ] `model_compatibility` (array)

- [ ] Prompt includes all required sections:
  - [ ] Title (H1 heading)
  - [ ] Description
  - [ ] Use Case
  - [ ] Instructions
  - [ ] Example Input (recommended)
  - [ ] Example Output (recommended)
  - [ ] Tips (optional)

- [ ] Content quality checks:
  - [ ] No embedded credentials, API keys, or secrets
  - [ ] No personally identifiable information (PII)
  - [ ] No proprietary or leaked content
  - [ ] Placeholders use proper format: `[YOUR_API_KEY]`, `{{variable}}`, or `<placeholder>`

- [ ] Testing verification:
  - [ ] Tested with at least one AI model
  - [ ] Example Input/Output verified to work
  - [ ] Documented any model-specific behavior or limitations

- [ ] File organization:
  - [ ] File placed in correct category directory
  - [ ] Filename uses lowercase-with-hyphens format
  - [ ] File has `.txt` or `.md` extension

### Security & Ethics

- [ ] Prompt serves a legitimate, documented purpose
- [ ] Prompt does not bypass AI safety measures maliciously
- [ ] Prompt does not enable harmful, illegal, or unethical activities
- [ ] No malicious code generation capabilities
- [ ] Complies with acceptable use policy

## Testing Notes

Describe how you tested this prompt/change:

**Models tested:**
- [ ] GPT-4
- [ ] Claude 3 (Opus/Sonnet/Haiku)
- [ ] Gemini Pro
- [ ] Other: _______________

**Test scenarios:**
<!-- Describe specific test cases you ran -->

## Additional Context

<!-- Add any other context, screenshots, or information about the PR here -->

## Checklist for Reviewers

- [ ] Frontmatter is complete and valid
- [ ] Content follows style guidelines
- [ ] No security concerns
- [ ] Prompt provides genuine value
- [ ] Documentation is clear

---

**By submitting this PR, I confirm that:**
- My contributions are my original work or properly licensed
- I agree to license my contributions under the MIT License
- I have not included any confidential or proprietary information
