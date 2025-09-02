from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError

class InduccionLineaEmpleado(models.Model):
    _name = 'induccion.linea.empleado'
    _description = 'Empleado en Inducción'

    induccion_id = fields.Many2one('induccion.registro', string='Inducción', ondelete='cascade')
    empleado_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    asistio = fields.Boolean(string="¿Asistió?")
    estatus = fields.Selection([
        ('asistio', 'Asistió'),
        ('no_asistio', 'No Asistió'),
        ('justificado', 'Justificado'),
    ], string='Estatus', default='no_asistio')

    motivo = fields.Text(string="Motivo", help="Indique la razón cuando se seleccione 'Justificado'")
    observacion = fields.Text(string="Observación", help="Comentarios adicionales si el estatus es 'Justificado'")

    # =====================================
    # NUEVO: Número único de control
    # =====================================
    control_numero = fields.Char(
        string="Número de Control",
        readonly=True,
        copy=False,
        index=True,
        default="Nuevo"
    )

    # =====================================
    # Campo computado para los items del participante
    # =====================================
    item_ids = fields.One2many(
        'induccion.linea.item',
        compute='_compute_item_ids',
        string='Items de Inducción'
    )

    @api.depends('induccion_id')
    def _compute_item_ids(self):
        for record in self:
            if record.induccion_id:
                record.item_ids = self.env['induccion.linea.item'].search([
                    ('registro_id', '=', record.induccion_id.id)
                ])
            else:
                record.item_ids = self.env['induccion.linea.item']

    # =====================================
    # Reglas de negocio
    # =====================================
    @api.onchange('asistio')
    def _onchange_asistio(self):
        for record in self:
            if record.asistio:
                record.estatus = 'asistio'
            else:
                if record.estatus == 'asistio':
                    record.estatus = 'no_asistio'

    @api.constrains('estatus', 'observacion')
    def _check_observacion_if_justificado(self):
        for record in self:
            if record.estatus == 'justificado' and not record.observacion:
                raise ValidationError("Debe ingresar una observación cuando el estatus es 'Justificado'.")

    def write(self, vals):
        campos_prohibidos = {'empleado_id', 'induccion_id'}
        if any(campo in vals for campo in campos_prohibidos):
            raise ValidationError("No está permitido modificar los datos del participante.")
        return super().write(vals)

    @api.model
    def create(self, vals):
        # Seguridad para creación manual
        if not self.env.context.get('allow_create_linea_empleado'):
            raise ValidationError("No está permitido agregar participantes manualmente.")

        # Asignar número de control único
        if vals.get('control_numero', 'Nuevo') == 'Nuevo':
            vals['control_numero'] = self.env['ir.sequence'].next_by_code('induccion.linea.empleado.seq') or 'Nuevo'

        return super().create(vals)

    def unlink(self):
        raise ValidationError("No está permitido eliminar participantes.")

    # =====================================
    # Método para generar PDF individual
    # =====================================
    def action_print_acta_individual(self):
        """Genera el PDF solo de este participante"""
        if not self:
            raise UserError("No hay participante seleccionado para imprimir el acta.")
        return self.env.ref('induccion_emple.action_report_acta_participante').report_action(self)
