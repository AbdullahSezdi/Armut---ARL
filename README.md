# Armut ARL (Association Rule Learning) Öneri Sistemi

## Proje Hakkında

Bu proje, Türkiye'nin önde gelen hizmet platformu Armut.com için geliştirilmiş bir öneri sistemi çalışmasıdır. Association Rule Learning (ARL) tekniklerini kullanarak kullanıcı davranışlarını analiz eden sistem, kişiselleştirilmiş hizmet önerileri ve çapraz satış fırsatları sunmaktadır.

### Amaç
- Kullanıcılara kişiselleştirilmiş hizmet önerileri sunmak
- Hizmetler arası ilişkileri keşfetmek
- Mevsimsel trendleri analiz etmek
- Çapraz satış fırsatlarını belirlemek
- Platform verimliliğini artırmak

## Veri Seti

Kullanılan veri seti şu özelliklere sahiptir:
- **UserId**: Müşteri numarası
- **ServiceId**: Hizmet numarası (0-49 arası)
- **CategoryId**: Kategori numarası
- **CreateDate**: Hizmet alım tarihi

### Veri Seti İstatistikleri
- En yüksek işlem hacmine sahip hizmet: ServiceId 18 (32,740 işlem)
- İkinci en popüler hizmet: ServiceId 15 (11,348 işlem)
- Üçüncü en popüler hizmet: ServiceId 2 (11,326 işlem)

## Metodoloji

### 1. Veri Ön İşleme
- Kullanıcı-hizmet matrisinin oluşturulması
- Kategori bazlı segmentasyon
- Tarihsel analiz için veri hazırlama

### 2. Association Rule Learning
- Apriori algoritması uygulaması
- Support, Confidence ve Lift metriklerinin hesaplanması
- Kural filtreleme ve optimizasyon

### 3. Görselleştirme
- Hizmetler arası ilişki ağı
- Mevsimsel kullanım heat map'i
- Kategori bazlı analiz grafikleri

## Temel Bulgular

### 1. Hizmet Kümeleri
1. **Birinci Küme**
   - Hizmetler: 25_0, 22_0, 29_0, 11_11
   - Özellik: Yüksek birlikte kullanım

2. **İkinci Küme**
   - Hizmetler: 40_8, 0_8, 16_8
   - Özellik: En yüksek lift değeri (7.28)

3. **Üçüncü Küme**
   - Hizmetler: 41_3, 7_3
   - Özellik: İzole ancak güçlü ikili ilişki

### 2. Mevsimsel Trendler
- **Yaz Dönemi (6-8. Aylar)**
  - ServiceId 18'de belirgin artış
  - Kategori 4 hizmetlerinde yükseliş

- **Kış Dönemi (11-1. Aylar)**
  - Daha dengeli hizmet dağılımı
  - Bazı hizmetlerde düşüş trendi

### 3. Önerilen Paketler
1. **Premium Paket**
   - Hizmetler: 16_8 ve 0_8
   - Lift: 7.28
   - Güven: 0.31

2. **Kategori-0 Paketi**
   - Hizmetler: 29_0, 22_0, 25_0
   - Lift: 4.84
   - Güven: 0.52

## Kurulum ve Kullanım

### Gereksinimler
```bash
pandas==2.0.3
numpy==1.24.3
mlxtend==0.22.0
scikit-learn==1.3.0
seaborn==0.12.2
matplotlib==3.7.1
networkx==3.1
```

### Kurulum
1. Repository'yi klonlayın:
```bash
git clone https://github.com/AbdullahSezdi/Armut---ARL.git
cd Armut---ARL
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

### Kullanım
```bash
python armut_arl.py
```

## Proje Yapısı

```
Armut---ARL/
│
├── armut_arl.py           # Ana kod dosyası
├── armut_data.csv         # Veri seti
├── armut_arl_analysis.md  # Detaylı analiz raporu
├── requirements.txt       # Gerekli Python kütüphaneleri
├── LICENSE               # MIT lisans dosyası
└── README.md            # Proje dokümantasyonu
```

## Analiz Sonuçları

Detaylı analiz sonuçları ve görselleştirmeler için [armut_arl_analysis.md](armut_arl_analysis.md) dosyasını inceleyebilirsiniz.

### Önemli Metrikler
- Yüksek hacimli hizmetlerde %25 kapasite optimizasyonu
- Çapraz satış oranlarında %20-25 artış potansiyeli
- Mevsimsel dalgalanmalarda %30 daha iyi planlama imkanı

