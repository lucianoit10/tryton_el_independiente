from trytond.pool import Pool
from .presupuestacion_efectivo import *
from .sale import *


def register():
    Pool.register(
        TipoYCategoria,
        Producto,
        AvisoComun,
        AvisoEspecial,
        FunebreComun,
        FunebreDestacado,
        ClasificadoComun,
        ClasificadoDestacado,
        EdictoJudicial,
        Insert,
        Suplemento,
        Radio,
        Digital,
        SeleccionFechas,
        Finalizar,
        Sale,
        module='presupuestacion_efectivo', type_='model')
    Pool.register(
        PresupuestacionWizard,
        module='presupuestacion_efectivo', type_='wizard')