from trytond.pool import Pool
from .edicion import *


def register():
    Pool.register(
        Edicion,
        PublicacionDiario,
        PublicacionRadio,
        PublicacionDigital,
        PublicacionPresupuestadaDiario,
        PublicacionPresupuestadaRadio,
        PublicacionPresupuestadaDigital,
        EdicionPublicacionDigital,
        TipoYCategoria,
        Producto,
        AvisoComun,
        AvisoEspecial,
        FunebreDestacado,
        ClasificadoDestacado,
        SeleccionFechas,
        Finalizar,
        module='edicion', type_='model')
    Pool.register(
        ReporteEdicion,
        module='edicion', type_='report')
    Pool.register(
        PresupuestacionCentimetros,
        module='edicion', type_='wizard')