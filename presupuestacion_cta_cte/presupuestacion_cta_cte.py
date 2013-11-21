# -*- coding: utf-8 -*-

from trytond.pool import Pool
from decimal import Decimal
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, Bool, Or, Not, And, Equal
from trytond.transaction import Transaction

tyc_cat_diario =[
                    ('Aviso Comun', '1- Aviso Comun'),
                    ('Aviso Especial', '2- Aviso Especial'),
                    ('Clasificado', '3- Clasificado'),
                    ('Funebre', '4- Funebre'),
                    ('Edicto', '5- Edicto'),
                    ('Centimetros', '6- Centimetros'),
                ]

aviso_ubicacion=[
                    ('0', '1- Libre'),
                    ('1', '2- Pagina Par'),
                    ('2', '3- Pagina Impar'),
                    ('3', '4- Tapa'),
                    ('4', '5- Central'),
                    ('5', '6- Contratapa'),
                    ('6', '7- Suplemento'),
                 ]

select_apariciones=    [
                           ('1', '1- Dia/s especifico/s'),
                           ('7', '2- Semana/s(7 dias)'),
                           ('30', '3- Mes/es (30 dias)'),
                           ('365', '4- ANUAL(365 dias)'),
                       ]

tipo_bonificacion= [
                       ('$', '$- Fijo'),
                       ('p', '%- Porcentual'),
                   ]


insert_tipo_impresion= [
                            ('0', '1- Si'),
                            ('1', '2- No'),
                       ]



class TipoYCategoria(ModelSQL,ModelView):
    'Tipo y Categoria'
    __name__ = 'presupuestacion_cta_cte.tipo_y_categoria.start'
    diario = fields.Char('DIARIO',readonly=True)
    categoriaDiario = fields.Selection(tyc_cat_diario, 'CATEGORIA',required=True,states={'readonly':Not(Bool(Eval('diario')))})

    @staticmethod
    def default_diario():
        return 'DIARIO'

class Producto(ModelSQL,ModelView):
    'Producto'
    __name__ = 'presupuestacion_cta_cte.producto'
    cat = fields.Char('Categoria Seleccionada', readonly=True)
    producto = fields.Many2One('product.template', 'Productos',domain=[('category', '=', Eval('cat'))], required=True)


class AvisoComun(ModelSQL,ModelView):
    'AvisoComun'
    __name__ = 'presupuestacion_cta_cte.aviso_comun'
    ubicacion = fields.Selection(aviso_ubicacion, 'UBICACION', readonly=False, required=True)
    nro_pag = fields.Char('PAGINA NRO', states={'readonly': And(Not(Equal(Eval('ubicacion'),'1')),Not(Equal(Eval('ubicacion'),'2')))})
    suplemento = fields.Char('SUPLEMENTO', states={'readonly': (Eval('ubicacion') != '6')})
    cant_centimetros = fields.Numeric('CENTIMETROS', required=True)
    cant_columnas = fields.Numeric('COLUMNAS', required=True)
    apariciones = fields.Selection(select_apariciones, 'APARICIONES',  on_change=['apariciones'], required=True)
    cant_apariciones = fields.Numeric('NRO.', states={'readonly': (Eval('apariciones') == '365')}, required=True)
    inicio = fields.Date('INICIO', states={'readonly': (Eval('apariciones') == '1')}, required=True)
    bonificacion = fields.Boolean('bonificacion', select=False)
    tipo_bonif = fields.Selection(tipo_bonificacion, 'tipo_bonif' , states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    valor = fields.Numeric('VALOR', states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    motivo = fields.Char('MOTIVO',states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=False)
    descripcion = fields.Text('DESCRIPCION',readonly=False)


    @staticmethod
    def default_bonificacion():
        return False


    def on_change_apariciones(self):
        if self.apariciones == '365':
            v = 1
            return {'cant_apariciones': v}
        return{}


class AvisoEspecial(ModelSQL,ModelView):
    'AvisoEspecial'
    __name__ = 'presupuestacion_cta_cte.aviso_especial'
    ubicacion = fields.Char('UBICACION', size=8, readonly=True)
    cant_centimetros = fields.Char('CENTIMETROS', size=8, readonly=True)
    cant_columnas = fields.Char('COLUMNAS', size=8, readonly=True)
    apariciones = fields.Selection(select_apariciones, 'APARICIONES',  on_change=['apariciones'], required=True)
    cant_apariciones = fields.Numeric('NRO.', states={'readonly': (Eval('apariciones') == '365')}, required=True)
    inicio = fields.Date('INICIO', states={'readonly': (Eval('apariciones') == '1')}, required=True)
    bonificacion = fields.Boolean('bonificacion', select=False)
    tipo_bonif = fields.Selection(tipo_bonificacion, 'tipo_bonif' , states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    valor = fields.Numeric('VALOR', states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    motivo = fields.Char('MOTIVO',states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=False)
    descripcion = fields.Text('DESCRIPCION',readonly=False)

    @staticmethod
    def default_bonificacion():
        return False

    @staticmethod
    def default_ubicacion():
        return '1- Libre'

    def on_change_apariciones(self):
        if self.apariciones == '365':
            v = 1
            return {'cant_apariciones': v}
        return{}

class FunebreComun(ModelSQL,ModelView):
    'FunebreComun'
    __name__ = 'presupuestacion_cta_cte.funebre_comun'
    apariciones = fields.Selection(select_apariciones, 'APARICIONES',  on_change=['apariciones'], required=True)
    cant_apariciones = fields.Numeric('NRO.', states={'readonly': (Eval('apariciones') == '365')}, required=True)
    inicio = fields.Date('INICIO', states={'readonly': (Eval('apariciones') == '1')}, required=True)
    bonificacion = fields.Boolean('bonificacion', select=False)
    tipo_bonif = fields.Selection(tipo_bonificacion, 'tipo_bonif' , states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    valor = fields.Numeric('VALOR', states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    motivo = fields.Char('MOTIVO',states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=False)
    descripcion = fields.Text('DESCRIPCION',readonly=False)

    @staticmethod
    def default_bonificacion():
        return False

    def on_change_apariciones(self):
        if self.apariciones == '365':
            v = 1
            return {'cant_apariciones': v}
        return{}

class FunebreDestacado(ModelSQL,ModelView):
    'FunebreDestacado'
    __name__ = 'presupuestacion_cta_cte.funebre_destacado'
    cant_centimetros = fields.Numeric('CENTIMETROS', readonly=False, required=True)
    cant_columnas = fields.Numeric('COLUMNAS', readonly=False, required=True)
    apariciones = fields.Selection(select_apariciones, 'APARICIONES',  on_change=['apariciones'], required=True)
    cant_apariciones = fields.Numeric('NRO.', states={'readonly': (Eval('apariciones') == '365')}, required=True)
    inicio = fields.Date('INICIO', states={'readonly': (Eval('apariciones') == '1')}, required=True)
    bonificacion = fields.Boolean('bonificacion', select=False)
    tipo_bonif = fields.Selection(tipo_bonificacion, 'tipo_bonif' , states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    valor = fields.Numeric('VALOR', states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    motivo = fields.Char('MOTIVO',states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=False)
    descripcion = fields.Text('DESCRIPCION',readonly=False)

    @staticmethod
    def default_bonificacion():
        return False

    def on_change_apariciones(self):
        if self.apariciones == '365':
            v = 1
            return {'cant_apariciones': v}
        return{}

class ClasificadoComun(ModelSQL,ModelView):
    'ClasificadoComun'
    __name__ = 'presupuestacion_cta_cte.clasificado_comun'
    tipo = fields.Char('TIPO', readonly=True)
    apariciones = fields.Selection(select_apariciones, 'APARICIONES',  on_change=['apariciones'], required=True)
    cant_apariciones = fields.Numeric('NRO.', states={'readonly': (Eval('apariciones') == '365')}, required=True)
    inicio = fields.Date('INICIO', states={'readonly': (Eval('apariciones') == '1')}, required=True)
    bonificacion = fields.Boolean('bonificacion', select=False)
    tipo_bonif = fields.Selection(tipo_bonificacion, 'tipo_bonif' , states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    valor = fields.Numeric('VALOR', states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    motivo = fields.Char('MOTIVO',states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=False)
    descripcion = fields.Text('DESCRIPCION',readonly=False)

    @staticmethod
    def default_bonificacion():
        return False

    def on_change_apariciones(self):
        if self.apariciones == '365':
            v = 1
            return {'cant_apariciones': v}
        return{}

class ClasificadoDestacado(ModelSQL,ModelView):
    'ClasificadoDestacado'
    __name__ = 'presupuestacion_cta_cte.clasificado_destacado'
    tipo = fields.Char('TIPO', readonly=True)
    cant_centimetros = fields.Numeric('CENTIMETROS', readonly=False, required=True)
    cant_columnas = fields.Numeric('COLUMNAS',  readonly=False, required=True)
    apariciones = fields.Selection(select_apariciones, 'APARICIONES',  on_change=['apariciones'], required=True)
    cant_apariciones = fields.Numeric('NRO.', states={'readonly': (Eval('apariciones') == '365')}, required=True)
    inicio = fields.Date('INICIO', states={'readonly': (Eval('apariciones') == '1')}, required=True)
    bonificacion = fields.Boolean('bonificacion', select=False)
    tipo_bonif = fields.Selection(tipo_bonificacion, 'tipo_bonif' , states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    valor = fields.Numeric('VALOR', states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    motivo = fields.Char('MOTIVO',states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=False)
    descripcion = fields.Text('DESCRIPCION',readonly=False)

    @staticmethod
    def default_bonificacion():
        return False

    def on_change_apariciones(self):
        if self.apariciones == '365':
            v = 1
            return {'cant_apariciones': v}
        return{}

class EdictoJudicial(ModelSQL,ModelView):
    'EdictoJudcial'
    __name__ = 'presupuestacion_cta_cte.edicto_judicial'
    cant_lineas = fields.Numeric('CANTIDAD DE LINEAS', required=True)
    apariciones = fields.Selection(select_apariciones, 'APARICIONES',  on_change=['apariciones'], required=True)
    cant_apariciones = fields.Numeric('NRO.', states={'readonly': (Eval('apariciones') == '365')}, required=True)
    inicio = fields.Date('INICIO', states={'readonly': (Eval('apariciones') == '1')}, required=True)
    bonificacion = fields.Boolean('bonificacion', select=False)
    tipo_bonif = fields.Selection(tipo_bonificacion, 'tipo_bonif' , states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    valor = fields.Numeric('VALOR', states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=True)
    motivo = fields.Char('MOTIVO',states={'readonly': (Bool(Eval('bonificacion')) == False)}, required=False)
    descripcion = fields.Text('DESCRIPCION',readonly=False)

    @staticmethod
    def default_bonificacion():
        return False

    def on_change_apariciones(self):
        if self.apariciones == '365':
            v = 1
            return {'cant_apariciones': v}
        return{}

class Centimetros(ModelSQL,ModelView):
    'Centimetros'
    __name__ = 'presupuestacion_cta_cte.centimetros'
    cant_centimetros = fields.Numeric('CENTIMETROS', readonly=False, required=True)
    cant_columnas = fields.Numeric('COLUMNAS', readonly=False, required=True)
    precio_cm = fields.Numeric('PRECIO POR CM', readonly=False, required=True)
    descripcion = fields.Text('DESCRIPCION',readonly=False)

class SeleccionFechas(ModelSQL,ModelView):
    'SeleccionFechas'
    __name__ = 'presupuestacion_cta_cte.seleccion_fechas'
    cant_apariciones = fields.Numeric('CANTIDAD DE APARICIONES YA CARGADAS:', readonly=True)
    fecha = fields.Date('FECHA DE LA EDICION O MENCION', required=True)

class Finalizar(ModelView):
    'Finalizar'
    __name__ = 'presupuestacion_cta_cte.finalizar'
    texto = fields.Char('EL PROCESO DE PRESUPUESTACION A TERMINADO CON EXITO', readonly=True)


class PresupuestacionWizard(Wizard):
    'PresupuestacionWizard'
    __name__ = 'presupuestacion_cta_cte.presupuestacion_wizard'

    start = StateTransition()
    #-----------------------------------------INICIO-----------------------------------------#
    start_view = StateView('presupuestacion_cta_cte.tipo_y_categoria.start',
                      'presupuestacion_cta_cte.tipo_y_categoria_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Siguiente', 'eleccion_producto', 'tryton-go-next', default=True)])

    #-----------------------------------------PRODUCTO-----------------------------------------#
    producto = StateView('presupuestacion_cta_cte.producto',
                      'presupuestacion_cta_cte.producto_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'volver_start', 'tryton-go-previous'),
                      Button('Siguiente', 'datos_categoria', 'tryton-go-next', default=True)])

    #-----------------------------------------DIARIO-----------------------------------------#
    aviso_comun = StateView('presupuestacion_cta_cte.aviso_comun',
                      'presupuestacion_cta_cte.aviso_comun_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_aviso_comun', 'tryton-go-next', default=True)])

    aviso_especial = StateView('presupuestacion_cta_cte.aviso_especial',
                      'presupuestacion_cta_cte.aviso_especial_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_aviso_especial', 'tryton-go-next', default=True)])

    funebre_comun = StateView('presupuestacion_cta_cte.funebre_comun',
                      'presupuestacion_cta_cte.funebre_comun_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_funebre_comun', 'tryton-go-next', default=True)])

    funebre_destacado = StateView('presupuestacion_cta_cte.funebre_destacado',
                      'presupuestacion_cta_cte.funebre_destacado_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_funebre_destacado', 'tryton-go-next', default=True)])

    clasif_comun = StateView('presupuestacion_cta_cte.clasificado_comun',
                      'presupuestacion_cta_cte.clasificado_comun_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_clasif_comun', 'tryton-go-next', default=True)])

    clasif_destacado = StateView('presupuestacion_cta_cte.clasificado_destacado',
                      'presupuestacion_cta_cte.clasificado_destacado_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_clasif_destacado', 'tryton-go-next', default=True)])

    edicto = StateView('presupuestacion_cta_cte.edicto_judicial',
                      'presupuestacion_cta_cte.edicto_judicial_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_edicto', 'tryton-go-next', default=True)])

    centimetros = StateView('presupuestacion_cta_cte.centimetros',
                      'presupuestacion_cta_cte.centimetros_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Atras', 'eleccion_producto', 'tryton-go-previous'),
                      Button('Siguiente', 'terminar_centimetros', 'tryton-go-next', default=True)])


    edicion_aviso_comun = StateView('presupuestacion_cta_cte.seleccion_fechas',
                      'presupuestacion_cta_cte.seleccion_fechas_form',
                      [Button('Siguiente', 'terminar_edicion_aviso_comun', 'tryton-go-next', default=True)])

    edicion_aviso_especial = StateView('presupuestacion_cta_cte.seleccion_fechas',
                      'presupuestacion_cta_cte.seleccion_fechas_form',
                      [Button('Siguiente', 'terminar_edicion_aviso_especial', 'tryton-go-next', default=True)])

    edicion_funebre_comun = StateView('presupuestacion_cta_cte.seleccion_fechas',
                      'presupuestacion_cta_cte.seleccion_fechas_form',
                      [Button('Siguiente', 'terminar_edicion_funebre_comun', 'tryton-go-next', default=True)])

    edicion_funebre_destacado = StateView('presupuestacion_cta_cte.seleccion_fechas',
                      'presupuestacion_cta_cte.seleccion_fechas_form',
                      [Button('Siguiente', 'terminar_edicion_funebre_destacado', 'tryton-go-next', default=True)])

    edicion_clasif_comun = StateView('presupuestacion_cta_cte.seleccion_fechas',
                      'presupuestacion_cta_cte.seleccion_fechas_form',
                      [Button('Siguiente', 'terminar_edicion_clasif_comun', 'tryton-go-next', default=True)])

    edicion_clasif_destacado = StateView('presupuestacion_cta_cte.seleccion_fechas',
                      'presupuestacion_cta_cte.seleccion_fechas_form',
                      [Button('Siguiente', 'terminar_edicion_clasif_destacado', 'tryton-go-next', default=True)])

    edicion_edicto = StateView('presupuestacion_cta_cte.seleccion_fechas',
                      'presupuestacion_cta_cte.seleccion_fechas_form',
                      [Button('Siguiente', 'terminar_edicion_edicto', 'tryton-go-next', default=True)])

    #-----------------------------------------FIN-----------------------------------------#
    finalizar = StateView('presupuestacion_cta_cte.finalizar',
                  'presupuestacion_cta_cte.finalizar_form',
                  [Button('Finalizar', 'end', 'tryton-ok', default=True)])


    volver_start = StateTransition()
    eleccion_producto = StateTransition()
    datos_categoria = StateTransition()
    #--------------------------------------------------
    terminar_aviso_comun = StateTransition()
    terminar_edicion_aviso_comun = StateTransition()
    #--------------------------------------------------
    terminar_aviso_especial = StateTransition()
    terminar_edicion_aviso_especial = StateTransition()
    #--------------------------------------------------
    terminar_funebre_comun = StateTransition()
    terminar_edicion_funebre_comun = StateTransition()
    #--------------------------------------------------
    terminar_funebre_destacado = StateTransition()
    terminar_edicion_funebre_destacado = StateTransition()
    #--------------------------------------------------
    terminar_clasif_comun = StateTransition()
    terminar_edicion_clasif_comun = StateTransition()
    #--------------------------------------------------
    terminar_clasif_destacado = StateTransition()
    terminar_edicion_clasif_destacado = StateTransition()
    #--------------------------------------------------
    terminar_edicto = StateTransition()
    terminar_edicion_edicto = StateTransition()
    #--------------------------------------------------
    terminar_centimetros = StateTransition()
    #--------------------------------------------------

    def crear_linea_producto(self,producto,precio_unitario,cantidad,descripcion):
        sale = Pool().get('sale.sale')
        linea = Pool().get('sale.line')
        tax = Pool().get('sale.line-account.tax')
        nueva = linea.create([{
                    'sale':sale(Transaction().context.get('active_id')),
                    'product': producto,
                    'sequence':'0',
                    'type':'line',
                    'unit': producto.default_uom,
                    'unit_price':precio_unitario,
                    'quantity':cantidad,
                    'description':str(descripcion)
                    }])[0]
        nueva.save()
        try:
            impuesto_cliente = producto.category.parent.customer_taxes[0]
            impuesto_linea = tax.create([{
                'line' : linea(nueva),
                'tax' : impuesto_cliente
                }])[0]
            impuesto_linea.save()
        except:
            pass
        return nueva

    def crear_linea_recargo(self,producto,precio_unitario,ubic):
        sale = Pool().get('sale.sale')
        linea = Pool().get('sale.line')
        rec = linea.create([{
                    'sale':sale(Transaction().context.get('active_id')),
                    'sequence':'0',
                    'product' : producto,
                    'type':'line',
                    'unit': producto.default_uom,
                    'unit_price': precio_unitario,
                    'quantity':'1',
                    'description':'Recargo por ubicacion, ' + str(ubic)  + '.'
                    }])[0]
        rec.save()

    def crear_linea_bonificacion(self,producto,precio_unitario,motivo):
        sale = Pool().get('sale.sale')
        linea = Pool().get('sale.line')
        bonif = linea.create([{
                    'sale':sale(Transaction().context.get('active_id')),
                    'sequence':'0',
                    'type':'line',
                    'product' : producto,
                    'unit': producto.default_uom,
                    'unit_price': precio_unitario,
                    'quantity':'1',
                    'description':'Bonificacion por ventas. \n MOTIVO:\n'+motivo
                    }])[0]
        bonif.save()


    def crear_linea_publicacion_diario(self,nueva,producto,descripcion,medida,fecha):
        edicion = Pool().get('edicion.edicion')
        sale = Pool().get('sale.sale')
        publicacion = Pool().get('edicion.publicacion_diario')
        ubicacion = "NO POSEE"
        try:
            split = descripcion.split("\n")[1].split("Ubicacion:")
            ubicacion = split[0] + split[1]
        except:
            pass
        edic = 0
        try:
            edic= edicion(edicion.search([('fecha', '=', fecha)])[0])
        except:
            edic=edicion.create([{
            'fecha':fecha
            }])[0]
            edic.save()
        pub = publicacion.create([{
            'termino_pago':(sale(Transaction().context.get('active_id'))).payment_term,
            'cliente':(sale(Transaction().context.get('active_id'))).party,
            'linea':nueva,
            'producto' : producto,
            'descrip' : nueva.description,
            'medidas' : medida,
            'ubicacion': ubicacion,
            'edicion' : edic,
            }])[0]
        pub.save()

    def crear_linea_publicacion_diario_centimetros(self,nueva,producto,descripcion,medida):
        edicion = Pool().get('edicion.edicion')
        sale = Pool().get('sale.sale')
        publicacion = Pool().get('edicion.publicacion_diario')
        edic = None
        pub = publicacion.create([{
            'termino_pago':(sale(Transaction().context.get('active_id'))).payment_term,
            'cliente':(sale(Transaction().context.get('active_id'))).party,
            'linea':nueva,
            'producto' : producto,
            'descrip' : nueva.description,
            'medidas' : medida,
            'ubicacion': 'REDIMENSIONAR',
            'edicion' : edic,
            'state' : 'reprogramar',
            'venta_cm' : 'si',
            'venta' : sale(Transaction().context.get('active_id')),
            }])[0]
        pub.save()


#valores por defecto de los estados de vista

    def default_producto(self,fields):
        default = {}
        default['cat']=str('Diario') + ' / ' + str(self.start_view.categoriaDiario)
        return default

    def default_aviso_comun(self,fields):
        default = {}
        default['ubicacion']='0'
        default['cant_centimetros']=3
        default['cant_columnas']=1
        default['apariciones']='1'
        default['cant_apariciones']=1
        default['tipo_bonif']='p'
        return default

    def default_aviso_especial(self,fields):
        default = {}
        cm=str(self.producto.producto.name).split('x')[-1]
        col=(str(self.producto.producto.name).split('x')[0]).split(' ')[-1]
        default['cant_centimetros']=cm
        default['cant_columnas']=col
        default['apariciones']='1'
        default['cant_apariciones']=1
        default['tipo_bonif']='p'
        return default

    def default_funebre_comun(self,fields):
        default = {}
        default['apariciones']='1'
        default['cant_apariciones']=1
        default['tipo_bonif']='p'
        return default

    def default_funebre_destacado(self,fields):
        default = {}
        default['cant_centimetros']=3
        default['cant_columnas']=1
        default['apariciones']='1'
        default['cant_apariciones']=1
        default['tipo_bonif']='p'
        return default

    def default_clasif_comun(self,fields):
        default = {}
        default['tipo']=self.producto.producto.name.split(' ')[0]
        default['apariciones']='1'
        default['cant_apariciones']=1
        default['tipo_bonif']='p'
        return default


    def default_clasif_destacado(self,fields):
        default = {}
        default['tipo']=self.producto.producto.name.split(' ')[0]
        default['cant_centimetros']=3
        default['cant_columnas']=1
        default['apariciones']='1'
        default['cant_apariciones']=1
        default['tipo_bonif']='p'
        return default

    def default_edicto(self,fields):
        default = {}
        default['cant_lineas']=1
        default['apariciones']='1'
        default['cant_apariciones']=1
        default['tipo_bonif']='p'
        return default

    def default_centimetros(self,fields):
        default = {}
        default['cant_centimetros']=1
        default['cant_columnas']=1
        default['precio_cm']=1
        return default

    def default_edicion_aviso_comun(self,fields):
        default = {}
        try:
            default['cant_apariciones']=Decimal(self.edicion_aviso_comun.cant_apariciones) +1
        except:
            default['cant_apariciones']=1
        return default

    def default_edicion_aviso_especial(self,fields):
        default = {}
        try:
            default['cant_apariciones']=Decimal(self.edicion_aviso_especial.cant_apariciones) +1
        except:
            default['cant_apariciones']=1
        return default

    def default_edicion_funebre_comun(self,fields):
        default = {}
        try:
            default['cant_apariciones']=Decimal(self.edicion_funebre_comun.cant_apariciones) +1
        except:
            default['cant_apariciones']=1
        return default

    def default_edicion_funebre_destacado(self,fields):
        default = {}
        try:
            default['cant_apariciones']=Decimal(self.edicion_funebre_destacado.cant_apariciones) +1
        except:
            default['cant_apariciones']=1
        return default

    def default_edicion_clasif_comun(self,fields):
        default = {}
        try:
            default['cant_apariciones']=Decimal(self.edicion_clasif_comun.cant_apariciones) +1
        except:
            default['cant_apariciones']=1
        return default

    def default_edicion_clasif_destacado(self,fields):
        default = {}
        try:
            default['cant_apariciones']=Decimal(self.edicion_clasif_destacado.cant_apariciones) +1
        except:
            default['cant_apariciones']=1
        return default

    def default_edicion_edicto(self,fields):
        default = {}
        try:
            default['cant_apariciones']=Decimal(self.edicion_edicto.cant_apariciones) +1
        except:
            default['cant_apariciones']=1
        return default


#ACCION DE LAS TRANSICIONES

    @classmethod
    def __setup__(cls):
        super(PresupuestacionWizard, cls).__setup__()

        cls._error_messages.update({
            'error_wizard': 'Termino de pago o cliente no pertenecen a Cuenta Corriente',
            'error_wizard_dos': 'Venta Procesada'
            })

    def transition_start(self):
        sale = Pool().get('sale.sale')
        party_cat = Pool().get('party.party-party.category')
        entidad = (sale(Transaction().context.get('active_id'))).party
        res_cat = party_cat.search([('party', '=',entidad)])[0].category
        term_pago = (sale(Transaction().context.get('active_id'))).payment_term
        if ((res_cat.parent.name != 'Cuenta Corriente') or (term_pago.name != 'Cuenta Corriente')):
            self.raise_user_error('error_wizard')
        if (sale(Transaction().context.get('active_id')).state=='processing'):
            self.raise_user_error('error_wizard_dos')
        return 'start_view'

    def transition_volver_start(self):
        return 'start_view'

    def transition_eleccion_producto(self):
        return 'producto'

    def transition_datos_categoria(self):
        if self.start_view.diario:
            if(self.start_view.categoriaDiario == 'Aviso Comun'):
                return 'aviso_comun'
            elif(self.start_view.categoriaDiario == 'Aviso Especial'):
                return 'aviso_especial'
            elif(self.start_view.categoriaDiario == 'Funebre'):
                if(self.producto.producto.default_uom.symbol != 'cm'):
                    return 'funebre_comun'
                else:
                    return 'funebre_destacado'
            elif(self.start_view.categoriaDiario == 'Clasificado'):
                if(self.producto.producto.default_uom.symbol != 'cm'):
                    return 'clasif_comun'
                else:
                    return 'clasif_destacado'
            elif(self.start_view.categoriaDiario == 'Edicto'):
                return 'edicto'
            elif(self.start_view.categoriaDiario == 'Centimetros'):
                return 'centimetros'


    def transition_terminar_aviso_comun(self):
        if self.aviso_comun.apariciones!='1':
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            repeticion = self.aviso_comun.cant_apariciones*Decimal(self.aviso_comun.apariciones)
            desc = prod.name +', '+str(self.aviso_comun.cant_centimetros) +' centimetro/s por '+ str(self.aviso_comun.cant_columnas)+' columna/s.\n'
            #ubicacion
            ubic = ''
            porcent = 0
            if (self.aviso_comun.ubicacion == '6'):
                ubic = 'Ubicacion: Suplemento - '+ self.aviso_comun.suplemento +'\n'
            elif (self.aviso_comun.ubicacion == '0'):
                ubic = 'Ubicacion: Libre\n'
            elif (self.aviso_comun.ubicacion == '1'):
                porcent = 0.25
                ubic = 'Ubicacion: Pagina Par\nPagina: '+self.aviso_comun.nro_pag +'\n'
            elif (self.aviso_comun.ubicacion == '2'):
                porcent = 0.3
                ubic = 'Ubicacion: Pagina Impar\nPagina: '+self.aviso_comun.nro_pag +'\n'
            else:
                porcent = 0.5
                if (self.aviso_comun.ubicacion == '3'):
                    ubic = 'Ubicacion: Tapa\n'
                elif (self.aviso_comun.ubicacion == '4'):
                    ubic = 'Ubicacion: Central\n'
                else:
                    ubic = 'Ubicacion: Contratapa\n'
            #--------------------------------------------------------
            texto = 'TEXTO:\n'+ self.aviso_comun.descripcion.encode('utf-8')
            desc = desc.encode('utf-8') + ubic + texto
            precio_unitario=prod.list_price
            cant=self.aviso_comun.cant_centimetros * self.aviso_comun.cant_columnas
            nueva = 0
            fecha = self.aviso_comun.inicio
            medida = str(self.aviso_comun.cant_centimetros)+ 'x' + str(self.aviso_comun.cant_columnas) + '= ' + str(cant)
            for i in range(repeticion):
                nueva = self.crear_linea_producto(prod,precio_unitario,cant,desc)
                self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
                fecha = fecha +timedelta(days=1)
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            precio_recargo = 0
            if (self.aviso_comun.ubicacion != '0') and (self.aviso_comun.ubicacion != '6'):
                #si es distintode libre o suplemento tiene un recargo
                pr = productos(productos.search([('name', '=', 'Recargo')])[0])
                precio_recargo = (Decimal(precio) * Decimal(porcent))
                self.crear_linea_recargo(pr,precio_recargo,ubic)
            if (self.aviso_comun.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.aviso_comun.motivo
                if(self.aviso_comun.tipo_bonif=='p'):
                    porcent = (self.aviso_comun.valor)/Decimal('100')
                    precio_parcial = precio + precio_recargo
                    monto = Decimal('-1')*(Decimal(precio_parcial) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.aviso_comun.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_aviso_comun'

    def transition_terminar_edicion_aviso_comun(self):
        productos = Pool().get('product.product')
        prod = self.producto.producto.products[0]
        repeticion = self.aviso_comun.cant_apariciones*Decimal(self.aviso_comun.apariciones)
        desc = prod.name +', '+str(self.aviso_comun.cant_centimetros) +' centimetro/s por '+ str(self.aviso_comun.cant_columnas)+' columna/s.\n'
        #ubicacion
        ubic = ''
        porcent = 0
        if (self.aviso_comun.ubicacion == '6'):
            ubic = 'Ubicacion: Suplemento - '+ self.aviso_comun.suplemento +'\n'
        elif (self.aviso_comun.ubicacion == '0'):
            ubic = 'Ubicacion: Libre\n'
        elif (self.aviso_comun.ubicacion == '1'):
            porcent = 0.25
            ubic = 'Ubicacion: Pagina Par\nPagina: '+self.aviso_comun.nro_pag +'\n'
        elif (self.aviso_comun.ubicacion == '2'):
            porcent = 0.3
            ubic = 'Ubicacion: Pagina Impar\nPagina: '+self.aviso_comun.nro_pag +'\n'
        else:
            porcent = 0.5
            if (self.aviso_comun.ubicacion == '3'):
                ubic = 'Ubicacion: Tapa\n'
            elif (self.aviso_comun.ubicacion == '4'):
                ubic = 'Ubicacion: Central\n'
            else:
                ubic = 'Ubicacion: Contratapa\n'
        #--------------------------------------------------------
        texto = 'TEXTO:\n' + self.aviso_comun.descripcion.encode('utf-8')
        desc = desc.encode('utf-8') + ubic + texto
        precio_unitario=prod.list_price
        cant=self.aviso_comun.cant_centimetros * self.aviso_comun.cant_columnas
        nueva = 0
        fecha = self.edicion_aviso_comun.fecha
        medida = str(self.aviso_comun.cant_centimetros) + 'x' + str(self.aviso_comun.cant_columnas) + '= ' + str(cant)
        nueva = self.crear_linea_producto(prod,precio_unitario,cant,desc)
        self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)

        #se calcula el precio
        if self.edicion_aviso_comun.cant_apariciones==self.aviso_comun.cant_apariciones:
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            precio_recargo = 0
            if (self.aviso_comun.ubicacion != '0') and (self.aviso_comun.ubicacion != '6'):
                #si es distintode libre o suplemento tiene un recargo
                pr = productos(productos.search([('name', '=', 'Recargo')])[0])
                precio_recargo = (Decimal(precio) * Decimal(porcent))
                self.crear_linea_recargo(pr,precio_recargo,ubic)
            if (self.aviso_comun.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.aviso_comun.motivo
                if(self.aviso_comun.tipo_bonif=='p'):
                    porcent = (self.aviso_comun.valor)/Decimal('100')
                    precio_parcial = precio + precio_recargo
                    monto = Decimal('-1')*(Decimal(precio_parcial) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.aviso_comun.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_aviso_comun'


    def transition_terminar_aviso_especial(self):
        if self.aviso_especial.apariciones!='1':
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            repeticion = self.aviso_especial.cant_apariciones*Decimal(self.aviso_especial.apariciones)
            desc = prod.name +', '+str(self.aviso_especial.cant_centimetros) +' centimetro/s por '+ str(self.aviso_especial.cant_columnas)+' columna/s.\n'
            ubic = 'Ubicacion: Libre\n'
            texto = 'TEXTO:\n' + self.aviso_especial.descripcion.encode('utf-8')
            desc = desc.encode('utf-8') + ubic + texto
            nueva = 0
            precio_unitario = prod.list_price
            fecha = self.aviso_especial.inicio
            cantidad = Decimal(self.aviso_especial.cant_centimetros) * Decimal(self.aviso_especial.cant_columnas)
            medida = str(self.aviso_especial.cant_centimetros) + 'x' + str(self.aviso_especial.cant_columnas) + '= ' + str(cantidad)
            for i in range(repeticion):
                nueva = self.crear_linea_producto(prod,precio_unitario,'1',desc)
                #    AGREGO PUBLICACION Y EDICION
                self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
                fecha = fecha +timedelta(days=1)
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.aviso_especial.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.aviso_especial.motivo
                if(self.aviso_especial.tipo_bonif=='p'):
                    porcent = (self.aviso_especial.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.aviso_especial.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_aviso_especial'

    def transition_terminar_edicion_aviso_especial(self):
        productos = Pool().get('product.product')
        prod = self.producto.producto.products[0]
        repeticion = self.aviso_especial.cant_apariciones*Decimal(self.aviso_especial.apariciones)
        desc = prod.name +', '+str(self.aviso_especial.cant_centimetros) +' centimetro/s por '+ str(self.aviso_especial.cant_columnas)+' columna/s.\n'
        ubic = 'Ubicacion: Libre\n'
        texto = 'TEXTO:\n' + self.aviso_especial.descripcion.encode('utf-8')
        desc = desc.encode('utf-8') + ubic + texto
        precio_unitario = prod.list_price
        fecha = self.edicion_aviso_especial.fecha
        cantidad = Decimal(self.aviso_especial.cant_centimetros) * Decimal(self.aviso_especial.cant_columnas)
        medida = str(self.aviso_especial.cant_centimetros) + 'x' + str(self.aviso_especial.cant_columnas) + '= ' + str(cantidad)
        nueva = 0
        nueva = self.crear_linea_producto(prod,precio_unitario,'1',desc)
        self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)

        #se calcula el precio
        if self.edicion_aviso_especial.cant_apariciones==self.aviso_especial.cant_apariciones:
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.aviso_especial.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.aviso_especial.motivo
                if(self.aviso_especial.tipo_bonif=='p'):
                    porcent = (self.aviso_especial.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.aviso_especial.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_aviso_especial'

    def transition_terminar_funebre_comun(self):
        if self.funebre_comun.apariciones!='1':
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            repeticion = self.funebre_comun.cant_apariciones*Decimal(self.funebre_comun.apariciones)
            desc = prod.name +', durante '  + str(repeticion) + ' dias.\n'
            texto = 'TEXTO:\n' + self.funebre_comun.descripcion.encode('utf-8')
            ubic = 'Ubicacion: Libre\n'
            desc = desc.encode('utf-8') + ubic + texto
            precio_unitario = prod.list_price
            nueva = 0
            fecha = self.funebre_comun.inicio
            medida = "Unidad= 1"
            for i in range(repeticion):
                nueva = self.crear_linea_producto(prod,precio_unitario,'1',desc)
                self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
                fecha = fecha +timedelta(days=1)
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.funebre_comun.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.funebre_comun.motivo
                if(self.funebre_comun.tipo_bonif=='p'):
                    porcent = (self.funebre_comun.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.funebre_comun.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_funebre_comun'


    def transition_terminar_edicion_funebre_comun(self):
        productos = Pool().get('product.product')
        prod = self.producto.producto.products[0]
        repeticion = self.funebre_comun.cant_apariciones*Decimal(self.funebre_comun.apariciones)
        desc = prod.name +', durante '  + str(repeticion) + ' dias.\n'
        texto = 'TEXTO:\n' + self.funebre_comun.descripcion.encode('utf-8')
        ubic = 'Ubicacion: Libre\n'
        desc = desc.encode('utf-8') + ubic + texto
        precio_unitario = prod.list_price
        nueva = 0
        fecha = self.edicion_funebre_comun.fecha
        medida = "Unidad= 1"
        nueva = self.crear_linea_producto(prod,precio_unitario,'1',desc)
        self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
            #se calcula el precio
        if self.edicion_funebre_comun.cant_apariciones==self.funebre_comun.cant_apariciones:
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.funebre_comun.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.funebre_comun.motivo
                if(self.funebre_comun.tipo_bonif=='p'):
                    porcent = (self.funebre_comun.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.funebre_comun.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_funebre_comun'


    def transition_terminar_funebre_destacado(self):
        if self.funebre_destacado.apariciones!='1':
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            repeticion = self.funebre_destacado.cant_apariciones*Decimal(self.funebre_destacado.apariciones)
            desc = prod.name +', '+str(self.funebre_destacado.cant_centimetros) +' centimetro/s por '+ str(self.funebre_destacado.cant_columnas)+' columna/s.\n'
            texto = 'TEXTO:\n' + self.funebre_destacado.descripcion.encode('utf-8')
            ubic = 'Ubicacion: Libre\n'
            desc = desc.encode('utf-8') + ubic + texto
            precio_unitario = prod.list_price
            cantidad = self.funebre_destacado.cant_centimetros * self.funebre_destacado.cant_columnas
            nueva = 0
            fecha = self.funebre_destacado.inicio
            medida = str(self.funebre_destacado.cant_centimetros) +'x'+ str(self.funebre_destacado.cant_columnas) + '= ' + str(cantidad)
            for i in range(repeticion):
                nueva = self.crear_linea_producto(prod,precio_unitario,cantidad,desc)
                self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
                fecha = fecha +timedelta(days=1)
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.funebre_destacado.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.funebre_destacado.motivo
                if(self.funebre_destacado.tipo_bonif=='p'):
                    porcent = (self.funebre_destacado.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.funebre_destacado.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_funebre_destacado'

    def transition_terminar_edicion_funebre_destacado(self):
        productos = Pool().get('product.product')
        prod = self.producto.producto.products[0]
        repeticion = self.funebre_destacado.cant_apariciones*Decimal(self.funebre_destacado.apariciones)
        desc = prod.name +', '+str(self.funebre_destacado.cant_centimetros) +' centimetro/s por '+ str(self.funebre_destacado.cant_columnas)+' columna/s durante '  + str(repeticion) + ' dias.\n'
        texto = 'TEXTO:\n' + self.funebre_destacado.descripcion.encode('utf-8')
        ubic = 'Ubicacion: Libre\n'
        desc = desc.encode('utf-8') + ubic + texto
        precio_unitario = prod.list_price
        cantidad = self.funebre_destacado.cant_centimetros * self.funebre_destacado.cant_columnas
        nueva = 0
        fecha = self.edicion_funebre_destacado.fecha
        medida = str(self.funebre_destacado.cant_centimetros) +'x'+ str(self.funebre_destacado.cant_columnas) + '= ' + str(cantidad)
        nueva = self.crear_linea_producto(prod,precio_unitario,cantidad,desc)
        self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
        if self.edicion_funebre_destacado.cant_apariciones==self.funebre_destacado.cant_apariciones:
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.funebre_destacado.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.funebre_destacado.motivo
                if(self.funebre_destacado.tipo_bonif=='p'):
                    porcent = (self.funebre_destacado.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.funebre_destacado.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_funebre_destacado'

    def transition_terminar_clasif_comun(self):
        if self.clasif_comun.apariciones!='1':
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            cant = 1
            index = 0
            repeticion = self.clasif_comun.cant_apariciones*Decimal(self.clasif_comun.apariciones)
            for c in self.clasif_comun.descripcion:
                index+=1
                if (index>35 or c=='\n'):
                    cant+=1
                    index=0
            desc = prod.name +', de '+str(cant)+' linea/s.\n'
            tipo = 'Tipo: ' + self.clasif_comun.tipo.encode('utf-8')
            ubic = 'Ubicacion: Libre\n'
            texto = 'TEXTO:\n' + self.clasif_comun.descripcion.encode('utf-8')
            desc = desc.encode('utf-8') + tipo +'\n' + texto
            precio_unitario = prod.list_price
            nueva = 0
            fecha = self.clasif_comun.inicio
            medida = 'Lineas= ' + str(cant)
            for i in range(repeticion):
                nueva = self.crear_linea_producto(prod,precio_unitario,cant,desc)
                self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
                fecha = fecha +timedelta(days=1)
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.clasif_comun.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.clasif_comun.motivo
                if(self.clasif_comun.tipo_bonif=='p'):
                    porcent = (self.clasif_comun.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.clasif_comun.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_clasif_comun'


    def transition_terminar_edicion_clasif_comun(self):
        productos = Pool().get('product.product')
        prod = self.producto.producto.products[0]
        cant = 1
        index = 0
        repeticion = self.clasif_comun.cant_apariciones*Decimal(self.clasif_comun.apariciones)
        for c in self.clasif_comun.descripcion:
            index+=1
            if (index>35 or c=='\n'):
                cant+=1
                index=0
        desc = prod.name +', de '+str(cant)+' linea/s.\n'
        tipo = 'Tipo: ' + self.clasif_comun.tipo.encode('utf-8')
        ubic = 'Ubicacion: Libre\n'
        texto = 'TEXTO:\n' + self.clasif_comun.descripcion.encode('utf-8')
        desc = desc.encode('utf-8') + tipo +'\n' + texto
        precio_unitario = prod.list_price
        nueva = 0
        fecha = self.edicion_clasif_comun.fecha
        medida = 'Lineas= ' + str(cant)
        nueva = self.crear_linea_producto(prod,precio_unitario,cant,desc)
        self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
        if self.edicion_clasif_comun.cant_apariciones==self.clasif_comun.cant_apariciones:
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.clasif_comun.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.clasif_comun.motivo
                if(self.clasif_comun.tipo_bonif=='p'):
                    porcent = (self.clasif_comun.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.clasif_comun.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_clasif_comun'


    def transition_terminar_clasif_destacado(self):
        if self.clasif_destacado.apariciones!='1':
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            repeticion = self.clasif_destacado.cant_apariciones*Decimal(self.clasif_destacado.apariciones)
            desc = prod.name +', '+str(self.clasif_destacado.cant_centimetros) +' centimetro/s por '+ str(self.clasif_destacado.cant_columnas)+' columna/s.\n'
            tipo = 'Tipo: ' + self.clasif_destacado.tipo.encode('utf-8')
            texto = 'TEXTO:\n' + self.clasif_destacado.descripcion.encode('utf-8')
            ubic = 'Ubicacion: Libre\n'
            desc = desc.encode('utf-8') + tipo + '\n' + texto
            precio_unitario = prod.list_price
            cantidad = Decimal(self.clasif_destacado.cant_centimetros) * Decimal(self.clasif_destacado.cant_columnas)
            nueva = 0
            fecha = self.clasif_destacado.inicio
            medida = str(self.clasif_destacado.cant_centimetros) +'x'+ str(self.clasif_destacado.cant_columnas) + '= ' + str(cantidad)
            for i in range(repeticion):
                nueva = self.crear_linea_producto(prod,precio_unitario,cantidad,desc)
                self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
                fecha = fecha +timedelta(days=1)
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.clasif_destacado.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.clasif_destacado.motivo
                if(self.clasif_destacado.tipo_bonif=='p'):
                    porcent = (self.clasif_destacado.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.clasif_destacado.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_clasif_destacado'

    def transition_terminar_edicion_clasif_destacado(self):
        productos = Pool().get('product.product')
        prod = self.producto.producto.products[0]
        repeticion = self.clasif_destacado.cant_apariciones*Decimal(self.clasif_destacado.apariciones)
        desc = prod.name +', '+str(self.clasif_destacado.cant_centimetros)+' centimetro/s por '+str(self.clasif_destacado.cant_columnas)+' columna/s.\n'
        tipo = 'Tipo: ' + self.clasif_destacado.tipo.encode('utf-8')
        texto = 'TEXTO:\n' + self.clasif_destacado.descripcion.encode('utf-8')
        ubic = 'Ubicacion: Libre\n'
        desc = desc.encode('utf-8') + tipo + '\n' + texto
        precio_unitario = prod.list_price
        cantidad = Decimal(self.clasif_destacado.cant_centimetros) * Decimal(self.clasif_destacado.cant_columnas)
        nueva = 0
        fecha = self.edicion_clasif_destacado.fecha
        medida = str(self.clasif_destacado.cant_centimetros) +'x'+ str(self.clasif_destacado.cant_columnas) + '= ' + str(cantidad)
        nueva = self.crear_linea_producto(prod,precio_unitario,cantidad,desc)
        self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
        if self.edicion_clasif_destacado.cant_apariciones==self.clasif_destacado.cant_apariciones:
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.clasif_destacado.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.clasif_destacado.motivo
                if(self.clasif_destacado.tipo_bonif=='p'):
                    porcent = (self.clasif_destacado.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.clasif_destacado.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_clasif_destacado'


    def transition_terminar_edicto(self):
        if self.edicto.apariciones!='1':
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            repeticion = self.edicto.cant_apariciones*Decimal(self.edicto.apariciones)
            lineas = str(self.edicto.cant_lineas)
            desc = prod.name +', de '+lineas+' lineas.'
            texto = 'TEXTO:\n' + self.edicto.descripcion.encode('utf-8')
            ubic = 'Ubicacion: Libre\n'
            desc = desc.encode('utf-8')+ ubic + texto
            nueva = 0
            fecha = self.edicto.inicio
            medida = "Lineas= "+ str(lineas)
            for i in range(repeticion):
                nueva = self.crear_linea_producto(prod,prod.list_price,Decimal(lineas),desc)
                self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
                fecha = fecha +timedelta(days=1)
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.edicto.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.edicto.motivo
                if(self.edicto.tipo_bonif=='p'):
                    porcent = (self.edicto.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.edicto.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_edicto'

    def transition_terminar_edicion_edicto(self):
        productos = Pool().get('product.product')
        prod = self.producto.producto.products[0]
        repeticion = self.edicto.cant_apariciones*Decimal(self.edicto.apariciones)
        lineas = str(self.edicto.cant_lineas)
        desc = prod.name +', de '+lineas+' lineas.'
        texto = 'TEXTO:\n' + self.edicto.descripcion.encode('utf-8')
        ubic = 'Ubicacion: Libre\n'
        desc = desc.encode('utf-8') + ubic + texto
        nueva = 0
        fecha = self.edicion_edicto.fecha
        medida = "Lineas= "+ str(lineas)
        nueva = self.crear_linea_producto(prod,prod.list_price,Decimal(lineas),desc)
        self.crear_linea_publicacion_diario(nueva,prod,desc,medida,fecha)
        if self.edicion_edicto.cant_apariciones==self.edicto.cant_apariciones:
            #se calcula el precio
            cant = Decimal(nueva.quantity) * repeticion
            precio = cant * Decimal(nueva.unit_price)
            if (self.edicto.bonificacion):
                pr = productos(productos.search([('name', '=', 'Bonificacion')])[0])
                monto = 0
                motivo = self.edicto.motivo
                if(self.edicto.tipo_bonif=='p'):
                    porcent = (self.edicto.valor)/Decimal('100')
                    monto = Decimal('-1')*(Decimal(precio) * Decimal(porcent))
                else:
                    monto = Decimal('-1')*self.edicto.valor
                self.crear_linea_bonificacion(pr,monto,motivo)
            return 'finalizar'
        else:
            return 'edicion_edicto'


    def transition_terminar_centimetros(self):
            productos = Pool().get('product.product')
            prod = self.producto.producto.products[0]
            cantidad = Decimal(self.centimetros.cant_centimetros) * Decimal(self.centimetros.cant_columnas)
            precio_unitario = Decimal(self.centimetros.precio_cm)
            total = precio_unitario * cantidad
            texto = 'DESCRIPCION:\n' + self.centimetros.descripcion.encode('utf-8')
            desc = 'Cantidad de centimetros totales: '+ str(cantidad) + '\nPrecio por centimetro: '+str(precio_unitario)+'\nTotal: '+ str(total)+'\n'+texto
            #Date = Pool().get('ir.date')
            #fecha = Date.today()
            nueva = 0
            nueva = self.crear_linea_producto(prod,total,'1',desc)
            self.crear_linea_publicacion_diario_centimetros(nueva,prod,desc,str(cantidad))
            return 'finalizar'
