# -*- coding: utf-8 -*-

from trytond.pool import Pool
from trytond.modules.company import CompanyReport
from trytond.model import Workflow,ModelSQL, ModelView
from datetime import timedelta


class Sale(Workflow, ModelSQL, ModelView):
    'Sale'
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._error_messages.update({
            'error_sale': 'Excepcion en confirmacion de venta o creacion de publicaciones'
            })

    @classmethod
    @ModelView.button
    @Workflow.transition('confirmed')
    def confirm(cls, sales):
        edicion = Pool().get('edicion.edicion')
        super(Sale, cls).confirm(sales)
        for s in sales:
            if (s.payment_term.name == 'Efectivo'):
                super(Sale, cls).process(sales)
                try:
                    publicacion_diario = Pool().get('edicion.publicacion_diario')
                    pub_pres_diario = Pool().get('edicion.publicacion_presupuestada_diario')
                    desactualizadas_diario= pub_pres_diario.search([('venta.state', '=', 'processing')])
                    for d in desactualizadas_diario:
                        edic = 0
                        try:
                            edic= edicion(edicion.search([('fecha', '=', d.fecha)])[0])
                        except:
                            edic=edicion.create([{
                            'fecha':d.fecha
                            }])[0]
                            edic.save()
                        pub_diario=""
                        Date = Pool().get('ir.date')
                        hoy = Date.today()
                        if(d.fecha>(hoy+timedelta(days=1))):
                            pub_diario = publicacion_diario.create([{
                                'termino_pago':d.venta.payment_term,
                                'linea':d.linea,
                                'cliente':d.cliente,
                                'producto' : d.producto,
                                'descrip' : d.linea.description,
                                'medidas' : d.medidas,
                                'ubicacion': d.ubicacion,
                                'edicion' : edic,
                                }])[0]
                        else:
                            pub_diario = publicacion_diario.create([{
                                'termino_pago':d.venta.payment_term,
                                'linea':d.linea,
                                'cliente':d.cliente,
                                'producto' : d.producto,
                                'descrip' : d.linea.description,
                                'medidas' : d.medidas,
                                'ubicacion': d.ubicacion,
                                'edicion' : edic,
                                'state':'reprogramar',
                                }])[0]
                        pub_diario.save()
                    for d in desactualizadas_diario:
                        pub_pres_diario.delete([d])
                except:
                    cls.raise_user_error('error_sale')
                try:
                    publicacion_radio = Pool().get('edicion.publicacion_radio')
                    pub_pres_radio = Pool().get('edicion.publicacion_presupuestada_radio')
                    desactualizadas_radio= pub_pres_radio.search([('venta.state', '=', 'processing')])
                    for d in desactualizadas_radio:
                        edic = 0
                        try:
                            edic= edicion(edicion.search([('fecha', '=', d.fecha)])[0])
                        except:
                            edic=edicion.create([{
                            'fecha':d.fecha
                            }])[0]
                            edic.save()
                        pub_radio = publicacion_radio.create([{
                            'linea':d.linea,
                            'cliente':d.cliente,
                            'producto' : d.producto,
                            'descrip' : d.linea.description,
                            'edicion' : edic,
                            'categoria':str(d.producto.category.name),
                            }])[0]
                        pub_radio.save()
                    for d in desactualizadas_radio:
                        pub_pres_radio.delete([d])
                except:
                    cls.raise_user_error('error_sale')
                try:
                    publicacion_digital = Pool().get('edicion.publicacion_digital')
                    edicion_publicacion_digital = Pool().get('edicion.edicion_publicacion_digital')
                    pub_pres_digital = Pool().get('edicion.publicacion_presupuestada_digital')
                    desactualizadas_digital= pub_pres_digital.search([('venta.state', '=', 'processing')])
                    for d in desactualizadas_digital:
                        fecha_aux = d.fecha
                        pub_digital = publicacion_digital.create([{
                            'linea':d.linea,
                            'cliente':d.cliente,
                            'producto' : d.producto,
                            'descrip' : d.linea.description,
                            'categoria':str(d.producto.category.name),
                            }])[0]
                        pub_digital.save()
                        for j in range(32):
                            edic = 0
                            try:
                                edic= edicion(edicion.search([('fecha', '=', fecha_aux)])[0])
                            except:
                                edic=edicion.create([{
                                'fecha':fecha_aux
                                }])[0]
                                edic.save()
                            ed_pub_digital = edicion_publicacion_digital.create([{
                                            'edicion_id':edic,
                                            'digital_id':pub_digital,
                                            }])[0]
                            ed_pub_digital.save()
                            fecha_aux = fecha_aux +timedelta(days=1)
                    for d in desactualizadas_digital:
                        pub_pres_digital.delete([d])
                except:
                    cls.raise_user_error('error_sale')
            else:
                s.state = 'processing'
                s.save()