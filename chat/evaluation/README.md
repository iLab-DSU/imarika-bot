# 📊 Evaluation Framework

## Overview
Performance evaluation and metrics analysis for fine-tuning improvements.

## Structure
```
evaluation/
├── metrics/
│   └── metrics_comparison.py # Performance metrics comparison
└── reports/
    └── show_improvements.py  # Improvement analysis reports
```

## Key Metrics
- **Composite Score**: Overall performance (0-1)
- **Keyword Density**: Agricultural terminology coverage
- **Completeness**: Response depth and structure
- **Accuracy**: Expected content presence
- **Specificity**: Query-response relevance

## Usage
```bash
# Run performance comparison
python evaluation/metrics/metrics_comparison.py

# Generate improvement reports
python evaluation/reports/show_improvements.py
```

## Results
- **Overall Improvement**: +107.9%
- **Performance Rating**: ✅ Good Improvement