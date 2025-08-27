{
    'name': "Gestión de Inducciones para Empleados",
    'summary': "Módulo para gestionar indicaciones e inducciones a empleados",
    'description': """
        Este módulo permite llevar registro de las indicaciones dadas a empleados,
        con tipos de inducción y items específicos.
    """,
    'author': "Tu Nombre",
    'website': "https://www.tusitio.com",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['base', 'hr','web'],
   'data': [
    'security/ir.model.access.csv',
    'data/ir_sequence_data.xml',
    'views/tipo_induccion_views.xml',  
    'views/tipo_capacitacion_views.xml',
    'views/capacitador_views.xml', 
    'views/action_asignacion.xml',         # ✅ debe ir antes
    'views/asignacion_views.xml',
    'views/menu.xml',
    'views/asignacion_report_button.xml',
    'reports/asignacion_report.xml',
    'views/asignacion_capacitacion_views.xml',
    'views/acta.xml',
    'views/report_acta_induccion.xml',

],

     'assets': {
        'web.report_assets_common': [
            'induccion_emple/static/src/img/logo.png',
        ],
    },
   

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}