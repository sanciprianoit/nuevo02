from odoo import models, fields

class InduccionRegistro(models.Model):
    _name = 'induccion.registro'
    _description = 'Registro de Inducciones'

    nombre = fields.Char(string='Nombre de la Inducción', required=True)
    fecha = fields.Date(string='Fecha de Inducción', required=True)
    tipo_induccion_id = fields.Many2one('induccion.tipo', string='Tipo de Inducción')
    tipo_registro = fields.Selection([
        ('Induccion', 'Inducción'),
        ('Otro', 'Otro')
    ], string='Tipo de Registro', required=True)

    empleados_ids = fields.Many2many('hr.employee', string='Participantes')
    capacitador_id = fields.Many2one('induccion_emple.capacitador', string='Capacitador')
    empresa_externa = fields.Char(
        string='Empresa Externa',
        related='capacitador_id.empresa_externa',
        store=True
    )
    descripcion = fields.Text(string='Descripción')

    asignacion_id = fields.Many2one(
        'induccion_emple.asignacion',
        string='Asignación',
        readonly=True
    )

    control_numero = fields.Char(
        string='Número de Control',
        related='asignacion_id.control_numero',
        store=True,
        readonly=True
    )
