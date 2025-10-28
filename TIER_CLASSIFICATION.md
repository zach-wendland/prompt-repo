# Prompt Tier Classification

**Version:** 1.0.0
**Last Updated:** October 27, 2025

This document defines the tier structure for all prompts in the repository and explains the pricing/access model.

## Tier Overview

### Free Tier (Public Access)
- **Count:** 8 prompts
- **Purpose:** Showcase quality, provide immediate value, attract users
- **Characteristics:** Basic utility, common use cases, self-explanatory

### Premium Tier (Paid Access)
- **Count:** 10 prompts
- **Purpose:** Professional tools with advanced features
- **Pricing:** $29/month subscription or $99 lifetime access
- **Characteristics:** Specialized knowledge, enterprise-ready, regular updates

### Enterprise Tier (Custom Pricing)
- **Count:** 3 prompts + custom development
- **Purpose:** Mission-critical applications with support
- **Pricing:** Custom quotes starting at $5,000/year
- **Characteristics:** Complex workflows, dedicated support, customization

---

## Free Tier Prompts (8 Total)

### Simple Category (4 prompts)
All simple prompts are free to demonstrate immediate value:

1. **code-debugging.txt**
   - Use Case: Quick code fixes
   - Value: Immediate problem solving
   - User Segment: Developers

2. **meeting-notes.txt**
   - Use Case: Meeting documentation
   - Value: Time savings
   - User Segment: Business professionals

3. **strict-data-analysis.txt**
   - Use Case: Factual data analysis
   - Value: Objective insights
   - User Segment: Analysts

4. **text-review.txt**
   - Use Case: Writing improvement
   - Value: Quality enhancement
   - User Segment: Content creators

### Work Prompts Category (2 prompts)
Selected to showcase enterprise capabilities:

5. **copilot-chat-summary**
   - Use Case: Meeting summaries
   - Value: Quick recaps
   - User Segment: Microsoft 365 users

6. **data-analyst-sap** (Basic version)
   - Use Case: SAP data queries
   - Value: Introduction to SAP prompts
   - User Segment: SAP users

### Fun Category (2 prompts)
Educational and creative prompts:

7. **gpt4o-job-interview.txt**
   - Use Case: Interview preparation
   - Value: Career development
   - User Segment: Job seekers

8. **wargame-master** (Limited version)
   - Use Case: Game facilitation
   - Value: Entertainment
   - User Segment: Gamers

---

## Premium Tier Prompts (10 Total)

### Work Prompts (6 prompts)
Professional enterprise tools:

1. **sap-assistant.txt**
   - Value: Complete SAP S/4HANA data extraction
   - Pricing Justification: Saves hours of manual work
   - Target: Enterprise SAP users
   - ROI: $5,000+ annually in time savings

2. **Snowflake-sql.md**
   - Value: Advanced Snowflake query assistance
   - Pricing Justification: Reduces query development time by 60%
   - Target: Data engineers and analysts
   - ROI: $3,000+ annually

3. **servicenow-rfc.md**
   - Value: Complete RFC generation following ITIL standards
   - Pricing Justification: Reduces RFC creation time from 2 hours to 15 minutes
   - Target: IT change managers
   - ROI: $2,000+ annually

4. **copilot_settings.md**
   - Value: Advanced Microsoft Copilot configuration
   - Pricing Justification: Optimizes Copilot for enterprise use
   - Target: Microsoft 365 admins
   - ROI: Improved team productivity

5. **copilot-session**
   - Value: Structured Copilot interaction workflows
   - Pricing Justification: Maximizes Copilot effectiveness
   - Target: Power users
   - ROI: 30% productivity increase

6. **technical-meeting-notes**
   - Value: Technical documentation from meetings
   - Pricing Justification: Creates publishable technical docs
   - Target: Technical writers, engineers
   - ROI: $1,500+ annually

### Stocks (1 prompt)

7. **company-investigator**
   - Value: Comprehensive corporate due diligence
   - Pricing Justification: Professional research would cost $500-2,000 per company
   - Target: Investors, analysts, researchers
   - ROI: Replaces expensive research services

### Fun (1 prompt)

8. **meta_prompter.txt**
   - Value: Professional prompt engineering training
   - Pricing Justification: Equivalent to $200+ course
   - Target: Prompt engineers, developers
   - ROI: Skill development worth thousands

### Agentic (2 prompts)

9. **dynamic-cheatsheet-prompter.txt**
   - Value: Dynamic learning assistant
   - Pricing Justification: Adaptive learning system
   - Target: Students, professionals learning new skills
   - ROI: Accelerated learning

10. **ICL-baseline.txt**
    - Value: In-context learning framework
    - Pricing Justification: Advanced AI interaction methodology
    - Target: AI researchers, advanced users
    - ROI: Research efficiency

---

## Enterprise Tier Prompts (3 Total + Custom)

### Agentic Category (1 prompt)

1. **domain-specific-prompter.txt**
   - Value: Autonomous agent framework with proven strategies
   - Pricing: $5,000/year + implementation support
   - Requirements: API integrations, customization
   - Target: Enterprises automating workflows
   - ROI: $50,000+ annually in automation savings
   - Support: Dedicated implementation assistance

### Work Prompts (2 prompts)

2. **copilot-it-agent**
   - Value: Complete IT automation agent
   - Pricing: $8,000/year + support
   - Requirements: Enterprise Copilot license, customization
   - Target: IT departments
   - ROI: $100,000+ in labor cost savings
   - Support: Integration consulting, training

3. **copilot-pbi-dashboard**
   - Value: Power BI automation and insights
   - Pricing: $6,000/year + support
   - Requirements: Power BI Pro/Premium, customization
   - Target: Business intelligence teams
   - ROI: $30,000+ annually
   - Support: Dashboard design, optimization

### Custom Development (Not in repository)

4. **Custom Prompt Development**
   - Value: Bespoke prompts for specific use cases
   - Pricing: $2,000-10,000 per prompt
   - Includes: Discovery, development, testing, documentation
   - Support: Ongoing updates and optimization

---

## Pricing Model

### Individual Plans

**Free Tier**
- Cost: $0
- Access: 8 free prompts
- Updates: Community updates only
- Support: Community forums

**Professional**
- Cost: $29/month or $299/year (save $49)
- Access: All 10 premium prompts
- Updates: Regular monthly updates
- Support: Email support (48-hour response)
- Bonus: Early access to new prompts

**Professional Plus**
- Cost: $99 one-time (lifetime access)
- Access: All 10 premium prompts (current)
- Updates: Major version updates for 2 years
- Support: Community support
- Note: New prompts added after purchase may require upgrade

### Team Plans

**Team (5 users)**
- Cost: $99/month or $999/year
- Access: All free + premium prompts
- Updates: Priority updates
- Support: Priority email support (24-hour response)
- Features: Team workspace, usage analytics

**Enterprise (Unlimited users)**
- Cost: Custom (starting at $5,000/year)
- Access: Everything + enterprise tier prompts
- Updates: Custom development included
- Support: Dedicated account manager, SLA
- Features: SSO, audit logs, custom integrations, training

---

## Access Control Implementation

### GitHub Repository Structure

```
/free/           <- Public access
  /simple/
  /work/
  /fun/

/premium/        <- Requires authentication/payment
  /work/
  /stocks/
  /fun/
  /agentic/

/enterprise/     <- Custom access only
  /agentic/
  /work/
  /custom/
```

### Future Platform Features

When web platform launches:
- User authentication system
- Subscription management
- Download tracking
- Usage analytics
- Team collaboration tools
- Version control for prompts
- Custom prompt requests

---

## Tier Migration Policy

### Moving Prompts Between Tiers

**Free → Premium:**
- Allowed for prompts that gain significant enhancements
- Provide 90-day notice to existing users
- Maintain basic version in free tier
- Example: Basic SAP query prompt (free) vs. Full SAP assistant (premium)

**Premium → Free:**
- Allowed to increase adoption or deprecate
- Can be used as marketing strategy
- Notify premium subscribers with bonus content
- Example: Older premium prompts moved to free when v2.0 launches

**Premium → Enterprise:**
- Only for prompts requiring significant support/customization
- Maintain simplified version in premium
- Notify users 30 days before migration

### Version Control

- Free tier: Major versions only (1.0, 2.0, 3.0)
- Premium tier: All updates (1.0, 1.1, 1.2, etc.)
- Enterprise tier: Custom versions + all updates

---

## Value Justification

### Why Users Should Pay

**Premium Tier Value:**
- Average time savings: 5-10 hours/month
- Hourly value at $50/hour: $250-500/month
- Subscription cost: $29/month
- **ROI: 860% - 1,720%**

**Enterprise Tier Value:**
- Average time savings: 20-40 hours/month per team
- Team of 10 at $75/hour: $15,000-30,000/month
- Enterprise cost: $5,000/year ($417/month)
- **ROI: 3,600% - 7,200%**

### Competitive Comparison

| Feature | Our Platform | PromptBase | ChatGPT Plus | Consultant |
|---------|--------------|------------|--------------|------------|
| Cost | $29/mo | $9-49/prompt | $20/mo | $150+/hour |
| Prompts | 10 premium | 1 per purchase | 0 (just access) | Custom |
| Updates | Included | None | N/A | Hourly rate |
| Support | Email | None | Limited | Included |
| **Value** | **Best** | One-time | Basic | Expensive |

---

## Future Tier Additions

### Planned Expansions

**Q1 2026:**
- Add 15 new premium prompts
- Launch 5 industry-specific collections
- Introduce API access tier ($49/month)

**Q2 2026:**
- Educational tier for students ($9/month)
- Agency tier for consultants ($199/month, white-label)
- Marketplace for community prompts (revenue share)

**Q3 2026:**
- Mobile app access tier
- AI-powered prompt generator (premium feature)
- Custom workspace tier ($149/month)

---

## Metrics & KPIs

### Track for Each Tier

**Free Tier:**
- Total downloads
- User registrations
- Conversion rate to premium
- Most popular prompts
- User feedback ratings

**Premium Tier:**
- Monthly Recurring Revenue (MRR)
- Churn rate
- Average Customer Lifetime Value (LTV)
- Usage frequency
- Feature requests

**Enterprise Tier:**
- Annual Contract Value (ACV)
- Customer satisfaction score (CSAT)
- Support ticket volume
- Renewal rate
- Expansion revenue

---

## Summary

- **Free Tier (8 prompts):** Attract and demonstrate value
- **Premium Tier (10 prompts):** Core revenue, professional tools
- **Enterprise Tier (3+ prompts):** High-value accounts, custom solutions

**Total Prompts:** 21 existing + future additions
**Revenue Potential:** $50,000-170,000 Year 1

Next steps:
1. Implement access control system
2. Set up payment processing
3. Launch with free tier
4. Market premium tier
5. Build enterprise pipeline

---

**Last Review:** October 27, 2025
**Next Review:** November 27, 2025
**Owner:** Repository maintainer
