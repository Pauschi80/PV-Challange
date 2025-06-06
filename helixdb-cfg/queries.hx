// Start writing your queries here.
//
// You can use the schema to help you write your queries.
//
// Queries take the form:
//     QUERY {query name}({input name}: {input type}) =>
//         {variable} <- {traversal}
//         RETURN {variable}
//
// Example:
//     QUERY GetUserFriends(user_id: String) =>
//         friends <- N<User>(user_id)::Out<Knows>
//         RETURN friends
//
//
// For more information on how to write queries,
// see the documentation at https://docs.helix-db.com
// or checkout our GitHub at https://github.com/HelixDB/helix-db

QUERY insert_patient(n_Name: String, n_Alter: String, n_Geschlecht: String, n_AktuelleKrebserkrankung: String, n_Alkoholkonsum: String, n_Raucher: String, n_VitalBMI: String, n_BerufDerzeit: String, n_WohnsituationSonstiges: String, n_Diagnose: String, n_AnamneseAllgemein: String, n_JetzigeBeschwerden: String, n_RehaSpezifischeAnamnese: String, n_Aufenthaltsdauer: String, n_Indikation: String, n_Leistungskategorie: String, n_Aufenthaltstyp: String, n_Teilhabeziel: String) =>
    patient <- AddN<Patient>({
        name: n_Name,
        alter: n_Alter,
        geschlecht: n_Geschlecht,
        aktuellekrebserkrankung: n_AktuelleKrebserkrankung,
        alkoholkonsum: n_AktuelleKrebserkrankung,
        raucher: n_Raucher,
        vitalbmi: n_VitalBMI,
        berufderzeit: n_BerufDerzeit,
        wohnsituationsonstiges: n_WohnsituationSonstiges,
        diagnose: n_Diagnose,
        anamneseallgemein: n_AnamneseAllgemein,
        jetzigebeschwerden: n_JetzigeBeschwerden,
        rehaspezifischeanamnese: n_RehaSpezifischeAnamnese,
        aufenthaltsdauer: n_Aufenthaltsdauer,
        indikation: n_Indikation,
        leistungskategorie: n_Leistungskategorie,
        aufenthaltstyp: n_Aufenthaltsdauer,
        teilhabeziel: n_Teilhabeziel
    })
    RETURN patient

QUERY search_by_name(name: String) =>
    patient <- N<Patient>::WHERE(_::{name}::EQ(name))
    RETURN patient

