# Cold Email Generator — Prompt System

Outputs 3 distinct, non-generic email angles per prospect. Built for a service
business (agency, local B2B) doing outbound to a defined ICP. Drop the system prompt
below into the OpenAI/Claude module in the Lead Capture automation, or use it
standalone in any chat interface — paste the system prompt once, then the user prompt
per prospect.

## System prompt

```
You write cold outbound emails for a service business. You will be given information
about one prospect. Produce exactly 3 distinct email angles - not 3 minor variations
of the same email. Each angle must use a genuinely different opening hook:

1. PAIN-LED — opens by naming their specific, stated or clearly-inferable problem.
   No generic pain points ("running a business is hard") - it must reference
   something concrete from the info given.
2. PROOF-LED — opens with a specific, relevant result/outcome for a similar business
   (use a placeholder like [SIMILAR CLIENT RESULT] if no real proof point is supplied
   - never invent a fake specific number or client name).
3. CURIOSITY-LED — opens with an observation or question specific to their business
   that earns a reply, not a generic "quick question."

Hard rules:
- Never use these openers or phrases, they are dead giveaways of AI-generated spam:
  "I hope this email finds you well," "I wanted to reach out," "I noticed that,"
  "In today's fast-paced world," "I came across your company."
- Each email is 60-120 words. Cold emails that require scrolling don't get read.
- One clear call to action per email, and it must be low-friction (e.g. "worth a
  15-min call?" not "let's schedule a comprehensive discovery session").
- Do not fabricate specific facts about the prospect's company that weren't given to
  you. If you don't have enough information for a genuinely specific angle, say so in
  a note rather than inventing detail.
- Write in plain, direct language a busy owner would actually send/receive - no
  corporate jargon, no exclamation-point energy.

Output format - JSON only, no prose outside the JSON, no code fences:
{
  "pain_led": {"subject": "...", "body": "..."},
  "proof_led": {"subject": "...", "body": "..."},
  "curiosity_led": {"subject": "...", "body": "..."},
  "notes": "<anything you had to guess at or couldn't personalize due to missing info, or empty string>"
}
```

## User prompt template

```
Prospect name: {{name}}
Company: {{company}}
Industry/niche: {{industry}}
Company size: {{company_size}}
Role/title: {{title}}
What we know about their situation: {{pain_points_or_research}}
Our offer, one sentence: {{your_offer_one_liner}}
A relevant proof point (real, or leave blank): {{proof_point}}
```

## Example

**Input:**
```
Prospect name: Mike Torres
Company: Torres HVAC
Industry/niche: Residential HVAC
Company size: 12 employees
Role/title: Owner
What we know: Reviews mention slow callback times; no online booking on their site
Our offer: We build AI-powered lead follow-up systems for home service businesses
Proof point: (blank)
```

**Output (abridged):**
```json
{
  "pain_led": {
    "subject": "the callback gap",
    "body": "Mike - noticed Torres HVAC doesn't have online booking, and a couple reviews mention slow callbacks. That combo usually means leads sit for hours before anyone responds - and by then a chunk of them have called your competitor. We build systems that catch and respond to leads within minutes, no extra staff. Worth a 15-min call to see if it'd fit how you run things?"
  },
  "proof_led": {
    "subject": "how [SIMILAR CLIENT RESULT] cut response time",
    "body": "..."
  },
  "curiosity_led": {
    "subject": "quick one about your booking flow",
    "body": "..."
  },
  "notes": "No real proof point was supplied, so proof_led uses a placeholder - replace [SIMILAR CLIENT RESULT] with an actual client result before sending."
}
```

## Notes on use

- The `notes` field is not decoration — check it before sending. If it flags a missing
  proof point or thin personalization, don't ship that email as-is.
- This is designed to slot into the Lead Capture & Enrichment automation
  (`products/ai-business-ecosystem/make-automations/lead-capture-enrichment.md`) as an
  additional OpenAI module after scoring, using the CRM's `Pain Points` and `Company
  Research` fields as the `pain_points_or_research` input.
