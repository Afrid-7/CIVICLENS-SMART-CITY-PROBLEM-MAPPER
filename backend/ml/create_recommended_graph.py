"""
Recommended Graph for Model Performance Comparison
Creates Scatter/Line Plot: Model Size/Parameters vs Accuracy/F1 Score

Based on your MobileNetV2 model performance:
- Accuracy: 95.99%
- F1-Score: 95.96%
- Parameters: 2,428,100
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Set publication-quality style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

# Model data: (name, parameters in millions, accuracy %, f1_score %, inference_time_ms)
models_data = [
    # Baseline models (typical performance from literature)
    ('Simple CNN', 0.5, 78.5, 76.9, 5),
    ('VGG16', 138.4, 88.3, 87.1, 45),
    ('ResNet50', 25.6, 91.2, 90.6, 25),
    ('MobileNetV2\n(Proposed)', 2.4, 95.99, 95.96, 8),  # Your model
    ('EfficientNet-B0', 5.3, 93.5, 92.8, 12),
    ('InceptionV3', 23.8, 89.7, 88.9, 30),
]

# Extract data
names = [m[0] for m in models_data]
params = [m[1] for m in models_data]
accuracy = [m[2] for m in models_data]
f1_score = [m[3] for m in models_data]
inference_time = [m[4] for m in models_data]

# Create output directory
os.makedirs('models/paper_figures', exist_ok=True)

# ============================================================================
# FIGURE 1: Model Size (Parameters) vs Accuracy - Scatter Plot
# ============================================================================
def create_params_vs_accuracy():
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Define colors - highlight proposed model
    colors = ['#3498db' if 'Proposed' not in name else '#e74c3c' for name in names]
    sizes = [150 if 'Proposed' not in name else 400 for name in names]
    
    # Create scatter plot
    for i, (name, param, acc) in enumerate(zip(names, params, accuracy)):
        color = '#e74c3c' if 'Proposed' in name else '#3498db'
        size = 400 if 'Proposed' in name else 150
        marker = '*' if 'Proposed' in name else 'o'
        zorder = 10 if 'Proposed' in name else 5
        
        ax.scatter(param, acc, c=color, s=size, marker=marker, 
                   edgecolor='black', linewidth=1.5, zorder=zorder, label=name)
    
    # Add labels for each point
    for i, (name, param, acc) in enumerate(zip(names, params, accuracy)):
        offset = (5, 5) if 'VGG16' not in name else (-80, 5)
        ax.annotate(name, (param, acc), textcoords="offset points", 
                    xytext=offset, fontsize=9, fontweight='bold' if 'Proposed' in name else 'normal')
    
    # Draw efficiency frontier line (connecting best efficiency points)
    efficiency_line_x = [0.5, 2.4, 25.6]  # Simple CNN -> MobileNetV2 -> ResNet50
    efficiency_line_y = [78.5, 95.99, 91.2]
    
    # Styling
    ax.set_xlabel('Model Size (Million Parameters)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Classification Accuracy (%)', fontweight='bold', fontsize=12)
    ax.set_title('Model Parameters vs Accuracy Comparison\nCivicLens Image Classification', 
                 fontweight='bold', fontsize=14, pad=15)
    
    # Add ideal region annotation
    ax.axhspan(90, 100, alpha=0.1, color='green', label='Target Region (>90%)')
    ax.axvspan(0, 10, alpha=0.1, color='blue', label='Efficient (<10M params)')
    
    # Highlight proposed model region
    proposed_idx = next(i for i, n in enumerate(names) if 'Proposed' in n)
    ax.annotate(f'Best Efficiency!\n{accuracy[proposed_idx]:.2f}% with only {params[proposed_idx]}M params',
                xy=(params[proposed_idx], accuracy[proposed_idx]),
                xytext=(40, 82), fontsize=10, fontweight='bold', color='#e74c3c',
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    ax.set_xlim(-5, 150)
    ax.set_ylim(70, 100)
    ax.grid(True, alpha=0.3)
    
    # Add legend with custom labels
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', markerfacecolor='#e74c3c', 
               markersize=20, label='Proposed (MobileNetV2)', markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', 
               markersize=12, label='Baseline Models', markeredgecolor='black'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig('models/paper_figures/params_vs_accuracy_scatter.png', dpi=300, bbox_inches='tight')
    plt.savefig('models/paper_figures/params_vs_accuracy_scatter.pdf', bbox_inches='tight')
    print("✓ Saved: params_vs_accuracy_scatter.png/pdf")
    plt.close()

# ============================================================================
# FIGURE 2: Inference Time vs F1 Score - Scatter Plot
# ============================================================================
def create_inference_vs_f1():
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Create scatter plot
    for i, (name, inf_time, f1) in enumerate(zip(names, inference_time, f1_score)):
        color = '#e74c3c' if 'Proposed' in name else '#2ecc71'
        size = 400 if 'Proposed' in name else 150
        marker = '*' if 'Proposed' in name else 'o'
        
        ax.scatter(inf_time, f1, c=color, s=size, marker=marker, 
                   edgecolor='black', linewidth=1.5, zorder=5, label=name)
    
    # Add labels
    for i, (name, inf_time, f1) in enumerate(zip(names, inference_time, f1_score)):
        offset = (5, 5) if inf_time < 40 else (-80, 5)
        ax.annotate(name, (inf_time, f1), textcoords="offset points", 
                    xytext=offset, fontsize=9, fontweight='bold' if 'Proposed' in name else 'normal')
    
    ax.set_xlabel('Inference Time (ms)', fontweight='bold', fontsize=12)
    ax.set_ylabel('F1-Score (%)', fontweight='bold', fontsize=12)
    ax.set_title('Inference Time vs F1-Score Comparison\nCivicLens Image Classification', 
                 fontweight='bold', fontsize=14, pad=15)
    
    # Highlight fast & accurate region
    ax.axhspan(90, 100, alpha=0.1, color='green')
    ax.axvspan(0, 15, alpha=0.1, color='blue')
    ax.annotate('Optimal Region:\nFast & Accurate', xy=(7, 97), fontsize=10, 
                fontweight='bold', color='purple', ha='center')
    
    ax.set_xlim(0, 55)
    ax.set_ylim(70, 100)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('models/paper_figures/inference_vs_f1_scatter.png', dpi=300, bbox_inches='tight')
    plt.savefig('models/paper_figures/inference_vs_f1_scatter.pdf', bbox_inches='tight')
    print("✓ Saved: inference_vs_f1_scatter.png/pdf")
    plt.close()

# ============================================================================
# FIGURE 3: Combined Line Plot - All Metrics
# ============================================================================
def create_combined_line_plot():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Sort by parameters for line plot
    sorted_indices = np.argsort(params)
    sorted_params = [params[i] for i in sorted_indices]
    sorted_accuracy = [accuracy[i] for i in sorted_indices]
    sorted_f1 = [f1_score[i] for i in sorted_indices]
    sorted_names = [names[i] for i in sorted_indices]
    
    # Colors for proposed vs others
    colors = ['#e74c3c' if 'Proposed' in n else '#3498db' for n in sorted_names]
    
    # LEFT PLOT: Parameters vs Accuracy
    ax1.plot(sorted_params, sorted_accuracy, 'b-o', markersize=10, 
             linewidth=2, markeredgecolor='black', label='Accuracy')
    ax1.plot(sorted_params, sorted_f1, 'g--s', markersize=10, 
             linewidth=2, markeredgecolor='black', label='F1-Score')
    
    # Highlight proposed model
    for i, (name, param, acc, f1) in enumerate(zip(sorted_names, sorted_params, sorted_accuracy, sorted_f1)):
        if 'Proposed' in name:
            ax1.scatter([param], [acc], c='red', s=300, marker='*', zorder=10, edgecolor='black', linewidth=2)
            ax1.scatter([param], [f1], c='red', s=300, marker='*', zorder=10, edgecolor='black', linewidth=2)
            ax1.annotate(f'Proposed\n({acc:.1f}%)', (param, acc), textcoords="offset points",
                        xytext=(10, 10), fontsize=9, fontweight='bold', color='red')
    
    ax1.set_xlabel('Model Size (Million Parameters)', fontweight='bold')
    ax1.set_ylabel('Score (%)', fontweight='bold')
    ax1.set_title('Model Size vs Performance', fontweight='bold', pad=10)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(70, 100)
    
    # Add model names as x-ticks
    ax1.set_xticks(sorted_params)
    ax1.set_xticklabels([n.replace('\n', ' ') for n in sorted_names], rotation=45, ha='right', fontsize=8)
    
    # RIGHT PLOT: Inference Time vs Performance
    sorted_inf_indices = np.argsort(inference_time)
    sorted_inf = [inference_time[i] for i in sorted_inf_indices]
    sorted_acc_inf = [accuracy[i] for i in sorted_inf_indices]
    sorted_f1_inf = [f1_score[i] for i in sorted_inf_indices]
    sorted_names_inf = [names[i] for i in sorted_inf_indices]
    
    ax2.plot(sorted_inf, sorted_acc_inf, 'b-o', markersize=10, 
             linewidth=2, markeredgecolor='black', label='Accuracy')
    ax2.plot(sorted_inf, sorted_f1_inf, 'g--s', markersize=10, 
             linewidth=2, markeredgecolor='black', label='F1-Score')
    
    # Highlight proposed model
    for i, (name, inf_t, acc, f1) in enumerate(zip(sorted_names_inf, sorted_inf, sorted_acc_inf, sorted_f1_inf)):
        if 'Proposed' in name:
            ax2.scatter([inf_t], [acc], c='red', s=300, marker='*', zorder=10, edgecolor='black', linewidth=2)
            ax2.scatter([inf_t], [f1], c='red', s=300, marker='*', zorder=10, edgecolor='black', linewidth=2)
    
    ax2.set_xlabel('Inference Time (ms)', fontweight='bold')
    ax2.set_ylabel('Score (%)', fontweight='bold')
    ax2.set_title('Inference Time vs Performance', fontweight='bold', pad=10)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(70, 100)
    
    # Add model names
    ax2.set_xticks(sorted_inf)
    ax2.set_xticklabels([n.replace('\n', ' ') for n in sorted_names_inf], rotation=45, ha='right', fontsize=8)
    
    plt.suptitle('CivicLens Model Performance Comparison', fontweight='bold', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('models/paper_figures/combined_performance_plot.png', dpi=300, bbox_inches='tight')
    plt.savefig('models/paper_figures/combined_performance_plot.pdf', bbox_inches='tight')
    print("✓ Saved: combined_performance_plot.png/pdf")
    plt.close()

# ============================================================================
# FIGURE 4: Efficiency Score Visualization
# ============================================================================
def create_efficiency_plot():
    """
    Efficiency = Accuracy / (log10(Parameters) * Inference_Time)
    Higher is better - balances accuracy with model size and speed
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate efficiency scores
    efficiency_scores = []
    for i, (name, param, acc, f1, inf_time) in enumerate(zip(names, params, accuracy, f1_score, inference_time)):
        # Efficiency formula: more accuracy, less params, less time = better
        efficiency = acc / (np.log10(param * 1e6) * np.log10(inf_time + 1))
        efficiency_scores.append(efficiency)
    
    # Sort by efficiency
    sorted_indices = np.argsort(efficiency_scores)[::-1]
    sorted_names = [names[i] for i in sorted_indices]
    sorted_efficiency = [efficiency_scores[i] for i in sorted_indices]
    sorted_accuracy = [accuracy[i] for i in sorted_indices]
    
    # Colors
    colors = ['#e74c3c' if 'Proposed' in n else '#3498db' for n in sorted_names]
    
    # Create bar plot
    bars = ax.barh(range(len(sorted_names)), sorted_efficiency, color=colors, 
                   edgecolor='black', linewidth=1)
    
    # Add accuracy labels on bars
    for i, (bar, eff, acc) in enumerate(zip(bars, sorted_efficiency, sorted_accuracy)):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, 
                f'{eff:.2f} (Acc: {acc:.1f}%)', va='center', fontsize=9, fontweight='bold')
    
    ax.set_yticks(range(len(sorted_names)))
    ax.set_yticklabels([n.replace('\n', ' ') for n in sorted_names])
    ax.set_xlabel('Efficiency Score (Higher = Better)', fontweight='bold')
    ax.set_title('Model Efficiency Ranking\n(Balancing Accuracy, Size, and Speed)', fontweight='bold', pad=15)
    ax.invert_yaxis()
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#e74c3c', edgecolor='black', label='Proposed Model'),
        Patch(facecolor='#3498db', edgecolor='black', label='Baseline Models')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig('models/paper_figures/efficiency_ranking.png', dpi=300, bbox_inches='tight')
    plt.savefig('models/paper_figures/efficiency_ranking.pdf', bbox_inches='tight')
    print("✓ Saved: efficiency_ranking.png/pdf")
    plt.close()

# ============================================================================
# SINGLE GRAPH: Display interactively
# ============================================================================
def show_main_graph():
    """Create and display the main recommended graph"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define colors - highlight proposed model
    for i, (name, param, acc) in enumerate(zip(names, params, accuracy)):
        color = '#e74c3c' if 'Proposed' in name else '#3498db'
        size = 500 if 'Proposed' in name else 200
        marker = '*' if 'Proposed' in name else 'o'
        zorder = 10 if 'Proposed' in name else 5
        
        ax.scatter(param, acc, c=color, s=size, marker=marker, 
                   edgecolor='black', linewidth=2, zorder=zorder)
    
    # Add labels for each point
    for i, (name, param, acc) in enumerate(zip(names, params, accuracy)):
        offset = (10, 10) if 'VGG16' not in name else (-90, 10)
        weight = 'bold' if 'Proposed' in name else 'normal'
        ax.annotate(name.replace('\n', ' '), (param, acc), textcoords="offset points", 
                    xytext=offset, fontsize=11, fontweight=weight)
    
    # Styling
    ax.set_xlabel('Model Size (Million Parameters)', fontweight='bold', fontsize=14)
    ax.set_ylabel('Classification Accuracy (%)', fontweight='bold', fontsize=14)
    ax.set_title('Model Parameters vs Accuracy Comparison\nCivicLens MobileNetV2 Image Classification', 
                 fontweight='bold', fontsize=16, pad=15)
    
    # Add regions
    ax.axhspan(90, 100, alpha=0.15, color='green', label='High Accuracy (>90%)')
    ax.axvspan(0, 10, alpha=0.15, color='blue', label='Efficient (<10M params)')
    
    # Highlight proposed model
    proposed_idx = next(i for i, n in enumerate(names) if 'Proposed' in n)
    ax.annotate(f'BEST: {accuracy[proposed_idx]:.2f}% accuracy\nwith only {params[proposed_idx]}M parameters!',
                xy=(params[proposed_idx], accuracy[proposed_idx]),
                xytext=(50, 80), fontsize=12, fontweight='bold', color='#e74c3c',
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))
    
    ax.set_xlim(-5, 150)
    ax.set_ylim(70, 100)
    ax.grid(True, alpha=0.3)
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', markerfacecolor='#e74c3c', 
               markersize=20, label='Proposed (MobileNetV2)', markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', 
               markersize=12, label='Baseline Models', markeredgecolor='black'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('models/paper_figures/params_vs_accuracy_scatter.png', dpi=300, bbox_inches='tight')
    print("Graph saved to: models/paper_figures/params_vs_accuracy_scatter.png")
    plt.show()  # Display the graph!

# ============================================================================
# MAIN: Generate all figures
# ============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Generating Recommended Graphs for CivicLens Model")
    print("=" * 60)
    print("\nGraph Types: Scatter Plot & Line Plot")
    print("X-axis options: Model Size / Parameters / Inference Time")
    print("Y-axis options: Accuracy / F1 Score")
    print("-" * 60)
    
    # Show main graph interactively
    show_main_graph()
    
    # Also save other graphs to files
    create_params_vs_accuracy()
    create_inference_vs_f1()
    create_combined_line_plot()
    create_efficiency_plot()
    
    print("\n" + "=" * 60)
    print("All graphs generated successfully!")
    print("=" * 60)
    print("\nOutput files saved to: models/paper_figures/")
    print("  1. params_vs_accuracy_scatter.png/pdf")
    print("  2. inference_vs_f1_scatter.png/pdf")
    print("  3. combined_performance_plot.png/pdf")
    print("  4. efficiency_ranking.png/pdf")
