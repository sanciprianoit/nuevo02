# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ActaCapacitacion(models.Model):
    _name = 'induccion_emple.acta_capacitacion'
    _description = 'Acta de Capacitación'
    
    name = fields.Char(string='Referencia del Acta', compute='_compute_name', store=True)
    
    # Campo para la relación con la asignación
    asignacion_id = fields.Many2one('induccion_emple.asignacion', string='Asignación')
    
    # Campos que se llenarán automáticamente desde la asignación
    capacitador_id = fields.Many2one(
        'induccion_emple.capacitador', 
        string='Capacitador/Instructor',
        related='asignacion_id.capacitador_id',
        store=True, 
        readonly=True
    )
    
    tipo_id = fields.Many2one(
        'capacitacion.tipo', 
        string='Tipo de Capacitación',
        related='asignacion_id.tipo_capacitacion_id',
        store=True,
        readonly=True
    )

    fecha = fields.Date(
        string='Fecha de Asignación',
        related='asignacion_id.fecha_asignacion',
        store=True,
        readonly=True
    )

    fecha_ejecucion = fields.Date(
        string='Fecha de Ejecución'
    )
    
    # Campo para la relación con el nuevo modelo AsistenciaParticipante
    asistencia_ids = fields.One2many(
        'induccion_emple.asistencia_participante', 
        'acta_id', 
        string='Asistencia de Participantes'
    )
    
    # La relación con el modelo PautaActa
    pauta_ids = fields.One2many(
        'induccion_emple.pauta_acta',
        'acta_id',
        string='Pautas Impartidas'
    )

    @api.depends('asignacion_id')
    def _compute_name(self):
        """Calcula el nombre del acta basándose en el número de control de la asignación."""
        for record in self:
            if record.asignacion_id:
                record.name = f"Acta de {record.asignacion_id.control_numero}"
            else:
                record.name = False

    @api.constrains('fecha_ejecucion', 'pauta_ids')
    def _check_acta_validations(self):
        """Valida que la fecha de ejecución sea correcta y que se hayan agregado pautas."""
        for record in self:
            # Validación 1: Fecha de ejecución es obligatoria.
            if not record.fecha_ejecucion:
                raise ValidationError("Debe ingresar la fecha de culminación de la capacitación.")
            
            # Validación 2: Fecha de ejecución no es menor que la fecha de asignación.
            if record.fecha and record.fecha_ejecucion < record.fecha:
                raise ValidationError("La fecha de culminación no puede ser anterior a la fecha de asignación.")
            
            # Validación 3: Debe haber al menos una pauta agregada.
            if not record.pauta_ids:
                raise ValidationError("Debe agregar al menos una pauta antes de guardar el acta.")

# Nuevo modelo para la asistencia de participantes
class AsistenciaParticipante(models.Model):
    _name = 'induccion_emple.asistencia_participante'
    _description = 'Asistencia de Participantes a la Capacitación'

    acta_id = fields.Many2one('induccion_emple.acta_capacitacion', string='Acta de Capacitación', required=True, ondelete='cascade')
    participante_id = fields.Many2one('hr.employee', string='Participante', required=True)

    status = fields.Selection([
        ('presente', 'Presente'),
        ('ausente', 'Ausente')
    ], string='Estatus', required=True, default='presente')
    
    observacion = fields.Text(string='Observación')

    @api.constrains('status', 'observacion')
    def _check_observacion_ausente(self):
        """Valida que la observación sea obligatoria si el estatus es 'Ausente'."""
        for record in self:
            if record.status == 'ausente' and not record.observacion:
                raise ValidationError("El campo 'Observación' es obligatorio si el estatus es 'Ausente'.")

# Nuevo modelo para las pautas
class PautaActa(models.Model):
    _name = 'induccion_emple.pauta_acta'
    _description = 'Pautas Impartidas en el Acta de Capacitación'

    acta_id = fields.Many2one('induccion_emple.acta_capacitacion', string='Acta de Capacitación', required=True, ondelete='cascade')
    titulo = fields.Char(string='Título de la Pauta', required=True)
    observacion = fields.Text(string='Observación')

    @api.constrains('observacion')
    def _check_observacion_obligatoria(self):
        """Valida que la observación sea obligatoria si se crea una pauta."""
        for record in self:
            if not record.observacion:
                raise ValidationError("El campo 'Observación' es obligatorio al agregar una pauta.")