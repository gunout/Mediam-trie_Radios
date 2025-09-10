import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import time
import warnings
warnings.filterwarnings('ignore')

class ReunionRadioAnalyzer:
    def __init__(self):
        self.radios = {
            'Réunion 1ère': {'type': 'Public', 'lancement': 1960, 'couleur': '#FF6B00'},
            'NRJ Réunion': {'type': 'Commercial', 'lancement': 1990, 'couleur': '#FF0000'},
            'Freedom': {'type': 'Commercial', 'lancement': 1982, 'couleur': '#0000FF'},
            'RCI': {'type': 'Commercial', 'lancement': 1981, 'couleur': '#800080'},
            'Radio Est': {'type': 'Associative', 'lancement': 1983, 'couleur': '#008000'},
            'Radio Kreol': {'type': 'Culturelle', 'lancement': 1995, 'couleur': '#FFD700'},
            'Hit West': {'type': 'Commercial', 'lancement': 2005, 'couleur': '#FF1493'},
            'Radio Sun': {'type': 'Commercial', 'lancement': 1987, 'couleur': '#FFA500'}
        }
        
        # Données simulées basées sur les tendances réelles connues
        self.audience_data = self._create_realistic_audience_data()
    
    def _create_realistic_audience_data(self):
        """Crée des données réalistes basées sur les tendances connues"""
        audience_data = {}
        
        # Données basées sur les tendances réelles observées
        trends = {
            'Réunion 1ère': {'2002': 28.5, 'trend': -0.25, 'volatility': 0.8},
            'NRJ Réunion': {'2002': 16.8, 'trend': 0.15, 'volatility': 1.0},
            'Freedom': {'2002': 14.2, 'trend': 0.10, 'volatility': 0.9},
            'RCI': {'2002': 12.5, 'trend': -0.08, 'volatility': 0.7},
            'Radio Est': {'2002': 8.3, 'trend': 0.05, 'volatility': 0.6},
            'Radio Kreol': {'2002': 6.7, 'trend': 0.20, 'volatility': 0.8},
            'Hit West': {'2005': 4.5, 'trend': 0.35, 'volatility': 1.2},
            'Radio Sun': {'2002': 5.2, 'trend': 0.12, 'volatility': 0.7}
        }
        
        for radio, params in trends.items():
            audience_data[radio] = {}
            start_year = 2002
            if radio == 'Hit West':
                start_year = 2005
            
            base_value = params[str(start_year)]
            trend = params['trend']
            volatility = params['volatility']
            
            for year in range(2002, 2026):
                if year < start_year:
                    continue
                
                # Calcul avec tendance linéaire
                years_passed = year - start_year
                value = base_value + (trend * years_passed)
                
                # Variation aléatoire
                variation = np.random.normal(0, volatility)
                value += variation
                
                # Événements spéciaux
                if year == 2008:  # Crise économique
                    value += np.random.uniform(-2, -1)
                elif year == 2020:  # COVID-19
                    value += np.random.uniform(2, 4)  # Hausse de l'écoute
                elif year == 2021:  # Post-COVID
                    value += np.random.uniform(-1, 1)
                
                # Assurance des limites réalistes
                value = max(1.0, min(35.0, round(value, 1)))
                audience_data[radio][str(year)] = value
        
        return audience_data
    
    def get_radio_data(self, radio_name):
        """Retourne les données pour une radio spécifique"""
        return self.audience_data.get(radio_name, {})
    
    def get_all_data(self):
        """Retourne toutes les données sous forme de DataFrame"""
        all_data = []
        
        for radio, data in self.audience_data.items():
            for year, audience in data.items():
                all_data.append({
                    'Radio': radio,
                    'Type': self.radios[radio]['type'],
                    'Année': int(year),
                    'Audience (%)': audience,
                    'Lancement': self.radios[radio]['lancement'],
                    'Couleur': self.radios[radio]['couleur']
                })
        
        return pd.DataFrame(all_data)
    
    def create_comprehensive_analysis(self, df):
        """Crée une analyse complète avec visualisations"""
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))
        axes = axes.flatten()
        
        # 1. Évolution temporelle
        for radio in df['Radio'].unique():
            radio_data = df[df['Radio'] == radio].sort_values('Année')
            color = self.radios[radio]['couleur']
            axes[0].plot(radio_data['Année'], radio_data['Audience (%)'], 
                        label=radio, linewidth=2.5, color=color, marker='o', markersize=4)
        
        axes[0].set_title('📻 Évolution des Audiences des Radios Réunionnaises (2002-2025)', 
                         fontsize=14, fontweight='bold', pad=20)
        axes[0].set_ylabel('Part d\'audience (%)', fontsize=12)
        axes[0].set_xlabel('Année', fontsize=12)
        axes[0].grid(True, alpha=0.3, linestyle='--')
        axes[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        axes[0].tick_params(axis='x', rotation=45)
        
        # 2. Classement 2024
        latest_year = df['Année'].max()
        latest_data = df[df['Année'] == latest_year]
        top_radios = latest_data.nlargest(10, 'Audience (%)')
        
        colors = [self.radios[radio]['couleur'] for radio in top_radios['Radio']]
        bars = axes[1].barh(top_radios['Radio'], top_radios['Audience (%)'], color=colors)
        axes[1].set_title(f'🏆 Classement des Audiences en {latest_year}', 
                         fontsize=14, fontweight='bold', pad=20)
        axes[1].set_xlabel('Part d\'audience (%)', fontsize=12)
        
        for bar in bars:
            width = bar.get_width()
            axes[1].text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                        f'{width:.1f}%', ha='left', va='center', fontweight='bold')
        
        # 3. Répartition par type
        type_data = latest_data.groupby('Type')['Audience (%)'].sum()
        colors_type = ['#FF6B00', '#FF0000', '#008000', '#FFD700']
        wedges, texts, autotexts = axes[2].pie(type_data.values, labels=type_data.index,
                                              autopct='%1.1f%%', startangle=90,
                                              colors=colors_type, textprops={'fontsize': 11})
        axes[2].set_title(f'📊 Répartition par Type de Radio en {latest_year}', 
                         fontsize=14, fontweight='bold', pad=20)
        
        # 4. Tendances 2002-2025
        trends = []
        for radio in df['Radio'].unique():
            radio_data = df[df['Radio'] == radio]
            if len(radio_data) > 1:
                start_audience = radio_data['Audience (%)'].iloc[0]
                end_audience = radio_data['Audience (%)'].iloc[-1]
                trend = end_audience - start_audience
                trends.append({'Radio': radio, 'Tendance': trend, 
                              'Type': radio_data['Type'].iloc[0]})
        
        trends_df = pd.DataFrame(trends)
        colors_trend = [self.radios[radio]['couleur'] for radio in trends_df['Radio']]
        
        bars = axes[3].barh(trends_df['Radio'], trends_df['Tendance'], color=colors_trend)
        axes[3].set_title('📈 Tendances 2002-2025 (Variation en points)', 
                         fontsize=14, fontweight='bold', pad=20)
        axes[3].set_xlabel('Variation (points %)', fontsize=12)
        axes[3].axvline(x=0, color='black', linestyle='-', alpha=0.8)
        
        for bar in bars:
            width = bar.get_width()
            color = 'green' if width >= 0 else 'red'
            axes[3].text(width + (0.1 if width >=0 else -0.1), 
                        bar.get_y() + bar.get_height()/2, 
                        f'{width:+.1f}', ha='left' if width >=0 else 'right', 
                        va='center', fontweight='bold', color=color)
        
        plt.tight_layout()
        plt.savefig('analyse_complete_radios_reunion.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Affichage des statistiques
        self._display_statistics(df)
    
    def _display_statistics(self, df):
        """Affiche les statistiques détaillées"""
        print("\n" + "="*60)
        print("📊 STATISTIQUES DÉTAILLÉES - AUDIENCE RADIO RÉUNION")
        print("="*60)
        
        latest_year = df['Année'].max()
        latest_data = df[df['Année'] == latest_year]
        
        print(f"\n🏆 CLASSEMENT {latest_year}:")
        print("-" * 40)
        top_5 = latest_data.nlargest(5, 'Audience (%)')
        for i, (_, row) in enumerate(top_5.iterrows(), 1):
            print(f"{i}. {row['Radio']}: {row['Audience (%)']:.1f}%")
        
        print(f"\n📈 TENDANCES 2002-2025:")
        print("-" * 40)
        for radio in df['Radio'].unique():
            radio_data = df[df['Radio'] == radio]
            if len(radio_data) > 1:
                start = radio_data['Audience (%)'].min()
                end = radio_data['Audience (%)'].max()
                avg = radio_data['Audience (%)'].mean()
                trend = end - radio_data['Audience (%)'].iloc[0]
                print(f"• {radio}: {trend:+.1f} pts (Moyenne: {avg:.1f}%)")
        
        print(f"\n📋 RÉPARTITION PAR TYPE ({latest_year}):")
        print("-" * 40)
        type_stats = latest_data.groupby('Type').agg({
            'Audience (%)': ['sum', 'mean', 'count']
        }).round(1)
        print(type_stats)

    def export_to_excel(self, df):
        """Exporte les données vers Excel"""
        with pd.ExcelWriter('audience_radios_reunion.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Données Brutes', index=False)
            
            # Feuille de synthèse
            summary = df.pivot_table(values='Audience (%)', 
                                   index='Année', 
                                   columns='Radio', 
                                   aggfunc='mean')
            summary.to_excel(writer, sheet_name='Synthèse')
            
            # Statistiques par type
            type_stats = df.groupby(['Type', 'Année'])['Audience (%)'].mean().unstack()
            type_stats.to_excel(writer, sheet_name='Par Type')
        
        print("💾 Données exportées vers 'audience_radios_reunion.xlsx'")

def main():
    """Fonction principale"""
    print("🎯 Analyse des audiences radio de la Réunion (2002-2025)")
    print("⏳ Génération des données simulées...")
    
    # Créer l'analyseur
    analyzer = ReunionRadioAnalyzer()
    
    # Récupérer les données
    df = analyzer.get_all_data()
    
    # Afficher les premières lignes
    print(f"\n📋 Aperçu des données ({len(df)} lignes):")
    print(df.head())
    
    # Créer l'analyse visuelle
    analyzer.create_comprehensive_analysis(df)
    
    # Exporter vers Excel
    analyzer.export_to_excel(df)
    
    # Sauvegarder en CSV
    df.to_csv('audience_radios_reunion.csv', index=False)
    print("💾 Données sauvegardées dans 'audience_radios_reunion.csv'")
    
    print("\n✅ Analyse terminée avec succès!")

if __name__ == "__main__":
    main()
