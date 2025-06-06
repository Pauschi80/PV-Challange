import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    # Create patients table with all fields as TEXT (string entries)
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            [alter] TEXT,
            geschlecht TEXT,
            aktuelle_krebserkrankung TEXT,
            alkoholkonsum TEXT,
            raucher TEXT,
            vital_bmi TEXT,
            beruf_derzeit TEXT,
            wohnsituation_sonstiges TEXT,
            diagnose TEXT,
            anamnese_allgemein TEXT,
            jetzige_beschwerden TEXT,
            reha_spezifische_anamnese TEXT,
            aufenthaltsdauer TEXT,
            indikation TEXT,
            leistungskategorie TEXT,
            aufenthaltstyp TEXT,
            teilhabeziel TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_data(csv_file: str):
    # Read CSV file
    df = pd.read_csv(csv_file, sep=';', encoding='latin1')
    # Connect to SQLite database
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    # Insert data into patients table
    for i, (_, row) in enumerate(df.iterrows()):
        c.execute('''
            INSERT INTO patients (
                name, [alter], geschlecht, aktuelle_krebserkrankung, alkoholkonsum,
                raucher, vital_bmi, beruf_derzeit, wohnsituation_sonstiges, diagnose,
                anamnese_allgemein, jetzige_beschwerden, reha_spezifische_anamnese,
                aufenthaltsdauer, indikation, leistungskategorie, aufenthaltstyp,
                teilhabeziel
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            "sample_name" + str(i),
            str(row[0]) if pd.notna(row[0]) else '',  # name
            str(row[1]) if pd.notna(row[1]) else '',  # alter
            str(row[2]) if pd.notna(row[2]) else '',  # geschlecht
            str(row[3]) if pd.notna(row[3]) else '',  # aktuelle_krebserkrankung
            str(row[4]) if pd.notna(row[4]) else '',  # alkoholkonsum
            str(row[5]) if pd.notna(row[5]) else '',  # raucher
            str(row[6]) if pd.notna(row[6]) else '',  # vital_bmi
            str(row[7]) if pd.notna(row[7]) else '',  # beruf_derzeit
            str(row[8]) if pd.notna(row[8]) else '',  # wohnsituation_sonstiges
            str(row[9]) if pd.notna(row[9]) else '',  # diagnose
            str(row[10]) if pd.notna(row[10]) else '',  # anamnese_allgemein
            str(row[11]) if pd.notna(row[11]) else '',  # jetzige_beschwerden
            str(row[12]) if pd.notna(row[12]) else '',  # reha_spezifische_anamnese
            str(row[13]) if pd.notna(row[13]) else '',  # aufenthaltsdauer
            str(row[14]) if pd.notna(row[14]) else '',  # indikation
            str(row[15]) if pd.notna(row[15]) else '',  # leistungskategorie
            str(row[16]) if pd.notna(row[16]) else '',  # aufenthaltstyp
            #str(row[17]) if pd.notna(row[17]) else '',  # teilhabeziel
        ))

    conn.commit()
    conn.close()
    print(f"Loaded {len(df)} records into the database")

if __name__ == '__main__':
    create_database()
    load_data('Reha_Datensatz.csv')

