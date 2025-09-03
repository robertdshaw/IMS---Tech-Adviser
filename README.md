# Public Interest Infrastructure Assessment Tool

A Streamlit-based assessment framework to help community media organizations and alternative platforms evaluate whether their digital tools align with public interest values.

## Overview

This tool helps organizations like community radio stations, digital newsrooms, and citizen forums make informed decisions about their technology stack by evaluating tools across three key dimensions:

- **Privacy & Security**: Data protection, anonymity, surveillance resistance
- **Community Ownership**: Local control, language support, democratic governance
- **Sustainability**: Cost effectiveness, platform independence, long-term viability

## Features

- **Interactive Assessment Dashboard**: Visual scoring across public interest dimensions
- **Tool Trade-off Analysis**: Compare privacy vs. reach for different communication tools
- **Personalized Recommendations**: Context-aware suggestions based on your organization type and operating environment
- **Implementation Roadmap**: Step-by-step guidance for improving your tech stack
- **Export Capabilities**: Generate reports for stakeholders and funders

## Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install streamlit pandas numpy plotly pillow
```

3. Place your organization logo as `logo.png` in the same directory as the script

## Usage

1. Run the application:
```bash
streamlit run IMS_PIA_prototype.py
```

2. Configure your organization profile in the sidebar:
   - Organization type (Community Media, Digital Newsroom, etc.)
   - Operating region
   - Context factors (connectivity, digital literacy, regulatory pressure)

3. Adjust value priorities to match your mission

4. Navigate through the assessment tabs:
   - **Overview**: Dashboard with current scores and gaps
   - **Tool Assessment**: Evaluate your current tech stack
   - **Recommendations**: Get personalized improvement suggestions  
   - **Export**: Generate reports for sharing

## Based on Real-World Cases

The framework draws from successful public interest media organizations:

- **JamiiAfrica (Tanzania)**: Prioritized anonymity and encryption for sensitive reporting
- **CGNet Swara (India)**: Built offline-capable voice platform in local languages
- **Community radio networks**: Balanced reach with community control

## Assessment Dimensions

### Privacy & Security (Target: 80%)
- End-to-end encryption
- Anonymous submission capabilities
- Resistance to surveillance
- Data ownership and control

### Community Ownership (Target: 75%)
- Local language support
- Community governance structures
- Open source alternatives
- User control over content and data

### Sustainability (Target: 70%)
- Cost effectiveness
- Platform independence
- Long-term maintenance capability
- Community technical capacity

## File Structure

```
project/
├── IMS_PIA_prototype.py    # Main application
├── logo.png                # Organization logo (optional)
├── README.md              # This file
└── requirements.txt       # Dependencies (optional)
```

## Customization

- **Adding Tools**: Extend the `tool_scores` dictionary with new platforms
- **Scoring Logic**: Modify calculation functions for different weighting schemes
- **Regional Context**: Add location-specific factors and recommendations
- **Export Options**: Implement PDF generation and email functionality

## Contributing

This tool is designed to be adapted by different organizations. Feel free to:
- Add new assessment criteria
- Include region-specific tools and contexts
- Extend export and reporting capabilities
- Improve the user interface and visualizations

## License

Open for community use and adaptation.

## Support

For questions about implementation or customization, create an issue or reach out to the development team.

---

*This tool supports community media organizations in making technology choices that advance the public interest rather than extractive business models.*
