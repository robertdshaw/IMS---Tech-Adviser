import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="PIM Dashboard - Simple Version", layout="wide")

st.title("📊 Public Interest Media KPI Dashboard")
st.markdown("*Adapting User Needs Model for Civic Impact Measurement*")

# Sidebar - Simple explanation
st.sidebar.markdown(
    """
### Quick Setup Guide
1. Adjust the weights to match your organization's mission
2. View how different priorities affect your score
3. See recommendations based on gaps

**This is a prototype using simulated data**
"""
)

# User Needs Weights - Keep it simple with normalized sliders
st.sidebar.markdown("### Set Your Priorities")
st.sidebar.markdown("*What matters most to your organization?*")

col1, col2 = st.sidebar.columns(2)
with col1:
    educate = st.slider("Educate", 0, 10, 4)
    perspective = st.slider("Perspective", 0, 10, 3)
    help = st.slider("Help", 0, 10, 2)
with col2:
    update = st.slider("Update", 0, 10, 1)
    inspire = st.slider("Inspire", 0, 10, 1)

# Normalize weights
total = educate + perspective + help + update + inspire
if total == 0:
    total = 1

weights = {
    "Educate": educate / total,
    "Perspective": perspective / total,
    "Help": help / total,
    "Update": update / total,
    "Inspire": inspire / total,
}


# SIMPLIFIED DATA SIMULATION
# In real world, this would connect to your analytics
@st.cache_data
def get_mock_performance_data():
    """
    Simulates performance data for each user need category
    In production, this would pull from:
    - Google Analytics (engagement)
    - CMS (content analysis)
    - Surveys (impact measurement)
    """
    # Current performance (simulate realistic scores)
    current_performance = {
        "Educate": np.random.uniform(0.5, 0.7),  # Usually decent
        "Perspective": np.random.uniform(0.4, 0.6),  # Often challenging
        "Help": np.random.uniform(0.2, 0.4),  # Usually low
        "Update": np.random.uniform(0.6, 0.8),  # Usually good
        "Inspire": np.random.uniform(0.3, 0.5),  # Variable
    }

    # Set realistic targets based on industry benchmarks
    targets = {
        "Educate": 0.70,
        "Perspective": 0.65,
        "Help": 0.50,
        "Update": 0.75,
        "Inspire": 0.60,
    }

    return current_performance, targets


performance, targets = get_mock_performance_data()

# Calculate Public Interest Score
public_interest_score = sum(performance[k] * weights[k] for k in weights.keys())

# MAIN METRICS DISPLAY
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🎯 Public Interest Score",
        f"{public_interest_score:.1%}",
        help="Weighted average of all category performances",
    )

with col2:
    # Simple trust proxy (combination of metrics)
    trust_score = np.mean(list(performance.values())) * 1.4  # Simplified
    st.metric(
        "🤝 Trust Indicator",
        f"{min(trust_score, 1.0):.1%}",
        help="Simplified trust measurement",
    )

with col3:
    # Biggest gap
    gaps = {k: targets[k] - performance[k] for k in performance.keys()}
    biggest_gap = max(gaps.items(), key=lambda x: x[1])
    st.metric(
        "⚠️ Biggest Gap",
        f"{biggest_gap[0]}",
        f"-{biggest_gap[1]:.1%}",
        help="Area needing most improvement",
    )

with col4:
    # Improvement potential
    potential = sum(
        max(0, targets[k] - performance[k]) * weights[k] for k in weights.keys()
    )
    st.metric(
        "📈 Improvement Potential",
        f"+{potential:.1%}",
        help="Possible score increase if targets met",
    )

# VISUALIZATION SECTION
st.markdown("---")
st.subheader("Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    # Simple Radar Chart
    categories = list(weights.keys())

    fig = go.Figure()

    # Current Performance
    fig.add_trace(
        go.Scatterpolar(
            r=[performance[cat] for cat in categories],
            theta=categories,
            fill="toself",
            name="Current",
            line_color="rgb(31, 119, 180)",
        )
    )

    # Targets
    fig.add_trace(
        go.Scatterpolar(
            r=[targets[cat] for cat in categories],
            theta=categories,
            fill="toself",
            name="Target",
            line_color="rgb(255, 127, 14)",
            opacity=0.3,
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Current vs Target Performance",
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Weighted Contribution Bar Chart
    contribution_data = pd.DataFrame(
        {
            "Category": categories,
            "Weight (%)": [weights[k] * 100 for k in categories],
            "Performance (%)": [performance[k] * 100 for k in categories],
            "Gap to Target (%)": [
                (targets[k] - performance[k]) * 100 for k in categories
            ],
        }
    )

    fig2 = px.bar(
        contribution_data,
        x="Category",
        y=["Weight (%)", "Performance (%)", "Gap to Target (%)"],
        title="Weights, Performance, and Gaps",
        barmode="group",
        color_discrete_map={
            "Weight (%)": "lightblue",
            "Performance (%)": "darkblue",
            "Gap to Target (%)": "red",
        },
    )
    st.plotly_chart(fig2, use_container_width=True)

# SIMPLE RECOMMENDATIONS
st.markdown("---")
st.subheader("📋 Recommendations Based on Your Weights")

# Sort by weighted importance of gaps
weighted_gaps = {k: gaps[k] * weights[k] for k in gaps.keys()}
sorted_gaps = sorted(weighted_gaps.items(), key=lambda x: x[1], reverse=True)

for category, weighted_gap in sorted_gaps[:3]:  # Top 3 priorities
    if gaps[category] > 0:  # Only show if there's actually a gap
        with st.expander(f"Priority: Improve {category} (Gap: {gaps[category]:.1%})"):

            # Specific recommendations by category
            if category == "Educate":
                st.markdown(
                    """
                **Quick Wins:**
                - Add reading time estimates to articles
                - Create summary boxes for key points
                - Use more infographics and visual explanations
                
                **Measurement:**
                - Track completion rates (scroll depth > 80%)
                - Add simple comprehension polls
                - Monitor time on page vs expected reading time
                """
                )

            elif category == "Perspective":
                st.markdown(
                    """
                **Quick Wins:**
                - Create a source diversity tracker spreadsheet
                - Set quotas for underrepresented voices
                - Add "different viewpoints" sidebar to articles
                
                **Measurement:**
                - Count unique sources per story
                - Track geographic diversity of sources
                - Monitor viewpoint balance in coverage
                """
                )

            elif category == "Help":
                st.markdown(
                    """
                **Quick Wins:**
                - Add "Take Action" boxes to relevant stories
                - Create civic engagement resource pages
                - Partner with local civic organizations
                
                **Measurement:**
                - Track clicks on civic action buttons
                - Survey readers about actions taken
                - Count resource downloads
                """
                )

            elif category == "Update":
                st.markdown(
                    """
                **Quick Wins:**
                - Improve breaking news push notifications
                - Create news summary newsletters
                - Speed up publishing workflow
                
                **Measurement:**
                - Track unique reach for breaking news
                - Monitor time to publish vs competitors
                - Measure notification engagement
                """
                )

            elif category == "Inspire":
                st.markdown(
                    """
                **Quick Wins:**
                - Launch "Solutions Friday" series
                - Highlight local success stories
                - Create shareable quote cards
                
                **Measurement:**
                - Track social shares of positive stories
                - Monitor sentiment in comments
                - Survey for inspired actions
                """
                )

# IMPLEMENTATION ROADMAP
st.markdown("---")
st.subheader("🗺️ Simple Implementation Plan")

tab1, tab2, tab3 = st.tabs(["Week 1: Setup", "Week 2-4: Pilot", "Month 2-3: Scale"])

with tab1:
    st.markdown(
        """
    ### Week 1: Basic Tracking Setup
    1. **Google Analytics Setup**
       - Enable scroll tracking
       - Set up event tracking for CTAs
       - Create custom reports
    
    2. **Content Tagging**
       - Tag articles by user need category
       - Start tracking sources in spreadsheet
       - Add feedback widgets to articles
    
    3. **Baseline Measurement**
       - Document current performance
       - Set initial targets
       - Share plan with team
    """
    )

with tab2:
    st.markdown(
        """
    ### Week 2-4: Pilot Program
    1. **Pick One Category to Focus**
       - Choose your biggest gap area
       - Implement 2-3 quick wins
       - Track daily metrics
    
    2. **Test and Learn**
       - A/B test different approaches
       - Gather team feedback
       - Adjust tactics based on data
    
    3. **Early Wins**
       - Document improvements
       - Share success stories
       - Build momentum
    """
    )

with tab3:
    st.markdown(
        """
    ### Month 2-3: Scale Up
    1. **Expand to All Categories**
       - Roll out tracking across all content
       - Train entire team
       - Automate reporting
    
    2. **Advanced Metrics**
       - Add survey components
       - Integrate multiple data sources
       - Build real dashboard
    
    3. **Strategic Integration**
       - Monthly KPI reviews
       - Quarterly target adjustments
       - Annual strategy alignment
    """
    )

# DATA EXPLANATION
with st.expander("📊 How Performance Scores Are Calculated"):
    st.markdown(
        """
    ### Simplified Calculation Method
    
    Each category performance score (0-100%) represents effectiveness, not volume:
    
    **Educate Performance = Average of:**
    - Completion rate (did they finish reading?)
    - Time on page (did they engage deeply?)
    - Comprehension (did they understand?)
    
    **Perspective Performance = Average of:**
    - Source diversity (how many different voices?)
    - Geographic spread (local vs national sources?)
    - Viewpoint balance (multiple perspectives?)
    
    **Help Performance = Average of:**
    - CTA click rate (did they click action buttons?)
    - Resource downloads (did they use tools?)
    - Follow-through (did they actually act?)
    
    **Update Performance = Average of:**
    - Reach (how many people informed?)
    - Speed (how quickly published?)
    - Accuracy (corrections needed?)
    
    **Inspire Performance = Average of:**
    - Share rate (did they spread the story?)
    - Positive sentiment (were they moved?)
    - Behavior change (did they act?)
    
    ### Public Interest Score
    ```
    Score = Σ(Performance × Weight) for all categories
    ```
    
    *Note: This demo uses simulated data. In production, connect to real analytics.*
    """
    )

# FOOTER
st.markdown("---")
st.caption(
    """
**For Your Test:** This dashboard demonstrates how to operationalize the User Needs Model for public interest media. 
The key innovation is shifting from engagement metrics (clicks, views) to impact metrics (learning, action, diversity).
The adjustable weights show how different organizations can prioritize based on their mission.
"""
)

# Add a final insight box
st.info(
    """
**💡 Key Insight for Your Interview:**

This framework bridges the gap between editorial mission and measurable impact. Unlike commercial media KPIs 
that optimize for attention, this system optimizes for civic outcomes while remaining practical to implement 
with existing tools like Google Analytics and simple surveys.
"""
)
