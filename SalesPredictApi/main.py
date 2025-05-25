from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd


from karlilik_module import karlilik_hesapla
from birliktelik_module import birliktelik_analizi

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    girdiEnlem: float
    girdiBoylam: float
    girdiAlan: float
    tahminiKira: float

class OutputData(BaseModel):
    elemanSayisi: int
    dukkanMasraflari: float
    yillikKar: float
    karlilik: List[Dict[str, Any]]

class BirliktelikInput(BaseModel):
    ITEMCODE: int

@app.post("/tahmin", response_model=OutputData)
def tahmin_et(input: InputData):
    karlilik_df, yillikKar, elemanSayisi, dukkanMasraflari = karlilik_hesapla(
        input.girdiEnlem,
        input.girdiBoylam,
        input.girdiAlan,
        input.tahminiKira
    )

    karlilik_json = karlilik_df.to_dict(orient="records")

    return OutputData(
        elemanSayisi=elemanSayisi,
        dukkanMasraflari=dukkanMasraflari,
        yillikKar=yillikKar,
        karlilik=karlilik_json
    )

@app.post("/birliktelik")
def birliktelik(input: BirliktelikInput):
    df = birliktelik_analizi(input.ITEMCODE)
    return df.to_dict(orient="records")
