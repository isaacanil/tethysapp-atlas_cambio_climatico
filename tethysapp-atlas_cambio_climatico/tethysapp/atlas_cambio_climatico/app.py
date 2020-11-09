from tethys_sdk.base import TethysAppBase, url_map_maker


class AtlasCambioClimatico(TethysAppBase):
    """
    Tethys app class for Atlas Digital de Cambio Climatico.
    """

    name = 'Atlas Digital de Cambio Climatico'
    index = 'atlas_cambio_climatico:home'
    icon = 'atlas_cambio_climatico/images/icon.gif'
    package = 'atlas_cambio_climatico'
    root_url = 'atlas-cambio-climatico'
    color = '#16a085'
    description = 'Este Atlas despliega mapas de precipitacion y temperatura proyectadas para diferentes periodos.'
    tags = 'Cambio Climático'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='atlas-cambio-climatico',
                controller='atlas_cambio_climatico.controllers.home'
            ),
        )

        return url_maps