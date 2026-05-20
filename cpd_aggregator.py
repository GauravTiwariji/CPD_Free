
"""
CPD & Webinar Aggregator for Structural Engineers
A Streamlit app that catalogs free CPD seminars and webinars
from multiple professional bodies and industry providers.

Run: streamlit run cpd_aggregator.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="CPD & Webinar Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CPD DATABASE
# ============================================

cpd_data = [
    # RIBA
    {"provider": "RIBA", "name": "RIBA Academy", "url": "https://riba-academy.architecture.com/ilp/", 
     "type": "Online Platform", "cost": "Free / Discounted", "cpd_hours": "Variable",
     "topics": "Architecture, Design, Sustainability, Accessibility, Conservation",
     "format": "Webinars, Courses, Podcasts", "frequency": "Year-round",
     "notes": "RIBA Members get 20% discount. Free RIBA CPD Hours available.",
     "region": "UK / Global", "registration": "Free account required"},

    {"provider": "RIBA", "name": "RIBA CPD Providers Network", "url": "https://www.ribacpd.com/events",
     "type": "Event Directory", "cost": "Free", "cpd_hours": "1-5 per event",
     "topics": "Products, Materials, Technologies, Design",
     "format": "Webinars, In-person Expos", "frequency": "Monthly",
     "notes": "500+ RIBA CPD Providers. Free to attend online and in-person events.",
     "region": "UK", "registration": "Free, per-event"},

    {"provider": "RIBA", "name": "RIBAJ Learning", "url": "https://www.ribaj.com/learning/",
     "type": "Content Hub", "cost": "Free", "cpd_hours": "Self-certified",
     "topics": "Housing, Neurodiversity, Sustainability, Conservation",
     "format": "Articles, Videos, Podcasts, Webinars", "frequency": "Weekly updates",
     "notes": "RIBA Journal learning section with free reading and viewing CPD.",
     "region": "UK / Global", "registration": "None"},

    # Institution of Structural Engineers (IStructE)
    {"provider": "IStructE", "name": "IStructE CPD Programme 2026", "url": "https://www.istructe.org/resources/training/cpd-2026/",
     "type": "Course Calendar", "cost": "Paid / Member discounts", "cpd_hours": "Variable",
     "topics": "Structural Design, Analysis, Materials, Safety, Management",
     "format": "In-person, Online, Recorded", "frequency": "Year-round",
     "notes": "Full CPD programme downloadable. Some free resources available.",
     "region": "UK / Global", "registration": "Member login"},

    # ASCE (American Society of Civil Engineers)
    {"provider": "ASCE", "name": "ASCE Free On-Demand Webinars", "url": "https://sa360.asce.org/ascewebapp/benefits/membership/freeondemandwebinars.aspx",
     "type": "On-Demand Library", "cost": "Free (Members)", "cpd_hours": "1.0 PDH each",
     "topics": "Structural, Geotechnical, Transportation, Environmental",
     "format": "Recorded Webinars with Exam", "frequency": "200+ available",
     "notes": "ASCE members get 10 free webinars/year. Must pass exam for PDH credit.",
     "region": "USA / Global", "registration": "ASCE membership required"},

    # Structural Engineering Institute (SEI)
    {"provider": "SEI", "name": "SEU - Structural Engineers United", "url": "https://learnwithseu.com/",
     "type": "Membership Platform", "cost": "Subscription", "cpd_hours": "12-18 live/year",
     "topics": "Diaphragms, Concrete, Ethics, Tilt-up, Wind, Masonry, Revit",
     "format": "Live Webinars, Archive", "frequency": "Monthly live sessions",
     "notes": "EIT Ramp Up program for young engineers. Multi-office pricing.",
     "region": "USA", "registration": "Annual subscription"},

    # CABE (Chartered Association of Building Engineers)
    {"provider": "CABE", "name": "CABE Free CPD Webinars 2026", "url": "https://cbuilde.com/page/cabewebinars_2026",
     "type": "Live Webinars", "cost": "Free", "cpd_hours": "1 per webinar",
     "topics": "Building Engineering, Sustainability, Regulations, Technology",
     "format": "Live 1-hour webinars", "frequency": "Monthly",
     "notes": "Open to all Building Engineers and industry professionals.",
     "region": "UK", "registration": "Free, advance booking"},

    # IAST (Institute of Asphalt, Slate & Tile) - User's example
    {"provider": "IAST", "name": "IAST Online Courses", "url": "https://www.iast.uk/courses",
     "type": "Online Courses", "cost": "Free / Paid", "cpd_hours": "Variable",
     "topics": "Roofing, Cladding, Facades, Waterproofing, Slate, Tile",
     "format": "Self-paced online courses", "frequency": "On-demand",
     "notes": "Includes facade access & maintenance courses. Mix of free and paid content.",
     "region": "UK", "registration": "Free account"},

    # Institution of Civil Engineers (ICE)
    {"provider": "ICE", "name": "ICE Learning", "url": "https://www.ice.org.uk/learning-and-resources",
     "type": "Learning Platform", "cost": "Member discounts", "cpd_hours": "Variable",
     "topics": "Civil Engineering, Infrastructure, Sustainability, Management",
     "format": "Webinars, Courses, Publications", "frequency": "Weekly",
     "notes": "ICE members access discounted and some free CPD resources.",
     "region": "UK / Global", "registration": "ICE membership"},

    # Concrete Centre
    {"provider": "Concrete Centre", "name": "Concrete Centre Webinars", "url": "https://www.concretecentre.com/webinars.aspx",
     "type": "Webinar Series", "cost": "Free", "cpd_hours": "1 per webinar",
     "topics": "Concrete Design, Sustainability, Innovation, Case Studies",
     "format": "Live and recorded webinars", "frequency": "Monthly",
     "notes": "Free registration. Recordings available after live event.",
     "region": "UK", "registration": "Free"},

    # Steel Construction Institute (SCI)
    {"provider": "SCI", "name": "SCI CPD & Training", "url": "https://www.steel-sci.com/training/",
     "type": "Training Courses", "cost": "Paid / Member discounts", "cpd_hours": "Variable",
     "topics": "Steel Design, Connections, Fire, Eurocodes, BIM",
     "format": "In-person, Online, In-house", "frequency": "Scheduled courses",
     "notes": "Some free resources and publications. Member discounts on courses.",
     "region": "UK", "registration": "Per course"},

    # Timber Development UK
    {"provider": "TDUK", "name": "Timber Development UK CPD", "url": "https://www.tdruk.org/cpd/",
     "type": "CPD Directory", "cost": "Free / Paid", "cpd_hours": "Variable",
     "topics": "Timber Engineering, Mass Timber, CLT, Sustainability, Fire",
     "format": "Webinars, Seminars, Site visits", "frequency": "Monthly",
     "notes": "Growing resource for timber engineering CPD. Free webinars available.",
     "region": "UK", "registration": "Free / Member"},

    # Passivhaus Trust
    {"provider": "Passivhaus Trust", "name": "Passivhaus CPD", "url": "https://www.passivhaustrust.org.uk/cpd",
     "type": "Training & Events", "cost": "Paid / Free intro", "cpd_hours": "Variable",
     "topics": "Passivhaus Design, Energy Efficiency, Building Physics, Retrofit",
     "format": "Webinars, Workshops, Certification", "frequency": "Quarterly",
     "notes": "Introductory webinars often free. Certification courses are paid.",
     "region": "UK / Global", "registration": "Per event"},

    # Building Research Establishment (BRE)
    {"provider": "BRE", "name": "BRE Academy", "url": "https://www.bre.academy/",
     "type": "Online Academy", "cost": "Paid / Free trials", "cpd_hours": "Variable",
     "topics": "Fire Safety, Sustainability, BIM, Building Regulations, Testing",
     "format": "Online courses, Assessments", "frequency": "On-demand",
     "notes": "Some free introductory modules. BRE certification available.",
     "region": "UK / Global", "registration": "Free account"},

    # CPD Providers (Industry)
    {"provider": "Newton Waterproofing", "name": "RIBA CPD Webinars", "url": "https://www.newtonwaterproofing.co.uk/company/full-list-of-2025-riba-cpd-webinars-by-newton/",
     "type": "RIBA-accredited Webinars", "cost": "Free", "cpd_hours": "Double CPD points",
     "topics": "Waterproofing, BS 8102, Type A/B/C Systems, Concrete",
     "format": "Live webinars, Teams", "frequency": "Bi-monthly",
     "notes": "RIBA-approved and double-points. Also available as office seminars.",
     "region": "UK", "registration": "Free, advance booking"},

    {"provider": "Safeguard Europe", "name": "RIBA CPD Webinars", "url": "https://safeguardeurope.com/cpd",
     "type": "RIBA-accredited Webinars", "cost": "Free", "cpd_hours": "1 per webinar",
     "topics": "Damp Proofing, Waterproofing, Structural Repair, Ventilation",
     "format": "Live webinars", "frequency": "Monthly",
     "notes": "RIBA certified CPD webinars. Request specific topics.",
     "region": "UK", "registration": "Free"},

    {"provider": "Quantum", "name": "RIBA-Accredited CPD Series", "url": "https://www.architectsdatafile.co.uk/news/join-quantum-free-riba-accredited-cpd-webinar-series/",
     "type": "RIBA Webinar Series", "cost": "Free", "cpd_hours": "1 per session",
     "topics": "Building Physics, Insulation, Thermal Performance, Sustainability",
     "format": "Live 3-part webinar series", "frequency": "Annual series",
     "notes": "Free-to-attend live webinars covering RIBA Core Curriculum.",
     "region": "UK", "registration": "Free"},

    # Eurocodes & Standards
    {"provider": "BSI", "name": "BSI Standards Training", "url": "https://www.bsigroup.com/en-GB/our-services/training-courses/",
     "type": "Training Courses", "cost": "Paid", "cpd_hours": "Variable",
     "topics": "Eurocodes, ISO Standards, BS Standards, Quality, Safety",
     "format": "In-person, Virtual, E-learning", "frequency": "Scheduled",
     "notes": "Official standards body training. Comprehensive but paid.",
     "region": "UK / Global", "registration": "Per course"},

    # Online Platforms
    {"provider": "FutureLearn", "name": "Construction & Engineering Courses", "url": "https://www.futurelearn.com/subjects/construction-engineering-courses",
     "type": "MOOC Platform", "cost": "Free audit / Paid certificates", "cpd_hours": "Self-certified",
     "topics": "Engineering, Construction Management, Sustainability, BIM",
     "format": "Self-paced online courses", "frequency": "On-demand",
     "notes": "Audit courses free. Certificates paid. University partners.",
     "region": "Global", "registration": "Free account"},

    {"provider": "Coursera", "name": "Structural Engineering Courses", "url": "https://www.coursera.org/browse/engineering/structural-engineering",
     "type": "MOOC Platform", "cost": "Free audit / Paid certificates", "cpd_hours": "Self-certified",
     "topics": "Structural Analysis, FEA, Materials, Seismic, Dynamics",
     "format": "Video lectures, Assignments", "frequency": "On-demand",
     "notes": "Courses from top universities. Audit free, certificate paid.",
     "region": "Global", "registration": "Free account"},

    {"provider": "edX", "name": "Engineering & Architecture", "url": "https://www.edx.org/learn/engineering",
     "type": "MOOC Platform", "cost": "Free audit / Paid certificates", "cpd_hours": "Self-certified",
     "topics": "Structural, Mechanical, Materials, Design",
     "format": "Self-paced courses", "frequency": "On-demand",
     "notes": "MIT, Harvard, Delft courses available. Audit for free.",
     "region": "Global", "registration": "Free account"},

    # YouTube Channels
    {"provider": "YouTube", "name": "The B1M - Construction", "url": "https://www.youtube.com/c/TheB1M",
     "type": "Video Channel", "cost": "Free", "cpd_hours": "Self-certified",
     "topics": "Construction, Architecture, Engineering, Innovation",
     "format": "Documentary-style videos", "frequency": "Weekly",
     "notes": "High-quality construction content. Can count as informal CPD.",
     "region": "Global", "registration": "None"},

    {"provider": "YouTube", "name": "Engineering Explained", "url": "https://www.youtube.com/c/EngineeringExplained",
     "type": "Video Channel", "cost": "Free", "cpd_hours": "Self-certified",
     "topics": "Engineering Principles, Mechanics, Materials",
     "format": "Educational videos", "frequency": "Weekly",
     "notes": "General engineering knowledge. Good for broad learning.",
     "region": "Global", "registration": "None"},

    # Podcasts
    {"provider": "Podcast", "name": "Engineering Matters", "url": "https://engineeringmatters.org/",
     "type": "Podcast", "cost": "Free", "cpd_hours": "Self-certified",
     "topics": "Infrastructure, Sustainability, Innovation, Policy",
     "format": "Audio episodes", "frequency": "Bi-weekly",
     "notes": "Institution of Civil Engineers podcast. Excellent for commute CPD.",
     "region": "UK", "registration": "None"},

    {"provider": "Podcast", "name": "The Structural Engineer Podcast", "url": "https://www.asce.org/publications-and-news/podcasts",
     "type": "Podcast", "cost": "Free", "cpd_hours": "Self-certified",
     "topics": "Structural Engineering, Design, Research, Career",
     "format": "Audio episodes", "frequency": "Monthly",
     "notes": "ASCE/SEI podcast. Interviews with leading structural engineers.",
     "region": "USA / Global", "registration": "None"},
]

df_cpd = pd.DataFrame(cpd_data)

# ============================================
# STREAMLIT APP
# ============================================

st.markdown("# 🎓 CPD & Webinar Hub for Structural Engineers")
st.markdown("### Your one-stop directory for free and discounted professional development")

# Sidebar filters
st.sidebar.markdown("## 🔍 Filter CPD Resources")

# Cost filter
cost_filter = st.sidebar.multiselect(
    "Cost",
    options=df_cpd['cost'].unique(),
    default=["Free", "Free (Members)", "Free / Discounted", "Free / Paid"]
)

# Format filter
format_filter = st.sidebar.multiselect(
    "Format",
    options=df_cpd['format'].unique(),
    default=df_cpd['format'].unique()
)

# Topic search
topic_search = st.sidebar.text_input("Search Topics", placeholder="e.g., concrete, steel, sustainability")

# Provider filter
provider_filter = st.sidebar.multiselect(
    "Provider",
    options=sorted(df_cpd['provider'].unique()),
    default=[]
)

# Region filter
region_filter = st.sidebar.multiselect(
    "Region",
    options=df_cpd['region'].unique(),
    default=["UK", "UK / Global", "Global"]
)

# Apply filters
filtered_df = df_cpd.copy()

if cost_filter:
    filtered_df = filtered_df[filtered_df['cost'].isin(cost_filter)]
if format_filter:
    filtered_df = filtered_df[filtered_df['format'].isin(format_filter)]
if topic_search:
    filtered_df = filtered_df[filtered_df['topics'].str.contains(topic_search, case=False, na=False)]
if provider_filter:
    filtered_df = filtered_df[filtered_df['provider'].isin(provider_filter)]
if region_filter:
    filtered_df = filtered_df[filtered_df['region'].isin(region_filter)]

# Main content
st.markdown(f"**Showing {len(filtered_df)} of {len(df_cpd)} CPD resources**")

# Display as cards
for idx, row in filtered_df.iterrows():
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### {row['name']}")
            st.markdown(f"**Provider:** {row['provider']} | **Type:** {row['type']} | **Region:** {row['region']}")
            st.markdown(f"**Topics:** {row['topics']}")
            st.markdown(f"**Format:** {row['format']} | **Frequency:** {row['frequency']}")
            st.markdown(f"**CPD Hours:** {row['cpd_hours']} | **Cost:** {row['cost']}")
            st.markdown(f"*{row['notes']}*")

        with col2:
            st.markdown("&nbsp;")
            st.markdown(f"[🔗 Visit Website]({row['url']})")
            st.markdown(f"**Registration:** {row['registration']}")

            # Copy URL button
            if st.button(f"📋 Copy URL", key=f"copy_{idx}"):
                st.code(row['url'], language=None)

        st.markdown("---")

# Summary statistics
st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Statistics")
st.sidebar.metric("Total Resources", len(df_cpd))
st.sidebar.metric("Filtered Results", len(filtered_df))

# Free resources count
free_count = len(df_cpd[df_cpd['cost'].str.contains('Free', na=False)])
st.sidebar.metric("Free Resources", free_count)

# Provider breakdown
st.sidebar.markdown("### By Provider")
provider_counts = df_cpd['provider'].value_counts().head(10)
for provider, count in provider_counts.items():
    st.sidebar.text(f"{provider}: {count}")

# Quick links section
st.markdown("## 🔗 Quick Access Links")

quick_links = {
    "RIBA Academy": "https://riba-academy.architecture.com/ilp/",
    "RIBA CPD Events": "https://www.ribacpd.com/events",
    "ASCE Free Webinars": "https://sa360.asce.org/ascewebapp/benefits/membership/freeondemandwebinars.aspx",
    "IStructE CPD": "https://www.istructe.org/resources/training/cpd-2026/",
    "CABE Webinars": "https://cbuilde.com/page/cabewebinars_2026",
    "SEU Learning": "https://learnwithseu.com/",
    "Concrete Centre": "https://www.concretecentre.com/webinars.aspx",
    "BRE Academy": "https://www.bre.academy/",
}

cols = st.columns(4)
for i, (name, url) in enumerate(quick_links.items()):
    with cols[i % 4]:
        st.markdown(f"[{name}]({url})")

# Add new resource form
st.markdown("---")
st.markdown("## ➕ Suggest a New CPD Resource")

with st.form("suggest_cpd"):
    col1, col2 = st.columns(2)
    with col1:
        new_provider = st.text_input("Provider Name")
        new_name = st.text_input("Resource Name")
        new_url = st.text_input("Website URL")
    with col2:
        new_type = st.selectbox("Type", ["Webinar", "Course", "Podcast", "Video", "Platform", "Event"])
        new_cost = st.selectbox("Cost", ["Free", "Free (Members)", "Free / Paid", "Paid", "Subscription"])
        new_topics = st.text_input("Topics (comma-separated)")

    new_notes = st.text_area("Notes")

    if st.form_submit_button("Suggest Resource"):
        st.success(f"Thanks! '{new_name}' has been noted for addition.")
        st.info("In a full app, this would save to a database. For now, add it to the cpd_data list in the code.")

# Footer
st.markdown("---")
st.markdown("*💡 Tip: Many professional institutions require 35+ CPD hours per year. Track your hours and keep certificates!*")
