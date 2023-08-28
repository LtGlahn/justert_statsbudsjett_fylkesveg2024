"""
Div kjekke funksjoner for nedlasting av data til KOSTRA-rapportering
"""
from copy import deepcopy
import pdb 

import pandas as pd
import geopandas as gpd 
from shapely import wkt 

import STARTHER 
import nvdbgeotricks  
import nvdbapiv3 

def fylker2024( myDataFrame, fylker2024='nyFylkesinndeling.csv'):
    """
    Oversetter 2023-kommunenummer til fylkesnummer gyldige i 2024

    ARGUMENTS
        myDataFrame - Dataframe eller GeoDataFrame. Må ha kolonnene kommune og fylke

    KEYWORDS
        fylke2024 - string, filnavn for CSV-fil med kolonnene Kommune2023 og Fylkesnummer2024

    RETURNS
        modifisert myDataFrame, som har fått nye kolonner fylke2023, fylkesnavn2024 og Fylkesnummer2024  
        kolonnen fylke er nå med 2024-fylkesnumrene 
    """

    mydf = myDataFrame.copy() # for å unngå sideeffekter
    mydf['fylke2023'] = mydf['fylke']

    fylker = pd.read_csv( fylker2024, sep=';')

    nyDf = pd.merge( mydf, fylker, how='inner', left_on='kommune', right_on='Kommune2023' )
    assert len(nyDf) == len( mydf), 'Feil i kobling 2024-kommunenummer vs 2023-fylker'

    nyDf['fylke'] = nyDf['Fylkesnummer2024']
    nyDf.drop( columns=['Kommune2023', 'KommuneNavn'], inplace=True )

    return nyDf 

# def filtersjekk( mittfilter={} ):
#     """
#     Beriker et filter med vegnett-spesifikke standardverdier for kostra-søk 
#     """

#     # if not 'kryssystem' in mittfilter.keys():
#     #     mittfilter['kryssystem'] = 'false' 

#     if not 'sideanlegg' in mittfilter.keys():
#         mittfilter['sideanlegg'] = 'false' 


#     # Kun kjørende, og kun øverste topologinivå, og ikke adskiltelop=MOT, og ikke konnekteringslenker 
#     mittfilter['trafikantgruppe'] = 'K'
#     mittfilter['detaljniva']      = 'VT,VTKB'
#     mittfilter['adskiltelop']     = 'med,nei' 
#     mittfilter['typeveg']         = 'kanalisertVeg,enkelBilveg,rampe,rundkjøring,gatetun' 
#     # mittfilter['historisk']       = 'true'
#     # mittfilter['tidspunkt']       = '2021-12-16'
#     mittfilter['veglenketype']       = 'hoved'

#     return mittfilter



