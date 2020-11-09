from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import TextInput
from tethys_sdk.gizmos import SelectInput
from tethys_sdk.gizmos import DatePicker
from tethys_sdk.gizmos import DatePicker
from tethys_sdk.gizmos import MapView, MVDraw, MVView, MVLayer, MVLegendClass


@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    view_options = MVView(
        projection='EPSG:4326',
        center=[-70, 18.8],
        zoom=8.3,
        maxZoom=18,
        minZoom=2
    )

    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point', 'LineString', 'Polygon', 'Box'],
        initial='Point',
        output_format='WKT'
    )


    esri_layer_names = [
        'NatGeo_World_Map',
        'Ocean_Basemap',
        'USA_Topo_Maps',
        'World_Imagery',
        'World_Physical_Map',
        'World_Shaded_Relief',
        'World_Street_Map',
        'World_Terrain_Base',
        'World_Topo_Map',
    ]

    esri_layers = [{'ESRI': {'layer': l}} for l in esri_layer_names]

    regional_layer = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
            'params': {'LAYERS': 'geoserver_app:Regiones_final'},
            'serverType': 'geoserver'},
        legend_title='Regiones',
        legend_extent=[-71.999550803099, 17.5742476510672, -68.32475920175474, 19.906746450024084]
    )

    # enercp_layer = MVLayer(
    #     source='ImageWMS',
    #     options={'url': 'http://localhost:8080/geoserver/wms',
    #         'params': {'LAYERS': 'geoserver_app:eneRCP60_2070'},
    #         'serverType': 'geoserver'},
    #     legend_title='Enero',
    #     legend_extent=[-126, 24.5, -66.2, 49]
    # )


    basemaps = [
        'Stamen',
        {'Stamen': {'layer': 'toner', 'control_label': 'Black and White'}},
        {'Stamen': {'layer': 'watercolor'}},
        'OpenStreetMap',
        'CartoDB',
        {'CartoDB': {'style': 'dark'}},
        {'CartoDB': {'style': 'light', 'labels': False, 'control_label': 'CartoDB-light-no-labels'}},
        {'XYZ':{'url':'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png', 'control_label':'Wikimedia'}},
      'ESRI'
    ]  

    basemaps.extend(esri_layers)

    MapView.ol_version = '5.3.0'

    map_view_options = MapView(
        height='600px',
        width='100%',
        controls=['ZoomSlider', 'Rotate', 'FullScreen',
                {'MousePosition': {'projection': 'EPSG:4326'}},
                {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
        layers=[regional_layer],
        view=view_options,
        basemap=basemaps,
        draw=drawing_options,
        legend=False
    )


    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    variable_input =TextInput(
        name='variableinput',
        display_text='Variable',
        placeholder='Seleccione la variable'
    )

    variable_select = SelectInput(
        display_text='Variable',
        name='variable',
        multiple=False,
        options=[('Precipitación','P'),('Temperatura','T')],
        select2_options={
            'placeholder':'Seleccione',
            'allowClear':True}
    )

    unidadTemp_select = SelectInput(
        display_text='Unidad Temporal',
        name='unidadTemp',
        multiple=False,
        options=[('Anual','A'),('Mensual','M')],
        select2_options={
            'placeholder':'Seleccione',
            'allowClear':True}
    )
    """
    periodo_datepicker = DatePicker(
        name='periodo',
        display_text='Periodo',
        autoclose=True,
        format='MM d, yyyy',
        start_date='January 1, 1950',
        start_view='decade',
        today_button=True,
        initial='January 1, 2020',
        min_view_mode='years',
        multidate=2,
        end_date='January 1, 2080')
    """
    periodo_datepicker = SelectInput(
        display_text='Periodo',
        name='periodo',
        multiple=False,
        options=[('1950-2000','1'),('2041-2060','2050'),('2061-2080','2070')],
        select2_options={
            'placeholder':'Seleccione',
            'allowClear':True
        }
    )

    escenerio_select = SelectInput(
        display_text='Escenario de cambio climatico',
        name='escenario',
        multiple=False,
        options=[('RCP 2.6','26'),('RCP 4.5','45'),('RCP 6.0','60'),('RCP 8.5','85')],
        select2_options={
            'placeholder':'Seleccione',
            'allowClear':True
        }
    )

    play_button = Button(
        display_text='',
        name='play-button',
        icon='glyphicon glyphicon-play',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Play',
            'onclick':'loadCCLayer();'
        }
    )

    stop_button = Button(
        display_text='',
        name='stop-button',
        icon='glyphicon glyphicon-stop',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Parar',
            'onclick':'stop();'
        }
    )

    back_button = Button(
        display_text='',
        name='back-button',
        icon='glyphicon glyphicon-backward',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Anterior',
            'onclick':'backLayer();'
        }
    )

    forward_button = Button(
        display_text='',
        name='forward-button',
        icon='glyphicon glyphicon-forward',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Siguiente',
            'onclick':'forwardLayer();'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button,
        'variable_input':variable_input,
        'variable_select':variable_select,
        'unidadTemp_select':unidadTemp_select,
        'periodo_datepicker':periodo_datepicker,
        'escenerio_select':escenerio_select,
        'map_view_options':map_view_options,
        'play_button':play_button,
        'stop_button':stop_button,
        'back_button':back_button,
        'forward_button':forward_button

    }

    return render(request, 'atlas_cambio_climatico/home.html', context)