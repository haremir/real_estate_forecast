"""
Rapor oluşturma için yardımcı fonksiyonlar.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def check_path_exists(path, create_if_not_exists=False):
    """
    Bir dosya yolunun varlığını kontrol eder
    
    Args:
        path (str): Kontrol edilecek yol
        create_if_not_exists (bool): True ise ve klasör yoksa oluşturur
        
    Returns:
        bool: Yol varsa True, yoksa False
    """
    if os.path.exists(path):
        return True
    elif create_if_not_exists and not os.path.isfile(path):
        os.makedirs(path, exist_ok=True)
        return True
    return False

def get_image_files(directory, extensions=('.png', '.jpg', '.jpeg')):
    """
    Belirtilen dizinden resim dosyalarını listeler
    
    Args:
        directory (str): Resim dosyalarının bulunduğu dizin
        extensions (tuple): Resim uzantıları
        
    Returns:
        list: Resim dosyası yollarının listesi
    """
    if not os.path.exists(directory):
        return []
        
    image_files = []
    for file in os.listdir(directory):
        if file.lower().endswith(extensions):
            image_files.append(os.path.join(directory, file))
    return image_files

def format_dataframe_summary(df):
    """
    DataFrame'in özet istatistiklerini biçimlendirilmiş metin olarak döndürür
    
    Args:
        df (pd.DataFrame): İstatistikleri hesaplanacak DataFrame
        
    Returns:
        str: Biçimlendirilmiş özet metin
    """
    stats = df.describe().round(2)
    stats_text = ""
    for col in stats.columns:
        stats_text += f"Özellik: {col}\n"
        for stat, value in stats[col].items():
            stats_text += f"   {stat}: {value}\n"
        stats_text += "\n"
    return stats_text

def load_image(image_path):
    """
    Bir resim dosyasını yükler
    
    Args:
        image_path (str): Resim dosyasının yolu
        
    Returns:
        numpy.ndarray: Yüklenen resim
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Resim bulunamadı: {image_path}")
    return mpimg.imread(image_path)