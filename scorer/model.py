"""Predictive Lead Scoring Engine for ERPNext CRM."""

from typing import Dict, Any, List
from pydantic import BaseModel


class LeadData(BaseModel):
    lead_name: str
    company_size: str  # 1-10, 11-50, 51-200, 200+
    industry: str
    source: str  # Website, Referral, Cold Call, Campaign
    email_opened_count: int = 0
    meetings_scheduled: int = 0
    has_custom_domain: bool = True


class LeadScoreResult(BaseModel):
    lead_name: str
    score: int  # 0 to 100
    tier: str  # Hot, Warm, Cold
    conversion_probability: float
    factors: List[str]


class LeadScoringEngine:
    """Calculates lead qualification probability."""

    INDUSTRY_WEIGHTS = {
        "Manufacturing": 20,
        "Information Technology": 25,
        "Real Estate": 20,
        "Retail": 15,
        "Healthcare": 18,
    }

    SIZE_WEIGHTS = {
        "200+": 25,
        "51-200": 20,
        "11-50": 15,
        "1-10": 10,
    }

    SOURCE_WEIGHTS = {
        "Referral": 25,
        "Website": 20,
        "Campaign": 15,
        "Cold Call": 5,
    }

    def score_lead(self, lead: LeadData) -> LeadScoreResult:
        score = 0
        factors = []

        # 1. Industry Fit
        ind_score = self.INDUSTRY_WEIGHTS.get(lead.industry, 10)
        score += ind_score
        factors.append(f"Industry fit ({lead.industry}): +{ind_score}")

        # 2. Company Size
        size_score = self.SIZE_WEIGHTS.get(lead.company_size, 10)
        score += size_score
        factors.append(f"Company scale ({lead.company_size}): +{size_score}")

        # 3. Inbound Source
        src_score = self.SOURCE_WEIGHTS.get(lead.source, 10)
        score += src_score
        factors.append(f"Channel origin ({lead.source}): +{src_score}")

        # 4. Behavioral Engagement
        if lead.meetings_scheduled > 0:
            meeting_pts = min(20, lead.meetings_scheduled * 10)
            score += meeting_pts
            factors.append(f"Meeting booked: +{meeting_pts}")

        if lead.email_opened_count >= 3:
            score += 10
            factors.append("High email engagement: +10")

        final_score = min(score, 100)

        if final_score >= 75:
            tier = "Hot"
        elif final_score >= 50:
            tier = "Warm"
        else:
            tier = "Cold"

        return LeadScoreResult(
            lead_name=lead.lead_name,
            score=final_score,
            tier=tier,
            conversion_probability=round(final_score / 100.0, 2),
            factors=factors,
        )
