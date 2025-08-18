from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

def migrate_existing_inductions(cr, registry):
    """
    Hook que se ejecuta al actualizar o instalar el módulo para
    asignar el valor 'induccion' a los registros existentes.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    _logger.info("Iniciando migración de registros de asignación de inducción existentes.")

    # Busca todos los registros de asignación que tienen un tipo de inducción,
    # pero que el nuevo campo tipo_registro está vacío.
    records_to_update = env['induccion_emple.asignacion'].search([
        ('tipo_induccion_id', '!=', False),
        ('tipo_registro', '=', False)
    ])

    if records_to_update:
        _logger.info("Se encontraron %d registros para actualizar.", len(records_to_update))
        # Asigna el valor 'induccion' al campo tipo_registro para cada uno
        records_to_update.write({'tipo_registro': 'induccion'})
        _logger.info("Migración completada. Registros actualizados.")
    else:
        _logger.info("No se encontraron registros de inducción para migrar.")