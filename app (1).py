
import streamlit as st
from openai import OpenAI
import json

st.set_page_config(
    page_title="AI Network Intelligence",
    page_icon="📡",
    layout="centered"
)

# ============================================
# HEADER
# ============================================
st.title("📡 AI Network Intelligence Tool")
st.markdown("""
**Built by Soham Sarkar — Senior PM at BT**  
Transforms anonymised mobile network data 
into actionable intelligence for transport 
and media decision makers.
""")

st.divider()

# ============================================
# SETUP
# ============================================
st.subheader("⚙️ Setup")
api_key = st.text_input(
    "Enter your OpenRouter API Key",
    type="password",
    help="Get a free key at openrouter.ai"
)

st.divider()

# ============================================
# SECTOR SELECTOR — THE CORE PM DECISION
# ============================================
st.subheader("🎯 Select Your Sector")
sector = st.radio(
    "Which intelligence report do you need?",
    options=[
        "🚌 Transport Intelligence",
        "📺 Media & Advertising Intelligence"
    ],
    horizontal=True
)

st.divider()

# ============================================
# SAMPLE DATA
# ============================================
transport_samples = {
    "Select a sample query...": "",
    "🚧 New Housing Development Impact": """
        A developer is planning 2,400 new homes 
        in Didsbury, Manchester. The site is 
        adjacent to the A34. We need to assess 
        traffic impact on surrounding roads and 
        recommend whether existing infrastructure 
        can support the development or requires 
        upgrade investment.
    """,
    "🏟️ Event Impact — Stadium": """
        Manchester City FC plays home games at 
        the Etihad Stadium with 53,000 capacity. 
        Greater Manchester Transport needs an 
        analysis of movement patterns on match 
        days vs non-match days to optimise 
        bus and tram frequency and routing.
    """,
    "🛣️ Road Closure Planning": """
        The M62 westbound between junctions 
        12 and 13 requires 6 weeks of overnight 
        maintenance closure. National Highways 
        needs to understand likely diversion 
        routes and impact on surrounding 
        A-road network based on current 
        movement patterns.
    """,
    "🚉 New Rail Station Assessment": """
        Transport for the North is evaluating 
        a new rail station at Golborne, Wigan. 
        We need origin-destination data showing 
        current movement patterns in the area 
        to assess potential station usage and 
        justify the business case.
    """
}

media_samples = {
    "Select a sample brief...": "",
    "👟 Premium Gym Wear Launch": """
        Brand: Premium athletic wear brand 
        launching new performance running line.
        Target: Health-conscious professionals 
        aged 25-40, household income £60k+.
        Budget: £80,000 OOH London.
        Objective: Drive footfall to flagship 
        Covent Garden store and online 
        conversion via QR codes.
        Format preference: DOOH screens.
        Campaign duration: 6 weeks.
    """,
    "💳 Luxury Financial Services": """
        Brand: Private banking division of 
        a major UK bank.
        Target: High-net-worth individuals, 
        C-suite executives, age 40-65.
        Budget: £200,000 premium OOH.
        Objective: Brand awareness and 
        appointment bookings.
        Format: Large format premium sites.
        Duration: 12 weeks.
    """,
    "🍔 Fast Casual Food Delivery": """
        Brand: Direct-to-consumer lunch 
        delivery app targeting office workers.
        Target: Urban professionals ordering 
        lunch, aged 22-38.
        Budget: £25,000.
        Objective: App downloads and 
        first orders during lunch hours.
        Format: Any digital.
        Duration: 4 weeks.
    """
}

# ============================================
# DYNAMIC INPUT BASED ON SECTOR
# ============================================
if "Transport" in sector:
    st.subheader("🚌 Transport Intelligence Query")
    selected = st.selectbox(
        "Load a sample query (optional)",
        options=list(transport_samples.keys())
    )
    default = transport_samples[selected]
    placeholder = """Describe your transport 
planning question here. Include location, 
scale of development or event, and what 
decisions this analysis will inform..."""
    input_label = "Or describe your transport planning question"
    
else:
    st.subheader("📺 Media Campaign Brief")
    selected = st.selectbox(
        "Load a sample brief (optional)",
        options=list(media_samples.keys())
    )
    default = media_samples[selected]
    placeholder = """Describe your campaign brief 
here. Include brand, target audience, budget, 
objective, and preferred format..."""
    input_label = "Or paste your campaign brief"

user_input = st.text_area(
    input_label,
    value=default,
    height=180,
    placeholder=placeholder
)

st.divider()

# ============================================
# GENERATE BUTTON
# ============================================
generate_clicked = st.button(
    "📊 Generate Intelligence Report",
    type="primary",
    use_container_width=True
)

# ============================================
# SYSTEM PROMPTS — ONE PER SECTOR
# ============================================
transport_prompt = """
You are a senior transport data analyst 
with 15 years of experience working with 
mobile network data for UK transport planning.

You help transport authorities, government 
departments, and infrastructure consultancies 
make evidence-based decisions using 
anonymised mobile network data.

You must always respond in EXACTLY this format:

QUERY TYPE: [Traffic Impact / Origin-Destination / 
             Event Analysis / Infrastructure Assessment]

EXECUTIVE SUMMARY: [3 sentences maximum, 
plain English, no jargon, suitable for 
a council executive or minister]

KEY FINDINGS:
- [Finding 1 with specific insight]
- [Finding 2 with specific insight]
- [Finding 3 with specific insight]

DATA SIGNALS TO ANALYSE:
- [Specific mobile data type needed 1]
- [Specific mobile data type needed 2]
- [Specific mobile data type needed 3]

INFRASTRUCTURE IMPLICATIONS:
[2-3 sentences on what this means for 
physical infrastructure decisions]

RECOMMENDED ACTIONS:
1. [Immediate action]
2. [Short term action]
3. [Longer term consideration]

CONFIDENCE: [High/Medium/Low]
REASON: [One sentence on data availability 
and coverage for this query]

LIMITATIONS: [One sentence on what this 
analysis cannot tell us and why]

Rules you must never break:
- Never invent specific traffic counts 
  or percentages not derivable from the query
- Always flag when query needs more 
  geographic specificity
- Never skip the limitations section
- If query is too vague, return CONFIDENCE: Low
  and ask for specific location and scale
- Always write for a non-technical 
  decision maker audience
"""

media_prompt = """
You are a senior media planning strategist 
with deep expertise in UK Out-of-Home 
advertising and mobile audience data.

You help media agencies, brands, and 
media owners make evidence-based OOH 
investment decisions using anonymised 
mobile network footfall data.

You must always respond in EXACTLY this format:

CAMPAIGN TYPE: [Brand Awareness / Footfall 
               Driver / App Downloads / 
               Product Launch]

EXECUTIVE SUMMARY: [3 sentences maximum, 
plain English, suitable for a brand 
manager or marketing director]

RECOMMENDED LOCATIONS:
- [Location 1: type, why it fits, 
  audience match score High/Medium/Low]
- [Location 2: type, why it fits, 
  audience match score High/Medium/Low]
- [Location 3: type, why it fits, 
  audience match score High/Medium/Low]

PEAK AUDIENCE TIMES:
- [Best time window 1 and why]
- [Best time window 2 and why]

AUDIENCE PROFILE FROM MOBILE DATA:
[3 sentences describing the target 
audience movement patterns relevant 
to this campaign]

BUDGET ALLOCATION RECOMMENDATION:
[2 sentences on how to split budget 
across location types]

ESTIMATED REACH: [Weekly unique audience 
estimate with confidence caveat]

CONFIDENCE: [High/Medium/Low]
REASON: [One sentence on how well 
the brief maps to available data]

ATTRIBUTION APPROACH: [One sentence on 
how campaign effectiveness can be 
measured using footfall data post-campaign]

Rules you must never break:
- Never invent specific footfall numbers 
  without caveating them as estimates
- Always include attribution approach — 
  this is BT data's key differentiator
- Never recommend locations without 
  explaining audience match rationale
- If budget seems misaligned with 
  objectives, flag it diplomatically
- Always write for a non-data-scientist 
  decision maker
"""

# ============================================
# CORE FUNCTION
# ============================================
def generate_report(query, system_prompt, key):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key
    )
    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", 
             "content": f"Generate intelligence report for:\n\n{query}"}
        ]
    )
    return response.choices[0].message.content

# ============================================
# OUTPUT
# ============================================
if generate_clicked:
    if not api_key:
        st.error("Please enter your OpenRouter API key.")
    elif not user_input or user_input.strip() == "":
        st.error("Please enter a query or select a sample.")
    else:
        with st.spinner("Analysing mobile network data patterns..."):
            
            prompt = (transport_prompt 
                     if "Transport" in sector 
                     else media_prompt)
            
            result = generate_report(
                user_input, prompt, api_key
            )
            
            st.divider()
            st.subheader("📊 Intelligence Report")
            
            # Confidence colour coding
            if "CONFIDENCE: High" in result:
                st.success("🟢 Data Confidence: High")
            elif "CONFIDENCE: Medium" in result:
                st.info("🟡 Data Confidence: Medium")
            else:
                st.warning("🟠 Data Confidence: Low")
            
            st.code(result, language=None)
            
            st.download_button(
                label="📋 Download Report",
                data=result,
                file_name="network_intelligence_report.txt",
                mime="text/plain"
            )
            
            st.divider()
            
            # Feedback layer
            st.subheader("📈 Analyst Feedback")
            st.markdown(
                "Was this report useful for "
                "your decision making?"
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("✅ Used directly")
            with col2:
                st.button("✏️ Needed adjustment")
            with col3:
                st.button("❌ Not useful")
            st.caption(
                "Feedback improves future reports. "
                "North star: % used without adjustment."
            )

# ============================================
# SIDEBAR — PRODUCT CONTEXT
# ============================================
with st.sidebar:
    st.markdown("### About This Tool")
    st.markdown("""
    Built to demonstrate AI product management 
    capabilities at the intersection of mobile 
    network data and AI-powered intelligence.
    
    **Powered by:**
    - Anonymised mobile network data
    - Large Language Models via OpenRouter
    - BT Active Intelligence methodology
    
    **Two verticals. One engine.**
    - 🚌 Transport planning
    - 📺 Media & advertising
    
    **Portfolio project by:**  
    Soham Sarkar  
    Senior PM, BT
    """)
    
    st.divider()
    st.markdown("### Key Product Decisions")
    st.markdown("""
    1. Sector selector at entry — same 
    engine, different output format
    
    2. Plain English input — users are 
    not data scientists
    
    3. Confidence scoring mandatory — 
    flags data gaps honestly
    
    4. Attribution built in — BT data's 
    core differentiator for media
    
    5. Limitations always shown — 
    trust through honesty
    """)

# ============================================
# FOOTER
# ============================================
st.divider()
st.markdown("""
<small>
Portfolio project demonstrating AI product 
management at the intersection of mobile 
network data and generative AI.  
GitHub: github.com/Soham-S-Sarkar/ai-network-intelligence
</small>
""", unsafe_allow_html=True)
