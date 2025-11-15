import pandas as pd
import numpy as np
import pyodbc
import torch
import pickle
from karlilik import MarketSalesModel, predict_sales
from dotenv import load_dotenv
import os


def karlilik_hesapla(girdiEnlem, girdiBoylam, girdiAlan, tahminiKira):
    load_dotenv()

    # SQL bağlantısı
    conn_str = f'
        DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER= '+ os.getenv("SERVER_NAME") +' ; \
        DATABASE=market; \
        Trusted_Connection=yes;
    '
    conn = pyodbc.connect(conn_str)

    # En yakın marketleri al
    marketler = pd.read_sql("""
        SELECT marketler.MagzaID, adresler.Enlem, adresler.Boylam
        FROM marketler
        JOIN adresler ON marketler.AdresID = adresler.ID
    """, conn)

    def haversine_metre(lat1, lon1, lat2, lon2):
        R = 6371000
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi / 2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))
        return round(R * c, 0)

    marketler['mesafe_metre'] = marketler.apply(lambda row: haversine_metre(girdiEnlem, girdiBoylam, row['Enlem'], row['Boylam']), axis=1)
    en_yakin_uc = marketler.sort_values('mesafe_metre').head(3).reset_index()

    urunler = pd.read_sql("""
        SELECT urunler.ID as ITEMCODE, urunler.ITEMNAME, ikinciKategoriler.CATEGORY_1_ID as CAT
        FROM urunler
        JOIN ucuncuKategoriler ON ucuncuKategoriler.ID = urunler.CATEGORY_3_ID
        JOIN ikinciKategoriler ON ikinciKategoriler.ID = ucuncuKategoriler.CATEGORY_2_ID
    """, conn)

    satislar = []
    for i in range(3):
        magza_id = en_yakin_uc['MagzaID'][i]
        mesafe = en_yakin_uc['mesafe_metre'][i]
        query = f"""
            SELECT Satis_detay.MagzaID, SUM(AMOUNT) AS ToplamSatis, ITEMCODE, marketler.Alan
            FROM Satis_detay
            JOIN marketler ON marketler.MagzaID = Satis_detay.MagzaID
            WHERE Satis_detay.MagzaID = {magza_id}
            GROUP BY Satis_detay.MagzaID, ITEMCODE, marketler.Alan
        """
        df = pd.read_sql(query, conn)
        df[f'Distance_m{i+1}'] = mesafe
        df = df.rename(columns={
            'MagzaID': f'NearestMarket{i+1}',
            'ToplamSatis': f'ToplamSatis{i+1}',
            'Alan': f'Alan{i+1}'
        })
        satislar.append(df)

    df = urunler.copy()
    for satis_df in satislar:
        df = pd.merge(df, satis_df, on='ITEMCODE', how='left')

    df['MarketID'] = 0
    df['Alan'] = girdiAlan
    df = df.fillna(0)

    tahminler = load_model_and_predict(df)
    results = df[['ITEMCODE']].copy()
    results['Tahmin'] = tahminler
    karlilik = pd.merge(urunler, results, on='ITEMCODE', how='left')

    avgPrice = pd.read_sql("""
        SELECT UrunMarket.ITEMCODE, AVG(PRICE) as avgPRICE
        FROM dbo.UrunMarket
        GROUP BY ITEMCODE
    """, conn)

    conn.close()

    karlilik = pd.merge(karlilik, avgPrice, on='ITEMCODE', how='left')

    marjlar = pd.DataFrame({
        'CAT': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'CatName':['BEBEK','DETERJAN TEMİZLİK','ET TAVUK','EV','GIDA','KAĞIT','KOZMETİK','MEYVE SEBZE','PET','SÜT KAHVALTILIK','SİGARA','İÇECEK'],
        'KarMarji': [0.30, 0.25, 0.15, 0.20, 0.20, 0.25, 0.40, 0.15, 0.35, 0.18, 0.10, 0.28]
    })

    karlilik = pd.merge(karlilik, marjlar, on='CAT', how='left')
    karlilik['TahminiKar'] = karlilik['Tahmin'] * karlilik['avgPRICE'] * karlilik['KarMarji']

    yillikKar = karlilik['TahminiKar'].sum().round()
    sıkSatılanlar = results[results['Tahmin'] > 2400].count()[0]

    if sıkSatılanlar < 2500:
        elemanSayisi = 4
        katalogBuyuklugu = 1
    elif sıkSatılanlar < 5000:
        elemanSayisi = 6
        katalogBuyuklugu = 1.25
    else:
        elemanSayisi = 8
        katalogBuyuklugu = 1.5

    elemanGiderleri = elemanSayisi * 32000
    dukkanMasraflari = 15000 + (katalogBuyuklugu * 5000)
    yillikGider = (tahminiKira + elemanGiderleri + dukkanMasraflari) * 12

    return karlilik, yillikKar, elemanSayisi, dukkanMasraflari


def load_model_and_predict(tahmin_verisi, model_path='market_sales_model_pytorch_no_marketid.pth',
                           scalers_path='scalers_no_marketid.pkl', encoders_path='label_encoders_no_marketid.pkl'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    checkpoint = torch.load(model_path, map_location=device)
    input_dims = checkpoint['input_dims']
    model = MarketSalesModel(input_dims).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    with open(scalers_path, 'rb') as f:
        scalers = pickle.load(f)
    with open(encoders_path, 'rb') as f:
        label_encoders = pickle.load(f)
    predictions = predict_sales(model, tahmin_verisi, scalers, label_encoders, device)
    return predictions

