# Armut.com Hizmet Platformu için Veri Odaklı Öneri Sistemi: Association Rule Learning Analizi

## İçindekiler
1. [Proje Özeti](#proje-özeti)
2. [Teknik Detaylar](#teknik-detaylar)
3. [Veri Analizi ve Bulgular](#veri-analizi-ve-bulgular)
4. [İş Öngörüleri ve Stratejik Öneriler](#iş-öngörüleri-ve-stratejik-öneriler)
5. [Uygulama Yol Haritası](#uygulama-yol-haritası)
6. [Sonuç ve Gelecek Vizyonu](#sonuç-ve-gelecek-vizyonu)

## Proje Özeti

### Genel Bakış
Bu proje, Armut.com'un hizmet platformundaki kullanıcı davranışlarını analiz ederek, veri odaklı bir öneri sistemi geliştirmeyi amaçlamaktadır. Association Rule Learning (ARL) tekniklerini kullanarak hizmetler arası ilişkileri ortaya çıkaran sistem, kişiselleştirilmiş öneriler ve çapraz satış fırsatları sunmaktadır.

### Temel Hedefler
- Kullanıcı deneyimini iyileştirme
- Çapraz satış potansiyelini artırma
- Mevsimsel trendleri belirleme
- Veri odaklı karar mekanizmaları geliştirme
- Hizmet kombinasyonlarını optimize etme

## Teknik Detaylar

### Kullanılan Teknolojiler
```python
# Temel Kütüphaneler
- Python 3.8+
- pandas & numpy: Veri manipülasyonu
- mlxtend: Association Rules analizi
- networkx: Ağ görselleştirmesi
- seaborn & matplotlib: Veri görselleştirme
```

### Metodoloji
1. **Veri Ön İşleme**
   - Kullanıcı-hizmet matrisinin oluşturulması
   - Kategori bazlı segmentasyon
   - Tarihsel analiz için veri hazırlama

2. **ARL Analizi**
   - Apriori algoritması uygulaması
   - Support, Confidence ve Lift metriklerinin hesaplanması
   - Kural filtreleme ve optimizasyon

## Veri Analizi ve Bulgular

### 1. Hizmet Kullanım Analizi

#### 1.1 En Çok Kullanılan Hizmetler
1. **ServiceId: 18 (Kategori 4)**
   - Toplam İşlem: 32,740
   - Platform genelinde en yüksek kullanım oranı
   - Heat map analizine göre yaz aylarında belirgin artış
   - Tüm hizmetler arasında en yüksek mevsimsel etki

2. **ServiceId: 15 (Kategori 1)**
   - Toplam İşlem: 11,348
   - İkinci en yüksek kullanım oranı
   - Yıl boyunca daha dengeli kullanım

3. **ServiceId: 2 (Kategori 0)**
   - Toplam İşlem: 11,326
   - Üçüncü en yüksek kullanım oranı

4. **Diğer Önemli Hizmetler**
   - ServiceId 49 (Kategori 1): 6,690 işlem
   - ServiceId 38 (Kategori 4): 5,604 işlem

### 2. Hizmet İlişki Analizi

#### 2.1 Güçlü Hizmet Kümeleri
Heat map ve ağ analizi sonuçlarına göre:

1. **Birinci Küme (En Güçlü İlişkiler)**
   - Hizmetler: 25_0, 22_0, 29_0, 11_11
   - Yüksek birlikte kullanım oranı
   - Güçlü mevsimsel korelasyon

2. **İkinci Küme**
   - Hizmetler: 40_8, 0_8, 16_8
   - En yüksek lift değeri (7.28)
   - Premium hizmet potansiyeli

3. **Üçüncü Küme**
   - Hizmetler: 41_3, 7_3
   - İzole ancak güçlü ikili ilişki

#### 2.2 Mevsimsel Örüntüler
Heat map analizinden elde edilen bulgular:

1. **Yaz Dönemi (6-8. Aylar)**
   - ServiceId 18'de belirgin artış
   - Kategori 4 hizmetlerinde genel yükseliş

2. **Kış Dönemi (11-1. Aylar)**
   - Daha dengeli hizmet dağılımı
   - Bazı hizmetlerde düşüş trendi

## İş Öngörüleri ve Stratejik Öneriler

### 1. Hizmet Optimizasyonu

#### 1.1 Kapasite Planlaması
- **Yüksek Hacimli Hizmetler (ServiceId: 18)**
  - Yaz ayları için %30 kapasite artırımı
  - Peak sezonlarda ek hizmet sağlayıcı planlaması
  - Dinamik fiyatlandırma stratejisi

- **Orta Hacimli Hizmetler (ServiceId: 15, 2)**
  - Yıl boyu dengeli kapasite planlaması
  - Çapraz satış fırsatları için optimizasyon

#### 1.2 Paket Önerileri
1. **Premium Paket (Lift: 7.28)**
   - Hizmetler: 16_8 ve 0_8
   - Yüksek güven oranı: 0.31
   - Özel fiyatlandırma potansiyeli

2. **Kategori-0 Paketi (Lift: 4.84)**
   - Hizmetler: 29_0, 22_0, 25_0
   - Güven oranı: 0.52
   - Mevsimsel paket potansiyeli

### 2. Platform İyileştirmeleri

#### 2.1 Kullanıcı Arayüzü
1. **Dinamik Öneri Sistemi**
   - Mevsime göre özelleştirilmiş öneriler
   - Kullanıcı geçmişine dayalı kişiselleştirme
   - Paket hizmet görünürlüğü

2. **Hizmet Keşif Özellikleri**
   - İlişkili hizmet önerileri
   - Popüler kombinasyonlar
   - Mevsimsel özel teklifler

## Uygulama Yol Haritası

### Faz 1: Temel Optimizasyonlar (1-3 Ay)
- Mevsimsel kapasite planlaması
- Temel öneri sistemi entegrasyonu
- A/B test altyapısı

### Faz 2: İleri Analizler (3-6 Ay)
- Dinamik fiyatlandırma sistemi
- Gelişmiş paket önerileri
- Kullanıcı segmentasyonu

### Faz 3: Yapay Zeka Entegrasyonu (6-12 Ay)
- Gerçek zamanlı öneri sistemi
- Otomatik kapasite optimizasyonu
- Tahmine dayalı planlama

## Sonuç ve Beklenen Etkiler

Veri analizine dayalı bu sistemin beklenen etkileri:
- Yüksek hacimli hizmetlerde (ServiceId 18) %25 kapasite optimizasyonu
- Çapraz satış oranlarında %20-25 artış
- Mevsimsel dalgalanmalarda %30 daha iyi planlama
- Kullanıcı memnuniyetinde %15 artış

### Gelecek Adımlar
1. Derin öğrenme tabanlı öneri sistemi
2. Gerçek zamanlı kapasite optimizasyonu
3. Otomatik fiyatlandırma algoritmaları
4. Gelişmiş kullanıcı segmentasyonu

## Referanslar
1. Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules.
2. Han, J., Pei, J., & Kamber, M. (2011). Data mining: concepts and techniques.
3. Armut.com API Documentation
4. Python mlxtend Documentation 