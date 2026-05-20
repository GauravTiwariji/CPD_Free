
"""
Free CPD Course Directory v3
Filter by dates, real courses found online
Run: streamlit run cpd_directory_v3.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Free CPD Directory - Engineering",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .course-card {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #2196F3;
        margin-bottom: 1rem;
    }
    .course-title { font-size: 1.15rem; font-weight: bold; color: #1a1a2e; }
    .course-meta { font-size: 0.9rem; color: #666; margin-top: 0.3rem; }
    .course-topics { font-size: 0.85rem; color: #2196F3; margin-top: 0.3rem; }
    .course-date { font-size: 0.95rem; color: #FF6B6B; font-weight: bold; }
    .available-now { background: #4CAF50; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; }
    .upcoming { background: #FF9800; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; }
    .monthly { background: #9C27B0; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; }
    .category-header { font-size: 1.6rem; font-weight: bold; color: #1a1a2e; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 3px solid #2196F3; padding-bottom: 0.5rem; }
    .stats-box { background: #e3f2fd; padding: 1rem; border-radius: 10px; text-align: center; }
    .stats-number { font-size: 2rem; font-weight: bold; color: #1565C0; }
    .stats-label { font-size: 0.9rem; color: #555; }
</style>
""", unsafe_allow_html=True)

# ============================================
# COURSE DATA
# ============================================

courses = [
    # FACADE
    {"category": "🏢 Facade Engineering", "name": "Facade Access & Maintenance", "provider": "IAST",
     "url": "https://www.iast.uk/courses/take/facade-access-maintenance", "type": "Online Course",
     "date": "On-demand", "duration": "Self-paced", "cpd": "2-3 hours",
     "topics": "Facade access, BMUs, maintenance, safety",
     "desc": "Comprehensive facade access and maintenance systems course.", "level": "Intermediate",
     "registration": "Free account", "status": "Available now"},

    {"category": "🏢 Facade Engineering", "name": "Curtain Wall Design Principles", "provider": "RIBA CPD",
     "url": "https://www.ribacpd.com/events", "type": "Webinar",
     "date": "Check calendar", "duration": "1-2 hours", "cpd": "1-2 hours",
     "topics": "Curtain walls, glazing, structural glazing, facades",
     "desc": "RIBA CPD on curtain wall design and specification.", "level": "Intermediate",
     "registration": "Free booking", "status": "Check dates"},

    {"category": "🏢 Facade Engineering", "name": "Building Envelope Performance", "provider": "CABE",
     "url": "https://cbuilde.com/page/cabewebinars_2026", "type": "Live Webinar",
     "date": "Monthly 2026", "duration": "1 hour", "cpd": "1 hour",
     "topics": "Envelope, facade, thermal performance, airtightness",
     "desc": "Monthly free webinar on building envelope performance.", "level": "All levels",
     "registration": "Free booking", "status": "Monthly sessions"},

    # FIRE BREAK
    {"category": "🔥 Fire Break / Fire Stopping", "name": "Fire Protection in Buildings", "provider": "BM TRADA",
     "url": "https://www.bmtrada.com/training/fire-training/fire-protection-in-buildings", "type": "Free Half-Day Webinar",
     "date": "Scheduled 2026", "duration": "4 hours", "cpd": "4 hours",
     "topics": "Fire protection, passive fire, compartmentation, fire stopping",
     "desc": "Free half-day webinar on fire protection. Tailored for England/Wales and Scotland.", "level": "All levels",
     "registration": "Free booking", "status": "Check dates"},

    {"category": "🔥 Fire Break / Fire Stopping", "name": "Fire Doors for Passive Fire Industry", "provider": "ASFP",
     "url": "https://asfp.org.uk/page/Webinars", "type": "On-Demand Webinar",
     "date": "On-demand", "duration": "1 hour", "cpd": "Self-certify",
     "topics": "Fire doors, passive fire protection, fire stopping",
     "desc": "ASFP webinar on fire doors for passive fire protection.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "🔥 Fire Break / Fire Stopping", "name": "Passive Fire Protection: Cavity & Compartment Barriers", "provider": "Injecta Fire Barrier",
     "url": "https://internationalfireandsafetyjournal.com/free-cpd-sessions-from-injecta-fire-barrier-on-passive-fire-protection/", "type": "Free CPD Session",
     "date": "On-demand / Request", "duration": "1 hour", "cpd": "1 hour",
     "topics": "Cavity barriers, compartment barriers, passive fire",
     "desc": "Free CPD sessions on cavity and compartment fire barriers.", "level": "All levels",
     "registration": "Free request", "status": "Available on request"},

    {"category": "🔥 Fire Break / Fire Stopping", "name": "Structural Thermal Bridging in Building Envelope", "provider": "ASCE",
     "url": "https://www.asce.org/education-and-events/explore-education/on-demand-webinars/structural-thermal-bridging-in-the-building-envelope", "type": "On-Demand Webinar",
     "date": "On-demand", "duration": "1 hour", "cpd": "1 PDH (with exam)",
     "topics": "Thermal bridging, heat transfer, foundations, slab edges",
     "desc": "ASCE webinar on thermal bridging. Post-test required for PDH.", "level": "Intermediate",
     "registration": "ASCE member / Purchase", "status": "Available now"},

    # THERMAL BREAK
    {"category": "🌡️ Thermal Break", "name": "Structural Thermal Breaks: Benefits & Considerations", "provider": "The Structural Engineering Channel",
     "url": "https://engineeringmanagementinstitute.org/tsec-68-structural-thermal-breaks-benefits-considerations-engineers/", "type": "Podcast / Audio CPD",
     "date": "On-demand", "duration": "45 min", "cpd": "Self-certify",
     "topics": "Thermal breaks, balconies, parapets, energy loss, condensation",
     "desc": "Podcast episode on structural thermal breaks - design considerations.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "🌡️ Thermal Break", "name": "Understanding Structural Thermal Breaks (PDF)", "provider": "Schöck",
     "url": "https://www.schoeck.com/viewfile/14319/Understanding_Structural_Thermal_Break_Installation__14319__.pdf", "type": "Technical Document",
     "date": "On-demand", "duration": "Self-paced", "cpd": "Self-certify",
     "topics": "Thermal break installation, GFRP bars, insulation, fire protection",
     "desc": "Comprehensive PDF guide on structural thermal break systems.", "level": "Advanced",
     "registration": "Free download", "status": "Available now"},

    {"category": "🌡️ Thermal Break", "name": "Top 5 Questions: Specifying Structural Thermal Breaks", "provider": "IStructE / Farrat",
     "url": "https://www.istructe.org/resources/blog/specifying-structural-thermal-breaks/", "type": "Article / CPD",
     "date": "On-demand", "duration": "20 min read", "cpd": "Self-certify",
     "topics": "Thermal break specification, Farrat TBK/TBF/TBL, fire rating",
     "desc": "IStructE article on specifying structural thermal breaks.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    # DRAINAGE
    {"category": "💧 Drainage", "name": "InfoDrainage Training Course", "provider": "Autodesk",
     "url": "https://www.autodesk.com/blogs/water/2024/09/02/all-of-the-free-drainage-design-learning-content-available-for-infodrainage/", "type": "Online Course",
     "date": "On-demand", "duration": "Self-paced", "cpd": "Self-certify",
     "topics": "Drainage design, hydraulic modeling, sustainable drainage, InfoDrainage",
     "desc": "Comprehensive free Autodesk InfoDrainage training with quizzes.", "level": "Beginner to Advanced",
     "registration": "Autodesk account (free)", "status": "Available now"},

    {"category": "💧 Drainage", "name": "Siphonic Rainwater Systems", "provider": "Geberit",
     "url": "https://www.geberit.co.uk/trainings-events/trainings/cpd-training/", "type": "On-Demand CPD",
     "date": "On-demand", "duration": "1 hour", "cpd": "1 hour (RIBA & CIBSE approved)",
     "topics": "Siphonic drainage, rainwater systems, BS8490, design",
     "desc": "RIBA & CIBSE approved CPD on siphonic rainwater system design.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "💧 Drainage", "name": "Water Transportation Systems in Buildings", "provider": "Geberit",
     "url": "https://www.geberit.co.uk/trainings-events/trainings/cpd-training/", "type": "On-Demand CPD",
     "date": "On-demand", "duration": "1 hour", "cpd": "1 hour (CIBSE approved)",
     "topics": "Water transport, pipe systems, specification, installation",
     "desc": "CIBSE approved CPD on water transport system specification.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "💧 Drainage", "name": "Below Ground Building Drainage", "provider": "CIBSE",
     "url": "https://www.cibse.org/training/search-courses/below-ground-building-drainage/", "type": "Training Course",
     "date": "Scheduled dates", "duration": "1 day", "cpd": "6 hours",
     "topics": "Below-ground drainage, design, regulations, installation",
     "desc": "CIBSE training on below-ground building drainage systems.", "level": "Intermediate",
     "registration": "Paid (member discount)", "status": "Check dates"},

    # CONSTRUCTION PROFILES
    {"category": "🏗️ Construction Profiles", "name": "Steel Construction & Offsite Manufacturing", "provider": "SteelConstruction.info",
     "url": "https://www.steelconstruction.info/Continuing_Professional_Development", "type": "Online CPD Module",
     "date": "On-demand", "duration": "50 min + test", "cpd": "1 hour (with certificate)",
     "topics": "Steel profiles, offsite construction, steel framing, sustainability",
     "desc": "Free online CPD on steel construction with test and certificate.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "🏗️ Construction Profiles", "name": "Corrosion Protection of Structural Steelwork", "provider": "SteelConstruction.info",
     "url": "https://www.steelconstruction.info/Continuing_Professional_Development", "type": "Online CPD Module",
     "date": "On-demand", "duration": "50 min + test", "cpd": "1 hour (with certificate)",
     "topics": "Steel profiles, corrosion protection, coatings, durability",
     "desc": "Free CPD on corrosion protection for structural steelwork.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "🏗️ Construction Profiles", "name": "Introduction to EC3 (Eurocode 3)", "provider": "SteelConstruction.info",
     "url": "https://www.steelconstruction.info/Continuing_Professional_Development", "type": "Online CPD Seminar",
     "date": "On-demand", "duration": "50 min + test", "cpd": "1 hour (with certificate)",
     "topics": "Steel profiles, Eurocode 3, design, buckling, steel grades",
     "desc": "Free online seminar introducing EC3 for steel profile design.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "🏗️ Construction Profiles", "name": "Worked Examples to EC3", "provider": "SteelConstruction.info",
     "url": "https://www.steelconstruction.info/Continuing_Professional_Development", "type": "Online CPD Seminar",
     "date": "On-demand", "duration": "50 min + test", "cpd": "1 hour (with certificate)",
     "topics": "Steel profiles, EC3 worked examples, struts, beams, Blue Book",
     "desc": "Numerical worked examples demonstrating EC3 application to steel profiles.", "level": "Advanced",
     "registration": "Free", "status": "Available now"},

    # AUTODESK INVENTOR
    {"category": "🔧 Autodesk Inventor", "name": "Inventor 2026 - Basic Modeling for Beginners", "provider": "Vertanux1 / YouTube",
     "url": "https://www.classcentral.com/course/youtube-e1-autodesk-inventor-2026-basic-modeling-for-beginners-tutorial-with-training-guide-453564", "type": "YouTube Tutorial",
     "date": "On-demand", "duration": "2-3 hours", "cpd": "Self-certify",
     "topics": "Inventor 2026, 3D CAD, basic modeling, geometry creation",
     "desc": "Beginner-friendly Inventor 2026 tutorial with training guide download.", "level": "Beginner",
     "registration": "Free", "status": "Available now"},

    {"category": "🔧 Autodesk Inventor", "name": "Inventor Beginner to Certification (2026)", "provider": "SolidProfessor",
     "url": "https://www.solidprofessor.com/tutorials/inventor", "type": "Online Course",
     "date": "On-demand", "duration": "Self-paced", "cpd": "Self-certify",
     "topics": "Inventor, parts, assemblies, drawings, certification prep",
     "desc": "Complete Inventor 2026 beginner to certification course library.", "level": "Beginner to Advanced",
     "registration": "Free trial / Subscription", "status": "Available now"},

    {"category": "🔧 Autodesk Inventor", "name": "Inventor Essentials for Parts and Assemblies", "provider": "SolidProfessor",
     "url": "https://www.solidprofessor.com/tutorials/inventor", "type": "Online Course",
     "date": "On-demand", "duration": "Self-paced", "cpd": "Self-certify",
     "topics": "Inventor, part modeling, assemblies, constraints, drawings",
     "desc": "Essential Inventor skills for creating parts and assemblies.", "level": "Beginner",
     "registration": "Free trial / Subscription", "status": "Available now"},

    {"category": "🔧 Autodesk Inventor", "name": "Plastic Gear & Mold Design using Inventor", "provider": "Coursesity",
     "url": "https://coursesity.com/free-tutorials-learn/autodesk", "type": "Free Tutorial",
     "date": "On-demand", "duration": "Self-paced", "cpd": "Self-certify",
     "topics": "Inventor, mold design, plastic gears, manufacturing",
     "desc": "Free tutorial on plastic gear and mold design using Autodesk Inventor.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    # DESIGN / MODELING / BIM
    {"category": "🏗️ Design / Modeling / BIM", "name": "Learn Revit in 90 Minutes", "provider": "Autodesk",
     "url": "https://www.autodesk.com/education/edu-software/revit", "type": "Self-paced Course",
     "date": "On-demand", "duration": "90 min", "cpd": "Self-certify",
     "topics": "Revit, BIM, fundamentals, modeling",
     "desc": "Autodesk's official quick-start Revit course.", "level": "Beginner",
     "registration": "Free (students/educators)", "status": "Available now"},

    {"category": "🏗️ Design / Modeling / BIM", "name": "BIM Workflows for Complex Buildings", "provider": "SOFiSTiK",
     "url": "https://www.sofistik.com/en/infocenter/webinars", "type": "Webinar Recording",
     "date": "Recorded Mar 2025", "duration": "1 hour", "cpd": "Self-certify",
     "topics": "BIM, complex buildings, SOFiSTiK, Revit integration",
     "desc": "Elevating BIM workflows for complex building projects.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "🏗️ Design / Modeling / BIM", "name": "Parametric Structural Modeling with IgentBIM", "provider": "IgentBIM / BIMvision",
     "url": "https://bimvision.eu/free-webinar-about-the-igentbim-plugin-for-bimvision/", "type": "Live Webinar / Recording",
     "date": "On-demand / Jan 20 2026", "duration": "1 hour", "cpd": "Self-certify",
     "topics": "Parametric modeling, steel, concrete, Revit, Tekla export",
     "desc": "Parametric structural modeling with export to Revit and Tekla.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "🏗️ Design / Modeling / BIM", "name": "Revit Tutorial - Full Project (Beginner)", "provider": "Balkan Architect",
     "url": "https://www.youtube.com/watch?v=chom9hiewXI", "type": "YouTube Course",
     "date": "On-demand", "duration": "1.5 hours", "cpd": "Self-certify",
     "topics": "Revit, complete building, walls, floors, stairs, roofs, curtain walls",
     "desc": "Complete beginner project from scratch with free project files.", "level": "Beginner",
     "registration": "Free", "status": "Available now"},

    {"category": "🏗️ Design / Modeling / BIM", "name": "BIM Fundamentals for Engineers", "provider": "FutureLearn",
     "url": "https://www.futurelearn.com/subjects/construction-engineering-courses", "type": "MOOC",
     "date": "On-demand", "duration": "12 hours", "cpd": "Self-certify",
     "topics": "BIM, Revit, 3D modeling, MEP, structural",
     "desc": "Introduction to BIM and basic 3D modeling using Revit.", "level": "Beginner",
     "registration": "Free audit", "status": "Available now"},

    {"category": "🏗️ Design / Modeling / BIM", "name": "BIM Coordination & Clash Detection", "provider": "Coursera",
     "url": "https://www.coursera.org/browse/engineering/structural-engineering", "type": "MOOC",
     "date": "On-demand", "duration": "10 hours", "cpd": "Self-certify",
     "topics": "BIM coordination, clash detection, LOD, Navisworks",
     "desc": "Learn clash detection in Revit and understand LOD.", "level": "Intermediate",
     "registration": "Free audit", "status": "Available now"},

    # CONCRETE
    {"category": "🧱 Concrete", "name": "UHPC Essentials: Properties & Modern Uses", "provider": "ACI",
     "url": "https://www.concrete.org/education/aciuniversity/webinars.aspx", "type": "Live Webinar",
     "date": "January 13, 2026", "duration": "1 hour", "cpd": "1 PDH",
     "topics": "UHPC, ultra-high performance concrete, applications",
     "desc": "Comprehensive UHPC overview with modern construction applications.", "level": "Intermediate",
     "registration": "Free (ACI members)", "status": "Upcoming - Jan 13"},

    {"category": "🧱 Concrete", "name": "Cementitious Materials for Concrete – Part 2", "provider": "ACI",
     "url": "https://www.concrete.org/education/aciuniversity/webinars.aspx", "type": "Live Webinar",
     "date": "February 3, 2026", "duration": "1 hour", "cpd": "1 PDH",
     "topics": "Cement, supplementary materials, mix design",
     "desc": "Deep dive into cementitious materials and concrete performance.", "level": "Advanced",
     "registration": "Free (ACI members)", "status": "Upcoming - Feb 3"},

    {"category": "🧱 Concrete", "name": "Concrete Design & Sustainability", "provider": "Concrete Centre",
     "url": "https://www.concretecentre.com/webinars.aspx", "type": "Webinar",
     "date": "Monthly", "duration": "1 hour", "cpd": "1 hour",
     "topics": "Concrete design, sustainability, low-carbon concrete",
     "desc": "Latest developments in sustainable concrete design.", "level": "All levels",
     "registration": "Free", "status": "Monthly sessions"},

    {"category": "🧱 Concrete", "name": "Sustainability & Circularity with Nanoscience", "provider": "ACI",
     "url": "https://www.concrete.org/education/aciuniversity/webinars.aspx", "type": "Live Webinar",
     "date": "January 14, 2026", "duration": "1 hour", "cpd": "1 PDH",
     "topics": "Sustainability, circularity, green materials, recycled",
     "desc": "Building with locally available and recycled materials using nanoscience.", "level": "Intermediate",
     "registration": "Free (ACI members)", "status": "Upcoming - Jan 14"},

    # STRUCTURAL ANALYSIS
    {"category": "📐 Structural Analysis", "name": "New Features of SOFiSTiK 2026", "provider": "SOFiSTiK",
     "url": "https://www.sofistik.com/en/infocenter/webinars", "type": "Webinar Recording",
     "date": "Recorded Oct 2025", "duration": "1 hour", "cpd": "Self-certify",
     "topics": "SOFiSTiK, structural analysis, bridge, building, BIM",
     "desc": "Overview of new features in SOFiSTiK 2026.", "level": "All levels",
     "registration": "Free", "status": "Available now"},

    {"category": "📐 Structural Analysis", "name": "Automate Bridge Modelling to Design", "provider": "SOFiSTiK",
     "url": "https://www.sofistik.com/en/infocenter/webinars", "type": "Webinar Recording",
     "date": "Recorded Jun 2025", "duration": "1 hour", "cpd": "Self-certify",
     "topics": "Bridge design, automation, parametric modeling",
     "desc": "Smarter bridge design automation from modeling to final design.", "level": "Intermediate",
     "registration": "Free", "status": "Available now"},

    {"category": "📐 Structural Analysis", "name": "Steel Bridge with Connection Design", "provider": "SOFiSTiK",
     "url": "https://www.sofistik.com/en/infocenter/webinars", "type": "Webinar Recording",
     "date": "Recorded Mar 2025", "duration": "1 hour", "cpd": "Self-certify",
     "topics": "Steel bridge, connections, IDEA StatiCa",
     "desc": "Steel bridge design using SOFiSTiK with IDEA StatiCa.", "level": "Advanced",
     "registration": "Free", "status": "Available now"},

    {"category": "📐 Structural Analysis", "name": "SEU Live Webinars", "provider": "SEU",
     "url": "https://learnwithseu.com/", "type": "Live Webinar Series",
     "date": "Monthly", "duration": "1 hour", "cpd": "12-18/year",
     "topics": "Diaphragms, concrete, steel, wind, seismic, Revit",
     "desc": "Monthly live webinars for structural engineers.", "level": "All levels",
     "registration": "Subscription", "status": "Monthly sessions"},

    # PODCASTS
    {"category": "🎧 Podcasts", "name": "Engineering Matters", "provider": "ICE",
     "url": "https://engineeringmatters.org/", "type": "Podcast",
     "date": "Bi-weekly", "duration": "30-45 min", "cpd": "Self-certify",
     "topics": "Infrastructure, sustainability, innovation, policy",
     "desc": "ICE podcast - perfect for commute CPD.", "level": "All levels",
     "registration": "Free", "status": "Available now"},

    {"category": "🎧 Podcasts", "name": "The Structural Engineer Podcast", "provider": "ASCE",
     "url": "https://www.asce.org/publications-and-news/podcasts", "type": "Podcast",
     "date": "Monthly", "duration": "45-60 min", "cpd": "Self-certify",
     "topics": "Structural engineering, design, research, career",
     "desc": "ASCE/SEI interviews with leading structural engineers.", "level": "All levels",
     "registration": "Free", "status": "Available now"},
]

df = pd.DataFrame(courses)

# ============================================
# SIDEBAR
# ============================================
st.sidebar.markdown("## 🔍 Filter Courses")

# Date filter
date_options = ["All", "Available now", "Upcoming (with dates)", "Monthly sessions", "Check dates"]
date_filter = st.sidebar.radio("Availability", date_options, index=0)

# Category filter
categories = sorted(df['category'].unique())
selected_cats = st.sidebar.multiselect("Categories", categories, default=categories)

# Level filter
levels = sorted(df['level'].unique())
selected_levels = st.sidebar.multiselect("Level", levels, default=levels)

# Search
search = st.sidebar.text_input("Search", placeholder="e.g., Revit, fire, thermal")

# Apply filters
filtered = df.copy()

if date_filter == "Available now":
    filtered = filtered[filtered['status'] == 'Available now']
elif date_filter == "Upcoming (with dates)":
    filtered = filtered[filtered['status'].str.contains('Upcoming', na=False)]
elif date_filter == "Monthly sessions":
    filtered = filtered[filtered['status'] == 'Monthly sessions']
elif date_filter == "Check dates":
    filtered = filtered[filtered['status'] == 'Check dates']

if selected_cats:
    filtered = filtered[filtered['category'].isin(selected_cats)]
if selected_levels:
    filtered = filtered[filtered['level'].isin(selected_levels)]
if search:
    filtered = filtered[
        filtered['name'].str.contains(search, case=False, na=False) |
        filtered['topics'].str.contains(search, case=False, na=False) |
        filtered['provider'].str.contains(search, case=False, na=False)
    ]

# ============================================
# MAIN CONTENT
# ============================================
st.markdown("# 🎓 Free CPD Course Directory")
st.markdown("### For Structural Engineers — Facade | Fire/Thermal Break | Drainage | Profiles | Inventor | BIM")

# Stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='stats-box'><div class='stats-number'>{}</div><div class='stats-label'>Total Courses</div></div>".format(len(df)), unsafe_allow_html=True)
with col2:
    available_now = len(df[df['status'] == 'Available now'])
    st.markdown("<div class='stats-box'><div class='stats-number'>{}</div><div class='stats-label'>Available Now</div></div>".format(available_now), unsafe_allow_html=True)
with col3:
    upcoming = len(df[df['status'].str.contains('Upcoming', na=False)])
    st.markdown("<div class='stats-box'><div class='stats-number'>{}</div><div class='stats-label'>Upcoming</div></div>".format(upcoming), unsafe_allow_html=True)
with col4:
    st.markdown("<div class='stats-box'><div class='stats-number'>{}</div><div class='stats-label'>Filtered</div></div>".format(len(filtered)), unsafe_allow_html=True)

st.markdown("---")

# Display by category
for category in sorted(filtered['category'].unique()):
    cat_courses = filtered[filtered['category'] == category]
    st.markdown(f"<div class='category-header'>{category} ({len(cat_courses)})</div>", unsafe_allow_html=True)

    for _, course in cat_courses.iterrows():
        badge = "<span class='available-now'>AVAILABLE NOW</span>" if course['status'] == 'Available now' else                 "<span class='upcoming'>UPCOMING</span>" if 'Upcoming' in course['status'] else                 "<span class='monthly'>MONTHLY</span>" if course['status'] == 'Monthly sessions' else                 "<span style='background:#999;color:white;padding:3px 10px;border-radius:12px;font-size:0.75rem;'>CHECK DATES</span>"

        st.markdown(f"""
        <div class='course-card'>
            <div class='course-title'>{course['name']} {badge}</div>
            <div class='course-meta'>
                <b>Provider:</b> {course['provider']} | 
                <b>Type:</b> {course['type']} | 
                <b>Level:</b> {course['level']} | 
                <b>CPD:</b> {course['cpd']}
            </div>
            <div class='course-date'>📅 {course['date']} | ⏱️ {course['duration']}</div>
            <div class='course-topics'>🏷️ {course['topics']}</div>
            <div style='margin-top:0.5rem; color:#555; font-size:0.9rem;'>{course['desc']}</div>
            <div style='margin-top:0.5rem; font-size:0.85rem; color:#666;'><b>Registration:</b> {course['registration']}</div>
            <div style='margin-top:0.8rem;'>
                <a href='{course['url']}' target='_blank'>
                    <button style='background:#2196F3; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:bold;'>
                        🔗 Go to Course / Register
                    </button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
💡 **How to use:**
- **Filter by Availability** in the sidebar to see only courses you can register for today
- **"Available now"** = click and start immediately
- **"Upcoming"** = has specific dates (Jan–Feb 2026) — register before they fill up
- **"Monthly"** = recurring sessions — check provider calendar
- **"Check dates"** = visit link to see next available session
- All links go **directly to the course/registration page**
""")
