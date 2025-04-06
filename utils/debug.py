import pandas as pd
import numpy as np

# Test verisini oluştur
sample_data = pd.DataFrame({
    'CRIM': [0.1, 0.2, np.nan, 0.4],
    'MEDV': [30, 50, 1000, 40],
    'CHAS': [0, 1, 0, 0]
})

print("Başlangıç verisi:")
print(sample_data)
print("\nMEDV sütunu değerleri:", sample_data['MEDV'].values)
print("MEDV ortalama:", sample_data['MEDV'].mean())
print("MEDV standart sapma:", sample_data['MEDV'].std())

# NaN değerin sorun oluşturup oluşturmadığını kontrol et
print("\nNaN değerleri var mı?", sample_data.isna().any().any())

# Z-skorlarını manuel hesapla
mean_val = sample_data['MEDV'].mean()
std_val = sample_data['MEDV'].std()
z_scores = np.abs((sample_data['MEDV'] - mean_val) / std_val)
print("\nZ-skorları:")
print(z_scores)

# Threshold değeriyle filtreleme sonucu
threshold = 3.0
filtered = sample_data[z_scores < threshold]
print("\nFiltrelenmiş veri (z_scores < 3.0):")
print(filtered)
print("Filtreleme sonrası satır sayısı:", len(filtered))