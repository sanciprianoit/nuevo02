from odoo import models, fields, api

class ItemInduccion(models.Model):
    _name = 'induccion.item'
    _description = 'Items de Inducción'
    
    name = fields.Char(string='Nombre del Item', required=True)
    descripcion = fields.Text(string='Descripción Detallada')
    tipo_id = fields.Many2one(
        'induccion.tipo', 
        string='Tipo de Inducción',
        required=True
    )
    obligatorio = fields.Boolean(string='Obligatorio', default=True)

    # 👇 Este es el campo que debes agregar
    registro_id = fields.Many2one(
        'induccion.registro',
        string='Registro de Inducción',
        ondelete='cascade'
    )
