import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

from PIL import Image

# Load the logo image
try:
    logo = Image.open("logo2.png")
    st.set_page_config(
        page_title="Public Interest Infrastructure Assessment",
        page_icon=logo,
        layout="wide",
    )
except Exception as e:
    print(f"Could not load logo: {e}")
    st.set_page_config(
        page_title="Public Interest Infrastructure Assessment",
        page_icon="🏢",  # Fallback emoji
        layout="wide",
    )

st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        color: #1a365d;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1ecf1;
        border: 1px solid #b8daff;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border: 1px solid #b8daff;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

if "assessment_data" not in st.session_state:
    st.session_state.assessment_data = {}

if "tool_scores" not in st.session_state:
    st.session_state.tool_scores = {}


def calculate_dimension_score(responses, dimension):
    """Calculate score for a specific dimension based on responses"""
    if dimension in responses:
        return responses[dimension]
    return 0.5


def calculate_overall_score(privacy, community, sustainability, weights):
    """Calculate weighted overall public interest score"""
    total = (
        privacy * weights["privacy"]
        + community * weights["community"]
        + sustainability * weights["sustainability"]
    )
    return total


def create_radar_chart(current_scores, target_scores, dimensions):
    """Create a radar chart comparing current vs target scores"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=list(current_scores.values()),
            theta=list(dimensions.values()),
            fill="toself",
            name="Current State",
            fillcolor="rgba(102, 126, 234, 0.25)",
            line=dict(color="rgba(102, 126, 234, 1)", width=2),
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=list(target_scores.values()),
            theta=list(dimensions.values()),
            fill="toself",
            name="Target State",
            fillcolor="rgba(16, 185, 129, 0.25)",
            line=dict(color="rgba(16, 185, 129, 1)", width=2),
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Public Interest Alignment Assessment",
        height=500,
    )

    return fig


def create_trade_off_matrix(selected_tools):
    """Create a visualization of tool trade-offs"""
    tools_data = {
        "Tool": [
            "WhatsApp",
            "Signal",
            "Telegram",
            "Email Lists",
            "Forums",
            "Bluetooth Share",
            "SMS",
            "Radio",
            "WordPress",
            "Custom Platform",
        ],
        "Reach": [0.95, 0.3, 0.7, 0.5, 0.6, 0.2, 0.8, 0.9, 0.7, 0.4],
        "Privacy": [0.2, 0.95, 0.6, 0.4, 0.7, 0.9, 0.3, 0.5, 0.6, 0.8],
        "Cost": [0.9, 0.9, 0.8, 0.6, 0.4, 0.95, 0.7, 0.3, 0.5, 0.2],
        "Ease": [0.95, 0.7, 0.8, 0.5, 0.4, 0.3, 0.9, 0.8, 0.7, 0.3],
    }

    df = pd.DataFrame(tools_data)
    df["Selected"] = df["Tool"].isin(selected_tools)
    df["Size"] = df["Selected"].apply(lambda x: 100 if x else 50)

    fig = px.scatter(
        df,
        x="Privacy",
        y="Reach",
        size="Size",
        color="Ease",
        hover_name="Tool",
        size_max=40,
        title="Tool Trade-off Analysis: Privacy vs Reach",
        labels={
            "Privacy": "Privacy Protection →",
            "Reach": "Audience Reach →",
            "Ease": "Ease of Use",
        },
        color_continuous_scale="viridis",
    )

    for tool in selected_tools:
        tool_data = df[df["Tool"] == tool]
        if not tool_data.empty:
            fig.add_scatter(
                x=tool_data["Privacy"],
                y=tool_data["Reach"],
                mode="markers",
                marker=dict(
                    size=25, color="rgba(0,0,0,0)", line=dict(color="red", width=3)
                ),
                showlegend=False,
                hoverinfo="skip",
            )

    fig.update_layout(height=450)
    return fig


def main():
    # Simple logo above title
    try:
        from PIL import Image

        logo = Image.open("logo.png")

        # Center the logo
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.image(logo, width=120)
    except:
        pass  # Just skip logo if it fails

    st.markdown(
        '<h1 class="main-header">Public Interest Infrastructure Assessment</h1>\n\n'
        "**Evaluate your organization's tech stack against public interest values**\n\n"
        "This framework helps community media and alternative platforms assess whether their digital tools "
        "align with their values and mission. Based on the experiences of organizations like JamiiAfrica "
        "(Tanzania) and CGNet Swara (India), we'll help you make informed decisions about your technology choices.",
        unsafe_allow_html=True,
    )

    st.sidebar.header("⚙️ Assessment Configuration")

    # Org profile
    st.sidebar.subheader("Organization Profile")
    org_name = st.sidebar.text_input("Organization Name", "Your Organization")

    org_type = st.sidebar.selectbox(
        "Organization Type",
        [
            "Community Media",
            "Digital Newsroom",
            "Citizen Forum",
            "Audio Platform",
            "Hybrid Platform",
        ],
    )

    region = st.sidebar.selectbox(
        "Region",
        [
            "East Africa",
            "West Africa",
            "Central Africa",
            "Southern Africa",
            "South Asia",
            "Southeast Asia",
            "Latin America",
            "Other",
        ],
    )

    # Context factors
    st.sidebar.subheader("Operating Context")

    connectivity = st.sidebar.select_slider(
        "Average Connectivity Level",
        options=["None", "Low", "Medium", "High"],
        value="Medium",
    )

    literacy_level = st.sidebar.select_slider(
        "Audience Digital Literacy", options=["Low", "Medium", "High"], value="Medium"
    )

    regulatory_pressure = st.sidebar.select_slider(
        "Regulatory Pressure",
        options=["Low", "Medium", "High", "Severe"],
        value="Medium",
    )

    st.sidebar.subheader("Value Priorities")
    st.sidebar.markdown("*Adjust based on your mission (must sum to 100%)*")

    privacy_weight = st.sidebar.slider("Privacy & Security", 0, 100, 35, 5)
    community_weight = st.sidebar.slider("Community Ownership", 0, 100, 35, 5)
    sustainability_weight = st.sidebar.slider("Sustainability", 0, 100, 30, 5)

    total_weight = privacy_weight + community_weight + sustainability_weight
    if total_weight > 0:
        weights = {
            "privacy": privacy_weight / total_weight,
            "community": community_weight / total_weight,
            "sustainability": sustainability_weight / total_weight,
        }
    else:
        weights = {"privacy": 0.33, "community": 0.33, "sustainability": 0.34}

    if abs(total_weight - 100) > 1:
        st.sidebar.warning(f"Weights sum to {total_weight}% (normalized automatically)")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            " Assessment Overview",
            " Tool Assessment & Trade-offs",
            " Recommendations",
            " Export Report",
        ]
    )

    # Calculate scores based on context
    privacy_score = 0.4 if regulatory_pressure in ["High", "Severe"] else 0.6
    community_score = 0.5 if literacy_level == "Low" else 0.7
    sustainability_score = 0.3 if connectivity in ["None", "Low"] else 0.5
    overall_score = calculate_overall_score(
        privacy_score, community_score, sustainability_score, weights
    )

    with tab1:
        st.subheader(f"Assessment Dashboard for {org_name}")

        with st.expander("How to read this dashboard", expanded=False):
            st.markdown(
                """
            **Overall PI Score**: Your weighted average across all public interest dimensions. 
            Target of 75% represents strong alignment with public interest values.
            
            **Privacy Score**: Measures how well your tools protect user data, enable anonymity, 
            and resist surveillance. Critical for organizations like JamiiAfrica operating under 
            government pressure.
            
            **Community Score**: This checks whether the people actually using the platform have real power. 
            Can they help run it, shape decisions, and see content in their own languages? If yes, the score goes up.
            
            **Sustainability**: Can your platform keep running without being chained to expensive corporate tools or big tech companies? 
            If it’s low-cost, independent, and not locked-in, the score is strong.
            
            **Gaps**: The percentage difference from recommended targets based on global best 
            practices for public interest media.
            """
            )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Overall PI Score", f"{overall_score:.1%}", delta="Target: 75%")

        with col2:
            st.metric(
                "Privacy Score",
                f"{privacy_score:.1%}",
                delta=f"Gap: {(0.8 - privacy_score):.1%}",
            )

        with col3:
            st.metric(
                "Community Score",
                f"{community_score:.1%}",
                delta=f"Gap: {(0.75 - community_score):.1%}",
            )

        with col4:
            st.metric(
                "Sustainability",
                f"{sustainability_score:.1%}",
                delta=f"Gap: {(0.7 - sustainability_score):.1%}",
            )

        col1, col2 = st.columns([2, 1])

        with col1:
            current = {
                "privacy": privacy_score,
                "community": community_score,
                "sustainability": sustainability_score,
            }

            target = {"privacy": 0.8, "community": 0.75, "sustainability": 0.7}

            dimensions = {
                "privacy": "Privacy & Security",
                "community": "Community Ownership",
                "sustainability": "Sustainability",
            }

            fig = create_radar_chart(current, target, dimensions)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Gap Analysis")

            gaps = {
                "Privacy & Security": 0.8 - privacy_score,
                "Community Ownership": 0.75 - community_score,
                "Sustainability": 0.7 - sustainability_score,
            }

            for dimension, gap in gaps.items():
                if gap > 0.3:
                    st.error(f"🔴 {dimension}: {gap:.1%} gap")
                elif gap > 0.15:
                    st.warning(f"🟡 {dimension}: {gap:.1%} gap")
                else:
                    st.success(f"🟢 {dimension}: {gap:.1%} gap")

            st.markdown("---")
            st.markdown("### Context Factors")
            st.info(f"**Connectivity:** {connectivity}")
            st.info(f"**Digital Literacy:** {literacy_level}")
            st.info(f"**Regulatory:** {regulatory_pressure}")

    with tab2:
        st.subheader("Tool Assessment & Trade-off Analysis")

        with st.expander("Understanding Tool Assessment & Trade-offs", expanded=False):
            st.markdown(
                """
            **Why this matters:**
            Each tool in your stack involves trade-offs. WhatsApp reaches everyone but compromises privacy. 
            Signal protects privacy but limits reach. Understanding these trade-offs helps you make 
            intentional choices aligned with your mission.
            
            **How to use this assessment:**
            1. Select your current tools on the left
            2. Review their scores in the table
            3. See how they map on the trade-off visualization
            4. Red circles highlight your selected tools
            
            **Real-world examples:**
            - **JamiiAfrica**: Chose anonymity over reach, using Tor despite lower user numbers
            - **CGNet Swara**: Prioritized offline access with Bluetooth over internet scale
            
            **Strategic approach:**
            Use different tools for different purposes:
            - Sensitive content → High-privacy tools (Signal, Tor)
            - Public broadcasts → High-reach platforms (with awareness of risks)
            - Community building → Owned infrastructure (forums, mailing lists)
            """
            )

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### Select Your Current Tools")

            tools = st.multiselect(
                "Which tools does your organization currently use?",
                [
                    "WhatsApp",
                    "Signal",
                    "Telegram",
                    "Facebook",
                    "Twitter/X",
                    "Email Lists",
                    "Forums",
                    "WordPress",
                    "Custom Platform",
                    "Bluetooth Share",
                    "SMS",
                    "Radio",
                    "Other",
                ],
                default=["WhatsApp", "Facebook"],
                help="Select all tools currently in your tech stack",
            )

            st.markdown("---")

            if tools:
                high_privacy = [
                    t
                    for t in tools
                    if t in ["Signal", "Bluetooth Share", "Custom Platform"]
                ]
                low_privacy = [
                    t for t in tools if t in ["WhatsApp", "Facebook", "Twitter/X"]
                ]

                if low_privacy and not high_privacy:
                    st.warning("Your stack lacks privacy-preserving tools")
                elif high_privacy and not low_privacy:
                    st.info("Limited reach but strong privacy")
                elif high_privacy and low_privacy:
                    st.success("Balanced portfolio approach")

        with col2:
            if tools:
                st.markdown("### Tool Scoring Matrix")

                assessment_data = []
                tool_scores = {
                    "WhatsApp": {
                        "Privacy": 0.2,
                        "Reach": 0.9,
                        "Cost": 0.9,
                        "Control": 0.1,
                    },
                    "Signal": {
                        "Privacy": 0.9,
                        "Reach": 0.3,
                        "Cost": 0.9,
                        "Control": 0.7,
                    },
                    "Telegram": {
                        "Privacy": 0.6,
                        "Reach": 0.7,
                        "Cost": 0.8,
                        "Control": 0.5,
                    },
                    "Facebook": {
                        "Privacy": 0.1,
                        "Reach": 0.95,
                        "Cost": 0.8,
                        "Control": 0.05,
                    },
                    "Twitter/X": {
                        "Privacy": 0.2,
                        "Reach": 0.8,
                        "Cost": 0.9,
                        "Control": 0.1,
                    },
                    "Email Lists": {
                        "Privacy": 0.4,
                        "Reach": 0.5,
                        "Cost": 0.6,
                        "Control": 0.8,
                    },
                    "Forums": {
                        "Privacy": 0.7,
                        "Reach": 0.5,
                        "Cost": 0.4,
                        "Control": 0.9,
                    },
                    "WordPress": {
                        "Privacy": 0.6,
                        "Reach": 0.7,
                        "Cost": 0.5,
                        "Control": 0.8,
                    },
                    "Custom Platform": {
                        "Privacy": 0.8,
                        "Reach": 0.4,
                        "Cost": 0.2,
                        "Control": 1.0,
                    },
                    "Bluetooth Share": {
                        "Privacy": 0.9,
                        "Reach": 0.2,
                        "Cost": 0.95,
                        "Control": 0.8,
                    },
                    "SMS": {"Privacy": 0.3, "Reach": 0.8, "Cost": 0.7, "Control": 0.2},
                    "Radio": {
                        "Privacy": 0.5,
                        "Reach": 0.9,
                        "Cost": 0.3,
                        "Control": 0.4,
                    },
                }

                for tool in tools:
                    scores = tool_scores.get(
                        tool,
                        {"Privacy": 0.5, "Reach": 0.5, "Cost": 0.5, "Control": 0.5},
                    )
                    pi_alignment = (scores["Privacy"] + scores["Control"]) / 2

                    assessment_data.append(
                        {
                            "Tool": tool,
                            "Privacy": f"{scores['Privacy']:.1%}",
                            "Reach": f"{scores['Reach']:.1%}",
                            "Cost Eff.": f"{scores['Cost']:.1%}",
                            "Control": f"{scores['Control']:.1%}",
                            "PI Score": f"{pi_alignment:.1%}",
                        }
                    )

                df = pd.DataFrame(assessment_data)

                def highlight_pi_score(val):
                    try:
                        score = float(val.strip("%")) / 100
                        if score < 0.3:
                            return "background-color: #ffcccc"
                        elif score < 0.5:
                            return "background-color: #ffffcc"
                        else:
                            return "background-color: #ccffcc"
                    except:
                        return ""

                styled_df = df.style.applymap(highlight_pi_score, subset=["PI Score"])
                st.dataframe(styled_df, use_container_width=True)

                if any(
                    float(row["PI Score"].strip("%")) < 50 for row in assessment_data
                ):
                    st.warning(
                        "Tools with PI Score below 50% extract value from your community through data harvesting"
                    )

    with tab3:
        st.subheader("Personalized Recommendations")

        recommendations = []

        if privacy_score < 0.5:
            recommendations.append(
                {
                    "Priority": "HIGH",
                    "Area": "Privacy & Security",
                    "Action": "Implement encrypted communication tools",
                    "Specific": "Deploy Signal for sensitive communications, keep WhatsApp for public broadcasts",
                    "Example": "JamiiAfrica uses Tor for anonymous submissions while maintaining public forums",
                    "Timeline": "Next 30 days",
                }
            )

        if community_score < 0.6:
            recommendations.append(
                {
                    "Priority": "MEDIUM",
                    "Area": "Community Ownership",
                    "Action": "Build local language tools",
                    "Specific": "Create Swahili/Hindi/local language interfaces",
                    "Example": "CGNet Swara's Gondi language voice platform",
                    "Timeline": "Next 90 days",
                }
            )

        if sustainability_score < 0.5:
            recommendations.append(
                {
                    "Priority": "MEDIUM",
                    "Area": "Sustainability",
                    "Action": "Reduce platform dependency",
                    "Specific": "Implement self-hosted alternatives like Nextcloud",
                    "Example": "Community-maintained infrastructure",
                    "Timeline": "Next 6 months",
                }
            )

        for rec in recommendations:
            if rec["Priority"] == "HIGH":
                st.error(f"🔴 **{rec['Priority']} PRIORITY: {rec['Area']}**")
            else:
                st.warning(f"🟡 **{rec['Priority']} PRIORITY: {rec['Area']}**")

            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Action:** {rec['Action']}")
                st.markdown(f"**Specific Steps:** {rec['Specific']}")
                st.markdown(f"**Case Study:** {rec['Example']}")
            with col2:
                st.markdown(f"**Timeline:** {rec['Timeline']}")

        st.markdown("### Implementation Roadmap")

        phases = {
            "Phase 1 (Month 1)": [
                "Audit current tool permissions and data policies",
                "Survey community on tool preferences",
                "Test high-priority alternatives with small group",
            ],
            "Phase 2 (Months 2-3)": [
                "Implement encrypted tools for sensitive content",
                "Train staff on new platforms",
                "Develop migration plan for community",
            ],
            "Phase 3 (Months 4-6)": [
                "Full deployment of new tools",
                "Monitor adoption and gather feedback",
                "Iterate based on community needs",
            ],
        }

        for phase, tasks in phases.items():
            with st.expander(phase):
                for task in tasks:
                    st.checkbox(task, key=f"{phase}_{task}")

    with tab4:
        st.subheader("Export Assessment Report")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Report Summary")

            report_data = {
                "Organization": org_name,
                "Type": org_type,
                "Region": region,
                "Assessment Date": datetime.now().strftime("%Y-%m-%d"),
                "Overall PI Score": f"{overall_score:.1%}",
                "Privacy Score": f"{privacy_score:.1%}",
                "Community Score": f"{community_score:.1%}",
                "Sustainability Score": f"{sustainability_score:.1%}",
                "Primary Gaps": [],
                "Key Recommendations": [],
            }

            if privacy_score < 0.5:
                report_data["Primary Gaps"].append("Privacy & Security")
            if community_score < 0.6:
                report_data["Primary Gaps"].append("Community Ownership")
            if sustainability_score < 0.5:
                report_data["Primary Gaps"].append("Platform Sustainability")

            for rec in recommendations[:3]:
                report_data["Key Recommendations"].append(rec["Action"])

            st.json(report_data)

        with col2:
            st.markdown("### Export Options")

            if st.button("Generate PDF Report", type="primary"):
                st.success(
                    "PDF report generated! (In production, this would download a formatted PDF)"
                )

            if st.button("Export to CSV"):
                st.success(
                    "Data exported to CSV! (In production, this would download assessment data)"
                )

            if st.button("Email to Team"):
                st.success(
                    "Report sent to team! (In production, this would send an email)"
                )

            st.markdown("---")
            st.markdown("### Share with Funders")
            st.info(
                """
            This report demonstrates your commitment to public interest values and provides 
            evidence-based justification for technology investments.
            """
            )


if __name__ == "__main__":
    main()
