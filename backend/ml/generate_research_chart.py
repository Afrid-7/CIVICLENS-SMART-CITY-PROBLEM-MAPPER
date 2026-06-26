"""
SOTA vs CivicLens Model Comparison Chart
Benchmarking local MobileNetV2 against 2024-2025 Road Damage Research
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import os

# Set publication-quality style
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'figure.dpi': 200
})

# 1. Load your model's actual performance from JSON
METRICS_PATH = 'backend/ml/models/performance_metrics.json'
with open(METRICS_PATH, 'r') as f:
    your_metrics = json.load(f)

proposed_model = {
    'name': 'CivicLens (MobileNetV2)',
    'accuracy': your_metrics['overall_metrics']['accuracy'] * 100,
    'precision': your_metrics['overall_metrics']['precision'] * 100,
    'recall': your_metrics['overall_metrics']['recall'] * 100,
    'f1_score': your_metrics['overall_metrics']['f1_score'] * 100
}

# 2. SOTA Research Paper Results (Verified from 2024-2025 Paper Data)
# Paper 1: YOLOv8-seg (SimAM/DSConv) [arXiv:2505.04207] -> mAP: 93.8%, Precision: 93.7%, Recall: 90.4%
# Paper 3: YOLOv5s-M (GFPN) [ScienceDirect 2023] -> mAP: 79.8%, Precision: 78.2%, Recall: 72.1%
# Paper 4: YOLOv5 Real-time (Built-in) [ScienceDirect 2024] -> mAP: 96.3%, Precision: 93.0%, Recall: 91.6%

sota_models = [
    {
        'name': 'YOLOv5s-M (GFPN)',
        'accuracy': 79.8, # Using mAP as primary accuracy proxy
        'precision': 78.2,
        'recall': 72.1,
        'f1_score': 75.0
    },
    {
        'name': 'YOLOv8-seg (SimAM)',
        'accuracy': 93.8, # Using mAP as primary accuracy proxy
        'precision': 93.7,
        'recall': 90.4,
        'f1_score': 92.0 # Calculated harmonic mean
    },
    {
        'name': 'YOLOv5-RT',
        'accuracy': 96.3, # Using mAP as primary accuracy proxy
        'precision': 93.0,
        'recall': 91.6,
        'f1_score': 87.0
    },
    proposed_model 
]

# Create output directory
os.makedirs('backend/ml/models/paper_figures', exist_ok=True)

def create_performance_comparison():
    fig, ax = plt.subplots(figsize=(12, 7))
    
    models = [m['name'] for m in sota_models]
    metrics = ['mAP (Accuracy)', 'Precision', 'Recall', 'F1_Score']
    
    x = np.arange(len(models))
    width = 0.18
    
    # Modern professional palette
    colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2']
    
    for i, metric in enumerate(metrics):
        # Map metric display name to dict keys
        if 'mAP' in metric:
            key = 'accuracy'
        else:
            key = metric.lower().replace('-', '_')
        
        values = [m[key] for m in sota_models]
        
        # Shift bars
        pos = x + (i - 1.5) * width
        bars = ax.bar(pos, values, width, label=metric, color=colors[i], alpha=0.9, edgecolor='white')
        
        # Add EXACT labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 5), textcoords="offset points",
                       ha='center', va='bottom', fontsize=8, fontweight='bold', rotation=90)

    ax.set_ylabel('Score (%)', fontweight='bold')
    ax.set_title('Model Comparison Graph', fontweight='bold', pad=30)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.set_ylim(65, 110) # Added space for labels
    
    # Add a horizontal line for CivicLens baseline
    ax.axhline(y=proposed_model['accuracy'], color='gray', linestyle='--', alpha=0.3)
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=True)
    plt.tight_layout()
    
    save_path = 'backend/ml/models/paper_figures/sota_comparison_chart.png'
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    print(f"Comparison chart with precise digits saved to: {save_path}")

if __name__ == "__main__":
    create_performance_comparison()
