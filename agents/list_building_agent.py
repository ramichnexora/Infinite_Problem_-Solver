"""AI List Building Agent - specialized for lead collection and email list growth.

This agent focuses on one mandate: build a qualified email list of target customers.
It implements 4 SOPs:
1. source_identification - find high-value lead sources (communities, partnerships, ads)
2. lead_collection - gather emails from identified sources with consent
3. segmentation - organize leads by lifecycle stage (expectant, new parent, established)
4. engagement_planning - draft initial email sequence and nurture strategy

Unlike the marketing agent (which creates content), this agent answers the question:
"Who should we be reaching, and how do we reach them with their permission?"

See: docs/roles/ai-list-building.md (placeholder — this seat will get one if the
team decides to keep it; for now it lives as a specialized sub-seat under sales).
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

SOURCE_IDENTIFICATION_PROMPT = """You are the List Building Agent's source-identification SOP.
Your job: find high-value lead sources for new parents in the US and UK.

High-value sources share three traits:
1. Access to 100+ target people who match the buyer persona (new/expectant parents, solopreneurs, creators, VAs)
2. Trust/authority in their niche (so a mention from them carries weight)
3. Willingness to partner/recommend (not a scrape; they actively send traffic your way)

Examples of high-value sources:
- Facebook groups for new parents (20k+ members each, active)
- OB/GYN clinics & midwife collectives (referral partnerships)
- Postpartum recovery centers
- Parenting blogs/newsletters with engaged audiences
- Creator collectives (YouTube, TikTok parents)
- Mom influencers (5k-50k followers, authentic voice)
- Pregnancy/postpartum podcasts

For each source, provide:
1. Name & type (group, clinic, influencer, etc.)
2. Size (estimated reach in target region)
3. Engagement level (low/med/high)
4. Contact method (DM, email, partner intake form)
5. Proposed ask (recommendation post, guest appearance, affiliate link, referral fee)
6. Estimated leads per month from this source (conservative estimate)

Respond with JSON only, no prose:
{
  "sources": [
    {
      "name": "source name",
      "type": "facebook_group|clinic|influencer|podcast|blog|community",
      "region": ["us", "uk", "both"],
      "estimated_reach": 5000,
      "engagement_level": "high",
      "contact_method": "facebook_dm",
      "proposed_ask": "guest post in group feed recommending Postpartum Sleep Handbook",
      "monthly_leads": 50,
      "confidence": 0.85,
      "notes": "active group, founder is postpartum specialist"
    }
  ],
  "total_estimated_monthly_leads": 250,
  "confidence": 0.75
}
"""

LEAD_COLLECTION_PROMPT = """You are the List Building Agent's lead-collection SOP.
Given a source (Facebook group, influencer, clinic, etc.), your job is to draft a
message/offer/landing-page copy that gets permission-based email signups.

Key rules:
1. Always ask for permission (double opt-in) — no scraped lists
2. Lead magnet must have real value (free guide, email series, tool, template)
3. Capture: email, first name, region (state/province), baby age/due date
4. Tone: friendly, not salesy — match the source's voice

For each source, output:
1. The ask message (DM copy, comment, or guest post intro)
2. Landing page headline & CTA
3. Lead magnet (what's offered free)
4. Email capture form fields
5. Legal/compliance notes (GDPR for UK, CAN-SPAM for US)

Respond with JSON only:
{
  "source_name": "source",
  "message_for_source": "exact text to post/send",
  "landing_page": {
    "headline": "...",
    "subheading": "...",
    "lead_magnet_title": "...",
    "lead_magnet_description": "...",
    "form_fields": ["email", "first_name", "region", "baby_age_or_due_date"],
    "cta_button": "Get Free [Lead Magnet Title]",
    "privacy_notice": "We respect your privacy..."
  },
  "follow_up_email_sequence": {
    "subject_line_1": "Welcome! Here's your [lead magnet]",
    "subject_line_2": "New parents say this changed their sleep...",
    "subject_line_3": "Is the Postpartum Sleep Handbook right for you?"
  },
  "confidence": 0.8,
  "monthly_lead_estimate": 30
}
"""

SEGMENTATION_PROMPT = """You are the List Building Agent's segmentation SOP.
Given a list of new parents (with email, name, location, baby age/due date), your job
is to segment them into lifecycle stages so the right message reaches the right person
at the right time.

Segments:
1. Expectant Parents (pregnant, <6 months to due date)
2. New Parents 0-6 months (baby just arrived, sleep deprivation peak)
3. New Parents 6-12 months (early childhood, sleep training questions)
4. Established Parents (1+ years, toddler phase)

For each lead provided, output:
- Email
- Name
- Segment
- Recommended next email in sequence
- Product recommendation

Respond with JSON only:
{
  "segments": {
    "expectant_parents": [{"email": "...", "name": "...", "due_date": "..."}],
    "new_parents_0_6m": [{"email": "...", "name": "...", "baby_age_months": ...}],
    "new_parents_6_12m": [...],
    "established_parents": [...]
  },
  "by_country": {
    "us": {"total": 0, "segments": {...}},
    "uk": {"total": 0, "segments": {...}}
  },
  "segment_email_recommendations": {
    "expectant_parents": "email_sequence_expecting",
    "new_parents_0_6m": "email_sequence_newborn_survival",
    "new_parents_6_12m": "email_sequence_first_year",
    "established_parents": "email_sequence_toddler"
  }
}
"""

ENGAGEMENT_PLANNING_PROMPT = """You are the List Building Agent's engagement-planning SOP.
Given a list segment (e.g., "new parents 0-6 months"), design a 7-email sequence that
builds trust, teaches real value, and moves them toward purchase.

Structure: Welcome → Value → Story → Problem → Solution → Social proof → Offer

Each email should:
1. Have a clear subject line
2. Open with a hook (problem, question, or insight)
3. Deliver one core lesson or story
4. End with a single CTA
5. Match the brand voice (friendly, practical, no hype)

Respond with JSON only:
{
  "segment": "segment name",
  "email_sequence": [
    {
      "day": 0,
      "subject": "...",
      "preview_text": "...",
      "hook": "...",
      "body_1": "core message",
      "cta": "...",
      "link_destination": "..."
    }
  ],
  "total_sequence_length": 7,
  "expected_open_rate": 0.35,
  "expected_click_rate": 0.08,
  "expected_conversion_to_product": 0.03,
  "confidence": 0.75
}
"""


class ListBuildingAgent(Agent):
    seat = "list_building"

    def source_identification(self, target_audience: str, regions: list[str] | None = None) -> AgentResult:
        """SOP 1 - Identify high-value lead sources.

        Args:
            target_audience: e.g., "new parents", "solopreneurs", "creators"
            regions: list of target regions (us, uk, etc.)
        """
        region_str = ", ".join(regions) if regions else "us, uk"
        user_prompt = f"""Target audience: {target_audience}
Regions: {region_str}

Find 10-15 high-value lead sources we can partner with or run campaigns through.
Focus on quality over quantity - we want sources with engaged, qualified leads."""

        return self.run_sop(
            sop="source_identification",
            system_prompt=SOURCE_IDENTIFICATION_PROMPT,
            user_prompt=user_prompt,
            inputs={"target_audience": target_audience, "regions": regions or []},
            default_tier=Tier.NOTIFY,
        )

    def lead_collection(self, source: dict[str, str]) -> AgentResult:
        """SOP 2 - Draft lead-collection message for a specific source.

        Args:
            source: dict with 'name', 'type', 'region' keys
        """
        user_prompt = f"""Source name: {source.get('name', '')}
Source type: {source.get('type', '')}
Region: {source.get('region', 'us')}

Draft the message, landing page, and email follow-up for collecting emails
from this source with full consent."""

        return self.run_sop(
            sop="lead_collection",
            system_prompt=LEAD_COLLECTION_PROMPT,
            user_prompt=user_prompt,
            inputs={"source": source},
            default_tier=Tier.NOTIFY,
        )

    def segmentation(self, leads: list[dict[str, str]]) -> AgentResult:
        """SOP 3 - Segment leads by lifecycle stage.

        Args:
            leads: list of dicts with email, name, location, baby_age_or_due_date
        """
        leads_str = "\n".join([json.dumps(l) for l in leads[:20]])  # Sample first 20
        user_prompt = f"""Here are {len(leads)} leads collected from our sources.
Segment them by lifecycle stage (expectant, new 0-6m, new 6-12m, established).

Leads (first 20 shown):
{leads_str}

Total leads count: {len(leads)}"""

        return self.run_sop(
            sop="segmentation",
            system_prompt=SEGMENTATION_PROMPT,
            user_prompt=user_prompt,
            inputs={"leads_count": len(leads), "regions": self._extract_regions(leads)},
            default_tier=Tier.NOTIFY,
        )

    def engagement_planning(self, segment: str) -> AgentResult:
        """SOP 4 - Plan email engagement sequence for a segment.

        Args:
            segment: lifecycle segment name (e.g., "new_parents_0_6m")
        """
        user_prompt = f"""Segment: {segment}

Design a 7-email nurture sequence for this segment. Lead with value, build trust,
move toward the Postpartum Sleep Handbook and other guides at the right time."""

        return self.run_sop(
            sop="engagement_planning",
            system_prompt=ENGAGEMENT_PLANNING_PROMPT,
            user_prompt=user_prompt,
            inputs={"segment": segment},
            default_tier=Tier.NOTIFY,
        )

    def _extract_regions(self, leads: list[dict[str, str]]) -> list[str]:
        """Extract unique regions from leads."""
        regions = set()
        for lead in leads:
            location = lead.get("location_country", "").lower()
            if "us" in location or "united states" in location:
                regions.add("us")
            if "uk" in location or "united kingdom" in location:
                regions.add("uk")
        return list(regions)


import json
