from odoo import models, fields, api

class TipoInduccion(models.Model):
    _name = 'induccion.tipo'
    _description = 'Tipos de Inducción'
    _rec_name = 'name'
    
    name = fields.Char(string='Nombre del Tipo', required=True)
    descripcion = fields.Text(string='Descripción')
    activo = fields.Boolean(string='Activo', default=True)

    tipo_registro = fields.Selection([
        ('induccion', 'Inducción'),
        ('reinduccion', 'Reinducción')
    ], string='Tipo de Registro', required=True, help='Clasificación del tipo de inducción.')

    item_ids = fields.One2many(
        'induccion.item', 
        'tipo_id', 
        string='Items de Inducción'
    )
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El nombre del tipo debe ser único'),
    ]
