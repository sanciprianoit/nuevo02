# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    acta_id = fields.Many2one('induccion_emple.acta_capacitacion', string='Acta de Capacitación')

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
        self.ensure_one()

        if not self._origin or not self._origin.id:
            raise ValidationError("Debes guardar el registro antes de imprimir los ítems.")

        if self.tipo_registro != 'induccion':
            raise ValidationError("Este botón solo aplica para registros de tipo inducción.")

        if not all([
            self.tipo_induccion_id,
            self.fecha_asignacion,
            self.capacitador_id,
            self.empleado_ids
        ]):
            raise ValidationError("Debes completar todos los campos requeridos antes de imprimir los ítems.")

        return self.env.ref('induccion_reportes.action_report_asignacion_items').report_action(self)

    def print_asignacion_induccion_participantes(self):
        self.ensure_one()

        if not self._origin or not self._origin.id:
            raise ValidationError("Debes guardar el registro antes de imprimir los participantes.")

        if self.tipo_registro != 'induccion':
            raise ValidationError("Este botón solo aplica para registros de tipo inducción.")

        if not all([
            self.tipo_induccion_id,
            self.fecha_asignacion,
            self.capacitador_id,
            self.empleado_ids
        ]):
            raise ValidationError("Debes completar todos los campos requeridos antes de imprimir los participantes.")

        return self.env.ref('induccion_reportes.action_report_asignacion_participantess').report_action(self)

    def action_imprimir_acta_capacitacion(self):
        self.ensure_one()

        if not self._origin or not self._origin.id:
            raise ValidationError("Debes guardar el registro antes de imprimir el acta.")

        if self.tipo_registro != 'capacitacion':
            raise ValidationError("Este botón solo aplica para registros de tipo capacitación.")

        if not all([
            self.tipo_capacitacion_id,
            self.fecha_asignacion,
            self.capacitador_id,
            self.empleado_ids
        ]):
            raise ValidationError("Debes completar todos los campos requeridos antes de imprimir el acta de capacitación.")

        return self.env.ref('induccion_emple.action_report_asignacion_capacitacion').report_action(self)

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
            registro = self.env['induccion.registro'].create({
                'nombre': asignacion.tipo_nombre,
                'fecha': asignacion.fecha_asignacion,
                'tipo_induccion_id': asignacion.tipo_induccion_id.id,
                'capacitador_id': asignacion.capacitador_id.id,
                'empresa_externa': asignacion.capacitador_empresa_externa,
                'descripcion': asignacion.descripcion,
                'tipo_registro': 'Induccion',
                'asignacion_id': asignacion.id
            })

            for empleado in asignacion.empleado_ids:
                self.env['induccion.linea.empleado'].with_context(
                    allow_create_linea_empleado=True
                ).create({
                    'induccion_id': registro.id,
                    'empleado_id': empleado.id,
                    'asistio': False,
                    'estatus': 'no_asistio'
                })

        elif asignacion.tipo_registro == 'capacitacion':
            acta = self.env['induccion_emple.acta_capacitacion'].create({
                'asignacion_id': asignacion.id,
                'capacitador_id': asignacion.capacitador_id.id,
                'tipo_id': asignacion.tipo_capacitacion_id.id,
                'fecha': asignacion.fecha_asignacion,
            })

            asistencia_records = []
            for empleado in asignacion.empleado_ids:
                asistencia_records.append((0, 0, {
                    'participante_id': empleado.id,
                    'status': 'presente',
                    'observacion': '',
                }))
            acta.asistencia_ids = asistencia_records
            asignacion.acta_id = acta.id

        return asignacion

    @api.constrains('tipo_registro', 'tipo_induccion_id', 'tipo_capacitacion_id')
    def _check_tipo_registro(self):
        for record in self:
            if record.tipo_registro == 'induccion' and not record.tipo_induccion_id:
                raise ValidationError("El tipo de inducción es obligatorio para una inducción.")
            if record.tipo_registro == 'capacitacion' and not record.tipo_capacitacion_id:
                raise ValidationError("El tipo de capacitación es obligatorio para una capacitación.")

    def action_generar_acta(self):
        self.ensure_one()
        acta = self.env['induccion_emple.acta_capacitacion'].create({
            'asignacion_id': self.id,
            'capacitador_id': self.capacitador_id.id,
            'tipo_id': self.tipo_capacitacion_id.id,
            'fecha': self.fecha_asignacion,
        })

        asistencia_records = []
        for empleado in self.empleado_ids:
            asistencia_records.append((0, 0, {
                'participante_id': empleado.id,
                'status': 'presente',
                'observacion': '',
            }))
        acta.asistencia_ids = asistencia_records
        self.acta_id = acta.id

        return {
            'name': 'Acta de Capacitación',
            'type': 'ir.actions.act_window',
            'res_model': 'induccion_emple.acta_capacitacion',
            'view_mode': 'form',
            'res_id': acta.id,
            'target': 'current',
        }
