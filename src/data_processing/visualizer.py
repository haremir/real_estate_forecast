# src/data_processing/visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
from typing import Optional, List
import numpy as np
import os

class BostonVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self._set_style()

    def _set_style(self):
        """Matplotlib stil ayarları"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12

    def _save_plot(self, fig, save_path: Optional[str] = None):
        """Güvenli kayıt fonksiyonu"""
        try:
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                fig.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close(fig)
                print(f"✅ Grafik kaydedildi: {save_path}")
            else:
                plt.show()
        except Exception as e:
            print(f"❌ Kayıt hatası: {str(e)}")
            plt.close()
            raise

    # 1. Eksik Veri Görselleştirme
    def plot_missing_data(self, save_path: Optional[str] = None, figsize: tuple = (12, 6)) -> None:
        """Eksik verileri interaktif heatmap ve çubuk grafikle gösterir."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Heatmap
        sns.heatmap(self.df.isnull(), cbar=False, cmap='magma', ax=ax1)
        ax1.set_title("Eksik Veri Heatmap", pad=20)

        # Çubuk Grafik
        missing = self.df.isnull().sum().sort_values(ascending=False)
        missing = missing[missing > 0]
        sns.barplot(x=missing.values, y=missing.index, ax=ax2, palette="rocket")
        ax2.set_title("Eksik Veri Sayısı", pad=20)
        ax2.set_xlabel("Eksik Kayıt Sayısı")

        plt.tight_layout()
        self._save_plot(fig, save_path)

    # 2. Korelasyon Matrisi
    def plot_correlation_matrix(self, save_path: Optional[str] = None, 
                             annot_kws: dict = {"size": 8}) -> None:
        """Dinamik thresholdlu korelasyon matrisi"""
        corr = self.df.corr(numeric_only=True)
        mask = np.triu(np.ones_like(corr, dtype=bool))

        plt.figure(figsize=(14, 10))
        heatmap = sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            annot_kws=annot_kws,
            vmin=-1, vmax=1,
            linewidths=0.5
        )
        plt.title("Özellik Korelasyon Matrisi\n(Üst Üçgen Filtreli)", pad=20)
        self._save_plot(heatmap.figure, save_path)

    # 3. Dağılım Grafikleri
    def plot_distribution(self, column: str, save_path: Optional[str] = None, 
                         hue: Optional[str] = None, kde: bool = True) -> None:
        """Dağılım grafiği + Boxplot kombinasyonu"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6),
            gridspec_kw={'width_ratios': [3, 1]})

        # Histogram + KDE
        sns.histplot(
            data=self.df, x=column, hue=hue,
            kde=kde, ax=ax1, palette="viridis",
            edgecolor="black", linewidth=0.5
        )
        ax1.set_title(f"{column} Dağılımı", pad=15)

        # Boxplot
        sns.boxplot(
            data=self.df, y=column, ax=ax2,
            color="skyblue", width=0.3,
            showfliers=True
        )
        ax2.set_title("Boxplot", pad=15)

        plt.tight_layout()
        self._save_plot(fig, save_path)

    # 4. Scatter Plot
    def plot_scatter(self, x_col: str, y_col: str,
               save_path: Optional[str] = None,
               hue: Optional[str] = None,
               size: Optional[str] = None,
               trendline: bool = True) -> None:
        """Regresyon çizgili ve boyutlandırmalı scatter plot"""
        plt.figure(figsize=(10, 8))
        
        sns.scatterplot(
            data=self.df,
            x=x_col, y=y_col,
            hue=hue, size=size,
            palette="Set2",
            alpha=0.7,
            edgecolor="black"
        )

        if trendline:
            sns.regplot(
                data=self.df, x=x_col, y=y_col,
                scatter=False, ci=95,
                line_kws={"color": "darkred", "linewidth": 2, "linestyle": "--"}
            )

        plt.title(f"{x_col} vs {y_col} İlişkisi", pad=20)
        
        if hue is not None:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
        self._save_plot(plt.gcf(), save_path)

    # 5. Çoklu Pairplot
    def plot_pairplot(self, columns: List[str],
                     save_path: Optional[str] = None,
                     diag_kind: str = "kde") -> None:
        """Özelleştirilmiş pairplot"""
        pairplot = sns.pairplot(
            self.df[columns],
            diag_kind=diag_kind,
            plot_kws={"alpha": 0.8, "edgecolor": "black"},
            diag_kws={"fill": True, "alpha": 0.7},
            corner=True
        )
        pairplot.fig.suptitle("Özellikler Arası İlişkiler", y=1.02)
        self._save_plot(pairplot.figure, save_path)

    # 6. Interaktif Plotly Grafiği
    def plot_interactive_scatter(self, x_col: str, y_col: str,
                              color_col: Optional[str] = None,
                              output_path: str = "visuals/interactive_plot.html"):
        """HTML olarak kaydedilebilen interaktif grafik"""
        fig = px.scatter(
            self.df, x=x_col, y=y_col, color=color_col,
            hover_data=self.df.columns,
            title=f"{x_col} vs {y_col} - Interaktif Grafik",
            width=1000, height=600
        )
        fig.write_html(output_path)
        print(f"✅ Interaktif grafik kaydedildi: {output_path}")
        return fig

    # 7. Tüm Grafikleri Otomatik Oluşturma
    def generate_all_visuals(self, output_dir: str = "visuals"):
        """Tüm temel grafikleri otomatik oluşturur ve kaydeder"""
        visuals = {
            "missing_data.png": lambda: self.plot_missing_data(f"{output_dir}/missing_data.png"),
            "correlation_matrix.png": lambda: self.plot_correlation_matrix(f"{output_dir}/correlation_matrix.png"),
            "medv_distribution.png": lambda: self.plot_distribution("MEDV", f"{output_dir}/medv_distribution.png"),
            "rm_medv_scatter.png": lambda: self.plot_scatter("RM", "MEDV", f"{output_dir}/rm_medv_scatter.png"),
            "interactive_plot.html": lambda: self.plot_interactive_scatter("RM", "MEDV", output_path=f"{output_dir}/interactive_plot.html")
        }

        os.makedirs(output_dir, exist_ok=True)
        for name, func in visuals.items():
            try:
                func()
            except Exception as e:
                print(f"❌ {name} oluşturulurken hata: {str(e)}")

    # visualizer.py'ye eklenmesi gereken yeni fonksiyon
    def plot_boxplot(self, column: str, save_path: Optional[str] = None):
        """Tek bir sütun için boxplot çizer"""
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.df, y=column, color="skyblue")
        plt.title(f"{column} Boxplot Dağılımı", pad=15)
        self._save_plot(plt.gcf(), save_path)