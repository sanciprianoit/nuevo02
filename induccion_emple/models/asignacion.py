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

    tipo_induccion_id = fields.Many2one('induccion.tipo', string='Tipo de Inducción')
    tipo_capacitacion_id = fields.Many2one('capacitacion.tipo', string='Tipo de Capacitación')
    fecha_asignacion = fields.Date(string='Fecha de Asignación', required=True)

    empleado_ids = fields.Many2many(
        'hr.employee',
        'asignacion_empleado_rel',
        'asignacion_id',
        'empleado_id',
        string='Empleados Asignados'
    )

    capacitador_id = fields.Many2one('induccion_emple.capacitador', string='Capacitador/Instructor')

    capacitador_empresa_externa = fields.Char(
        string="Empresa Externa",
        related='capacitador_id.empresa_externa',
        store=True,
        readonly=True,
    )

    descripcion = fields.Text(string='Descripción')

    tipo_nombre = fields.Char(
        string='Tipo',
        compute='_compute_tipo_nombre',
        store=False
    )

    @api.depends('tipo_registro', 'tipo_induccion_id', 'tipo_capacitacion_id')
    def _compute_tipo_nombre(self):
        for record in self:
            if record.tipo_registro == 'induccion' and record.tipo_induccion_id:
                record.tipo_nombre = record.tipo_induccion_id.name
            elif record.tipo_registro == 'capacitacion' and record.tipo_capacitacion_id:
                record.tipo_nombre = record.tipo_capacitacion_id.name
            else:
                record.tipo_nombre = ''

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

        asignacion = super(Asignacion, self).create(vals)

        if asignacion.tipo_registro == 'induccion':
            self.env['induccion.registro'].create({
                'nombre': asignacion.tipo_nombre,
                'fecha': asignacion.fecha_asignacion,
                'tipo_induccion_id': asignacion.tipo_induccion_id.id,
                'empleados_ids': [(6, 0, asignacion.empleado_ids.ids)],
                'capacitador_id': asignacion.capacitador_id.id,
                'empresa_externa': asignacion.capacitador_empresa_externa,
                'descripcion': asignacion.descripcion,
                'tipo_registro': 'Induccion',
                'asignacion_id': asignacion.id
            })

        return asignacion

    @api.constrains('tipo_registro', 'tipo_induccion_id', 'tipo_capacitacion_id')
    def _check_tipo_registro(self):
        for record in self:
            if record.tipo_registro == 'induccion' and not record.tipo_induccion_id:
                raise models.ValidationError("El tipo de inducción es obligatorio para una inducción.")
            if record.tipo_registro == 'capacitacion' and not record.tipo_capacitacion_id:
                raise models.ValidationError("El tipo de capacitación es obligatorio para una capacitación.")
