import datetime
from sqlalchemy.orm import Session
from app.models.intelligence import IntelligenceSource, NewsCluster, GlobalAlert, RegionCommandProfile

def seed_intelligence_data(db: Session):
    if db.query(RegionCommandProfile).first():
        return

    # 1. Region Command Profiles (Section 8 & 67)
    regions = [
        RegionCommandProfile(
            region_id="middle-east",
            name="Middle East & Levant",
            current_situation="Intense military confrontation across southern Lebanon, Gaza, and the Red Sea corridor. Civilian displacement exceeding 1.2 million with severe degradation of basic municipal infrastructure.",
            france_historical_role="France holds deep historical ties to Lebanon dating from the 1920 Mandate, co-drafted S/RES/1701 in 2006, and acts as a historic Western bridge to Arab capitals.",
            france_current_relevance="Over 700 French UNIFIL peacekeepers deployed along the Blue Line. France is a key humanitarian conference convener and penholder on Lebanese stability.",
            unsc_involvement_summary="Subject of frequent P5 polarization; repeated US, Russian, and Chinese vetoes on ceasefire and humanitarian draft resolutions.",
            escalation_risks=["Direct regional interstate conflict", "Cross-border strikes on UN peacekeeper positions", "Disruption of Suez maritime shipping"],
            deescalation_opportunities=["Phased ceasefire tied to hostage release", "Buffer enforcement under S/RES/1701 revitalization", "EU-Arab League reconstruction trust fund"],
            humanitarian_status="Catastrophic in urban pockets; famine risk high under blockade.",
            economic_dimension="Red Sea shipping detours increasing European freight costs by 35%.",
            legal_dimension="Application of Geneva Conventions, Article 51 self-defense boundaries, and ICJ provisional orders.",
            major_actors=[
                {"name": "Israel", "role": "Primary belligerent"},
                {"name": "Lebanese Armed Forces", "role": "State security pillar"},
                {"name": "Hezbollah", "role": "Non-state armed actor"},
                {"name": "UNIFIL", "role": "Peacekeeping buffer"}
            ],
            key_resolutions=["S/RES/1701 (2006)", "S/RES/2728 (2024)", "S/RES/2722 (2024)"],
            coordinates={"lat": 33.8938, "lng": 35.5018, "zoom": 5.2}
        ),
        RegionCommandProfile(
            region_id="eastern-europe",
            name="Eastern Europe & Black Sea",
            current_situation="High-intensity conventional conflict along eastern frontlines; critical infrastructure strikes; Black Sea grain shipping corridor under naval surveillance.",
            france_historical_role="Normandy Format co-mediator (France, Germany, Ukraine, Russia); proponent of European strategic autonomy and EU defense integration.",
            france_current_relevance="P5 nuclear guarantor; major supplier of SCALP missiles and Caesar howitzers; proponent of Ukrainian sovereignty within 1991 borders.",
            unsc_involvement_summary="Complete P5 structural deadlock due to Russian veto; frequent referral to General Assembly Emergency Special Sessions under 'Uniting for Peace'.",
            escalation_risks=["Spillover into NATO airspace", "Nuclear safety incidents at Zaporizhzhia", "Naval mining of maritime export corridors"],
            deescalation_opportunities=["IAEA nuclear safety buffer zones", "Prisoner-of-war exchanges under third-party auspices", "Black Sea civilian shipping protections"],
            humanitarian_status="Severe winter heating vulnerabilities; millions of refugees across EU member states.",
            economic_dimension="Global grain and fertilizer market volatility.",
            legal_dimension="UN Charter Article 2(4) territorial integrity prohibition and Article 51 collective self-defense.",
            major_actors=[
                {"name": "Ukraine", "role": "Sovereign state defending territory"},
                {"name": "Russian Federation", "role": "P5 belligerent"},
                {"name": "IAEA", "role": "Nuclear regulatory oversight"}
            ],
            key_resolutions=["S/RES/2202 (2015)", "UNGA A/RES/ES-11/1 (2022)"],
            coordinates={"lat": 48.3794, "lng": 31.1656, "zoom": 4.8}
        ),
        RegionCommandProfile(
            region_id="sub-saharan-africa",
            name="Sub-Saharan Africa & Sahel",
            current_situation="Expansion of jihadist insurgencies across the Liptako-Gourma tri-border; succession of military transitions in Mali, Burkina Faso, and Niger; humanitarian displacement.",
            france_historical_role="Historical bilateral defense agreements; Operation Serval and Barkhane legacy; historic penholder for Sahel resolutions in the UNSC.",
            france_current_relevance="Recalibration toward civilian development, EU multilateral partnerships, and supporting ECOWAS/AU regional leadership.",
            unsc_involvement_summary="Termination of MINUSMA; Russian PMC expansion; A3 member states pushing for predictable African Union peace funding.",
            escalation_risks=["Insurgent advance toward coastal West Africa", "Humanitarian corridor collapse", "Foreign mercenary entrenchment"],
            deescalation_opportunities=["AU-ECOWAS coordinated counter-terror architecture", "UN assessed contributions for AU missions under S/RES/2719"],
            humanitarian_status="Acute food insecurity and internal displacement exceeding 3 million.",
            economic_dimension="Transit disruption of trans-Saharan trade and critical mineral supplies.",
            legal_dimension="Host-nation consent for peacekeepers; international human rights compliance frameworks.",
            major_actors=[
                {"name": "ECOWAS", "role": "Regional economic community"},
                {"name": "African Union", "role": "Continental peace & security architecture"},
                {"name": "Alliance of Sahel States", "role": "Transition authorities"}
            ],
            key_resolutions=["S/RES/2719 (2023)", "S/RES/2391 (2017)"],
            coordinates={"lat": 14.4974, "lng": -14.4524, "zoom": 4.5}
        )
    ]
    db.add_all(regions)

    # 2. Intelligence Sources with Provenance Labels (Section 6)
    sources = [
        IntelligenceSource(
            source_id="UN-NEWS-2026-0901",
            title="UN Secretary-General Urges Council to Enforce Civilian Protection Along Demarcation Lines",
            publisher="United Nations News",
            source_type="PRIMARY_OFFICIAL",
            url="https://news.un.org/en/story/2026/09/security-council-briefing",
            publication_date=datetime.datetime(2026, 9, 20),
            region="Middle East",
            country="Lebanon",
            topic="Security & Peacekeeping",
            verification_status="VERIFIED FACT",
            confidence_score=0.98,
            summary="Secretary-General delivered formal briefing to the UNSC emphasizing that attacks affecting UN peacekeeper positions directly violate international humanitarian law."
        ),
        IntelligenceSource(
            source_id="FR-DIP-2026-0914",
            title="Quai d'Orsay Communiqué: France Reaffirms Unwavering Commitment to UNIFIL and S/RES/1701",
            publisher="Ministère de l'Europe et des Affaires étrangères",
            source_type="PRIMARY_OFFICIAL",
            url="https://diplomatie.gouv.fr/en/country-files/lebanon/news/article/unifil-mandate-france-statement",
            publication_date=datetime.datetime(2026, 9, 22),
            region="Middle East",
            country="France",
            topic="Diplomatic Statement",
            verification_status="OFFICIAL STATEMENT",
            confidence_score=1.0,
            summary="Permanent Representative of France declared that Paris is actively drafting Council language to guarantee UNIFIL supply corridors and prevent cross-border strikes."
        ),
        IntelligenceSource(
            source_id="ICG-CW-2026-0925",
            title="CrisisWatch Monthly Alert: Escalation Indicators Flash Amber in Eastern Mediterranean Buffer",
            publisher="International Crisis Group",
            source_type="RESEARCH_INSTITUTE",
            url="https://crisisgroup.org/crisiswatch/september-2026-alerts",
            publication_date=datetime.datetime(2026, 9, 25),
            region="Middle East",
            country="Regional",
            topic="Conflict Warning",
            verification_status="ANALYSIS",
            confidence_score=0.88,
            summary="Independent field monitoring warns that diplomatic negotiations in New York must outpace military troop mobilizations within 72 hours to prevent multi-front escalation."
        )
    ]
    db.add_all(sources)

    # 3. Global Alerts (Section 50)
    alerts = [
        GlobalAlert(
            alert_type="NEW_UNSC_MEETING",
            severity="CRITICAL",
            headline="France Requests Urgent Consultations of the Security Council on Civilian Protection",
            details="The French Mission has formally invoked Rule 2 of the Provisional Rules of Procedure following artillery strikes in the southern buffer zone.",
            region="Middle East",
            country_code="FRA",
            source_url="https://digitallibrary.un.org/record/4042850",
            active=True
        ),
        GlobalAlert(
            alert_type="HUMANITARIAN_ESCALATION",
            severity="HIGH",
            headline="OCHA Issues Level-3 Emergency Appeal for Frontier Displacement",
            details="Over 60,000 additional residents displaced in 48 hours; medical supply stockpiles depleted.",
            region="Middle East",
            country_code="LBN",
            source_url="https://ochaopt.org",
            active=True
        ),
        GlobalAlert(
            alert_type="DIPLOMATIC_STANDOFF",
            severity="MEDIUM",
            headline="P5 Consultations on Chapter VII Language Reveal Sharp Divergence",
            details="Russia and China signal firm reluctance to accept coercive inspection clauses in draft operative text.",
            region="Global",
            country_code="RUS",
            source_url="https://un.org/press",
            active=True
        )
    ]
    db.add_all(alerts)

    # 4. News Clusters (Section 48 & 49)
    clusters = [
        NewsCluster(
            cluster_title="Southern Buffer Zone Confrontation & UNIFIL Mandate Defense",
            region="Middle East",
            primary_event_summary="Renewed artillery strikes along the international demarcation line have hit civilian logistics depots and threatened UN peacekeeper installations.",
            primary_source_id="UN-NEWS-2026-0901",
            associated_source_ids=["FR-DIP-2026-0914", "ICG-CW-2026-0925"],
            conflicting_reporting="State authorities assert precision drone interception, while field observer reports confirm structural collateral damage to humanitarian corridors.",
            unsc_relevance_notes="Directly challenges compliance with S/RES/1701 and peacekeeper force-protection mandates.",
            france_relevance_notes="France is the primary penholder on Lebanon, contributor of 700 troops, and leading diplomatic mediator."
        )
    ]
    db.add_all(clusters)
    db.commit()
