import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

def load_data(file_path):
    """
    Veri setini yükler ve gerekli ön işlemeleri yapar
    """
    df = pd.read_csv(file_path)
    return df

def create_invoice_product_matrix(df):
    """
    Sepet-ürün matrisi oluşturur
    """
    # ServiceID ve CategoryID'leri birleştirerek yeni bir hizmet ID oluştur
    df['service'] = df['ServiceId'].astype(str) + '_' + df['CategoryId'].astype(str)
    
    # Invoice-Product matrisini oluştur
    return df.groupby(['UserId', 'service']).size().unstack().fillna(0).astype(int)

def generate_rules(basket_matrix, min_support=0.01, min_confidence=0.1):
    """
    Association rules oluşturur
    """
    # Binary matrix oluştur (1: hizmet alındı, 0: hizmet alınmadı)
    basket_matrix = basket_matrix.applymap(lambda x: 1 if x > 0 else 0)
    
    # Apriori algoritması ile frequent itemsetleri bul
    frequent_itemsets = apriori(basket_matrix, 
                              min_support=min_support,
                              use_colnames=True)
    
    # Association rules oluştur
    rules = association_rules(frequent_itemsets,
                            metric="confidence",
                            min_threshold=min_confidence)
    
    # Lift değerine göre sırala
    rules = rules.sort_values('lift', ascending=False)
    return rules

def get_service_recommendations(rules_df, service_id, top_n=5, min_confidence=0.1, min_lift=1):
    """
    Belirli bir hizmet için öneriler üretir
    """
    # Verilen hizmeti içeren kuralları filtrele
    service_rules = rules_df[rules_df['antecedents'].apply(lambda x: service_id in x)]
    
    # Minimum confidence ve lift değerlerine göre filtrele
    service_rules = service_rules[
        (service_rules['confidence'] >= min_confidence) &
        (service_rules['lift'] >= min_lift)
    ]
    
    # Top N öneriyi döndür
    recommendations = service_rules.nlargest(top_n, 'lift')
    return recommendations

def get_category_based_recommendations(df, rules_df, category_id, top_n=5):
    """
    Belirli bir kategori için en iyi hizmet önerilerini üretir
    """
    # Kategori içindeki hizmetleri bul
    category_services = df[df['CategoryId'] == category_id]['ServiceId'].unique()
    
    # Bu kategorideki hizmetleri içeren kuralları filtrele
    category_rules = rules_df[
        rules_df['antecedents'].apply(lambda x: any(f"{service}_" in str(item) for service in category_services for item in x))
    ]
    
    # En iyi önerileri döndür
    recommendations = category_rules.nlargest(top_n, 'lift')
    return recommendations

def get_seasonal_recommendations(df, rules_df, current_month, top_n=5):
    """
    Mevsimsel faktörleri göz önünde bulundurarak öneriler üretir
    """
    if 'CreateDate' not in df.columns:
        return None
        
    # Verilen ay için popüler hizmetleri bul
    df['month'] = pd.to_datetime(df['CreateDate']).dt.month
    monthly_popular = df[df['month'] == current_month]['service'].value_counts().head(top_n)
    
    # Bu hizmetler için association rules'ları filtrele
    seasonal_rules = rules_df[
        rules_df['antecedents'].apply(lambda x: any(service in x for service in monthly_popular.index))
    ]
    
    return seasonal_rules.nlargest(top_n, 'lift')

def get_user_based_recommendations(df, rules_df, user_id, top_n=5):
    """
    Kullanıcının geçmiş davranışlarına göre öneriler üretir
    """
    # Kullanıcının aldığı hizmetleri bul
    user_services = df[df['UserId'] == user_id]['service'].unique()
    
    if len(user_services) == 0:
        return None
    
    # Kullanıcının aldığı hizmetlere benzer hizmetleri bul
    user_recommendations = pd.DataFrame()
    
    for service in user_services:
        service_rules = rules_df[rules_df['antecedents'].apply(lambda x: service in x)]
        user_recommendations = pd.concat([user_recommendations, service_rules])
    
    # Tekrar eden önerileri kaldır ve en iyi N öneriyi döndür
    user_recommendations = user_recommendations.drop_duplicates(subset=['consequents'])
    return user_recommendations.nlargest(top_n, 'lift')

def get_bundle_recommendations(rules_df, min_confidence=0.3, min_lift=2, max_bundle_size=3):
    """
    Paket halinde sunulabilecek hizmet gruplarını önerir
    """
    # Yüksek güven ve lift değerine sahip kuralları filtrele
    bundle_rules = rules_df[
        (rules_df['confidence'] >= min_confidence) &
        (rules_df['lift'] >= min_lift)
    ]
    
    # Her kural için bundle oluştur
    bundles = []
    for _, rule in bundle_rules.iterrows():
        antecedents = list(rule['antecedents'])
        consequents = list(rule['consequents'])
        
        # Bundle boyutunu kontrol et
        if len(antecedents) + len(consequents) <= max_bundle_size:
            bundle = {
                'services': antecedents + consequents,
                'confidence': rule['confidence'],
                'lift': rule['lift']
            }
            bundles.append(bundle)
    
    return bundles

def visualize_service_network(rules_df, min_lift=1, max_connections=50):
    """
    Hizmetler arası ilişkileri ağ grafiği olarak görselleştirir
    """
    # Lift değeri yüksek olan ilişkileri filtrele
    important_rules = rules_df[rules_df['lift'] >= min_lift].head(max_connections)
    
    # Ağ grafiği oluştur
    G = nx.Graph()
    
    for _, row in important_rules.iterrows():
        antecedent = list(row['antecedents'])[0]
        consequent = list(row['consequents'])[0]
        lift = row['lift']
        
        G.add_edge(antecedent, consequent, weight=lift)
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Düğümleri çiz
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    plt.title("Hizmetler Arası İlişki Ağı")
    plt.axis('off')
    plt.show()

def analyze_service_patterns(df):
    """
    Hizmet kullanım örüntülerini analiz eder ve iş öngörüleri sunar
    """
    # Hizmet kullanım sıklıkları
    service_freq = df.groupby(['ServiceId', 'CategoryId']).size().reset_index(name='frequency')
    service_freq = service_freq.sort_values('frequency', ascending=False)
    
    # Mevsimsel analiz (eğer CreateDate varsa)
    if 'CreateDate' in df.columns:
        df['CreateDate'] = pd.to_datetime(df['CreateDate'])
        df['month'] = df['CreateDate'].dt.month
        seasonal_patterns = df.groupby(['month', 'ServiceId']).size().unstack()
        
        plt.figure(figsize=(15, 6))
        sns.heatmap(seasonal_patterns, cmap='YlOrRd')
        plt.title('Hizmetlerin Aylara Göre Kullanımı')
        plt.show()
    
    # En sık birlikte alınan hizmetler
    print("\nEn Popüler Hizmetler:")
    print(service_freq.head().to_string())
    
    return service_freq

def generate_business_insights(df, rules_df):
    """
    İş öngörüleri ve tavsiyeleri oluşturur
    """
    insights = []
    
    # 1. Yüksek lift değerine sahip ilişkileri analiz et
    high_lift_rules = rules_df[rules_df['lift'] > 2].sort_values('confidence', ascending=False)
    
    if not high_lift_rules.empty:
        insights.append("\n1. Güçlü Hizmet İlişkileri:")
        for _, rule in high_lift_rules.head().iterrows():
            ant = list(rule['antecedents'])[0]
            cons = list(rule['consequents'])[0]
            insights.append(f"- {ant} hizmeti alan müşteriler {cons} hizmetini alma eğiliminde (Lift: {rule['lift']:.2f})")
    
    # 2. Düşük destek ama yüksek güven oranına sahip fırsatları belirle
    opportunity_rules = rules_df[(rules_df['support'] < 0.05) & (rules_df['confidence'] > 0.5)]
    
    if not opportunity_rules.empty:
        insights.append("\n2. Potansiyel Fırsatlar:")
        for _, rule in opportunity_rules.head().iterrows():
            ant = list(rule['antecedents'])[0]
            cons = list(rule['consequents'])[0]
            insights.append(f"- {ant} hizmeti için {cons} hizmeti potansiyel çapraz satış fırsatı olabilir")
    
    # 3. Hizmet kullanım yoğunluğu analizi
    service_counts = df['ServiceId'].value_counts()
    insights.append("\n3. Hizmet Kullanım Analizi:")
    insights.append(f"- En çok kullanılan hizmet: {service_counts.index[0]}")
    insights.append(f"- En az kullanılan hizmet: {service_counts.index[-1]}")
    
    return "\n".join(insights)

def main():
    # Veri setini yükle
    df = load_data('armut_data.csv')
    
    # Sepet matrisini oluştur
    basket_matrix = create_invoice_product_matrix(df)
    
    # Association rules'ları oluştur
    rules = generate_rules(basket_matrix)
    
    # Hizmet örüntülerini analiz et
    print("\nHizmet Kullanım Analizi:")
    service_patterns = analyze_service_patterns(df)
    
    # İş öngörüleri oluştur
    print("\nİş Öngörüleri ve Tavsiyeler:")
    insights = generate_business_insights(df, rules)
    print(insights)
    
    # İlişki ağını görselleştir
    print("\nHizmetler Arası İlişki Ağı Görselleştiriliyor...")
    visualize_service_network(rules)
    
    # Farklı türde öneriler oluştur
    print("\nÖrnek Öneriler:")
    
    # 1. Genel hizmet önerileri
    sample_service = basket_matrix.columns[0]
    print("\n1. Genel Hizmet Önerileri:")
    recommendations = get_service_recommendations(rules, sample_service)
    print(recommendations[['consequents', 'confidence', 'lift']])
    
    # 2. Kategori bazlı öneriler (örnek kategori ID)
    if 'CategoryId' in df.columns:
        sample_category = df['CategoryId'].iloc[0]
        print("\n2. Kategori Bazlı Öneriler:")
        category_recommendations = get_category_based_recommendations(df, rules, sample_category)
        print(category_recommendations[['consequents', 'confidence', 'lift']])
    
    # 3. Mevsimsel öneriler (eğer tarih verisi varsa)
    if 'CreateDate' in df.columns:
        current_month = pd.Timestamp.now().month
        print(f"\n3. {current_month}. Ay için Mevsimsel Öneriler:")
        seasonal_recommendations = get_seasonal_recommendations(df, rules, current_month)
        if seasonal_recommendations is not None:
            print(seasonal_recommendations[['consequents', 'confidence', 'lift']])
    
    # 4. Paket önerileri
    print("\n4. Paket Hizmet Önerileri:")
    bundles = get_bundle_recommendations(rules)
    for i, bundle in enumerate(bundles[:5], 1):
        print(f"\nPaket {i}:")
        print(f"Hizmetler: {bundle['services']}")
        print(f"Güven: {bundle['confidence']:.2f}")
        print(f"Lift: {bundle['lift']:.2f}")

if __name__ == "__main__":
    main() 