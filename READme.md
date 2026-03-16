# NCAA D1 Coaching Pipeline & Demographic Analysis (2012–2025)

Interactive sports analytics dashboard examining demographic representation and leadership pipelines across NCAA Division I coaching.

_This project is part of a broader [sports analytics portfolio](https://www.notion.so/krystal-beasley/Sports-Analyst-Portfolio-231077fe20b880b381b7f9877bee2021) focused on leadership trends, competitive analytics, and data-driven decision tools in women's sports._

---

## Deliverables

| Format | Link |
|--------|------|
| 🖥️ HTML Dashboard | [Interactive Dashboard](https://kbsmd-sportsmusicdata.github.io/ncaa-d1-coaching-pipeline-dashboard/) |
| 📊 Slide Deck | [In Repo /docs](docs/NCAA_D1_Coaching_Pipeline_Slides.pptx) |
| 📄 Research Brief | [In Repo /docs](docs/NCAA_D1_Coaching_Pipeline_Research_Brief.pdf) |
| 📌 Portfolio Write-Up | [Notion Page](https://www.notion.so/krystal-beasley/NCAA-D1-Demographics-231077fe20b881619a17c861854e4f08) |

---

## Project Overview

This project investigates the structural pipeline from **student-athlete → assistant coach → head coach** across three NCAA Division I women's sports — using 14 years of longitudinal data from the NCAA Demographics Database.

The central finding: **the coaching pipeline is expanding at the assistant level but narrowing at the top.**

A key structural pattern — the **"Glass Clipboard"** — emerges in the data: certain groups, particularly Black and African American coaches, enter assistant coaching at strong rates but face disproportionate barriers advancing to head coaching positions. The barrier isn't visible until you map the promotion gap.

The analysis is designed as a research-style tool for athletic departments, conference offices, and NCAA governance stakeholders evaluating long-term coaching diversity and leadership development strategy.

---

## Dashboard Preview

![Dashboard Preview](dashboard-preview.png)

  3. Uncomment and update the lines below:

[WBB Dual-Line Chart](docs/screenshots/wbb_dual_line_chart.png) 
/ https://github.com/kbsmd-sportsmusicdata/ncaa-d1-coaching-pipeline-dashboard/blob/main/docs/screenshots/volleyball_multi_line_chart.png
[WBB Promotion Ladder](docs/screenshots/wbb_promotion_ladder.png)
-->

---

## Research Questions

- Are NCAA athlete populations diversifying faster than coaching staffs?
- Where does the coaching pipeline break down?
- Which sports show the largest promotion gaps?
- How aligned are coaching staffs with athlete demographics?
- Do international athletes transition into coaching roles?

---

## Key Findings

### 1. Athlete Diversity Is Increasing
Across all three sports, the Simpson Diversity Index (SDI) rose between **+19% and +33%** since 2012. Women's Basketball now has the highest athlete diversity in the dataset.

### 2. Coaching Leadership Lags Behind
White coaches remain overrepresented relative to athlete populations by an average of **13.4 percentage points** across all three sports (latest year).

### 3. Expansion Without Elevation
In WBB, estimated assistant coach counts rose **+33%** from 2012–2025, while head coaching positions grew only **+3%** — a widening bottleneck at the top of the pipeline.

### 4. Promotion Gaps Reveal the Glass Clipboard
Black and African American coaches hold ~30% of WBB assistant coaching positions but only ~17% of head coaching roles. The promotion gap is **−13.3 percentage points** — well above the 10pp structural disparity threshold.

| Race Group (WBB) | Asst Coach % | Head Coach % | Gap (pp) |
|-----------------|:------------:|:------------:|:--------:|
| White | 52% | 70% | +17.6 |
| Black / African American | 30% | 17% | **−13.3** |
| Hispanic / Latino | 5% | 4% | −0.8 |
| Asian | 2% | 1% | −1.3 |
| International | 4% | 4% | −0.5 |
| Two or More | 7% | 4% | −2.7 |

*Estimated values based on NCAA Demographics Database and known promotion gap data*

### 5. Female Leadership Has Plateaued
Women represent the majority of coaches across all three sports, but WBB female representation has held between **63–66%** for over a decade — a structural ceiling.

### 6. International Pipeline Gap
International athletes represent **~10% of WBB rosters** but less than **1% of coaching staff** — the largest structural pipeline deficit in the dataset.

> **The court may be level. The sideline still isn't.**

---

## Key Visualizations

### Pipeline Funnel
Maps the three-stage structure — athletes → assistant coaches → head coaches — across all three sports. Visually illustrates where the pipeline narrows and where diversity is lost at each transition.

### Dual-Line Chart: WBB Coach Counts Over Time *(est., WBB only)*
Shows estimated WBB head coach and assistant coach counts from 2012–2025. The diverging lines make the bottleneck effect immediately visible: assistants rising steeply while head coaching positions remain nearly flat.

### Promotion Ladder: Coach Representation by Race (Asst → Head)
A grouped horizontal bar chart pairing assistant coach % and head coach % side-by-side for each racial group — making the Glass Clipboard promotion gap legible at a glance. Available for WBB, Softball, and Volleyball.

---

## Dataset

**Source:** [NCAA Demographics Database](https://www.ncaa.org/sports/2018/12/13/ncaa-demographics-database.aspx)
**Coverage:** 2011–12 through 2024–25 (14 years)
**Published:** September 2025 on NCAA.org

| Sport | Athletes | Coaches |
|-------|:--------:|:-------:|
| Women's Basketball | 5,153 | 1,766 |
| Softball | 6,956 | 1,040 |
| Volleyball | 6,454 | 1,110 |
| **Total** | **18,563** | **3,916** |

---

## Dashboard Features

- Overview tab with system-level KPIs and cross-sport trends
- Sport-specific deep dives for WBB, Softball, and Volleyball
- Athlete vs. coach demographic comparisons
- Simpson Diversity Index trends (2012–2025)
- Promotion Ladder visualization (Asst % → Head Coach % by race group)
- Assistant → Head Coach promotion gap analysis
- Gender representation trends by sport
- International athlete coaching pipeline diagnostics
- Heatmap: gender × race representation intensity
- Metrics & Definitions tab

---

## Methods

- **Simpson Diversity Index (SDI)** — probability that two randomly selected individuals belong to different demographic groups; computed per sport per year
- **Representation Gap** — `Coach Share − Athlete Share`; positive = overrepresented in coaching, negative = underrepresented
- **Promotion Gap** — `Head Coach Share − Assistant Coach Share`; values ≤ −10pp flag structural disparity
- **Longitudinal trend analysis** — 14-season baseline from 2012–2025
- **Cross-sport benchmarking** — WBB, Softball, Volleyball compared on all core metrics

---

## Limitations

The analysis relies on publicly reported NCAA demographic data and does not capture individual career pathways or coaching tenure. Coaching counts track *positions*, not unique individuals — staff who coach multiple sports may be counted more than once. Estimated WBB coach counts are derived from reported assistant-to-head ratios applied to known program counts. Future work could integrate longitudinal coach career tracking and institutional hiring patterns.

---

## Tech Stack

- Python — data cleaning, transformation, and visualization
- HTML / CSS / JavaScript — dashboard interface
- Chart.js — interactive chart rendering
- GitHub Pages — dashboard hosting
- pptxgenjs — slide deck generation
- Sports analytics research design

---

## Repository Structure

```
ncaa-d1-coaching-pipeline-dashboard/
│
├── index.html                        # Interactive dashboard
├── README.md                         # Project documentation
├── dashboard-preview.png             # Dashboard screenshot for README
│
├── data/
│   └── ncaa_d1_womens_sports.parquet     # Processed dataset (14 years, 3 sports)
│
├── notebooks/
│   └── analysis_pipeline.ipynb       # Analysis notebook
│
├── docs/
│   ├── ncaa_d1_coaching_pipeline_slides.pptx
│   ├── ncaa_d1_coaching_pipeline_research_brief.pdf
│   └── screenshots/                  # Dashboard screenshots
│
└── NCAA_Pipeline_Infographic.png     # One-page portfolio/social infographic
```

---

## Potential Applications

- Athletic department leadership and pipeline health evaluations
- Conference-level diversity benchmarking across member institutions
- Leadership development program targeting and tracking
- NCAA governance policy and equity research
- Coaching pipeline monitoring and promotion gap diagnostics

---

## Author

**Krystal Beasley** | hey@krystalbcreative.com 

View My: [Sports Analytics Portfolio](https://www.notion.so/krystal-beasley/Sports-Analyst-Portfolio-231077fe20b880b381b7f9877bee2021) | [LinkedIn](https://www.linkedin.com/in/krystalbeasley/) | [GitHub](https://github.com/kbsmd-sportsmusicdata)
