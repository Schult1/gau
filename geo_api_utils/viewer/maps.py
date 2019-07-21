"""Show miscellaneous at maps.
"""
import pandas as pd
import folium

colors = [
    'red',
    'blue',
    'gray',
    'orange',
    'beige',
    'green',
    'darkblue',
    'purple',
    'pink',
    'cadetblue',
    'lightgray',
    'black',
    'lightred',
    'darkgreen',
    'lightblue',
    'lightgreen',
    'darkred',
    'darkpurple'
]

def show_trip(df, TId = None, DId = None):
    """Show Trip at Map.
    Filter on specific trip or device id if given.

    Arguments
    ---------
    df: pandas df
    TId: (optional) trip id
    DId: (optional) device id

    Returns
    -------
    m: folium map
    """

    if TId is not None:
        plotdf = df.loc[df.TripId == TId]
    elif DId is not None:
        plotdf = df.loc[df.DeviceId == DId]
    else:
        plotdf = df

    center = [(plotdf.Latitude.max() + plotdf.Latitude.min())/2,
            (plotdf.Longitude.max() + plotdf.Longitude.min())/2]

    m = folium.Map(
        location=center,
        #tiles='Mapbox Bright',
        zoom_start=10
    )
    TIds = plotdf.TripId.unique()

    for i, TId in enumerate(TIds):
        for j, row in plotdf.loc[plotdf.TripId == TId].iterrows():
            folium.Circle(
                radius=100,
                location=[row.Latitude, row.Longitude],
                popup = (
                    "Trip: {tripid}<br>"
                    "Time: {time}<br>"
                    "Speed: {speed} km/h<br>"
               ).format(tripid=TId, time=row.CaptureDate,speed=str(round(row['RawSpeed'],2)),
                       ),
                color=colors[i%len(colors)],
                fill=True,
            ).add_to(m)

    folium.LayerControl().add_to(m)

    print('#points:', plotdf.shape[0])
    print('#trips:', len(TIds))
    print('start:', plotdf.CaptureDate.min())
    print('ende:', plotdf.CaptureDate.max())

    return m

def show_incidents(loc, jn, provider):

    if provider == 'here':
        try:
            no_incidents = pd.DataFrame(jn['TRAFFIC_ITEMS']['TRAFFIC_ITEM']).shape[0]
        except:
            no_incidents = 0
            return "no incidents in response2"
        t_items={}
        for i in range(0, len(jn['TRAFFIC_ITEMS']['TRAFFIC_ITEM'])):
            from_lat = jn['TRAFFIC_ITEMS']['TRAFFIC_ITEM'][i]['LOCATION']['GEOLOC']['ORIGIN']['LATITUDE']
            from_lon = jn['TRAFFIC_ITEMS']['TRAFFIC_ITEM'][i]['LOCATION']['GEOLOC']['ORIGIN']['LONGITUDE']

            to_lat = jn['TRAFFIC_ITEMS']['TRAFFIC_ITEM'][i]['LOCATION']['GEOLOC']['TO'][0]['LATITUDE']
            to_lon = jn['TRAFFIC_ITEMS']['TRAFFIC_ITEM'][i]['LOCATION']['GEOLOC']['TO'][0]['LONGITUDE']

            try:
                desc = jn['TRAFFIC_ITEMS']['TRAFFIC_ITEM'][i]['TRAFFIC_ITEM_DESCRIPTION'][0]['value']
            except:
                desc = 'Non'
            t_items[i] = {'from': (from_lat, from_lon), 'to': (to_lat, to_lon),
                        'desc': desc}

    m = folium.Map(
        location=loc,
        #tiles='Stamen Toner',
        zoom_start=8
    )

    for i in range(0, len(t_items)):
        tit = t_items[i]
        folium.PolyLine(
            locations=[tit['from'], tit['to']],
            popup = (
                "from: {}<br>"
                "to: {}<br>"
                "description: {}"
           ).format(tit['from'], tit['to'], tit['desc'])
        ).add_to(m)

    return m
