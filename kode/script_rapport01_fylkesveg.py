"""
Henter vegnettsdata: 
"""
# %% 

from datetime import datetime 
import pandas as pd
from shapely import wkt
import geopandas as gpd 

import STARTHER
import regionreform  
import nvdbapiv3 
import nvdbgeotricks 


def tellfelt( feltoversikt ):
    felt = feltoversikt.split(',')
    count = 0
    for etfelt in felt:
        if 'O' in etfelt or 'H' in etfelt or 'V' in etfelt or 'S' in etfelt:
            pass
        else:
            count += 1
    return count


def tellallefelt( feltoversikt, skilletegn='#' ): 
    felt = feltoversikt.split( '#')
    count = len( felt ) 
    return count

if __name__ == '__main__': 
    t0 = datetime.now()

    # Laster ned hele fylkesvegnettet
    print( "Laster ned alt vegnett for fylkesveg")
    mittfilter = { 'vegsystemreferanse' : 'Fv', 'tidspunkt' : '2023-06-16', 'veglenketype' : 'hoved,konnektering' }
    veg = pd.DataFrame( nvdbapiv3.nvdbVegnett( filter=mittfilter).to_records())
    veg['geometry'] = veg['geometri'].apply( wkt.loads )
    veg = gpd.GeoDataFrame( veg, geometry='geometry', crs=5973 )

    t1 = datetime.now( )
    print( f"Lastet ned hele fylkesvegnettet, tidsbruk{t1-t0}")

    # veg.to_file( '../resultater/vegnettFV.gpkg', layer='fylkesveg', driver='GPKG')
    # veg  = gpd.read_file( '../resultater/vegnettFV.gpkg', layer='fylkesveg')

    # Legger på 2024 fylkesnummer og fylkesnavn
    veg = regionreform.fylker2024( veg )

    # # Kjørefelt og feltlengde for bilveg (trafikantgruppe == K) UTEN konnekteringslenker (som mangler data for kjørefelt)
    bilveg = veg[ (veg['trafikantgruppe'] == 'K') & (veg['type'] == 'HOVED')].copy()
    konnektering = veg[ (veg['trafikantgruppe'] == 'K') & (veg['type'] == 'KONNEKTERING')].copy()

    bilveg['antallFelt_ufiltrert'] = bilveg['feltoversikt'].apply( lambda x : tellallefelt( x, skilletegn=','))
    bilveg['antallFelt_filtrert']  = bilveg['feltoversikt'].apply( tellfelt )
    bilveg['Feltlengde ufiltrert (km)'] = bilveg['antallFelt_ufiltrert'] * bilveg['lengde'] / 1000
    bilveg['Feltlengde KOSTRA metode (km)'] = bilveg['antallFelt_filtrert'] * bilveg['lengde'] / 1000

    # Feltlengde skal også ha med adskilte løp = MOT, men det skal ikke telling av lengden på vegen
    fergefri = bilveg[ bilveg['typeVeg'] != 'Bilferje']
    kostraveg = fergefri[ fergefri['adskilte_lop'] != 'Mot']

    # %% Lengde konnekteringslenker
    print( f"Lengde konnekteringslenker: {konnektering['lengde'].sum()}" )
    konn_oppsummert = konnektering.groupby( ['Fylkesnummer2024', 'Fylke2024']).agg( {'lengde' : 'sum' }).reset_index()
    konn_oppsummert.rename( columns={'lengde' : 'Lengde konnekteringslenker (m)' }, inplace=True)
    nvdbgeotricks.skrivexcel( '../resultater/konnekteringslenker.xlsx', konn_oppsummert, sheet_nameListe=['Lengde konnekteringslenker'])



    # %% 

    feltlengde_ufiltrert_2023 = bilveg.groupby( 'fylke2023').agg( {'Feltlengde ufiltrert (km)' : 'sum'})
    feltlengde_kostra_2023 = kostraveg.groupby( 'fylke2023').agg( {'Feltlengde KOSTRA metode (km)' : 'sum'})
    feltlengde_ufiltrert_2023 = bilveg.groupby( ['Fylkesnummer2024', 'Fylke2024'] ).agg( {'Feltlengde ufiltrert (km)' : 'sum'})
    feltlengde_kostra_2023 = kostraveg.groupby( ['Fylkesnummer2024', 'Fylke2024'] ).agg( {'Feltlengde KOSTRA metode (km)' : 'sum'})

    # %% Henter feltlengde 

    # # Lagrer 2023-fylkesnummer for verifisering mot fjorårets leveranse
    # minAgg = myGdf.groupby( ['fylke'] ).agg( {'lengde' : 'sum', 'feltlengde' : 'sum' } ).reset_index()

    # minAgg['Lengde vegnett (km)'] = minAgg['lengde'] / 1000
    # minAgg['Lengde vegnett (km)'] = minAgg['Lengde vegnett (km)'].astype(int)
    # minAgg['Feltlengde (km)']     = minAgg['feltlengde'] / 1000
    # minAgg['Feltlengde (km)']     = minAgg['Feltlengde (km)'].astype(int)
    # minAgg.drop( columns=['lengde', 'feltlengde'], inplace=True )

    # skrivdataframe.skrivdf2xlsx( minAgg, '../resultater/verifiserVeglengder.xlsx')

    # # Repeter analysen, men nå med 2024-fylkesnummer
    # myGdf = lastnedvegnett.fylker2024( myGdf )
    # minAgg = myGdf.groupby( ['fylke'] ).agg( {'lengde' : 'sum', 'feltlengde' : 'sum' } ).reset_index()
    # minAgg['Lengde vegnett (km)'] = minAgg['lengde'] / 1000
    # minAgg['Lengde vegnett (km)'] = minAgg['Lengde vegnett (km)'].astype(int)
    # minAgg['Feltlengde (km)']     = minAgg['feltlengde'] / 1000
    # minAgg['Feltlengde (km)']     = minAgg['Feltlengde (km)'].astype(int)
    # minAgg.drop( columns=['lengde', 'feltlengde'], inplace=True )

    # skrivdataframe.skrivdf2xlsx( minAgg, '../resultater/veglengerFVJuni2023.xlsx')

    ## Laster ned feltstrekning-objekt (ihtt vianova-rapport)

    tNy = datetime.now()
    feltfilter = { 'vegsystemreferanse' : 'Fv', 'tidspunkt' : '2023-06-16' }

    felt = pd.DataFrame( nvdbapiv3.nvdbFagdata(616, filter=feltfilter).to_records())
    print( f"Tidsbruk datanedlasting feltoversikt: {datetime.now()-tNy}")
    felt['geometry'] = felt['geometri'].apply( wkt.loads )
    felt = gpd.GeoDataFrame( felt, geometry='geometry', crs=5973 )
    felt.to_file( 'feltstrekning.gpkg', layer='feltstrekning', driver='GPKG')
    # %% Analyserer feltlengde

    # felt = gpd.read_file( 'feltstrekning.gpkg', layer='feltstrekning')
    felt['Antall felt'] = felt['Feltoversikt, veglenkeretning'].apply( tellallefelt )
    felt['Feltlengde (km)'] = felt['Antall felt'] * felt['segmentlengde'] / 1000 
    felt = regionreform.fylker2024( felt )
    bilfelt= felt[ felt['trafikantgruppe'] == 'K' ]
    felt_2024 = bilfelt.groupby( ['Fylkesnummer2024', 'Fylke2024']).agg( {'Feltlengde (km)' : 'sum' } ).reset_index()
    felt_2023 = bilfelt.groupby( ['fylke2023']).agg( {'Feltlengde (km)' : 'sum' } ).reset_index()
    nvdbgeotricks.skrivexcel( '../resultater/revidertFeltlengde.xlsx', [felt_2024, felt_2023],
                             sheet_nameListe=['Feltlengde 2024-fylker', 'Feltlengde 2023-fylker'] )

    

    # print( f"Kjøretid totalt: {datetime.now()-t0}")
# %%
