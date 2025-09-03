import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Public Interest Infrastructure KPIs", page_icon="📊", layout="wide"
)

# CSS for styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f4e79;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .recommendation-box {
        background-color: #d1ecf1;
        border: 1px solid #b8daff;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_infrastructure_data():
    """Load sample infrastructure performance data"""
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="W")

    # Generate realistic performance data with some correlation patterns
    base_trend = np.linspace(0.4, 0.7, len(dates))
    noise = np.random.normal(0, 0.1, len(dates))

    data = {
        "date": dates,
        "democratic_empowerment": np.clip(
            base_trend + noise + np.random.uniform(-0.2, 0.2, len(dates)), 0, 1
        ),
        "information_integrity": np.clip(
            base_trend + noise * 0.8 + np.random.uniform(-0.1, 0.3, len(dates)), 0, 1
        ),
        "community_control": np.clip(
            base_trend * 0.7 + noise + np.random.uniform(-0.3, 0.1, len(dates)), 0, 1
        ),
        "user_rights_protection": np.clip(
            base_trend * 1.2 + noise * 0.6 + np.random.uniform(-0.1, 0.2, len(dates)),
            0,
            1,
        ),
        "inclusion_access": np.clip(
            base_trend * 0.9 + noise + np.random.uniform(-0.2, 0.2, len(dates)), 0, 1
        ),
        "sustainability": np.clip(
            base_trend + noise * 0.7 + np.random.uniform(-0.15, 0.25, len(dates)), 0, 1
        ),
    }

    return pd.DataFrame(data)


def calculate_weighted_score(data_row, weight_dict):
    """Calculate composite score using weighted average"""
    categories = [
        "democratic_empowerment",
        "information_integrity",
        "community_control",
        "user_rights_protection",
        "inclusion_access",
        "sustainability",
    ]

    total_score = 0
    for category in categories:
        total_score += data_row[category] * weight_dict[category]

    return total_score


def build_radar_chart(current_vals, target_vals, category_labels):
    """Build radar chart for performance comparison"""

    fig = go.Figure()

    # Add current performance trace
    fig.add_trace(
        go.Scatterpolar(
            r=list(current_vals.values()) + [list(current_vals.values())[0]],
            theta=list(category_labels.values()) + [list(category_labels.values())[0]],
            fill="toself",
            name="Current Performance",
            fillcolor="rgba(54, 162, 235, 0.2)",
            line_color="rgba(54, 162, 235, 1)",
        )
    )

    # Add target performance trace
    fig.add_trace(
        go.Scatterpolar(
            r=list(target_vals.values()) + [list(target_vals.values())[0]],
            theta=list(category_labels.values()) + [list(category_labels.values())[0]],
            fill="toself",
            name="Target Performance",
            fillcolor="rgba(255, 99, 132, 0.2)",
            line_color="rgba(255, 99, 132, 1)",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Performance vs Targets",
        height=500,
    )

    return fig


def main():
    st.markdown(
        '<h1 class="main-header">Public Interest Infrastructure Assessment</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    **Framework for measuring digital infrastructure impact on democratic values and public welfare**
    
    This analysis tracks six critical dimensions that determine whether infrastructure 
    empowers communities or extracts value from them.
    """
    )

    # Load the dataset
    df = load_infrastructure_data()

    # Configuration sidebar
    st.sidebar.header("Configuration Panel")
    st.sidebar.markdown("**Adjust weighting based on organizational priorities:**")

    # Weight configuration sliders
    demo_weight = st.sidebar.slider("Democratic Empowerment", 0.1, 0.5, 0.25, 0.05)
    info_weight = st.sidebar.slider("Information Integrity", 0.1, 0.3, 0.20, 0.05)
    community_weight = st.sidebar.slider("Community Control", 0.1, 0.3, 0.20, 0.05)
    privacy_weight = st.sidebar.slider("User Rights Protection", 0.1, 0.25, 0.15, 0.05)
    access_weight = st.sidebar.slider("Inclusion and Access", 0.05, 0.2, 0.10, 0.05)
    sustain_weight = st.sidebar.slider("Sustainability", 0.05, 0.2, 0.10, 0.05)

    # Normalize weights to sum to 1
    total_weights = (
        demo_weight
        + info_weight
        + community_weight
        + privacy_weight
        + access_weight
        + sustain_weight
    )

    normalized_weights = {
        "democratic_empowerment": demo_weight / total_weights,
        "information_integrity": info_weight / total_weights,
        "community_control": community_weight / total_weights,
        "user_rights_protection": privacy_weight / total_weights,
        "inclusion_access": access_weight / total_weights,
        "sustainability": sustain_weight / total_weights,
    }

    # Get latest data point for calculations
    current_data = df.iloc[-1]
    composite_score = calculate_weighted_score(current_data, normalized_weights)

    # Display key performance indicators
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Public Interest Score",
            f"{composite_score:.1%}",
            delta=(
                f"+{np.random.uniform(3, 12):.1f}%"
                if composite_score > 0.5
                else f"{np.random.uniform(-12, -3):.1f}%"
            ),
        )

    with col2:
        trust_metric = (
            current_data["information_integrity"] * 0.7
            + current_data["user_rights_protection"] * 0.3
        )
        st.metric(
            "Trust Index",
            f"{trust_metric:.1%}",
            delta=f"+{np.random.uniform(1, 7):.1f}%",
        )

    with col3:
        civic_metric = (
            current_data["democratic_empowerment"] * current_data["community_control"]
        )
        st.metric(
            "Civic Engagement",
            f"{civic_metric:.1%}",
            delta=f"+{np.random.uniform(0.5, 5):.1f}%",
        )

    with col4:
        rights_metric = (
            current_data["user_rights_protection"] + current_data["inclusion_access"]
        ) / 2
        st.metric(
            "Rights Protection Index",
            f"{rights_metric:.2f}",
            delta=f"+{np.random.uniform(0.01, 0.06):.2f}",
        )

    # Main analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Performance Overview", "Trend Analysis", "Gap Assessment", "Action Plan"]
    )

    with tab1:
        st.subheader("Infrastructure Performance Dashboard")

        # Current vs target performance data
        current_performance = {
            "democratic_empowerment": current_data["democratic_empowerment"],
            "information_integrity": current_data["information_integrity"],
            "community_control": current_data["community_control"],
            "user_rights_protection": current_data["user_rights_protection"],
            "inclusion_access": current_data["inclusion_access"],
            "sustainability": current_data["sustainability"],
        }

        target_performance = {
            "democratic_empowerment": 0.70,
            "information_integrity": 0.80,
            "community_control": 0.60,
            "user_rights_protection": 0.85,
            "inclusion_access": 0.65,
            "sustainability": 0.75,
        }

        category_names = {
            "democratic_empowerment": "Democratic\nEmpowerment",
            "information_integrity": "Information\nIntegrity",
            "community_control": "Community\nControl",
            "user_rights_protection": "User Rights\nProtection",
            "inclusion_access": "Inclusion &\nAccess",
            "sustainability": "Sustainability",
        }

        col1, col2 = st.columns([2, 1])

        with col1:
            radar_chart = build_radar_chart(
                current_performance, target_performance, category_names
            )
            st.plotly_chart(radar_chart, use_container_width=True)

        with col2:
            st.markdown("### Performance Summary")

            for key, label in category_names.items():
                current = current_performance[key]
                target = target_performance[key]
                weight = normalized_weights[key]

                performance_gap = target - current
                status_indicator = (
                    "On Track"
                    if performance_gap < 0.1
                    else "Needs Attention" if performance_gap < 0.2 else "Critical Gap"
                )

                st.markdown(
                    f"""
                **{label.replace(chr(10), ' ')}**
                - Weight: {weight:.1%}
                - Current: {current:.1%}
                - Target: {target:.1%}
                - Status: {status_indicator}
                """
                )

    with tab2:
        st.subheader("Performance Trends")

        # Multi-panel time series
        subplot_fig = make_subplots(
            rows=2,
            cols=3,
            subplot_titles=list(category_names.values()),
            specs=[
                [
                    {"secondary_y": False},
                    {"secondary_y": False},
                    {"secondary_y": False},
                ],
                [
                    {"secondary_y": False},
                    {"secondary_y": False},
                    {"secondary_y": False},
                ],
            ],
        )

        chart_positions = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]
        line_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

        for idx, (key, label) in enumerate(category_names.items()):
            row, col = chart_positions[idx]
            subplot_fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df[key],
                    mode="lines+markers",
                    name=label.replace("\n", " "),
                    line=dict(color=line_colors[idx]),
                    showlegend=False,
                ),
                row=row,
                col=col,
            )

            # Add target reference line
            subplot_fig.add_hline(
                y=target_performance[key],
                line_dash="dash",
                line_color="red",
                opacity=0.7,
                row=row,
                col=col,
            )

        subplot_fig.update_layout(height=600, title="Temporal Performance Analysis")
        st.plotly_chart(subplot_fig, use_container_width=True)

        # Correlation matrix
        st.markdown("### Inter-Category Correlations")
        corr_matrix = df[list(category_names.keys())].corr()

        heatmap_fig = px.imshow(
            corr_matrix,
            labels=dict(
                x="Infrastructure Categories",
                y="Infrastructure Categories",
                color="Correlation",
            ),
            x=[category_names[col].replace("\n", " ") for col in corr_matrix.columns],
            y=[category_names[col].replace("\n", " ") for col in corr_matrix.columns],
            color_continuous_scale="RdBu_r",
            aspect="auto",
        )
        heatmap_fig.update_layout(title="Category Correlation Matrix")
        st.plotly_chart(heatmap_fig, use_container_width=True)

    with tab3:
        st.subheader("Performance Gap Analysis")

        # Build gap analysis dataset
        gap_analysis = []
        for key, label in category_names.items():
            current = current_performance[key]
            target = target_performance[key]
            weight = normalized_weights[key]
            gap = target - current

            gap_analysis.append(
                {
                    "Category": label.replace("\n", " "),
                    "Performance Gap": gap,
                    "Strategic Weight": weight,
                    "Priority Score": abs(gap * weight),
                    "Current Performance": current,
                    "Target Performance": target,
                }
            )

        gap_df = pd.DataFrame(gap_analysis)
        gap_df = gap_df.sort_values("Priority Score", ascending=False)

        # Priority matrix visualization
        matrix_fig = px.scatter(
            gap_df,
            x="Strategic Weight",
            y="Performance Gap",
            size="Priority Score",
            color="Category",
            hover_data=["Current Performance", "Target Performance"],
            title="Priority Matrix: Gap vs Strategic Importance",
            labels={
                "Strategic Weight": "Strategic Importance (Weight)",
                "Performance Gap": "Performance Gap (Target - Current)",
            },
        )

        # Add quadrant reference lines
        matrix_fig.add_hline(
            y=gap_df["Performance Gap"].median(), line_dash="dash", opacity=0.5
        )
        matrix_fig.add_vline(
            x=gap_df["Strategic Weight"].median(), line_dash="dash", opacity=0.5
        )

        # Quadrant labels
        matrix_fig.add_annotation(
            x=gap_df["Strategic Weight"].max() * 0.8,
            y=gap_df["Performance Gap"].max() * 0.8,
            text="IMMEDIATE PRIORITY<br>Focus Resources Here",
            showarrow=False,
            font=dict(size=12, color="red"),
        )
        matrix_fig.add_annotation(
            x=gap_df["Strategic Weight"].min() * 1.2,
            y=gap_df["Performance Gap"].max() * 0.8,
            text="SECONDARY FOCUS<br>Address When Possible",
            showarrow=False,
            font=dict(size=10, color="orange"),
        )
        matrix_fig.add_annotation(
            x=gap_df["Strategic Weight"].max() * 0.8,
            y=gap_df["Performance Gap"].min() * 1.2,
            text="MAINTAIN STANDARDS<br>Monitor Performance",
            showarrow=False,
            font=dict(size=10, color="green"),
        )
        matrix_fig.add_annotation(
            x=gap_df["Strategic Weight"].min() * 1.2,
            y=gap_df["Performance Gap"].min() * 1.2,
            text="LOW PRIORITY<br>Minimal Resources",
            showarrow=False,
            font=dict(size=10, color="gray"),
        )

        st.plotly_chart(matrix_fig, use_container_width=True)

        # Priority ranking table
        st.markdown("### Priority Ranking")
        st.dataframe(
            gap_df[
                ["Category", "Performance Gap", "Strategic Weight", "Priority Score"]
            ].style.format(
                {
                    "Performance Gap": "{:.1%}",
                    "Strategic Weight": "{:.1%}",
                    "Priority Score": "{:.3f}",
                }
            ),
            use_container_width=True,
        )

    with tab4:
        st.subheader("Strategic Recommendations")

        # Identify highest priority items
        top_priority = gap_df.iloc[0]
        second_priority = gap_df.iloc[1]

        # Alert for critical gaps
        if top_priority["Performance Gap"] > 0.2:
            st.markdown(
                f"""
            <div class="warning-box">
            <h4>Critical Gap Alert: {top_priority['Category']}</h4>
            <p><strong>Performance deficit: {top_priority['Performance Gap']:.1%}</strong></p>
            <p>This category shows significant underperformance with high strategic importance ({top_priority['Strategic Weight']:.1%})</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Impact prediction model
        st.markdown("### Impact Modeling")

        improvement_target = st.slider(
            f"Model improvement in {top_priority['Category']} to:",
            float(top_priority["Current Performance"]),
            1.0,
            min(float(top_priority["Target Performance"]), 0.9),
            0.05,
        )

        # Calculate projected impact
        adjusted_performance = current_performance.copy()
        category_key = [
            k
            for k, v in category_names.items()
            if v.replace("\n", " ") == top_priority["Category"]
        ][0]
        adjusted_performance[category_key] = improvement_target

        projected_score = calculate_weighted_score(
            pd.Series(adjusted_performance), normalized_weights
        )
        score_improvement = projected_score - composite_score

        st.info(
            f"""
        **Projected Impact**: Improving {top_priority['Category']} to {improvement_target:.1%} 
        would increase overall Public Interest Score to **{projected_score:.1%}** 
        (improvement of **+{score_improvement:.1%}**)
        """
        )

        # Implementation roadmap
        st.markdown(
            """
        <div class="recommendation-box">
        <h4>Implementation Roadmap</h4>
        <h5>Immediate Actions (1-2 weeks):</h5>
        <ul>
        <li>Conduct comprehensive infrastructure assessment</li>
        <li>Survey community stakeholders on priority needs</li>
        <li>Audit current user rights and data protection measures</li>
        </ul>
        
        <h5>Short-term Initiatives (1-3 months):</h5>
        <ul>
        <li>Establish community governance mechanisms</li>
        <li>Deploy digital inclusion programs</li>
        <li>Strengthen information verification processes</li>
        </ul>
        
        <h5>Strategic Projects (3-12 months):</h5>
        <ul>
        <li>Build participatory infrastructure governance framework</li>
        <li>Implement algorithmic transparency standards</li>
        <li>Develop long-term sustainability model</li>
        </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Technical documentation
        with st.expander("Technical Documentation"):
            st.markdown(
                """
            ### Methodology Overview
            
            **Composite Score Calculation:**
            Public Interest Score = Σ (Category Performance × Category Weight)
            
            **Category Definitions:**
            - **Democratic Empowerment**: Measures civic participation rates, accountability mechanisms
            - **Information Integrity**: Tracks source diversity, fact-checking effectiveness, misinformation resistance  
            - **Community Control**: Assesses local ownership, governance participation, platform interoperability
            - **User Rights Protection**: Evaluates data sovereignty, privacy protection, surveillance resistance
            - **Inclusion & Access**: Monitors marginalized community representation, accessibility features
            - **Sustainability**: Reviews financial independence, maintenance capacity, environmental impact
            
            **Data Sources for Production Implementation:**
            - Community engagement surveys
            - Platform governance analytics  
            - Digital rights compliance audits
            - Accessibility testing results
            - Environmental impact assessments
            
            **Export Functionality:**
            """
            )

            # Data export option
            export_data = df.to_csv(index=False)
            st.download_button(
                label="Download Dataset (CSV)",
                data=export_data,
                file_name=f'infrastructure_kpis_{datetime.now().strftime("%Y%m%d")}.csv',
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
