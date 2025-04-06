# 📊 Boston Housing Veri Ön İşleme Projesi

## 🚀 Proje Amacı
Bu projede, Boston konut veri seti üzerinde makine öğrenimi için veri temizleme ve analiz işlemleri gerçekleştirilmiştir. Amaç, eksik verileri doldurup aykırı değerleri temizleyerek MEDV (ev fiyatları) tahmini için hazır bir veri seti oluşturmaktır.

## 📁 Kullanılan Veri Seti
- **Kaynak**: Scikit-learn kütüphanesi temelli Boston Housing dataseti
- **Özellikler**:
  - Toplam gözlem: 506
  - Kolon sayısı: 14
  - Kritik sütunlar:
    - `MEDV`: Hedef değişken (1000$ cinsinden ortalama ev fiyatı)
    - `LSTAT`: Nüfusun alt sınıf yüzdesi (en güçlü negatif korelasyon: -0.74)
    - `RM`: Konut başına ortalama oda sayısı (en güçlü pozitif korelasyon: 0.60)

## ⚙ Kullanılan Teknolojiler
- Python (pandas, numpy, sklearn, seaborn, matplotlib, plotly)
- Jupyter Notebook
- Scikit-learn IterativeImputer (RandomForest tabanlı eksik veri doldurma)

## 🧠 Uygulanan Yöntemler
1. **Veri Temizleme**:
   - Eksik verilerin RandomForestRegressor ile doldurulması
   - Aykırı değerlerin z-puanı (|z| > 3) ile tespiti
2. **Normalizasyon**: Tüm sayısal sütunların StandardScaler ile standartlaştırılması
3. **Gelişmiş Görselleştirme**:
   - Eksik veri analizi için interaktif heatmap ve çubuk grafikler
   - Dinamik korelasyon matrisi (üst üçgen filtreli)
   - Kombinasyon grafikler (KDE histogram + boxplot)
   - HTML çıktılı interaktif scatter plotlar (Plotly)
   - Çoklu değişken analizi için özelleştirilmiş pairplot

## 🔍 Öğrendiklerim
- IterativeImputer ile model tabanlı eksik veri doldurmanın etkinliği
- Korelasyon analizinde `LSTAT` ve `RM`'in MEDV ile güçlü ilişkisi
- Normalizasyon sonrası veri dağılımlarının nasıl değiştiği
- Plotly ile interaktif görselleştirmelerin raporlama avantajları

## 📌 Sonraki Adımlar
- [ ] `cleaner.py`'a loglama mekanizması eklenmesi
- [ ] Görselleştirmelerin `visualizer.py` modülünden otomatik üretilmesi
- [ ] Otomatik test kapsamının genişletilmesi
- [ ] Makine Öğrenmesi Algoritmaları eklenmesi
- [ ] Streamlit ile interaktif dashboard entegrasyonu

> ⚠ Bu proje şu an **Versiyon 1.0.0** olarak tamamlanmıştır. Geliştirmeler devam edecektir.

---

## 🛠 Kurulum & Çalıştırma
```bash
# Gereksinimlerin yüklenmesi
pip install -r requirements.txt

# Veri temizleme pipeline'ının çalıştırılması
python -m src.data_processing.cleaner
