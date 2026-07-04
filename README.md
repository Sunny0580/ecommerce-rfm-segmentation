 E-Commerce Customer Segmentation
RFM Analysis · Python · Power BI

PythonPandasMatplotlibPower BI
License: MIT


An end-to-end Data Analytics portfolio project — transforming raw e-commerce transactions into actionable customer intelligence using the industry-standard RFM framework, with a Power BI dashboard and a business-ready marketing strategy report.


📌 Table of Contents
The Business Problem
What is RFM?
Key Results
Customer Segments
Visualisations
Project Structure
Quick Start
Power BI Dashboard
Marketing Strategy Report
Tech Stack
Key Insights
Author
🎯 The Business Problem
Online retailers waste millions in marketing budget by treating all customers the same way — sending identical promotions to loyal high-spenders and churned one-time buyers alike.

The result?

VIP customers get irrelevant discounts they don't need
High-value churning customers receive nothing personalised
Marketing ROI stays low despite high spend
The solution: Use RFM Analysis — a battle-tested, data-driven customer segmentation methodology used by leading e-commerce brands worldwide — to understand exactly who each customer is and tailor every marketing action accordingly.

🔬 What is RFM?
RFM stands for Recency · Frequency · Monetary — three dimensions that together paint a complete picture of customer behaviour:


Dimension	Question it Answers	Score Range
R — Recency	How recently did the customer make a purchase?	1 (long ago) → 5 (very recent)
F — Frequency	How many times have they purchased?	1 (rarely) → 5 (very often)
M — Monetary	How much total money have they spent?	1 (low spender) → 5 (top spender)

Each customer receives a score of 1 to 5 for each dimension using quantile-based scoring — splitting customers into equal-sized buckets. The three scores combine to classify customers into 11 named segments.


Customer Score Example:
  R=5, F=5, M=5  →  🏆 Champion    (bought yesterday, buys constantly, top spender)
  R=1, F=1, M=1  →  💀 Lost        (hasn't bought in a year, rarely bought, lowest spender)
  R=1, F=4, M=5  →  ❗ Cannot Lose (was a VIP but hasn't returned — urgent!)
📊 Key Results
Metric	Value
🧑‍🤝‍🧑 Total Customers Analysed	4,000+
📦 Total Transactions Processed	94,398
🏷️ Segments Identified	11
🏆 Champions (13% of customers)	Generate 41.2% of revenue
🚨 At Risk customers	Hold 36.7% of revenue
💎 Loyal Customers	Contribute 17.8% of revenue

💡 The headline finding: Just 13% of customers (Champions) drive over 41% of all revenue. Meanwhile, the At Risk group — 952 customers who were once great buyers — account for 36.7% of revenue and are silently disengaging. A targeted intervention for this one segment could recover a massive amount of potential lost revenue.

🏷️ Customer Segments

#	Segment	Profile	Priority	Marketing Action
1	🏆 Champions	Recent, frequent, high spend	🔴 Protect	VIP rewards, early access, referral programs
2	💎 Loyal Customers	Consistent buyers, high LTV	🔴 Protect	Upsell premium, subscription offers
3	🌟 Potential Loyalists	Recent, growing engagement	🟡 Grow	Loyalty program enrollment, personalised recs
4	🆕 Recent Customers	Bought recently, just once	🟡 Nurture	Welcome series, free shipping next order
5	🌱 Promising	Recent, low frequency	🟡 Grow	Brand content, category introduction
6	⚠️ Need Attention	Slipping from good standing	🟠 Re-engage	Time-limited offers, satisfaction survey
7	😴 About To Sleep	Disengaging fast	🟠 Urgent	"We miss you" campaigns, bold discounts
8	🚨 At Risk	Were great, now cold	🔴 Win-back	Personalised win-back, tailored incentives
9	❗ Cannot Lose Them	Highest-value, long inactive	🔴 Critical	Direct outreach, account manager contact
10	🌙 Hibernating	Long inactive, low value	⚪ Minimal	Low-cost email, relevant discounts
11	💀 Lost	Lowest scores across all	⚪ Minimal	Final re-engagement attempt or remove
📈 Visualisations
Customer Segments — Treemap
Size of each block = customer count. Colour = segment. Numbers show revenue share.

Segment Treemap


Average RFM Scores Heatmap
How each segment scores across Recency, Frequency, and Monetary dimensions. Dark red = highest score.

RFM Heatmap


Recency vs Monetary Value — Coloured by Segment
Each dot is a customer. Left = bought recently, up = high spender. Colours = segments.

Scatter Plot


RFM Score Distributions
How scores are spread across all customers for each dimension.

RFM Distributions


Customer Count by Segment
Segment Bar


Revenue Contribution by Segment
Revenue Pie

📁 Project Structure

ecommerce-rfm-segmentation/
│
├── 📄 main.py                          ← Run this to execute the full pipeline
├── 📄 requirements.txt                 ← Python package dependencies
│
├── 📁 src/                             ← Core analysis modules
│   ├── data_loader.py                  ← Data loading, cleaning & synthetic generation
│   ├── rfm_engine.py                   ← RFM metric computation & quantile scoring
│   └── segmentation.py                 ← Segment assignment rules & metadata
│
├── 📁 data/                            ← Place real dataset here (optional)
│   └── online_retail.xlsx              ← UCI Online Retail II (if using real data)
│
├── 📁 outputs/                         ← All pipeline outputs
│   ├── rfm_scores.csv                  ← Per-customer RFM table (Power BI input)
│   ├── segment_summary.csv             ← Segment-level aggregated statistics
│   └── 📁 charts/                      ← All 6 generated visualisations (.png)
│
├── 📁 powerbi/
│   └── RFM_Dashboard_Guide.md          ← Step-by-step Power BI dashboard guide
│
└── 📁 report/
    └── marketing_strategy.html         ← 1-page business marketing strategy report
🚀 Quick Start
Prerequisites
Python 3.10 or higher
pip (comes with Python)
Installation & Run
bash

# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/ecommerce-rfm-segmentation.git
cd ecommerce-rfm-segmentation
# 2. Install dependencies
pip install -r requirements.txt
# 3. Run the full pipeline
python -X utf8 main.py
Expected Output

════════════════════════════════════════════════════════════
  E-COMMERCE RFM CUSTOMER SEGMENTATION
  Portfolio Project — Data Analytics
════════════════════════════════════════════════════════════
  Generating synthetic data for 4,000 customers ...
  Generated 94,398 transaction rows
  Snapshot date: 2011-12-10
  Customers computed: 4,000
  RFM scores assigned ✅
  Segment distribution:
  Champions           510   (12.8%)
  At Risk             952   (23.8%)
  Loyal Customers     700   (17.5%)
  ...
  ✅ PIPELINE COMPLETE
  Outputs saved to: /outputs/
════════════════════════════════════════════════════════════
Using Real Data (Optional)
This pipeline supports the UCI Online Retail II dataset (~500K real transactions):

Download from: UCI Machine Learning Repository
Place the file at: data/online_retail.xlsx
Re-run python -X utf8 main.py — it auto-detects the real file
📊 Power BI Dashboard
The pipeline generates two ready-to-import CSV files for Power BI:

File	Contents
outputs/rfm_scores.csv	4,000 rows — one per customer with R/F/M scores and segment
outputs/segment_summary.csv	11 rows — segment-level revenue, count, and averages
Dashboard panels built:

🍩 Donut Chart — Revenue % contribution by segment
📊 Horizontal Bar Chart — Customer count per segment
🔢 KPI Cards — Total customers, total revenue, avg customer value
🔵 Scatter Plot — Recency vs Monetary, coloured by segment
🎛️ Slicer — Filter all panels by segment interactively
See 
powerbi/RFM_Dashboard_Guide.md
 for the full step-by-step build guide, including colour codes for each segment.

📄 Marketing Strategy Report
Open 
report/marketing_strategy.html
 in any browser for a professional, print-ready 1-page strategy report covering:

Executive summary with key findings
Individual profile for all 11 segments
Specific marketing action recommendations per segment
Priority matrix (Protect / Grow / Win-back / Minimal)
Recommended marketing budget allocation table (% by segment group)
Pro tip: In Chrome, press Ctrl + Shift + P → "Capture full size screenshot" to export the entire report as an image for sharing.

🛠️ Tech Stack
Category	Technology	Purpose
Language	Python 3.10+	Core analysis & scripting
Data Manipulation	Pandas, NumPy	Cleaning, RFM computation, scoring
Visualisation	Matplotlib, Seaborn	All 6 charts & heatmaps
Treemap	Squarify	Segment treemap visualisation
BI Dashboard	Power BI Desktop	Interactive business dashboard
Report	HTML + CSS	1-page marketing strategy document
Dataset	UCI Online Retail II (Synthetic)	E-commerce transaction data
💡 Key Insights
1. The Pareto Principle in Action
12.8% of customers (Champions) generate 41.2% of all revenue. This is a stronger concentration than the classic 80/20 rule — making Champion retention the single highest-ROI marketing activity.

2. The Silent Revenue Risk
The At Risk segment (23.8% of customers) holds 36.7% of revenue — and they're going cold. These customers were once high-frequency, high-spend buyers. Without intervention, this is revenue walking out the door.

3. The Growth Opportunity
Potential Loyalists make up 27.8% of all customers but contribute only 3.1% of revenue. They're recent and engaged — converting even 20% of them to Loyal Customers would significantly grow LTV.

4. Budget Efficiency
Hibernating + Lost customers = 18.9% of customers but generate < 0.5% of revenue. Stop wasting paid ad budget on these groups. Redirect it to At Risk and Cannot Lose Them.

🔮 Future Improvements
 K-Means Clustering — Compare data-driven clusters against rule-based RFM segments
 CLV Prediction — Add Customer Lifetime Value model (BG/NBD + Gamma-Gamma)
 Automated Pipeline — Schedule weekly re-segmentation with fresh transaction data
 Streamlit Web App — Deploy as an interactive dashboard accessible via browser
 A/B Test Framework — Track which marketing actions actually improve segment migration
 Real Dataset — Replace synthetic data with live UCI Online Retail II dataset
👤 Author
Sunny Singh
www.linkedin.com/in/sunnysingh08


📜 License
This project is licensed under the MIT License — free to use, adapt, and share with attribution.

If this project helped you, please consider giving it a ⭐ star on GitHub!

Built as a data analytics portfolio project demonstrating Python, RFM Analysis, Power BI, and business communication skills.
