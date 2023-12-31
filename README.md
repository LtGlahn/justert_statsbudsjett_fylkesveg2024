Etter en del kritikk og diskusjon ble det åpenbart at datauttaket gjort i juni 2023 til _Kritieriedata for for fylkesveg_ til statsbudsjett 2024 måtte revideres. [datauttak - kriteriedata for fylkesveg for statsbudsjett 2024](https://github.com/LtGlahn/statsbudsjett-fylkesveg2024). Vi skal slavisk følge metodikken beskrevet i dokumentet   [Forslag til ny modell for beregning av kriteriet for fylkesveg i inntektssystemet for 
fylkeskommunene](https://www.regjeringen.no/contentassets/e8645ebe0e02470da89253caef0addba/rapport-forenklet-modell-til-kriteriet-for-utgiftsbehov-ti1405835.pdf), uten forsøk på faglig korreksjon. 

Fordelen er at metodikken blir enkel - og dermed robust, samt konsistent med slik det er gjort tidligere. 

Ulempen er at en del av tallene - lengder og mengder - avviker fra virkeligheten, vel og merke slik virkeligheten blir modellert i NVDB og BRUTUS. For eksempel er lengden på vegnettet ikke konsistent med KOSTRA-metodikk for å beregne lengde av fylkesvegnettet. Videre er det en del spørsmål om hvilke lengder som skal inkludere ferjestrekninger, konnekteringslenker, _adskilte løp = MOT_ og lignende. Disse spørsmålene er oppsummert i [problemer og dilemma med Vianova-metoden](./problemer.md)

Min evaluering av datauttaket i juni, der jeg avdekket flere feil, er i [dette PDF-dokumentet](./GjennomgangkriteriedataFv.pdf). Her er en kort oppsummering av forskjellen etter revisjon:

| Parameter | Justering | Kommentar |
|---|---|---|
| Feltlengde (km)	                        | Stor justering | Bilferjer skal tas med i feltlengde | 
| Trafikkarbeid (mill kjøretøykm)	        | Ingen | Forvirring rundt trafikkarbeid _per døgn_ vs _per år_  | 
| Lengde Ådt > 4000 (km)	| Ingen |  | 
| Lengde Ådt > 1500 (km)	| Ingen |  | 
| Rekkverk (lm)	| Stor | Rekkverk langs G/s veg, samt filtrering på eier | 
| Lyspunkt i dagen (antall)	| Ingen |  | 
| Lengde ikke-undersjøiske tunnelløp (m)	| Stor | Feil på summering av lengde-egenskap  | 
| Lengde undersjøiske tunnelløp (m)	| Bagatellmessig | Samme feil, men lite utslag | 
| Lengde bruer av stål (m)	| Stor | Ikke bruke BRUTUS-data, men NVDB | 
| Lengde bruer av andre materialtyper enn stål (m)	| Stor | Ikke bruke BRUTUS-data, men NVDB | 
| Ferjekaibruer og tilleggskaier (antall)	G/S-veglengde (km)	| Ingen |  | 
| Veg med fartsgrense 50 km/t eller lavere (km)| Ingen |  | 



