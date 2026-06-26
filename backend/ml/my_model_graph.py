"""
Graph for CivicLens MobileNetV2 Model Only
Scatter/Line Plot showing Model Metrics

X-axis: Model Size / Parameters / Inference Time
Y-axis: Accuracy / F1 Score
"""

import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'figure.dpi': 150
})

# ============================================================================
# YOUR MODEL DATA (MobileNetV2 - CivicLens)
# ============================================================================
model_name = "MobileNetV2 (CivicLens)"
parameters = 2.43  # Million parameters
accuracy = 95.99   # %
f1_score = 95.96   # %
precision = 96.04  # %
recall = 95.99     # %
inference_time = 8  # ms (estimated)
model_size_mb = 11.6  # MB

# Per-class F1 scores
classes = ['Garbage', 'Invalid_data', 'Potholes', 'Waterlogging']
class_f1 = [95.26, 98.18, 94.65, 91.79]
class_precision = [92.39, 97.83, 93.41, 96.37]
class_recall = [98.32, 98.52, 95.94, 87.63]

# ============================================================================
# FIGURE: Single Model Scatter Plot
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: Model Size vs Accuracy/F1
ax1 = axes[0]
ax1.scatter(parameters, accuracy, s=300, c='#e74c3c', marker='o', 
            edgecolor='black', linewidth=2, label='Accuracy', zorder=5)
ax1.scatter(parameters, f1_score, s=300, c='#3498db', marker='s', 
            edgecolor='black', linewidth=2, label='F1-Score', zorder=5)

# Add labels
ax1.annotate(f'Accuracy: {accuracy}%', (parameters, accuracy), 
             textcoords="offset points", xytext=(15, 10), fontsize=12, fontweight='bold')
ax1.annotate(f'F1-Score: {f1_score}%', (parameters, f1_score), 
             textcoords="offset points", xytext=(15, -15), fontsize=12, fontweight='bold')

ax1.set_xlabel('Model Size (Million Parameters)', fontweight='bold')
ax1.set_ylabel('Score (%)', fontweight='bold')
ax1.set_title(f'{model_name}\nModel Size vs Performance', fontweight='bold')
ax1.set_xlim(0, 5)
ax1.set_ylim(90, 100)
ax1.legend(loc='lower right', fontsize=11)
ax1.grid(True, alpha=0.3)

# Add model info box
info_text = f'Parameters: {parameters}M\nModel Size: {model_size_mb} MB\nInference: ~{inference_time}ms'
ax1.text(0.05, 0.95, info_text, transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# RIGHT: Inference Time vs Accuracy/F1
ax2 = axes[1]
ax2.scatter(inference_time, accuracy, s=300, c='#e74c3c', marker='o', 
            edgecolor='black', linewidth=2, label='Accuracy', zorder=5)
ax2.scatter(inference_time, f1_score, s=300, c='#3498db', marker='s', 
            edgecolor='black', linewidth=2, label='F1-Score', zorder=5)

ax2.annotate(f'Accuracy: {accuracy}%', (inference_time, accuracy), 
             textcoords="offset points", xytext=(15, 10), fontsize=12, fontweight='bold')
ax2.annotate(f'F1-Score: {f1_score}%', (inference_time, f1_score), 
             textcoords="offset points", xytext=(15, -15), fontsize=12, fontweight='bold')

ax2.set_xlabel('Inference Time (ms)', fontweight='bold')
ax2.set_ylabel('Score (%)', fontweight='bold')
ax2.set_title(f'{model_name}\nInference Time vs Performance', fontweight='bold')
ax2.set_xlim(0, 20)
ax2.set_ylim(90, 100)
ax2.legend(loc='lower right', fontsize=11)
ax2.grid(True, alpha=0.3)

plt.suptitle('CivicLens Image Classification Model Performance', fontweight='bold', fontsize=18, y=1.02)
plt.tight_layout()
plt.savefig('models/paper_figures/my_model_performance.png', dpi=300, bbox_inches='tight')
print("Saved: my_model_performance.png")
plt.close()

# ============================================================================
# FIGURE 2: Per-Class Performance Line Plot
# ============================================================================
fig2, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(classes))
width = 0.25

# Plot lines connecting the metrics
ax.plot(x, class_precision, 'o-', markersize=12, linewidth=2, 
        label='Precision', color='#2ecc71', markeredgecolor='black')
ax.plot(x, class_recall, 's--', markersize=12, linewidth=2, 
        label='Recall', color='#3498db', markeredgecolor='black')
ax.plot(x, class_f1, '^-', markersize=12, linewidth=2, 
        label='F1-Score', color='#e74c3c', markeredgecolor='black')

# Add value labels
for i, (p, r, f) in enumerate(zip(class_precision, class_recall, class_f1)):
    ax.annotate(f'{p:.1f}', (i, p), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9)
    ax.annotate(f'{r:.1f}', (i, r), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9)
    ax.annotate(f'{f:.1f}', (i, f), textcoords="offset points", xytext=(0, -12), ha='center', fontsize=9)

ax.set_xlabel('Class Category', fontweight='bold')
ax.set_ylabel('Score (%)', fontweight='bold')
ax.set_title(f'{model_name} - Per-Class Performance', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(classes, fontweight='bold')
ax.set_ylim(80, 102)
ax.legend(loc='lower right', fontsize=11)
ax.grid(True, alpha=0.3)

# Add overall metrics
overall_text = f'Overall: Accuracy={accuracy}%, F1={f1_score}%'
ax.text(0.5, 0.02, overall_text, transform=ax.transAxes, fontsize=11,
        ha='center', fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

plt.tight_layout()
plt.savefig('models/paper_figures/my_model_perclass.png', dpi=300, bbox_inches='tight')
print("Saved: my_model_perclass.png")
plt.close()

print("\n✓ Graphs saved!")

# Open the images
import subprocess
subprocess.Popen(['start', '', 'models/paper_figures/my_model_performance.png'], shell=True)
subprocess.Popen(['start', '', 'models/paper_figures/my_model_perclass.png'], shell=True)
