# tests/test_visualizer.py
import pytest
import pandas as pd
import os

"""
BU KOD KISMI DOSYA BULAMAMA PROBLEMİNİ ÇÖZÜYOR
"""
#-----------------------------------------

os.chdir(r"C:\Users\emirh\Desktop\mart3")  # Ana proje dizinine geç
print(os.getcwd())  # Doğru olduğuna emin ol
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join('..', 'src')))  # src klasörünü ekle

#-----------------------------------------

import logging
from pathlib import Path
import sys

# Log ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_visualizer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Proje yolunu ekle
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from src.data_processing.visualizer import BostonVisualizer

@pytest.fixture(scope="module")
def sample_data():
    """Test verisi fixture'ı"""
    data = {
        'price': [500, 350, None, 750, 900],
        'rooms': [3, None, 4, 5, 4],
        'age': [10, 20, 30, 20, None],
        'location': ['A', 'B', 'A', 'C', 'B']
    }
    logger.info("Test verisi oluşturuldu")
    return pd.DataFrame(data)

def test_advanced_missing_data_plot(sample_data, tmp_path):
    """Eksik veri grafiği testi"""
    save_path = os.path.join(tmp_path, "advanced_missing.png")
    visualizer = BostonVisualizer(sample_data)
    
    logger.info(f"Eksik veri grafiği oluşturuluyor: {save_path}")
    visualizer.plot_missing_data(save_path=save_path)
    
    assert os.path.exists(save_path)
    logger.info(f"Grafik başarıyla kaydedildi: {os.path.getsize(save_path)} bytes")

def test_interactive_plot(sample_data, tmp_path):
    """Interaktif grafik testi"""
    output_path = os.path.join(tmp_path, "interactive_plot.html")
    visualizer = BostonVisualizer(sample_data.dropna())
    
    logger.info(f"Interaktif grafik oluşturuluyor: {output_path}")
    fig = visualizer.plot_interactive_scatter(
        x_col="rooms", y_col="price",
        color_col="location",
        output_path=output_path
    )
    
    assert os.path.exists(output_path)
    logger.info(f"HTML çıktısı oluşturuldu: {os.path.getsize(output_path)} bytes")
    assert fig.layout.title.text == "rooms vs price - Interaktif Grafik"

def test_distribution_plot_with_hue(sample_data, tmp_path):
    """Dağılım grafiği testi (hue ile)"""
    save_path = os.path.join(tmp_path, "dist_with_hue.png")
    visualizer = BostonVisualizer(sample_data.dropna())
    
    logger.info(f"Dağılım grafiği oluşturuluyor (hue kullanarak): {save_path}")
    visualizer.plot_distribution(
        column="price",
        hue="location",
        save_path=save_path
    )
    
    assert os.path.exists(save_path)
    logger.info(f"Grafik başarıyla kaydedildi: {os.path.getsize(save_path)} bytes")

# Test sonu raporu
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    logger.info("\n\n=== TEST SONUÇ ÖZETİ ===")
    logger.info(f"Toplam test sayısı: {session.testscollected}")
    logger.info(f"Geçen testler: {session.testscollected - session.testsfailed}")
    logger.info(f"Başarısız testler: {session.testsfailed}")