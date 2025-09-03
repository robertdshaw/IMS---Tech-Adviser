import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Public Interest Infrastructure Assessment",
    page_icon="🌍",
    layout="wide",
)

# CSS styling
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

# Initialize session state
if "assessment_data" not in st.session_state:
    st.session_state.assessment_data = {}

if "tool_scores" not in st.session_state:
    st.session_state.tool_scores = {}


def calculate_dimension_score(responses, dimension):
    """Calculate score for a specific dimension based on responses"""
    # This is a simplified scoring mechanism
    if dimension in responses:
        return responses[dimension]
    return 0.5  # Default middle score


def calculate_overall_score(privacy, community, sustainability, weights):
    """Calculate weighted overall public interest score"""
    total = (
        privacy * weights["privacy"]
        + community * weights["community"]
        + sustainability * weights["sustainability"]
    )
    return total


def generate_recommendations(scores, context):
    """Generate tool recommendations based on scores and context"""
    recommendations = []

    # Privacy-focused tools
    if scores["privacy"] < 0.5:
        if context["connectivity"] == "High":
            recommendations.append(
                {
                    "category": "Secure Communication",
                    "suggestion": "Consider Signal or Element for encrypted messaging",
                    "trade_off": "May reduce reach compared to WhatsApp",
                    "example": "JamiiAfrica uses Tor to protect user anonymity",
                }
            )
        else:
            recommendations.append(
                {
                    "category": "Offline-First Privacy",
                    "suggestion": "Implement Briar or local mesh networks",
                    "trade_off": "Limited to local network reach",
                    "example": "CGNet Swara uses Bluetooth for offline sharing",
                }
            )

    # Community engagement tools
    if scores["community"] < 0.5:
        recommendations.append(
            {
                "category": "Community Platforms",
                "suggestion": "Deploy Discourse or local language forums",
                "trade_off": "Requires moderation resources",
                "example": "JamiiAfrica built Swahili-first forums",
            }
        )

    # Sustainability considerations
    if scores["sustainability"] < 0.5:
        recommendations.append(
            {
                "category": "Open Source Solutions",
                "suggestion": "Migrate to Nextcloud or similar self-hosted options",
                "trade_off": "Higher technical maintenance needs",
                "example": "Community-maintained infrastructure",
            }
        )

    return recommendations


def create_radar_chart(current_scores, target_scores, dimensions):
    """Create a radar chart comparing current vs target scores"""

    fig = go.Figure()

    # Current scores
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

    # Target scores
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


def create_trade_off_matrix(tools):
    """Create a visualization of tool trade-offs"""

    # Sample data for demonstration
    tools_data = {
        "Tool": [
            "WhatsApp",
            "Signal",
            "Telegram",
            "Email Lists",
            "Forums",
            "Bluetooth Share",
        ],
        "Reach": [0.95, 0.3, 0.7, 0.5, 0.6, 0.2],
        "Privacy": [0.2, 0.95, 0.6, 0.4, 0.7, 0.9],
        "Cost": [0.9, 0.9, 0.8, 0.6, 0.4, 0.95],
        "Ease": [0.95, 0.7, 0.8, 0.5, 0.4, 0.3],
    }

    df = pd.DataFrame(tools_data)

    fig = px.scatter(
        df,
        x="Privacy",
        y="Reach",
        size="Cost",
        color="Ease",
        hover_name="Tool",
        size_max=30,
        title="Tool Trade-off Analysis: Privacy vs Reach",
        labels={
            "Privacy": "Privacy Protection →",
            "Reach": "Audience Reach →",
            "Cost": "Cost Efficiency",
            "Ease": "Ease of Use",
        },
        color_continuous_scale="viridis",
    )

    fig.update_layout(height=400)

    return fig


def main():
    st.markdown(
        '<h1 class="main-header">🌍 Public Interest Infrastructure Assessment</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    **Evaluate your organization's tech stack against public interest values**
    
    This framework helps community media and alternative platforms assess whether their digital tools 
    align with their values and mission. Based on the experiences of organizations like JamiiAfrica 
    (Tanzania) and CGNet Swara (India), we'll help you make informed decisions about your technology choices.
    """
    )

    # Sidebar configuration
    st.sidebar.header("⚙️ Assessment Configuration")

    # Organization Profile
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

    # Value Weights
    st.sidebar.subheader("Value Priorities")
    st.sidebar.markdown("*Adjust based on your mission (must sum to 100%)*")

    privacy_weight = st.sidebar.slider("Privacy & Security", 0, 100, 35, 5)
    community_weight = st.sidebar.slider("Community Ownership", 0, 100, 35, 5)
    sustainability_weight = st.sidebar.slider("Sustainability", 0, 100, 30, 5)

    # Normalize weights
    total_weight = privacy_weight + community_weight + sustainability_weight
    if total_weight > 0:
        weights = {
            "privacy": privacy_weight / total_weight,
            "community": community_weight / total_weight,
            "sustainability": sustainability_weight / total_weight,
        }
    else:
        weights = {"privacy": 0.33, "community": 0.33, "sustainability": 0.34}

    # Display weight distribution
    if abs(total_weight - 100) > 1:
        st.sidebar.warning(f"Weights sum to {total_weight}% (normalized automatically)")

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Assessment Overview",
            "🔧 Tool Evaluation",
            "⚖️ Trade-off Analysis",
            "📋 Recommendations",
            "📥 Export Report",
        ]
    )

    with tab1:
        st.subheader(f"Assessment Dashboard for {org_name}")

        # Current scores (simulated based on context)
        privacy_score = 0.4 if regulatory_pressure in ["High", "Severe"] else 0.6
        community_score = 0.5 if literacy_level == "Low" else 0.7
        sustainability_score = 0.3 if connectivity in ["None", "Low"] else 0.5

        # Calculate overall score
        overall_score = calculate_overall_score(
            privacy_score, community_score, sustainability_score, weights
        )

        # Display key metrics
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

        # Radar chart
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
        st.subheader("Tool-by-Tool Evaluation")

        # Tool assessment form
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### Current Tools")

            tools = st.multiselect(
                "Select tools you currently use:",
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
                    "Bluetooth Sharing",
                    "SMS",
                    "Radio",
                    "Other",
                ],
                default=["WhatsApp", "Facebook"],
            )

            primary_tool = st.selectbox(
                "Primary communication tool:",
                tools if tools else ["Select tools first"],
            )

        with col2:
            st.markdown("### Tool Assessment Matrix")

            if tools:
                assessment_data = []
                for tool in tools:
                    # Simulated scores - in production, these would be from a database
                    scores = {
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
                        "Facebook": {
                            "Privacy": 0.1,
                            "Reach": 0.95,
                            "Cost": 0.8,
                            "Control": 0.05,
                        },
                        "Forums": {
                            "Privacy": 0.7,
                            "Reach": 0.5,
                            "Cost": 0.4,
                            "Control": 0.9,
                        },
                    }

                    tool_score = scores.get(
                        tool,
                        {"Privacy": 0.5, "Reach": 0.5, "Cost": 0.5, "Control": 0.5},
                    )
                    assessment_data.append(
                        {
                            "Tool": tool,
                            "Privacy": f"{tool_score['Privacy']:.1%}",
                            "Reach": f"{tool_score['Reach']:.1%}",
                            "Cost Efficiency": f"{tool_score['Cost']:.1%}",
                            "User Control": f"{tool_score['Control']:.1%}",
                            "PI Alignment": f"{(tool_score['Privacy'] + tool_score['Control'])/2:.1%}",
                        }
                    )

                df = pd.DataFrame(assessment_data)
                st.dataframe(df, use_container_width=True)

                st.warning(
                    "⚠️ Tools with PI Alignment below 50% may compromise your public interest values"
                )

    with tab3:
        st.subheader("Understanding Trade-offs")

        # Add comprehensive explainer
        with st.expander("📖 Why trade-offs matter for public interest media"):
            st.markdown(
                """
            **The fundamental tension:**
            Tools that reach the most people often compromise privacy and community control. 
            Understanding these trade-offs helps you make intentional choices rather than 
            defaulting to convenient options.
            
            **Real-world examples:**
            
            🇹🇿 **JamiiAfrica chose anonymity over convenience:**
            - Rejected real-name policies to protect sources
            - Lost potential Facebook/Google integration
            - Result: Became Tanzania's trusted platform for sensitive disclosures
            
            🇮🇳 **CGNet Swara prioritized local access over scale:**
            - Built for feature phones instead of smartphones  
            - Used Bluetooth instead of internet
            - Result: Reached truly disconnected tribal communities
            
            **The cost of "free" platforms:**
            WhatsApp and Facebook appear cost-efficient but extract value through:
            - Behavioral data collection for advertising
            - Content moderation that may silence dissent
            - Algorithmic amplification beyond community control
            - Platform lock-in with no data portability
            
            **Making strategic choices:**
            Instead of using one tool for everything, consider a portfolio approach:
            - Sensitive content → High-privacy tools (Signal, encrypted email)
            - Public broadcasts → Wide-reach platforms (with awareness of risks)
            - Community building → Owned infrastructure (forums, mailing lists)
            """
            )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Privacy vs. Reach Trade-off Visualization")
            fig = create_trade_off_matrix(tools if "tools" in locals() else [])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Key Trade-off Patterns")

            st.info(
                """
            **High Privacy + Low Reach**
            - Signal, Briar, Tor
            - Best for: Sensitive content, whistleblowers
            - Example: JamiiAfrica's anonymous tips system
            """
            )

            st.warning(
                """
            **Low Privacy + High Reach**
            - WhatsApp, Facebook
            - Risk: Data harvesting, surveillance
            - Mitigation: Use only for public content
            """
            )

            st.success(
                """
            **Balanced Approach**
            - Telegram, Community Forums
            - Mixed content strategy
            - Example: CGNet's multi-channel approach
            """
            )

        # Remove scenario modeling section

    with tab4:
        st.subheader("Personalized Recommendations")

        # Generate recommendations based on assessment
        recommendations = []

        # Privacy recommendations
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

        # Community control recommendations
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

        # Sustainability recommendations
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

        # Display recommendations
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

        # Implementation roadmap
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

    with tab5:
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

            # Identify primary gaps
            if privacy_score < 0.5:
                report_data["Primary Gaps"].append("Privacy & Security")
            if community_score < 0.6:
                report_data["Primary Gaps"].append("Community Ownership")
            if sustainability_score < 0.5:
                report_data["Primary Gaps"].append("Platform Sustainability")

            # Add top recommendations
            for rec in recommendations[:3]:
                report_data["Key Recommendations"].append(rec["Action"])

            # Display report preview
            st.json(report_data)

        with col2:
            st.markdown("### Export Options")

            # Export buttons
            if st.button("📄 Generate PDF Report", type="primary"):
                st.success(
                    "PDF report generated! (In production, this would download a formatted PDF)"
                )

            if st.button("📊 Export to CSV"):
                st.success(
                    "Data exported to CSV! (In production, this would download assessment data)"
                )

            if st.button("📧 Email to Team"):
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
