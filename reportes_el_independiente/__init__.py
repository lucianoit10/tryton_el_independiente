from trytond.pool import Pool
from .reportes_el_independiente import *

Pool.register(
    Sale,
    Invoice,
    SeleccionEntidad,
    module='reportes_el_independiente', type_='model')
Pool.register(
    ReporteSalePresupuestador,
    ReporteEstadoCuentaEntidad,
    ReporteInvoicePresupuestador,
    module='reportes_el_independiente', type_='report')
Pool.register(
    OpenEstadoCuentaEntidad,
    module='reportes_el_independiente', type_='wizard')
