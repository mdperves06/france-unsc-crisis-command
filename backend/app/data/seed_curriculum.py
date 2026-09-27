from sqlalchemy.orm import Session
from app.models.training import TrainingCurriculumModule

MODULES_DATA = [
    (1, "France in the UNSC: Historical Mandate & Permanent Seat", "Foundation",
     "The constitutional role of France as a founding member and permanent member of the Security Council under Article 23.",
     "Article 23 & 24 UN Charter; balancing P5 responsibility with independent Gaullist multilateralism.",
     [{"case": "1945 San Francisco Conference", "notes": "Securing permanent seat and French language equality."}]),
    
    (2, "France's Diplomatic Institutions: Quai d'Orsay & The Permanent Mission", "Foundation",
     "How the French Ministry of Europe and Foreign Affairs (Quai d'Orsay) formulates instructions for the Mission at 885 Second Avenue, New York.",
     "Inter-ministerial crisis cells, SGDSN, and instructions pipeline from the Élysée to New York.",
     [{"case": "Crisis Cell Operations", "notes": "24/7 coordination between Paris desk officers and UN negotiators."}]),
     
    (3, "France's UN Diplomacy: The Independent Bridge-Builder", "Foundation",
     "France's unique role as a Western P5 power capable of dialogue with the Global South, China, and the Arab world.",
     "European strategic autonomy, multilateralism, and adherence to international legality.",
     [{"case": "2003 Iraq Crisis", "notes": "Dominique de Villepin speech defending UN inspections and the Charter."}]),

    (4, "France and International Law: The Charter as Red Line", "Foundation",
     "French insistence on strict legal grounding: Chapter VI vs Chapter VII, Article 51 self-defense, and IHL.",
     "Geneva Conventions, Rome Statute of the ICC, and Universal Declaration of Human Rights.",
     [{"case": "R2P Adoption (2005)", "notes": "France championing the Responsibility to Protect civilian populations."}]),

    (5, "France and EU Diplomacy: European Consensus in New York", "Foundation",
     "Article 34 of the Treaty on European Union (TEU): France defending European interests on the Security Council.",
     "Coordination with EU Delegations, non-permanent European members, and the High Representative.",
     [{"case": "EU Article 34 Briefings", "notes": "France briefing EU member states weekly in New York."}]),

    (6, "France and NATO: Allied Deterrence vs Strategic Autonomy", "Foundation",
     "Navigating NATO Article 5 commitments while preserving independent sovereign decision-making.",
     "UN Charter Article 52-54 regional arrangements and collective defense.",
     [{"case": "1966 Gaullist Withdrawal & 2009 Reintegration", "notes": "Maintaining independent nuclear deterrent and command."}]),

    (7, "France in Africa: Penholdership, Partnership, and Reform", "Regional",
     "France's role as traditional penholder on Francophone Africa (Mali, CAR, DRC) and transitioning to AU-led solutions.",
     "S/RES/2719 financing for AU peace operations; respect for African Union Peace and Security Council.",
     [{"case": "MINUSCA in CAR", "notes": "Drafting resolutions stabilizing Bangui and supporting elections."}]),

    (8, "France in the Middle East: Lebanon, Levant, and the Arab League", "Regional",
     "Historic protective relationship with Lebanon, support for two-state solution, and maritime security in the Persian Gulf.",
     "S/RES/1701, S/RES/242, and diplomatic demarches with Gulf Cooperation Council partners.",
     [{"case": "2006 Lebanon War", "notes": "France and US co-drafting S/RES/1701 deploying UNIFIL."}]),

    (9, "France in the Indo-Pacific: Maritime Law and Sovereignty", "Regional",
     "France as an Indo-Pacific nation with 1.6 million citizens in overseas territories (Réunion, Mayotte, New Caledonia, Polynesia).",
     "UNCLOS freedom of navigation, rules-based maritime order, and dialogue with ASEAN and Quad.",
     [{"case": "South China Sea Demarches", "notes": "Joint E3 diplomatic statements on UNCLOS compliance."}]),

    (10, "France-US Relations: Transatlantic Partnership and Divergence", "Mechanisms",
     "Collaborating as P3 allies while standing firm when American positions bypass international consensus.",
     "Article 51 interpretations, sanctions design, and NATO coordination.",
     [{"case": "2013 Syria Red Line", "notes": "Coordination and subsequent recalibration on chemical weapons demarches."}]),

    (11, "France-UK Relations: Lancaster House and P3 Coordination", "Mechanisms",
     "The Lancaster House Treaties, shared European P5 outlook, and daily coordination between London and Paris.",
     "Joint drafting, dividing penholderships, and reciprocal veto deterrence.",
     [{"case": "Libya 2011 (S/RES/1973)", "notes": "Franco-British joint leadership establishing no-fly zone and civilian corridor."}]),

    (12, "France-Russia Relations: Deterrence, Dialogue, and Veto Politics", "Mechanisms",
     "Managing adversarial confrontation post-2022 while keeping diplomatic channels open on non-proliferation.",
     "Anticipating Russian veto triggers, sovereign equality arguments, and negotiating abstentions.",
     [{"case": "Syria Cross-Border Aid Resolutions", "notes": "Protracted negotiations with Moscow on Bab al-Hawa humanitarian corridor."}]),

    (13, "France-China Relations: Economic Leverage and Sovereignty Concerns", "Mechanisms",
     "Engaging Beijing as a non-interference advocate to prevent Chinese vetoes through neutral drafting.",
     "Belt and Road corridors, climate diplomacy, and trade route safety.",
     [{"case": "Mali and Myanmar PRSTs", "notes": "Securing Chinese consensus by avoiding unilateral sanctions language."}]),

    (14, "Humanitarian Diplomacy: France's Guiding Star", "Mechanisms",
     "Pioneering humanitarian corridors, protection of medical personnel (S/RES/2286), and children in armed conflict.",
     "International Humanitarian Law (IHL), ICRC coordination, and emergency OCHA funding.",
     [{"case": "French Veto Limitation Initiative", "notes": "France proposing P5 voluntary suspension of veto during mass atrocities."}]),

    (15, "Sanctions Diplomacy: Targeted Measures vs Collective Harm", "Mechanisms",
     "French doctrine on smart, targeted sanctions (travel bans, asset freezes, arms embargoes) with robust humanitarian carve-outs.",
     "UN Charter Article 41 and General Assembly Resolution 2664 humanitarian exemptions.",
     [{"case": "S/RES/2664 (2022)", "notes": "France co-sponsoring global humanitarian carve-out across all UN sanctions regimes."}]),

    (16, "Peacekeeping: Mandate Design and Force Protection", "Mechanisms",
     "Drafting clear, achievable peacekeeping mandates with robust rules of engagement and exit benchmarks.",
     "Chapter VII authorizations, peacekeeper safety, and host-nation status of forces agreements (SOFA).",
     [{"case": "UNIFIL Maritime Task Force", "notes": "France deploying naval assets to monitor Lebanese territorial waters."}]),

    (17, "Mediation: Confidential Good Offices and Host-Nation Consent", "Mechanisms",
     "Utilizing French bilateral leverage and EU special envoys to broker confidential ceasefires.",
     "UN Charter Chapter VI, Article 33 peaceful dispute settlement mechanisms.",
     [{"case": "Baghdad Conference for Cooperation", "notes": "France co-convening regional rivals for de-escalation dialogue."}]),

    (18, "Veto Strategy: France's Restraint Doctrine and P5 Mathematics", "Advanced",
     "France has not cast a veto since 1989. Mastering the moral authority of veto restraint while countering adversary vetoes.",
     "UNSC Article 27(3) voting calculus; pushing for 9 votes to isolate a single vetoing power.",
     [{"case": "1989 Panama Resolution", "notes": "The last time France cast a veto (jointly with US and UK)."}]),

    (19, "Coalition Building: Winning the 9 Votes with Elected Members", "Advanced",
     "The mathematical reality that P5 co-sponsorship is meaningless without 9 affirmative votes. Courting the A3 and GRULAC.",
     "Provisional Rules of Procedure Rule 38, informal consultations, and co-sponsorship incentives.",
     [{"case": "S/RES/2728 Passage", "notes": "E10 elected members tabling the draft that France and 13 members supported."}]),

    (20, "Crisis Communication: Quai d'Orsay Press Demarches and Media Leaks", "Advanced",
     "Managing the information battlespace during an active crisis. Press stakeouts outside the chamber.",
     "Press Elements, Presidential Statements (PRST), and Council Communiqués.",
     [{"case": "Council Stakeout Technique", "notes": "French PR speaking in French and English to shape global news coverage."}]),

    (21, "Negotiating Difficult Actors: Non-State Armed Groups and Rogue Regimes", "Advanced",
     "Handling hostage crises, rebel blockades, and non-signatory factions without conferring sovereign legitimacy.",
     "Third-party mediation, ICRC intermediaries, and humanitarian deconfliction protocols.",
     [{"case": "Sahel Hostage Negotiations", "notes": "Using regional intermediaries while preserving counter-terrorism principles."}]),

    (22, "Resolution Drafting: Surgical Operative Verbs and Annexes", "Advanced",
     "The art of drafting UNSC resolutions. Distinguishing 'Demands', 'Decides', 'Calls upon', and 'Urges'.",
     "Preambular referencing of precedent resolutions, Chapter VII triggers, and sunset clauses.",
     [{"case": "Drafting S/RES/1701", "notes": "The delicate balance between operative paragraph 8 (buffer) and paragraph 11 (UNIFIL)."}]),

    (23, "Emergency Decision-Making: The 15-Minute Crisis Turn", "Advanced",
     "Making high-stakes decisions under extreme time pressure and incomplete intelligence.",
     "The 14-Step Decision Framework; balancing moral instinct with tactical realism.",
     [{"case": "Midnight Consultations", "notes": "Drafting emergency press statements during sudden overnight escalations."}]),

    (24, "Handling EB / Chair Questioning: Defending the Quai d'Orsay Under Fire", "Advanced",
     "Mastering MUN cross-examination. Rebutting accusations of neo-colonialism, NATO subservience, or diplomatic paralysis.",
     "Rhetorical composure, citing international law, and redirecting focus to shared Council responsibilities.",
     [{"case": "Challenging Chair Aggression", "notes": "De-escalating aggressive questions by anchoring in Article 24 of the Charter."}])
]

def seed_curriculum_data(db: Session):
    if db.query(TrainingCurriculumModule).first():
        return

    for mod in MODULES_DATA:
        record = TrainingCurriculumModule(
            module_number=mod[0],
            title=mod[1],
            category=mod[2],
            description=mod[3],
            core_doctrine=mod[4],
            legal_basis="UN Charter & International Conventions",
            france_historical_cases=mod[5],
            key_takeaways=[f"Takeaway {i+1} for {mod[1]}" for i in range(3)],
            sources=[{"title": "Quai d'Orsay Diplomatic Archives", "url": "https://diplomatie.gouv.fr"}],
            unlocked=True
        )
        db.add(record)
    db.commit()
