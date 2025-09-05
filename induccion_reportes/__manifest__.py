# -*- coding: utf-8 -*-
{
    'name': 'Reportes de Asignación de Inducción',
    'summary': 'Módulo para generar reportes de asignaciones de inducción.',
    'description': """
        Este módulo añade la funcionalidad de generar dos planillas (reportes)
        para las asignaciones de inducción:
        1. Planilla de Ítems de Inducción.
        2. Planilla de Participantes de Inducción.
    """,
    'author': 'Tu Nombre/Empresa', # Reemplaza con tu nombre o el de tu empresa
    'website': 'http://www.yourcompany.com', # Reemplaza con tu sitio web

    # Categoría de la aplicación
    'category': 'Human Resources',
    'version': '1.0',

    # Dependencias de módulos
    # Asegúrate de que los módulos 'hr', 'induccion_emple' y 'mi_modulo_capacitadores'
    # estén listos y disponibles.
    'depends': [
        'base',
        'web',             # <-- ¡HE AGREGADO ESTA LÍNEA AQUÍ!
        'hr',
        'induccion_emple',
        # 'mi_modulo_capacitadores', # Si este módulo existe y es una dependencia real
    ],

    # Datos cargados al instalar el módulo
    'data': [
        'reports/asignacion_report_templates.xml',
        
    ],

     'images': ['static/description/icon.png'],

    'installable': True,
    'application': False,
    'auto_install': False,
}