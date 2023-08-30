import pandas as pd
import numpy as np

import STARTHER
import nvdbapiv3
import nvdbgeotricks
import regionreform

def finnlengder( row ):
    if np.isnan( row['Sum lengde alle løp'] ):
        return row['Lengde, offisiell']
    else:
        return row['Sum lengde alle løp']

sok = nvdbapiv3.nvdbFagdata( 581 )
sok.filter( {'vegsystemreferanse' : 'Fv', 'tidspunkt' : '2023-06-15' } )
tun = nvdbgeotricks.nvdbsok2GDF( sok )
# tun.to_file( '../resultater/vegnettFV.gpkg', layer='tunnel', driver='GPKG')

# Skal bruke Sum lengde alle løp, men faller tilbake på "lengde offisiell" hvis den ikke finnes

tun['Lengde'] = tun.apply( finnlengder, axis=1)
tun = tun[ tun['trafikantgruppe'] == 'K']

# undersjoisk = tun[ tun['Undersjøisk'] == 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()
# landtunnel = tun[ tun['Undersjøisk'] != 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()

# undersjoisk.rename( columns={ 'Lengde' : 'Lengde undersjøiske tunnelløp (m)' }, inplace=True )
# landtunnel.rename( columns={ 'Lengde' : 'Lengde ikke-undersjøiske tunnelløp (m)' }, inplace=True )
# tunnelltall = pd.merge( landtunnel, undersjoisk, on='fylke', how='left' )
# skrivdataframe.skrivdf2xlsx( tunnelltall, '../resultater/verifiserTunnel.xlsx' )

#-------------------------
# 2024- fylker
tun = regionreform.fylker2024( tun )

undersjoisk = tun[ tun['Undersjøisk'] == 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()
landtunnel = tun[ tun['Undersjøisk'] != 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()

undersjoisk.rename( columns={ 'Lengde' : 'Lengde undersjøiske tunnelløp (m)' }, inplace=True )
landtunnel.rename( columns={ 'Lengde' : 'Lengde ikke-undersjøiske tunnelløp (m)' }, inplace=True )
tunnelltall = pd.merge( landtunnel, undersjoisk, on='fylke', how='left' )
nvdbgeotricks.skrivexcel( '../resultater/tunneler.xlsx', tunnelltall )

