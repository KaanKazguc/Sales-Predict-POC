import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("SERVER_NAME")
database = 'market'

conn_str = f'''
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={server};
    DATABASE={database};
    Trusted_Connection=yes;
'''

def birliktelik_analizi(sorgulananDeger: int) -> pd.DataFrame:

    conn = pyodbc.connect(conn_str)

    # Sorgulanan değerin CATEGORY_3_ID'sini al
    target_query = "SELECT CATEGORY_3_ID FROM urunler WHERE ID = ?"
    target_category = pd.read_sql(target_query, conn, params=[sorgulananDeger])['CATEGORY_3_ID'][0]

    # Satış detayları ve ürün kategorilerini içeren veri
    query = """
        SELECT CATEGORY_3_ID, FICHENO
        FROM Satis_detay
        JOIN urunler ON urunler.ID = Satis_detay.ITEMCODE
    """
    df = pd.read_sql(query, conn)
    transactions = df.groupby('FICHENO')['CATEGORY_3_ID'].apply(set)

    # Tüm kategoriler
    categories = df['CATEGORY_3_ID'].unique()

    # Confidence ve birlikte satılma sayısı hesaplama
    results = []

    for category in categories:
        if category == target_category:
            continue

        # Seçili kategori ve diğer kategori birliktelikleri
        count_both = sum([target_category in trans and category in trans for trans in transactions])
        count_target = sum([target_category in trans for trans in transactions])

        # Confidence hesaplama
        confidence = count_both / count_target if count_target > 0 else 0
        results.append((category, count_both, confidence))


    results_df = pd.DataFrame(results, columns=['CATEGORY3ID', 'BirliktelikAdet', 'BirliktelikOran'])
    results_df = results_df.sort_values('BirliktelikAdet', ascending=False)

    # Kategori isimlerini almak için sorgu
    ad_query = """
        SELECT ucuncuKategoriler.ID AS CATEGORY3ID, CATEGORY_NAME3, CATEGORY_NAME2
        FROM ucuncuKategoriler
        JOIN ikinciKategoriler ON ucuncuKategoriler.CATEGORY_2_ID = ikinciKategoriler.ID
    """
    adif = pd.read_sql(ad_query, conn)
    conn.close()


    result_df = pd.merge(adif, results_df, on="CATEGORY3ID").sort_values('BirliktelikAdet', ascending=False)

    return result_df
