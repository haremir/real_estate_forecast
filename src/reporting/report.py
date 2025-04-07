#!/usr/bin/env python3
"""
Boston Housing - Tek Dosya Rapor Üretici
Kullanım:
  python report.py [--input <path>] [--output <path>] [--interactive]
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

# --------------------------
# KONFİGÜRASYON
# --------------------------
DEFAULT_INPUT = "data/processed/cleaned_boston.csv"
DEFAULT_OUTPUT = f"reports/report_{datetime.now().strftime('%Y%m%d')}.pdf"
STYLE_CONFIG = {
    'figure.figsize': (10, 6),
    'font.size': 12,
    'axes.titlesize': 14
}

# --------------------------
# GÖRSELLEŞTİRME FONKSİYONLARI
# --------------------------
def set_style():
    """Global stil ayarları"""
    plt.style.use('seaborn')
    sns.set_palette("husl")
    plt.rcParams.update(STYLE_CONFIG)

def save_plot(pdf=None, save_path=None):
    """Grafiği kaydet veya göster"""
    if pdf:
        pdf.savefig(bbox_inches='tight')
    elif save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    else:
        plt.show()
    plt.close()

# --------------------------
# RAPOR BİLEŞENLERİ
# --------------------------
def add_cover_page(df, pdf):
    """PDF kapak sayfası"""
    plt.figure()
    plt.text(0.5, 0.7, "Boston Konut Raporu", ha='center', va='center', fontsize=20)
    plt.text(0.5, 0.5, f"Gözlem Sayısı: {len(df)}", ha='center', va='center', fontsize=14)
    plt.axis('off')
    save_plot(pdf)

def add_correlation_matrix(df, pdf):
    """Korelasyon analizi"""
    corr = df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", 
               mask=np.triu(np.ones_like(corr, dtype=bool)))
    plt.title("Özellik Korelasyonları")
    save_plot(pdf)

# --------------------------
# ANA İŞLEM
# --------------------------
def generate_report(input_path, output_path):
    """Tüm raporu oluşturur"""
    try:
        df = pd.read_csv(input_path)
        set_style()
        
        with PdfPages(output_path) as pdf:
            add_cover_page(df, pdf)
            add_correlation_matrix(df, pdf)
            # Diğer fonksiyonlar...
        
        print(f"✓ Rapor oluşturuldu: {os.path.abspath(output_path)}")
        return True
    except Exception as e:
        print(f"✗ Hata: {str(e)}", file=sys.stderr)
        return False

# --------------------------
# KOMUT SATIRI ARAYÜZÜ
# --------------------------
def parse_args():
    parser = argparse.ArgumentParser(description='Boston Housing Rapor Üretici')
    parser.add_argument('--input', default=DEFAULT_INPUT, help='Girdi veri yolu')
    parser.add_argument('--output', default=DEFAULT_OUTPUT, help='Çıktı PDF yolu')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    sys.exit(0 if generate_report(args.input, args.output) else 1)