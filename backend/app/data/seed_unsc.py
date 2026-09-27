import datetime
from sqlalchemy.orm import Session
from app.models.unsc import UNSCMember, UNSCPresidency, UNSCResolution, UNSCVote, UNSCMeetingRecord, PeacekeepingMission

def seed_unsc_data(db: Session):
    if db.query(UNSCMember).first():
        return # Already seeded

    # 1. P5 & Elected Members
    members = [
        # Permanent 5
        UNSCMember(country_code="FRA", name="France", status="PERMANENT", term_start=1945, term_end=None, region_group="WEOG", has_veto=True, strategic_profile={"doctrine": "European strategic autonomy, multilateralism, international law, civilian protection."}),
        UNSCMember(country_code="USA", name="United States", status="PERMANENT", term_start=1945, term_end=None, region_group="WEOG", has_veto=True, strategic_profile={"doctrine": "Allied security deterrence, counter-terrorism, robust enforcement mechanisms."}),
        UNSCMember(country_code="GBR", name="United Kingdom", status="PERMANENT", term_start=1945, term_end=None, region_group="WEOG", has_veto=True, strategic_profile={"doctrine": "Rules-based international order, E3 coordination, precise legal drafting."}),
        UNSCMember(country_code="RUS", name="Russian Federation", status="PERMANENT", term_start=1945, term_end=None, region_group="Eastern Europe", has_veto=True, strategic_profile={"doctrine": "Westphalian sovereignty, non-intervention, anti-hegemonic balance."}),
        UNSCMember(country_code="CHN", name="China", status="PERMANENT", term_start=1945, term_end=None, region_group="Asia-Pacific", has_veto=True, strategic_profile={"doctrine": "Non-interference, political dialogue, opposes coercive sanctions."}),
        
        # Elected Members 2024-2025
        UNSCMember(country_code="DZA", name="Algeria", status="ELECTED", term_start=2024, term_end=2025, region_group="African Group", has_veto=False, strategic_profile={"doctrine": "Arab and African solidarity, Palestinian rights, decolonization."}),
        UNSCMember(country_code="GUY", name="Guyana", status="ELECTED", term_start=2024, term_end=2025, region_group="GRULAC", has_veto=False, strategic_profile={"doctrine": "Territorial integrity, ICJ adherence, climate security."}),
        UNSCMember(country_code="KOR", name="Republic of Korea", status="ELECTED", term_start=2024, term_end=2025, region_group="Asia-Pacific", has_veto=False, strategic_profile={"doctrine": "Non-proliferation, UN sanctions compliance, cybersecurity."}),
        UNSCMember(country_code="SLE", name="Sierra Leone", status="ELECTED", term_start=2024, term_end=2025, region_group="African Group", has_veto=False, strategic_profile={"doctrine": "A3+1 coordination, transitional justice, African peace architecture."}),
        UNSCMember(country_code="SVN", name="Slovenia", status="ELECTED", term_start=2024, term_end=2025, region_group="Eastern Europe", has_veto=False, strategic_profile={"doctrine": "IHL, protection of civilians, water diplomacy."}),
        
        # Elected Members 2025-2026
        UNSCMember(country_code="DNK", name="Denmark", status="ELECTED", term_start=2025, term_end=2026, region_group="WEOG", has_veto=False, strategic_profile={"doctrine": "Nordic multilateralism, human rights, climate and security nexus."}),
        UNSCMember(country_code="GRC", name="Greece", status="ELECTED", term_start=2025, term_end=2026, region_group="WEOG", has_veto=False, strategic_profile={"doctrine": "Law of the Sea (UNCLOS), maritime safety, Mediterranean peace."}),
        UNSCMember(country_code="PAK", name="Pakistan", status="ELECTED", term_start=2025, term_end=2026, region_group="Asia-Pacific", has_veto=False, strategic_profile={"doctrine": "Self-determination, counter-terrorism, UN peacekeeping contributor."}),
        UNSCMember(country_code="PAN", name="Panama", status="ELECTED", term_start=2025, term_end=2026, region_group="GRULAC", has_veto=False, strategic_profile={"doctrine": "Maritime corridors, migration security, multilateral consensus."}),
        UNSCMember(country_code="SOM", name="Somalia", status="ELECTED", term_start=2025, term_end=2026, region_group="African Group", has_veto=False, strategic_profile={"doctrine": "Counter-insurgency, regional sovereignty, post-conflict stabilization."})
    ]
    db.add_all(members)

    # 2. Presidencies 2026
    presidencies = [
        UNSCPresidency(year=2026, month=1, country_code="FRA", country_name="France", signature_theme="Civilian Protection and Humanitarian Law in Modern Conflicts"),
        UNSCPresidency(year=2026, month=2, country_code="GBR", country_name="United Kingdom", signature_theme="Maritime Security and Global Sea Lines of Communication"),
        UNSCPresidency(year=2026, month=3, country_code="GRC", country_name="Greece", signature_theme="Peaceful Settlement of Maritime Disputes under UNCLOS"),
        UNSCPresidency(year=2026, month=4, country_code="GUY", country_name="Guyana", signature_theme="Impact of Climate Change and Food Insecurity on Global Peace"),
        UNSCPresidency(year=2026, month=5, country_code="PAK", country_name="Pakistan", signature_theme="Safety and Mandate Performance of UN Peacekeepers"),
        UNSCPresidency(year=2026, month=6, country_code="PAN", country_name="Panama", signature_theme="Transnational Organized Crime and Regional Stability")
    ]
    db.add_all(presidencies)

    # 3. Benchmark Resolutions
    res1 = UNSCResolution(
        resolution_number="S/RES/2728 (2024)",
        code="2728",
        title="Immediate Ceasefire in Gaza for the Month of Ramadan",
        date_adopted=datetime.datetime(2024, 3, 25),
        agenda_item="The situation in the Middle East, including the Palestinian question",
        chapter_vii=False,
        operative_summary="Demanded an immediate ceasefire leading to a lasting sustainable ceasefire, the immediate and unconditional release of all hostages, and urgent expansion of humanitarian aid flow.",
        full_text_url="https://undocs.org/S/RES/2728(2024)",
        yes_votes=14,
        no_votes=0,
        abstentions=1, # USA abstained
        outcome="ADOPTED",
        france_vote="YES",
        source_url="https://digitallibrary.un.org/record/4042850"
    )
    res2 = UNSCResolution(
        resolution_number="S/RES/2722 (2024)",
        code="2722",
        title="Condemnation of Attacks on Merchant Vessels in the Red Sea",
        date_adopted=datetime.datetime(2024, 1, 10),
        agenda_item="Maintenance of international peace and security",
        chapter_vii=True,
        operative_summary="Demanded that Houthi militants immediately cease all attacks on merchant and commercial vessels, affirming the right of Member States to defend their vessels in accordance with international law.",
        full_text_url="https://undocs.org/S/RES/2722(2024)",
        yes_votes=11,
        no_votes=0,
        abstentions=4, # RUS, CHN, DZA, MOZ
        outcome="ADOPTED",
        france_vote="YES",
        source_url="https://digitallibrary.un.org/record/4035678"
    )
    res3 = UNSCResolution(
        resolution_number="S/RES/1701 (2006)",
        code="1701",
        title="Cessation of Hostilities in Southern Lebanon & UNIFIL Mandate",
        date_adopted=datetime.datetime(2006, 8, 11),
        agenda_item="The situation in the Middle East (Lebanon)",
        chapter_vii=False,
        operative_summary="Called for full cessation of hostilities, deployment of Lebanese armed forces to southern Lebanon, and expanded UNIFIL to monitor the buffer zone between the Blue Line and the Litani River.",
        full_text_url="https://undocs.org/S/RES/1701(2006)",
        yes_votes=15,
        no_votes=0,
        abstentions=0,
        outcome="ADOPTED",
        france_vote="YES",
        source_url="https://digitallibrary.un.org/record/580665"
    )
    db.add_all([res1, res2, res3])
    db.commit()

    # 4. Votes & Veto records
    vote1 = UNSCVote(
        resolution_id=res1.id,
        draft_symbol="S/2024/254",
        meeting_number="S/PV.9586",
        date=datetime.datetime(2024, 3, 25),
        agenda_item="Middle East",
        country_code="FRA",
        vote="YES",
        is_veto=False,
        explanation_of_vote="France voted in favor because the Council could no longer remain silent on the humanitarian catastrophe, while continuing to call for the release of all hostages.",
        source="https://digitallibrary.un.org/record/4042850"
    )
    vote_veto_rus = UNSCVote(
        resolution_id=None,
        draft_symbol="S/2024/255",
        meeting_number="S/PV.9585",
        date=datetime.datetime(2024, 3, 22),
        agenda_item="Middle East",
        country_code="RUS",
        vote="NO",
        is_veto=True,
        explanation_of_vote="Vetoed US draft on grounds it lacked an unambiguous, immediate ceasefire demand.",
        source="https://digitallibrary.un.org/record/4042810"
    )
    vote_veto_chn = UNSCVote(
        resolution_id=None,
        draft_symbol="S/2024/255",
        meeting_number="S/PV.9585",
        date=datetime.datetime(2024, 3, 22),
        agenda_item="Middle East",
        country_code="CHN",
        vote="NO",
        is_veto=True,
        explanation_of_vote="Vetoed US draft asserting that text set preconditions on halting military operations.",
        source="https://digitallibrary.un.org/record/4042810"
    )
    db.add_all([vote1, vote_veto_rus, vote_veto_chn])

    # 5. Peacekeeping Missions
    pko = [
        PeacekeepingMission(
            acronym="UNIFIL",
            name="United Nations Interim Force in Lebanon",
            country_or_region="Lebanon / Blue Line",
            mandate_summary="Monitor the cessation of hostilities, support Lebanese Armed Forces, and facilitate humanitarian access.",
            current_personnel=10000,
            france_contribution="France provides approx. 700 soldiers (FOB and mobile reserve) and key tactical command.",
            unsc_resolution_basis="S/RES/425 (1978) & S/RES/1701 (2006)",
            status="ACTIVE"
        ),
        PeacekeepingMission(
            acronym="MINUSCA",
            name="United Nations Multidimensional Integrated Stabilization Mission in the Central African Republic",
            country_or_region="Central African Republic",
            mandate_summary="Protection of civilians, support for extension of state authority, disarmament and demobilization.",
            current_personnel=14000,
            france_contribution="Key penholder on the Council; logistical intelligence support and training.",
            unsc_resolution_basis="S/RES/2149 (2014) & S/RES/2709 (2023)",
            status="ACTIVE"
        ),
        PeacekeepingMission(
            acronym="MONUSCO",
            name="United Nations Organization Stabilization Mission in the DRC",
            country_or_region="Democratic Republic of the Congo",
            mandate_summary="Protection of civilians, humanitarian space, support to DDR process in North and South Kivu.",
            current_personnel=12000,
            france_contribution="Penholder in the Security Council, championing responsible phased transition.",
            unsc_resolution_basis="S/RES/1925 (2010) & S/RES/2717 (2023)",
            status="ACTIVE"
        )
    ]
    db.add_all(pko)
    db.commit()
