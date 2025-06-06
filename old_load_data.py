from helix import Payload, Client, Query
from typing import List, Any
import pandas as pd

class insert_patient(Query):
    def __init__(self, data: List[Any]):
        super().__init__()
        self.data = data

    def query(self) -> List[Payload]:
        return [{
            "n_Name": self.data[0],
            "n_Alter": self.data[1],
            "n_Geschlecht": self.data[2],
            "n_AktuelleKrebserkrankung": self.data[3],
            "n_Alkoholkonsum": self.data[4],
            "n_Raucher": self.data[5],
            "n_VitalBMI": self.data[6],
            "n_BerufDerzeit": self.data[7],
            "n_WohnsituationSonstiges": self.data[8],
            "n_Diagnose": self.data[9],
            "n_AnamneseAllgemein": self.data[10],
            "n_JetzigeBeschwerden": self.data[11],
            "n_RehaSpezifischeAnamnese": self.data[12],
            "n_Aufenthaltsdauer": self.data[13],
            "n_Indikation": self.data[14],
            "n_Leistungskategorie": self.data[15],
            "n_Aufenthaltstyp": self.data[16],
            "n_Teilhabeziel": self.data[17],
            }]

    def response(self, response): return response

def get_data(csv_file: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file, sep=';', encoding='latin1')
    print(df.head())
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nDataset Info:")
    print(df.info())
    print("\nFirst entry of the DataFrame:")
    print(df.iloc[0])
    return df

def load_data_db(data: pd.DataFrame, hclient: Client):
    for point in data.iloc:
        res = hclient.query(insert_patient(["sample_name"] + [str(point[i]) for i in range(17)]))
        print(res)

if __name__ == '__main__':
    data = get_data("Reha_Datensatz.csv")
    client = Client(local=True)
    load_data_db(data, client)

