# Copilot Usage Guide

This document outlines key practices for effectively using Copilot.

---

## Setup
- Go to the Copilot app settings and set up custom instructions.
- Turn on GPT-5 when available.

## Usage Modes
- Use the Data Analyst agent or Work Chat depending on the task.

## Prompt Training
- Complete both basic and advanced prompt training.
- Accumulate enough chats to build prompt memory, ideally as many as you’ve done in ChatGPT.

## Feedback
- Tell Copilot when it provides incorrect responses.

## Features
- Use the Notebook function for structured tasks.

---

# Prompting Framework

To ensure Copilot reasons step-by-step, uses external resources, and provides verifiable anecdotes, apply the following recipe.

## Default Prompt Template

Role: You are my research copilot for [TOPIC].

Deliverable: Produce a [FORMAT: memo/brief/README] for [AUDIENCE] with an executive summary, main body, and references.

Method (follow exactly):
	1.	PLAN: List a numbered plan of the steps you’ll take (3–6 bullets). Keep rationale brief.
	2.	RESEARCH: Use web browsing/tools to consult at least 3 high-quality, independent sources. Prefer primary or official docs.
	3.	CITE: For every key claim, add an inline citation with outlet/author + publication date + link.
	4.	ANECDOTES: Include 2–3 concise, real-world examples (verifiable anecdotes) that name the org/person, date, and source link.
	5.	VALIDATION: Add a “What I couldn’t verify / conflicting info” section with links.
	6.	CHECKLIST: End with a 5-item fact-check checklist I can run quickly.

Constraints:
	•	Don’t speculate; mark uncertainty clearly.
	•	Keep reasoning summaries short (bullets).
	•	Show dates for all sources. Avoid paywalled or low-quality blogs.

Output format:
	•	H1 Title
	•	TL;DR (≤120 words)
	•	Numbered Sections
	•	References (APA-ish or [Outlet, Date] with URLs)

## Work Chat Guidance
- Start with:  
  **“Use web browsing and include citations for all non-obvious claims. Show your step-by-step plan first, then execute.”**  
- Enforce quality with follow-ups:
  - “Do a counter-evidence sweep and update conclusions with citations.”
  - “For each claim, add the source publication date inline.”
  - “Mark anything you couldn’t verify; don’t fill the gap.”

## Data Analyst Agent Guidance

Task: [question]
Data: [files/URLs]
Method:
	1.	Outline the analysis plan (steps + expected charts/tables).
	2.	Show code cells you will run. Use deterministic seeds. Explain outputs in ≤3 bullets per artifact.
	3.	Save and list all artifacts (tables/plots) and how to reproduce.
	4.	Limit assumptions; ask for missing columns/schema only if blocking.

Deliver: Summary, key metrics, links to artifacts, and a short “limitations & next steps”.

## Custom Instructions
Add this to Copilot’s custom instructions:
> “By default: present a brief step plan; use web browsing for non-trivial facts; cite outlet + date + link for each key claim; include 2–3 real-world examples with sources; add a ‘couldn’t verify’ section and a final fact-check checklist.”

## Verifiable Anecdotes
- A verifiable anecdote must be concrete (who/what/when/where).  
- Always include **date + reputable source link**.  
- Avoid hypotheticals or unsourced stories.

---