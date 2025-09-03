from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InduccionRegistro(models.Model):
    _name = 'induccion.registro'
    _description = 'Registro de Inducciones'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    nombre = fields.Char(string='Nombre de la Inducción', required=True)
    fecha = fields.Date(string='Fecha de Inducción', required=True)
    tipo_induccion_id = fields.Many2one('induccion.tipo', string='Tipo de Inducción')
    tipo_registro = fields.Selection([
        ('Induccion', 'Inducción'),
        ('Otro', 'Otro')
    ], string='Tipo de Registro', required=True)

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

    item_line_ids = fields.One2many(
        'induccion.linea.item',
        'registro_id',
        string='Items del Registro'
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

    def unlink(self):
        for record in self:
            # 🔐 Eliminación controlada de líneas hijas con validaciones contextuales
            record.linea_empleado_ids.with_context(allow_unlink_empleado_acta=True).unlink()
            record.item_line_ids.with_context(allow_unlink_linea_item=True).unlink()
            super(InduccionRegistro, record).unlink()
        return True

    def action_imprimir_acta(self):
        """Genera un PDF del registro de inducción"""
        if not self.linea_empleado_ids:
            raise UserError(_("No hay participantes para imprimir el acta."))
        return self.env.ref('induccion_emple.action_report_acta_induccion').report_action(self)

    def action_print_actas_empleados(self):
        """Genera PDFs individuales de cada participante"""
        self.ensure_one()
        empleados = self.linea_empleado_ids
        if not empleados:
            raise UserError(_("No hay participantes en este registro para imprimir actas."))

        report_action_list = []
        for empleado in empleados:
            if not empleado:
                continue
            action = self.env.ref('induccion_emple.action_report_acta_participante').report_action(empleado)
            report_action_list.append(action)

        return report_action_list[0] if report_action_list else False
