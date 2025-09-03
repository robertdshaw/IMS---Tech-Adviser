import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Public Interest Media KPI Dashboard", layout="wide")

# Title
st.title("Public Interest Media KPI Dashboard")
st.markdown("### Measuring Impact Through User Needs Framework")

# Sidebar for configuration
st.sidebar.header("Configuration")

# User Needs Weights for Public Interest Media
st.sidebar.subheader("User Needs Weights (%)")
educate_weight = st.sidebar.slider("Educate Me", 0, 100, 35)
perspective_weight = st.sidebar.slider("Give Me Perspective", 0, 100, 25)
help_weight = st.sidebar.slider("Help Me", 0, 100, 20)
update_weight = st.sidebar.slider("Update Me", 0, 100, 10)
inspire_weight = st.sidebar.slider("Inspire Me", 0, 100, 10)

# Normalize weights
total_weight = (
    educate_weight + perspective_weight + help_weight + update_weight + inspire_weight
)
if total_weight > 0:
    weights = {
        "Educate Me": educate_weight / total_weight,
        "Give Me Perspective": perspective_weight / total_weight,
        "Help Me": help_weight / total_weight,
        "Update Me": update_weight / total_weight,
        "Inspire Me": inspire_weight / total_weight,
    }
else:
    weights = {
        k: 0.2
        for k in [
            "Educate Me",
            "Give Me Perspective",
            "Help Me",
            "Update Me",
            "Inspire Me",
        ]
    }


# Generate sample data
@st.cache_data
def generate_sample_data():
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="W")

    data = {
        "date": dates,
        "educate_engagement": np.random.uniform(0.3, 0.7, len(dates)),
        "perspective_diversity": np.random.uniform(0.4, 0.8, len(dates)),
        "help_actions": np.random.uniform(0.1, 0.4, len(dates)),
        "update_reach": np.random.uniform(0.5, 0.9, len(dates)),
        "inspire_shares": np.random.uniform(0.2, 0.6, len(dates)),
        "trust_score": np.random.uniform(0.6, 0.9, len(dates)),
        "civic_participation": np.random.uniform(0.15, 0.45, len(dates)),
    }

    return pd.DataFrame(data)


df = generate_sample_data()


# Calculate Public Interest Score
def calculate_public_interest_score(row, weights):
    scores = {
        "Educate Me": row["educate_engagement"],
        "Give Me Perspective": row["perspective_diversity"],
        "Help Me": row["help_actions"],
        "Update Me": row["update_reach"],
        "Inspire Me": row["inspire_shares"],
    }

    weighted_score = sum(scores[k] * weights[k] for k in weights.keys())
    return weighted_score


df["public_interest_score"] = df.apply(
    lambda row: calculate_public_interest_score(row, weights), axis=1
)

# Main Dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_score = df["public_interest_score"].iloc[-1]
    prev_score = df["public_interest_score"].iloc[-2]
    delta = ((current_score - prev_score) / prev_score) * 100
    st.metric("Public Interest Score", f"{current_score:.2%}", f"{delta:.1f}%")

with col2:
    current_trust = df["trust_score"].iloc[-1]
    prev_trust = df["trust_score"].iloc[-2]
    delta_trust = ((current_trust - prev_trust) / prev_trust) * 100
    st.metric("Trust Score", f"{current_trust:.2%}", f"{delta_trust:.1f}%")

with col3:
    current_civic = df["civic_participation"].iloc[-1]
    prev_civic = df["civic_participation"].iloc[-2]
    delta_civic = ((current_civic - prev_civic) / prev_civic) * 100
    st.metric("Civic Participation Rate", f"{current_civic:.2%}", f"{delta_civic:.1f}%")

with col4:
    avg_diversity = df["perspective_diversity"].mean()
    st.metric("Avg Diversity Index", f"{avg_diversity:.2f}", "High")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(
    ["User Needs Performance", "Trend Analysis", "Impact Matrix", "Recommendations"]
)

with tab1:
    st.subheader("User Needs Category Performance")

    # Radar chart for user needs
    categories = list(weights.keys())
    current_values = [
        df["educate_engagement"].iloc[-1],
        df["perspective_diversity"].iloc[-1],
        df["help_actions"].iloc[-1],
        df["update_reach"].iloc[-1],
        df["inspire_shares"].iloc[-1],
    ]

    fig_radar = go.Figure()

    fig_radar.add_trace(
        go.Scatterpolar(
            r=current_values,
            theta=categories,
            fill="toself",
            name="Current Performance",
        )
    )

    fig_radar.add_trace(
        go.Scatterpolar(
            r=[0.7] * len(categories),
            theta=categories,
            fill="toself",
            name="Target",
            opacity=0.3,
        )
    )

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="User Needs Performance vs Target",
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    # Bar chart showing weighted contribution
    contribution_df = pd.DataFrame(
        {
            "Category": categories,
            "Weight": [weights[k] for k in categories],
            "Performance": current_values,
            "Weighted Contribution": [
                weights[k] * v for k, v in zip(categories, current_values)
            ],
        }
    )

    fig_bar = px.bar(
        contribution_df,
        x="Category",
        y=["Weight", "Performance", "Weighted Contribution"],
        title="User Needs: Weights, Performance, and Contribution",
        barmode="group",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Trend Analysis")

    # Time series of public interest score
    fig_trend = px.line(
        df, x="date", y="public_interest_score", title="Public Interest Score Over Time"
    )
    fig_trend.add_scatter(
        x=df["date"], y=df["trust_score"], mode="lines", name="Trust Score"
    )
    fig_trend.add_scatter(
        x=df["date"],
        y=df["civic_participation"],
        mode="lines",
        name="Civic Participation",
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # Correlation matrix
    st.subheader("KPI Correlations")
    corr_cols = [
        "educate_engagement",
        "perspective_diversity",
        "help_actions",
        "update_reach",
        "inspire_shares",
        "trust_score",
        "civic_participation",
    ]
    corr_matrix = df[corr_cols].corr()

    fig_corr = px.imshow(
        corr_matrix, text_auto=True, aspect="auto", title="Correlation Matrix of KPIs"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.subheader("Impact Matrix")

    # Create impact vs effort matrix
    impact_data = pd.DataFrame(
        {
            "Initiative": [
                "Long-form Explainers",
                "Community Forums",
                "Fact-Check Series",
                "Solution Journalism",
                "Civic Guides",
                "Diverse Voices Project",
            ],
            "Impact": np.random.uniform(0.4, 0.9, 6),
            "Effort": np.random.uniform(0.3, 0.8, 6),
            "User Need": [
                "Educate Me",
                "Give Me Perspective",
                "Update Me",
                "Inspire Me",
                "Help Me",
                "Give Me Perspective",
            ],
        }
    )

    fig_matrix = px.scatter(
        impact_data,
        x="Effort",
        y="Impact",
        text="Initiative",
        color="User Need",
        title="Impact vs Effort Matrix",
        size_max=20,
    )

    # Add quadrant lines
    fig_matrix.add_hline(y=0.65, line_dash="dash", line_color="gray", opacity=0.5)
    fig_matrix.add_vline(x=0.55, line_dash="dash", line_color="gray", opacity=0.5)

    # Add quadrant labels
    fig_matrix.add_annotation(x=0.25, y=0.85, text="Quick Wins", showarrow=False)
    fig_matrix.add_annotation(x=0.75, y=0.85, text="Strategic", showarrow=False)
    fig_matrix.add_annotation(x=0.25, y=0.35, text="Fill Ins", showarrow=False)
    fig_matrix.add_annotation(x=0.75, y=0.35, text="Question", showarrow=False)

    fig_matrix.update_traces(textposition="top center")
    st.plotly_chart(fig_matrix, use_container_width=True)

with tab4:
    st.subheader("AI-Generated Recommendations")

    # Calculate which areas need improvement
    performance_gaps = {
        "Educate Me": 0.7 - df["educate_engagement"].iloc[-1],
        "Give Me Perspective": 0.7 - df["perspective_diversity"].iloc[-1],
        "Help Me": 0.7 - df["help_actions"].iloc[-1],
        "Update Me": 0.7 - df["update_reach"].iloc[-1],
        "Inspire Me": 0.7 - df["inspire_shares"].iloc[-1],
    }

    # Sort by largest gaps
    sorted_gaps = sorted(performance_gaps.items(), key=lambda x: x[1], reverse=True)

    st.markdown("### Top Priority Areas")
    for i, (category, gap) in enumerate(sorted_gaps[:3], 1):
        if gap > 0:
            st.warning(f"**{i}. {category}** - Performance gap: {gap:.2%}")

            # Generate recommendations based on category
            if category == "Educate Me":
                st.markdown(
                    """
                - Develop more explanatory journalism series
                - Create interactive data visualizations
                - Launch civic literacy workshops
                """
                )
            elif category == "Give Me Perspective":
                st.markdown(
                    """
                - Increase diversity of sources and voices
                - Create community correspondent program
                - Host public debates on key issues
                """
                )
            elif category == "Help Me":
                st.markdown(
                    """
                - Develop civic participation guides
                - Create voter information resources
                - Build public service directory
                """
                )

    # Predictive model section
    st.markdown("### Predictive Impact Model")

    col1, col2 = st.columns(2)
    with col1:
        new_educate = st.number_input(
            "If 'Educate Me' improves to:",
            min_value=0.0,
            max_value=1.0,
            value=min(df["educate_engagement"].iloc[-1] + 0.1, 1.0),
        )
    with col2:
        predicted_civic = 0.15 + (new_educate * 0.45)  # Simple linear model
        st.metric(
            "Predicted Civic Participation",
            f"{predicted_civic:.2%}",
            f"+{(predicted_civic - df['civic_participation'].iloc[-1]):.2%}",
        )

    # Action items
    st.markdown("### Recommended Action Items")
    st.info(
        """
    1. **Immediate (This Week)**
       - Audit current content against user needs framework
       - Set up tracking for civic action conversions
    
    2. **Short-term (This Month)**
       - Launch pilot program for highest-gap category
       - Implement A/B testing for engagement metrics
    
    3. **Long-term (This Quarter)**
       - Develop comprehensive impact measurement system
       - Create feedback loops with community stakeholders
    """
    )

# Footer with methodology
with st.expander("Methodology & Calculations"):
    st.markdown(
        """
    ### Public Interest Score Calculation
    
    The Public Interest Score is a weighted average of performance across user need categories:
    
    ```
    Score = Σ (Category Performance × Category Weight)
    ```
    
    ### Key Metrics Definitions:
    
    - **Educate Engagement**: Completion rate of explanatory content
    - **Perspective Diversity**: Unique viewpoints per story / target
    - **Help Actions**: Users taking civic action / total users
    - **Update Reach**: Unique users reached / target audience
    - **Inspire Shares**: Social shares of solution stories / total shares
    - **Trust Score**: Survey-based trust measurement
    - **Civic Participation**: Users engaged in civic activities
    
    ### Data Sources:
    - Web analytics (engagement metrics)
    - Content analysis (diversity metrics)
    - User surveys (trust and impact)
    - Community feedback (civic participation)
    """
    )

# Add download functionality
st.sidebar.markdown("---")
st.sidebar.subheader("Export Data")
csv = df.to_csv(index=False)
st.sidebar.download_button(
    label="Download KPI Data as CSV",
    data=csv,
    file_name=f'pim_kpi_data_{datetime.now().strftime("%Y%m%d")}.csv',
    mime="text/csv",
)
