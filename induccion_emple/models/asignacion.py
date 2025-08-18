from odoo import models, fields, api

class Asignacion(models.Model):
    _name = 'induccion_emple.asignacion'
    _description = 'Asignación de Inducción y Capacitación'
    _order = 'control_numero desc'

    control_numero = fields.Char(
        string='Número de Control',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo'
    )

    tipo_registro = fields.Selection([
        ('induccion', 'Inducción'),
        ('capacitacion', 'Capacitación')
    ], string='Tipo de Registro', required=True, default='induccion')

    tipo_induccion_id = fields.Many2one(
        'induccion.tipo',
        string='Tipo de Inducción'
    )

    tipo_capacitacion_id = fields.Many2one(
        'capacitacion.tipo',
        string='Tipo de Capacitación'
    )

    fecha_asignacion = fields.Date(string='Fecha de Asignación', required=True)

    empleado_ids = fields.Many2many(
        'hr.employee',
        'asignacion_empleado_rel',
        'asignacion_id',
        'empleado_id',
        string='Empleados Asignados'
    )

    capacitador_id = fields.Many2one(
        'induccion_emple.capacitador',
        string='Capacitador/Instructor'
    )

    capacitador_empresa_externa = fields.Char(
        string="Empresa Externa",
        related='capacitador_id.empresa_externa',
        store=True,
        readonly=True,
    )

    descripcion = fields.Text(string='Descripción')

    def print_asignacion_induccion(self):
        return self.env.ref('induccion_reportes.action_report_asignacion_items').report_action(self)

    def print_asignacion_induccion_participantes(self):
        return self.env.ref('induccion_reportes.action_report_asignacion_participantess').report_action(self)

    @api.model
    def create(self, vals):
        if vals.get('control_numero', 'Nuevo') == 'Nuevo':
            if vals.get('tipo_registro') == 'capacitacion':
                seq = self.env['ir.sequence'].next_by_code('induccion_emple.capacitacion')
            else:
                seq = self.env['ir.sequence'].next_by_code('induccion_emple.asignacion')
            vals['control_numero'] = seq or '/'
        return super(Asignacion, self).create(vals)

    @api.constrains('tipo_registro', 'tipo_induccion_id', 'tipo_capacitacion_id')
    def _check_tipo_registro(self):
        for record in self:
            if record.tipo_registro == 'induccion' and not record.tipo_induccion_id:
                raise models.ValidationError("El tipo de inducción es obligatorio para una inducción.")
            if record.tipo_registro == 'capacitacion' and not record.tipo_capacitacion_id:
                raise models.ValidationError("El tipo de capacitación es obligatorio para una capacitación.")
