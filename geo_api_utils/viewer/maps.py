"""Show miscellaneous at maps.
"""
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

def show_polygons(poly_lst):
    m = folium.Map(
        location=poly_lst[0].centroid.coords[0],
        #tiles='Stamen Toner',
        zoom_start=7
    )

    for i, p in enumerate(poly_lst):
        folium.Polygon(
            locations=p.exterior.coords,
            color = colors[i%len(colors)]
        ).add_to(m)

    return m

def show_trips(data, start = True):
    """Show start or ends of Trips at Map.
    Filter on specific trip or device id if given.

    Arguments
    ---------
    data: pandas df with columns startloclat and startloclon
    start: BOOLEAN
        If True (default), show starts of the trips.
        If False, show ends of the trips.

    Returns
    -------
    m: folium map
    """

    if start:
        pre = 'start'
        col = 'green'
    else:
        pre = 'end'
        col = 'red'

    center = [(data['{}loclat'.format(pre)].max() + data['{}loclat'.format(pre)].min())/2,
            (data['{}loclon'.format(pre)].max() + data['{}loclon'.format(pre)].min())/2]


    m = folium.Map(
        location=center,
        #tiles='Mapbox Bright',
        zoom_start=8
    )


    for j, row in data.iterrows():
        folium.Circle(
            radius=1,
            location=[row['{}loclat'.format(pre)], row['{}loclon'.format(pre)]],
            popup = (
                    "Trip: {tripid}<br>"
                    "Time: {time}"
               ).format(tripid=row.tripid, time=row['{}date'.format(pre)]),
            color=col,
            fill=True,
        ).add_to(m)

    folium.LayerControl().add_to(m)

    return m
