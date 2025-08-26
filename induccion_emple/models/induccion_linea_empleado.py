from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
        if not self.env.context.get('allow_create_linea_empleado'):
            raise ValidationError("No está permitido agregar participantes manualmente.")
        return super().create(vals)

    def unlink(self):
        raise ValidationError("No está permitido eliminar participantes.")
