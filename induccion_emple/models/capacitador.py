# mi_modulo_capacitadores/models/capacitador.py
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Capacitador(models.Model):
    _name = 'induccion_emple.capacitador'
    _description = 'Instructor/Capacitador'
    _rec_name = 'display_name' # Define cómo se mostrará el registro en campos Many2one

    # Campo para seleccionar un empleado existente
    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado Odoo',
        help="Selecciona un empleado existente de Odoo si es un capacitador interno."
    )

    # Campos que se llenarán automáticamente si se selecciona un empleado
    cedula = fields.Char(string='Cédula', tracking=True)
    nombre = fields.Char(string='Nombre Completo', required=True, tracking=True)
    cargo = fields.Char(string='Cargo', tracking=True)
    sucursal = fields.Char(string='Sucursal', tracking=True)
    phone = fields.Char(string='Teléfono', tracking=True)
    email = fields.Char(string='Correo Electrónico', tracking=True)

    # Campo para definir si es Capacitador, Instructor o Ambos
    tipo_rol = fields.Selection([
        ('capacitador', 'Capacitador'),
        ('instructor', 'Instructor'),
        ('ambos', 'Ambos'),
    ], string='Tipo de Rol', required=True, default='capacitador')

    # Campo para el nombre de la empresa externa (opcional)
    empresa_externa = fields.Char(
        string='Empresa Externa',
        help="Nombre de la empresa si el capacitador es externo.",
        tracking=True
    )

    descripcion = fields.Text(string='Notas Adicionales', tracking=True)

    # Campo calculado para el nombre que se mostrará en las vistas
    display_name = fields.Char(compute='_compute_display_name', store=True)

    # Campo booleano para indicar si es externo o no
    es_externo = fields.Boolean(
        string='Es Externo',
        compute='_compute_es_externo',
        store=True,
        help="Indica si el capacitador es un empleado de Odoo o un tercero."
    )

    # Campo calculado para solo-lectura en la vista
    readonly_fields = fields.Boolean(compute='_compute_readonly_fields', store=True)

    @api.depends('employee_id')
    def _compute_es_externo(self):
        for record in self:
            record.es_externo = not bool(record.employee_id)

    @api.depends('employee_id', 'nombre', 'empresa_externa')
    def _compute_display_name(self):
        for record in self:
            if record.employee_id:
                record.display_name = record.employee_id.name
            elif record.nombre and record.empresa_externa:
                record.display_name = f"{record.nombre} ({record.empresa_externa})"
            else:
                record.display_name = record.nombre

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """
        Populates fields based on the selected employee.
        """
        if self.employee_id:
            self.cedula = self.employee_id.identification_id # Assuming identification_id is the ID field in hr.employee
            self.nombre = self.employee_id.name
            self.cargo = self.employee_id.job_id.name if self.employee_id.job_id else False
            self.sucursal = self.employee_id.department_id.complete_name if self.employee_id.department_id else False
            # ACTUALIZACIÓN EN ONCHANGE: Copia el teléfono y correo del empleado
            self.phone = self.employee_id.work_phone
            self.email = self.employee_id.work_email
            self.empresa_externa = False
            self.descripcion = False # Limpiar descripción si se selecciona un empleado
        else:
            self.cedula = False
            self.nombre = False
            self.cargo = False
            self.sucursal = False
            # ACTUALIZACIÓN EN ONCHANGE: Limpia los campos si no hay empleado seleccionado
            self.phone = False
            self.email = False
            # La empresa_externa se maneja por el 'required' en la vista XML
            # self.empresa_externa = False # No limpiar aquí para permitir entrada manual para externos
            self.descripcion = False

    @api.constrains('employee_id', 'nombre')
    def _check_employee_or_name(self):
        """
        Ensures either an employee is selected or a name is provided for external capacitator.
        """
        for record in self:
            if not record.employee_id and not record.nombre:
                raise ValidationError("Debes seleccionar un empleado o ingresar un nombre para el capacitador externo.")

    @api.constrains('employee_id', 'empresa_externa')
    def _check_external_data(self):
        """
        Ensures external company name is provided if capacitator is external.
        """
        for record in self:
            if not record.employee_id and not record.empresa_externa and record.es_externo:
                # Only require empresa_externa if es_externo is True and no employee_id
                if not record.empresa_externa:
                    raise ValidationError("Si el capacitador es externo, debes ingresar el nombre de la empresa externa.")

