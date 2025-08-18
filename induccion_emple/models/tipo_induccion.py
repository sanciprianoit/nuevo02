from odoo import models, fields, api

class TipoInduccion(models.Model):
    _name = 'induccion.tipo'
    _description = 'Tipos de Inducción'
    _rec_name = 'name'
    
    name = fields.Char(string='Nombre del Tipo', required=True)
    descripcion = fields.Text(string='Descripción')
    activo = fields.Boolean(string='Activo', default=True)
   # obligatorio = fields.Boolean(string='Obligatorio', default=True)
    item_ids = fields.One2many(
        'induccion.item', 
        'tipo_id', 
        string='Items de Inducción'
    )
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El nombre del tipo debe ser único'),
    ]