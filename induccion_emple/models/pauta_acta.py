from odoo import models, fields

class PautaActa(models.Model):
    _name = 'induccion_emple.pauta_acta'
    _description = 'Pautas Impartidas en el Acta de Capacitación'

    acta_id = fields.Many2one('induccion_emple.acta_capacitacion', string='Acta de Capacitación', required=True, ondelete='cascade')
    titulo = fields.Char(string='Título de la Pauta', required=True)
    observacion = fields.Text(string='Observación')