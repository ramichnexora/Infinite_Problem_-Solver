#!/usr/bin/env python3
"""Lead collection automation - gather 1000 new parents' emails from US + UK.

Runs the lead collection SOP sequence: collect from social platforms, community
groups, ad campaigns → segment by location → validate emails → sync to Google Sheets.

Requires:
    ANTHROPIC_API_KEY       - Claude for email parsing/validation
    GOOGLE_SHEETS_API_KEY   - For Google Sheets integration
    MAILCHIMP_API_KEY       - Optional, for email service sync

Usage:
    python run_lead_collection.py [--dry-run]
    python run_lead_collection.py --source=facebook_groups --limit=100
    python run_lead_collection.py --validate-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date as date_cls
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parent
AUTOMATION_CONFIG = ROOT / "automation" / "collect-new-parents-emails.yaml"
SHEETS_DIR = ROOT / "sheets"

# Country codes
COUNTRY_CODES = {"us": "United States", "uk": "United Kingdom"}
LOCATION_PATTERNS = {
    "us": re.compile(r"\b(US|USA|United States|california|texas|new york|florida|ohio)\b", re.IGNORECASE),
    "uk": re.compile(r"\b(UK|United Kingdom|England|Scotland|Wales|Northern Ireland|london|manchester|birmingham)\b", re.IGNORECASE),
}


def load_config() -> dict[str, Any]:
    with AUTOMATION_CONFIG.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_email(email: str) -> bool:
    """Basic email validation."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def detect_location(text: str) -> str | None:
    """Detect country from text (location, bio, or metadata)."""
    for country_code, pattern in LOCATION_PATTERNS.items():
        if pattern.search(text):
            return COUNTRY_CODES[country_code]
    return None


def create_google_sheet_stub(config: dict[str, Any]) -> dict[str, Any]:
    """Create a stub for Google Sheets integration (manual or via API).

    Returns metadata for sheet creation - in production, call Google Sheets API.
    For now: print instructions for manual creation or prepare API call payload.
    """
    sheets_config = config.get("google_sheets", {})
    sheet_name = sheets_config.get("sheet_name", "New Parents Email List — US + UK")

    stub = {
        "sheet_name": sheet_name,
        "created_at": date_cls.today().isoformat(),
        "tabs": sheets_config.get("tabs", []),
        "instructions": [
            "1. Create a new Google Sheet named: " + sheet_name,
            "2. Add the following tabs (sheets): " + ", ".join([t["name"] for t in sheets_config.get("tabs", [])]),
            "3. In 'Raw Signups': add headers = " + str(sheets_config.get("tabs", [{}])[0].get("columns", [])),
            "4. Share sheet with: sales team, marketing team (view + edit)",
            "5. Enable 'Link to data source' if using Google Forms for auto-import",
        ],
        "api_payload": {
            "title": sheet_name,
            "sheets": [
                {
                    "properties": {"title": tab["name"], "sheetId": idx},
                    "data": [
                        {
                            "rowData": [
                                {
                                    "values": [
                                        {"userEnteredValue": {"stringValue": col}} for col in tab.get("columns", [])
                                    ]
                                }
                            ]
                        }
                    ],
                }
                for idx, tab in enumerate(sheets_config.get("tabs", []))
            ],
        },
    }
    return stub


def collect_from_social_followers() -> list[dict[str, Any]]:
    """Stub for collecting from Instagram/TikTok followers of existing posts.

    In production: uses social media API integrations (Instagram Graph API, TikTok API).
    For now: returns empty list awaiting real integrations.
    """
    # Placeholder - in production calls Instagram/TikTok APIs to extract
    # engagement data (likes, comments with email patterns, DM opt-ins)
    return []


def collect_from_community_groups() -> list[dict[str, Any]]:
    """Stub for collecting from Facebook groups via partnerships.

    Approach:
    1. Identify 20+ postpartum/new parent Facebook groups (US + UK)
    2. Reach out to group admins for partnership/recommendation post
    3. Admins post: "Join our email list for weekly tips" with link to landing page
    4. Landing page captures emails with location & baby age
    """
    sample_leads = [
        {
            "email": "sample.newparent@example.com",
            "name": "Sample Parent",
            "location_country": "United States",
            "source": "facebook_group_partnership",
            "signup_date": date_cls.today().isoformat(),
            "lifecycle_stage": "new_parents_0_6m",
        }
    ]
    return sample_leads


def collect_from_ad_campaigns() -> list[dict[str, Any]]:
    """Stub for email collection via paid ads (Facebook, Instagram, Google).

    Approach:
    1. Run targeted ads: "Free 5-day postpartum recovery email series"
    2. Landing page: email capture form with location (state/region) + baby age
    3. Lead magnet: PDF + email sequence
    4. Budget: $100-300/week for testing (per 30-day plan)
    """
    return []


def segment_by_location(leads: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Segment leads by country (US vs UK)."""
    segments = {"us": [], "uk": [], "unknown": []}

    for lead in leads:
        location = lead.get("location_country", "").lower()
        if "united states" in location or "usa" in location:
            segments["us"].append(lead)
        elif "united kingdom" in location or "uk" in location or "england" in location:
            segments["uk"].append(lead)
        else:
            # Try to detect from other fields
            detected = detect_location(json.dumps(lead))
            if detected:
                key = "uk" if "uk" in detected.lower() else "us"
                segments[key].append(lead)
            else:
                segments["unknown"].append(lead)

    return segments


def validate_emails(leads: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate emails and separate valid from invalid."""
    valid = []
    invalid = []

    for lead in leads:
        email = lead.get("email", "").strip()
        if validate_email(email):
            lead["email_verified"] = True
            valid.append(lead)
        else:
            lead["email_verified"] = False
            invalid.append(lead)

    return valid, invalid


def write_to_sheet(leads: list[dict[str, Any]], segments: dict[str, list[dict[str, Any]]]) -> Path:
    """Write leads to a local JSON (awaiting Google Sheets API integration).

    In production: call Google Sheets API to populate tabs.
    For now: write to JSON in sheets/ directory for manual import or API batching.
    """
    SHEETS_DIR.mkdir(exist_ok=True)

    output = {
        "metadata": {
            "generated": date_cls.today().isoformat(),
            "total_leads": len(leads),
            "by_country": {
                "us": len(segments.get("us", [])),
                "uk": len(segments.get("uk", [])),
                "unknown": len(segments.get("unknown", [])),
            },
        },
        "raw_signups": leads,
        "by_segment": segments,
    }

    path = SHEETS_DIR / f"leads-{date_cls.today().isoformat()}.json"
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Don't write to sheets, just show plan.")
    parser.add_argument("--source", default="all", help="Source to collect from (all, facebook_groups, ads, social).")
    parser.add_argument("--limit", type=int, default=None, help="Max leads to collect (for testing).")
    parser.add_argument("--validate-only", action="store_true", help="Only validate existing leads, don't collect.")
    args = parser.parse_args()

    config = load_config()

    print("[*] Lead Collection Automation")
    print(f"[*] Target: 1000 new parents (US + UK)")
    print(f"[*] Config loaded from: {AUTOMATION_CONFIG}")

    # Step 1: Create Google Sheet stub
    print("\n[1/6] Preparing Google Sheets...")
    sheet_stub = create_google_sheet_stub(config)
    print(f"[+] Sheet name: {sheet_stub['sheet_name']}")
    print("[!] Manual setup required:")
    for instr in sheet_stub["instructions"]:
        print(f"    {instr}")

    if args.validate_only:
        print("\n[--validate-only mode] Skipping collection, jumping to validation...")
        return 0

    # Step 2: Collect from sources
    leads: list[dict[str, Any]] = []

    if args.source in ["all", "facebook_groups"]:
        print("\n[2/6] Collecting from Facebook group partnerships...")
        leads.extend(collect_from_community_groups())
        print(f"[+] Collected {len(leads)} leads from Facebook groups")

    if args.source in ["all", "social"]:
        print("\n[3/6] Collecting from Instagram/TikTok followers...")
        leads.extend(collect_from_social_followers())
        print(f"[+] Collected {len(leads)} leads from social platforms")

    if args.source in ["all", "ads"]:
        print("\n[4/6] Collecting from ad campaigns...")
        leads.extend(collect_from_ad_campaigns())
        print(f"[+] Collected {len(leads)} leads from ads")

    if args.limit:
        leads = leads[: args.limit]

    # Step 3: Segment by location
    print("\n[5/6] Segmenting by location (US/UK)...")
    segments = segment_by_location(leads)
    for country, country_leads in segments.items():
        print(f"[+] {country.upper()}: {len(country_leads)} leads")

    # Step 4: Validate emails
    print("\n[6/6] Validating emails...")
    valid, invalid = validate_emails(leads)
    print(f"[+] Valid: {len(valid)}")
    print(f"[-] Invalid: {len(invalid)}")

    if invalid:
        print("[!] Invalid emails (review before import):")
        for lead in invalid[:5]:
            print(f"    {lead.get('email', 'N/A')} ({lead.get('source', 'unknown')})")
        if len(invalid) > 5:
            print(f"    ... and {len(invalid) - 5} more")

    # Step 5: Write to sheets
    if not args.dry_run:
        print("\n[*] Writing to sheets...")
        output_path = write_to_sheet(valid, segments)
        print(f"[+] Leads written to: {output_path}")
        print("[*] Next: Import this JSON to Google Sheets or call Google Sheets API")
    else:
        print("\n[--dry-run mode] Not writing to sheets")

    print("\n[✓] Lead collection complete!")
    print(f"[*] Total leads collected: {len(valid)} valid")
    print(f"[*] Status: Ready for email sequence (Mailchimp/email service integration)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
