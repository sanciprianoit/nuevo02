from odoo import models, fields, api

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

    # 👥 Participantes con estatus
    linea_empleado_ids = fields.One2many(
        'induccion.linea.empleado',
        'induccion_id',
        string='Participantes con Estatus'
    )

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

    item_ids = fields.One2many(
        'induccion.item',
        'registro_id',
        string='Items Copiados'
    )

    tipo_item_ids = fields.One2many(
        'induccion.item',
        compute='_compute_tipo_item_ids',
        string='Items del Tipo de Inducción',
        store=False
    )

    @api.depends('tipo_induccion_id')
    def _compute_tipo_item_ids(self):
        for record in self:
            record.tipo_item_ids = record.tipo_induccion_id.item_ids
