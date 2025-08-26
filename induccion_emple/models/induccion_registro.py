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

    # Participantes con estatus
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

    # ----------------------------
    # Items del registro (modelo intermedio)
    # ----------------------------
    item_line_ids = fields.One2many(
        'induccion.linea.item',
        'registro_id',
        string='Items del Registro'
    )

    # Items del tipo de inducción (solo lectura)
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

    # ----------------------------
    # Crear items del registro automáticamente al crear la inducción
    # ----------------------------
    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.tipo_induccion_id:
            for item in record.tipo_induccion_id.item_ids:
                self.env['induccion.linea.item'].with_context(
                    allow_create_linea_item=True
                ).create({
                    'registro_id': record.id,
                    'item_id': item.id,
                    'estatus': 'pendiente'
                })
        return record

    # ----------------------------
    # Eliminar registro de inducción junto con items en cascada
    # ----------------------------
    def unlink(self):
        # Los items asociados se eliminan automáticamente por ondelete='cascade'
        return super().unlink()
