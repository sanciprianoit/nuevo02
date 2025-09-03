from odoo import fields, models, api
from odoo.exceptions import ValidationError

class InduccionLineaItem(models.Model):
    _name = 'induccion.linea.item'
    _description = 'Item en Inducción'

    registro_id = fields.Many2one('induccion.registro', string='Registro de Inducción', ondelete='cascade')
    item_id = fields.Many2one('induccion.item', string='Item', required=True)
    estatus = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('omitido', 'Omitido')
    ], string='Estatus', default='pendiente')

    # Bloquear modificación del item o del registro
    def write(self, vals):
        campos_prohibidos = {'item_id', 'registro_id'}
        if any(campo in vals for campo in campos_prohibidos):
            raise ValidationError("No está permitido modificar el item o el registro del item.")
        return super().write(vals)

    # Bloquear creación manual directa
    @api.model
    def create(self, vals):
        if not self.env.context.get('allow_create_linea_item'):
            raise ValidationError("No está permitido agregar items manualmente.")
        return super().create(vals)

    # Bloquear eliminación manual, permitir desde el padre con contexto
    def unlink(self):
        if not self.env.context.get('allow_unlink_linea_item'):
            raise ValidationError("No está permitido eliminar items manualmente.")
        return super().unlink()
