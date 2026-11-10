"""Unit tests for LeadScoringEngine."""

from scorer.model import LeadScoringEngine, LeadData


def test_hot_lead_scoring():
    engine = LeadScoringEngine()
    lead = LeadData(
        lead_name="TechCorp India",
        company_size="200+",
        industry="Information Technology",
        source="Referral",
        meetings_scheduled=2,
        email_opened_count=5,
    )
    res = engine.score_lead(lead)
    assert res.score >= 80
    assert res.tier == "Hot"
    assert res.conversion_probability >= 0.8


def test_cold_lead_scoring():
    engine = LeadScoringEngine()
    lead = LeadData(
        lead_name="Random Retail Shop",
        company_size="1-10",
        industry="Retail",
        source="Cold Call",
        meetings_scheduled=0,
        email_opened_count=0,
    )
    res = engine.score_lead(lead)
    assert res.score < 50
    assert res.tier == "Cold"
