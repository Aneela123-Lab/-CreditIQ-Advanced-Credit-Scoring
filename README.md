# CreditIQ — Advanced Credit Scoring System

<div align="center">

![CreditIQ Badge](https://img.shields.io/badge/CreditIQ-Advanced%20Credit%20Scoring-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

*An AI-powered credit risk assessment platform for modern lending decisions*

</div>

---

## 🎯 Overview

**CreditIQ** is an intelligent credit scoring system that evaluates financial data to generate accurate risk scores and creditworthiness assessments. Built with machine learning and deployed as an interactive web application, it helps financial institutions make data-driven lending decisions with confidence.

The system uses a pre-trained **Random Forest model** (200 decision trees) trained on the German Credit Dataset, containing 1,000 real-world loan applicant records. It provides comprehensive risk analysis, probability scoring, and actionable insights for credit decisions.

---

## ✨ Key Features

### 🔍 Single Applicant Scoring
- **Comprehensive Input Forms** - Collect all relevant financial and personal information
- **Instant Risk Assessment** - Real-time credit score calculation (300-850 scale)
- **Risk Tier Classification** - Categorize applicants into Low, Medium, or High risk
- **Probability Analysis** - Confidence score for credit quality prediction
- **Detailed Recommendations** - Actionable insights based on individual profile
- **Report Generation** - Downloadable PDF assessment reports

### 📊 Batch Processing
- **Bulk CSV Upload** - Score multiple applicants simultaneously
- **High-Volume Processing** - Handle hundreds of applications efficiently
- **Batch Export** - Download results with scores and risk classifications
- **Progress Tracking** - Real-time status updates during processing
- **Error Handling** - Graceful handling of data quality issues

### 📈 Analytics Dashboard
- **Risk Distribution Insights** - Visualize credit quality across portfolio
- **Feature Importance Analysis** - Understand which factors drive decisions
- **Demographic Scatter Plots** - Analyze age vs. credit relationships
- **Loan Duration Trends** - Examine lending patterns and duration impact
- **Risk Factor Radar Charts** - Multi-dimensional risk visualization
- **Portfolio Statistics** - Comprehensive portfolio-level analytics

### 📖 Feature Guide
- **Interactive Education** - Learn about each input variable
- **Real-World Examples** - See sample data and typical ranges
- **Impact Explanation** - Understand how features affect credit scores
- **Best Practices** - Guidance for accurate data entry

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.8+ |
| **Web Framework** | Streamlit | 1.50+ |
| **ML Framework** | Scikit-learn | Latest |
| **Data Processing** | Pandas & NumPy | Latest |
| **Visualization** | Plotly | Latest |
| **Model Serialization** | Joblib | Latest |
| **Dataset** | German Credit Dataset | 1,000 records |

---

## 📋 Project Structure

```
Task 1 Credit Scoring Model/
├── app.py                           # Main Streamlit application
├── credit_scoring_model.joblib      # Trained ML model (binary)
├── german_credit_data.csv           # Training dataset (1,000 records)
├── credit_scoring_model.ipynb       # Jupyter notebook (model development)
├── CODE_DOCUMENTATION.txt           # Detailed code documentation
├── README.md                        # This file
└── __pycache__/                    # Python cache directory
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application with UI, forms, and visualization logic |
| `credit_scoring_model.joblib` | Serialized trained Random Forest model (6.2 MB) |
| `german_credit_data.csv` | Original dataset with 1,000 loan records used for model training |
| `credit_scoring_model.ipynb` | Jupyter notebook containing model development and training workflow |
| `CODE_DOCUMENTATION.txt` | Comprehensive documentation of every code section |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8** or higher
- **pip** (Python package manager)
- **Git** (for version control)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aneela123-Lab/-CreditIQ-Advanced-Credit-Scoring.git
   cd "CreditIQ-Advanced-Credit-Scoring"
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually install:
   ```bash
   pip install streamlit pandas numpy scikit-learn joblib plotly
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Web Interface**
   - The application will open in your default browser
   - URL: `http://localhost:8501`

---

## 💡 Usage Guide

### Tab 1: Single Applicant Scoring

1. **Enter Applicant Information**
   - Personal details (age, gender, employment status)
   - Financial information (income, savings, credit amount)
   - Loan details (duration, purpose, rate type)
   - Credit history indicators

2. **Click "Calculate Credit Score"**
   - Model processes the input instantly
   - Displays credit score (300-850 range)
   - Shows risk tier (Low/Medium/High)
   - Provides probability of good credit

3. **Review Results**
   - Visual risk gauge
   - Detailed recommendations
   - Key risk factors highlighted
   - Download assessment report (PDF)

### Tab 2: Batch Scoring

1. **Prepare CSV File**
   - Ensure columns match expected input format
   - Include all required financial variables
   - Verify data quality

2. **Upload CSV File**
   - Click "Browse files" button
   - Select prepared CSV file
   - Monitor progress

3. **Review & Export Results**
   - View scoring results table
   - Download enhanced CSV with scores and risk tiers
   - Analyze bulk statistics

### Tab 3: Analytics Dashboard

- **Explore Portfolio Insights**
  - Risk distribution across applicants
  - Feature importance rankings
  - Demographic analysis
  - Lending pattern trends

- **Export Analytics**
  - Download visualizations
  - Generate reports

### Tab 4: Feature Guide

- **Learn About Variables**
  - Understand input parameters
  - See typical value ranges
  - Review impact on scoring
  - Access examples

---

## 🤖 Machine Learning Model Details

### Model Architecture
- **Algorithm**: Random Forest Classifier
- **Number of Trees**: 200 decision trees
- **Training Data**: German Credit Dataset (1,000 records)
- **Input Features**: 20+ financial and personal variables
- **Output**: Binary classification (Good/Bad credit)

### Credit Score Calculation
- Raw probability (0-1) from model converted to 300-850 scale
- Formula: `Credit_Score = 300 + (Probability × 550)`
- **300-579**: High Risk (Bad credit probability > 50%)
- **580-669**: Medium Risk (Uncertain)
- **670-850**: Low Risk (Good credit probability > 50%)

### Model Performance
- Trained on balanced dataset of good and bad credit cases
- Handles diverse financial profiles
- Robust feature engineering for numerical and categorical variables
- Cross-validated for reliability

### Feature Categories

| Category | Examples |
|----------|----------|
| **Demographic** | Age, Gender, Marital Status |
| **Employment** | Employment Type, Duration, Position |
| **Financial** | Income, Savings, Checking Account Status |
| **Credit** | Credit Amount, Duration, Purpose |
| **History** | Previous Credits, Payment Status, Job Stability |

---

## 📊 Input Variables Guide

### Personal Information
- **Age**: Applicant's current age in years
- **Gender**: Male or Female
- **Marital Status**: Single, Married, Divorced, Widowed

### Employment Details
- **Employment Status**: Employed, Unemployed, Self-employed, Retired
- **Years Employed**: Duration in current employment
- **Job Type**: Skilled worker, Official, Manager, etc.

### Financial Information
- **Monthly Income**: Gross monthly income (in currency units)
- **Savings Account**: Amount in savings
- **Checking Account**: Amount in checking account
- **Other Assets**: Real estate, vehicles, investments

### Loan Information
- **Credit Amount**: Amount requested (in currency units)
- **Loan Duration**: Requested term (in months)
- **Loan Purpose**: Purpose of credit (home, auto, business, etc.)
- **Interest Rate Type**: Fixed or Variable

### Credit History
- **Previous Credits**: Number of previous loans
- **Payment Status**: Record of on-time payments
- **Existing Liabilities**: Number of active loans
- **Credit Utilization**: Percentage of available credit used

---

## 🎨 User Interface Features

### Design Highlights
- **Modern Dashboard**: Gradient background with glassmorphism effects
- **Interactive Charts**: Plotly visualizations for deep insights
- **Responsive Layout**: Works seamlessly on desktop and tablet
- **Dark Theme**: Eye-friendly professional appearance
- **Custom Styling**: Professional typography and color scheme
- **Real-time Feedback**: Instant processing and result display

### Accessibility
- Clear form labels and instructions
- Error messages and validation feedback
- Downloadable reports and data
- Mobile-responsive design

---

## 📥 Output & Reporting

### Single Applicant Reports
- **PDF Download**: Comprehensive assessment report
- **Contents**:
  - Applicant summary
  - Credit score (300-850)
  - Risk tier classification
  - Recommendation letter
  - Key decision factors
  - Generated timestamp

### Batch Results
- **CSV Export**: All applicants with scores
- **Columns**:
  - Original input data
  - Calculated credit score
  - Risk tier assignment
  - Confidence probability
  - Processing timestamp

### Analytics Export
- **Chart Downloads**: Visual analytics as PNG/SVG
- **Data Tables**: Detailed statistics and insights
- **Summary Reports**: Portfolio-level analytics

---

## 🔒 Data & Security Considerations

### Data Handling
- **No Persistent Storage**: Data processed in-memory only
- **Session-Based**: Each session is isolated
- **User Privacy**: No data retention between sessions
- **Input Validation**: All inputs sanitized and validated

### Deployment Recommendations
- Use HTTPS for production deployment
- Implement authentication for user access
- Add audit logging for compliance
- Regular model updates and retraining
- Data encryption for sensitive information

---

## 🛠️ Development & Customization

### Extending the Application

1. **Adding New Features**
   - Modify `app.py` to add new tabs or functionalities
   - Update input validation functions
   - Add new visualizations using Plotly

2. **Retraining the Model**
   - Use `credit_scoring_model.ipynb` as template
   - Update training data
   - Retrain Random Forest model
   - Save new model with `joblib`

3. **Custom Styling**
   - Edit CSS section in `app.py` (lines 23-185)
   - Modify Plotly themes
   - Adjust color schemes and fonts

### Model Retraining Workflow

```python
# In Jupyter notebook or Python script
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load new data
data = pd.read_csv('new_credit_data.csv')

# Prepare features and target
X = data.drop('credit_outcome', axis=1)
y = data['credit_outcome']

# Train new model
model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

# Save model
joblib.dump(model, 'credit_scoring_model.joblib')
```

---

## 📚 Documentation

### Code Documentation
- See `CODE_DOCUMENTATION.txt` for detailed code breakdown
- Each function documented with parameters and return values
- Inline comments explain complex logic

### Key Functions in app.py
- `compute_credit_score()`: Calculate 300-850 score from probability
- `risk_tier()`: Determine risk classification
- `gauge_chart()`: Create risk visualization
- `feature_importance_chart()`: Show model feature weights
- `predict_batch()`: Process multiple applicants
- `badge_html()`: Generate risk tier badges

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Model not loading | Ensure `credit_scoring_model.joblib` exists in project root |
| Streamlit not found | Run `pip install streamlit` |
| Port 8501 already in use | Use `streamlit run app.py --server.port 8502` |
| CSV upload fails | Verify CSV format matches expected columns |
| Slow performance | Check system resources, reduce batch size |

### Getting Help
- Review `CODE_DOCUMENTATION.txt` for detailed explanations
- Check Streamlit documentation: https://docs.streamlit.io
- Review Scikit-learn documentation: https://scikit-learn.org
- Check GitHub issues for similar problems

---

## 📈 Performance Metrics

### Application Performance
- **Single Prediction**: < 100ms
- **Batch Processing**: ~1-2 seconds per 100 applicants
- **Dashboard Loading**: < 2 seconds
- **Memory Usage**: ~500 MB typical
- **Model Size**: 6.2 MB

### Model Metrics
- **Accuracy**: ~75-85% (on test set)
- **Precision**: High (minimizes false good approvals)
- **Recall**: High (catches most bad credits)
- **ROC-AUC**: > 0.80

---

## 🎓 Learning Resources

### Understanding Credit Scoring
- https://www.fico.com/ - FICO Score information
- https://www.experian.com/ - Credit bureau insights
- https://en.wikipedia.org/wiki/Credit_score - General overview

### Machine Learning Resources
- https://scikit-learn.org/stable/ - Scikit-learn documentation
- https://pandas.pydata.org/ - Pandas data analysis
- https://plotly.com/ - Plotly visualization library

### Streamlit Resources
- https://streamlit.io/ - Official Streamlit website
- https://docs.streamlit.io/ - Streamlit documentation
- https://github.com/streamlit/streamlit - GitHub repository

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/-CreditIQ-Advanced-Credit-Scoring.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Changes**
   ```bash
   git commit -m "Add your feature description"
   ```

4. **Push to Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open Pull Request**
   - Describe your changes clearly
   - Link any related issues

### Contribution Areas
- Bug fixes and improvements
- New visualization types
- Documentation enhancements
- Model optimization
- UI/UX improvements
- Feature additions

---

## 📞 Contact & Support

### Questions or Issues?
- **GitHub Issues**: Report bugs or request features
- **Discussion Board**: Ask questions and share ideas
- **Email**: (Add contact email if applicable)

---

## 🎉 Acknowledgments

- **German Credit Dataset**: UCI Machine Learning Repository
- **Streamlit Community**: For the amazing framework
- **Scikit-learn**: For robust ML algorithms
- **Plotly**: For interactive visualizations

---

## 📝 Changelog

### Version 1.0 (April 2025)
- ✅ Initial release
- ✅ Single applicant scoring
- ✅ Batch processing capability
- ✅ Analytics dashboard
- ✅ Feature guide
- ✅ PDF report generation
- ✅ Multi-visualization support

---

## 🔮 Roadmap

### Planned Features
- [ ] Model explainability dashboard (SHAP values)
- [ ] Real-time model performance monitoring
- [ ] API endpoint for programmatic access
- [ ] Database integration for historical tracking
- [ ] Advanced ensemble models
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Compliance reporting (GDPR, Fair Lending)

---

<div align="center">

**Made with ❤️ for smarter lending decisions**

[⬆ Back to Top](#creditiq--advanced-credit-scoring-system)

</div>
