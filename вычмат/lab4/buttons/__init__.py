# Экспорт всех setup-функций из кнопок
from .calc_button import setup_calc_button
from .auto_update import setup_auto_update_button
from .point_mode_button import setup_point_mode_button
from .import_export import setup_import_export_buttons
from .mode_toggle import setup_mode_toggle
from .help_exit import setup_help_exit

__all__ = [
    'setup_calc_button',
    'setup_auto_update_button',
    'setup_point_mode_button',
    'setup_import_export_buttons',
    'setup_mode_toggle',
    'setup_help_exit'
]