from odoo import models, fields, api

class TipoCapacitacion(models.Model):
    _name = 'capacitacion.tipo'
    _description = 'Tipos de Capacitación'
    
    name = fields.Char(string='Nombre del Tipo', required=True)
    descripcion = fields.Text(string='Descripción')
    activo = fields.Boolean(string='Activo', default=True)
   
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El nombre del tipo debe ser único'),
    ]