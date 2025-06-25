import numpy as np

# Tehlikeli kimyasalların isimlerini döndür.
# Input: DataFrame
# Output: Series (Chemical isimleri)
def get_hazardous_chemicals(df):
    return df[df['IsHazardous'] == True]['Chemical']


# Tüm "Amount" değerlerini grama çevir. (1 liter = 1000 gram, 1 kg = 1000 gram)
# Input: DataFrame
# Output: Yeni DataFrame, "Amount" sütunu gram cinsinden.
def convert_amounts_to_grams(df):
    df['Amount'] = df.apply(lambda i: i['Amount'] * 1000 if (i['Unit'] == 'liter') or (i['Unit'] == 'kg') else i['Amount'], axis=1)
    df['Unit'] = 'gram'
    return df


# Miktarı en fazla olan n kimyasalı döndür (gram cinsinden sıralı).
# Input: DataFrame, n=2
# Output: En fazla miktarda 2 kimyasal.
def get_top_n_chemicals(df, n):
    df = convert_amounts_to_grams(df)
    df_sorted = df.sort_values(by='Amount', ascending=False)
    return df_sorted.head(n)


# Kullanılan birimlerin listesini döndür ("liter", "kg" vb.)
# Input: DataFrame
# Output: Series ya da list
def get_unique_units(df):
    return df['Unit'].unique().tolist()


# İsim içerisinde keyword geçen kimyasalları filtrele.
# Input: keyword="Acetone"
# Output: "Acetone" içeren satırları içeren DataFrame
def filter_chemicals_by_name(df, keyword):
    keyword_chemicals = []
    keyword_lower = keyword.lower()
    for chemical in df['Chemical']:
        if keyword_lower in chemical.lower():
            keyword_chemicals.append(chemical)
    return df[df['Chemical'].isin(keyword_chemicals)]


# Toplam madde miktarını gram cinsinden hesapla.
# Output: float
def get_total_amount(df):
    df = convert_amounts_to_grams(df)
    return df['Amount'].sum()


# NumPy kullanarak miktarların standart sapmasını hesapla.
# Output: float
def calculate_standard_deviation(df):
    df = convert_amounts_to_grams(df)
    return np.std(df['Amount'])


# Miktarları min-max normalize et.
# (formül: (x - min) / (max - min))
# Output: Series (normalize edilmiş değerler)
def normalize_amounts(df):
    df = convert_amounts_to_grams(df)
    min_amount = df['Amount'].min()
    max_amount = df['Amount'].max()
    normalized = (df['Amount'] - min_amount) / (max_amount - min_amount)
    return normalized


# Tehlikeli olup miktarı 1000 gramdan fazla olanları "HighRisk" olarak işaretle.
# Output: Yeni DataFrame, HighRisk adında yeni sütun içerir.
def flag_high_risk(df):
    df = convert_amounts_to_grams(df)
    df['HighRisk'] = df.apply(lambda i: True if (i['IsHazardous'] == True) and (i['Amount'] > 1000) else False, axis=1)
    return df
    