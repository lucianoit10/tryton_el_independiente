from trytond.pool import Pool
from .presupuestacion_cta_cte import *



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
        Centimetros,
        SeleccionFechas,
        Finalizar,
        module='presupuestacion_cta_cte', type_='model')
    Pool.register(
        PresupuestacionWizard,
        module='presupuestacion_cta_cte', type_='wizard')