# visualization_dashboard.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class VisualizationDashboard:
    """Etkileşimli görselleştirme"""
    
    def __init__(self, results):
        self.results = results
        sns.set_style("whitegrid")
    
    def create_full_dashboard(self):
        """Tek sayfada tüm metrikler"""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Enerji Karşılaştırması
        ax1 = fig.add_subplot(gs[0, 0])
        self.plot_energy_comparison(ax1)
        
        # 2. Gecikme Karşılaştırması
        ax2 = fig.add_subplot(gs[0, 1])
        self.plot_latency_comparison(ax2)
        
        # 3. Güç-Verimlilik Trade-off
        ax3 = fig.add_subplot(gs[0, 2])
        self.plot_power_efficiency_tradeoff(ax3)
        
        # 4. Workload Scaling
        ax4 = fig.add_subplot(gs[1, :2])
        self.plot_workload_scaling(ax4)
        
        # 5. Termal Profil
        ax5 = fig.add_subplot(gs[1, 2])
        self.plot_thermal_profile(ax5)
        
        # 6. CNN Model Karşılaştırması
        ax6 = fig.add_subplot(gs[2, :])
        self.plot_cnn_model_comparison(ax6)
        
        plt.suptitle('Eco-PIM Performance Dashboard', 
                    fontsize=20, fontweight='bold')
        plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_energy_comparison(self, ax):
        # Implementasyon...
        pass