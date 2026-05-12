from odoo import fields, models


class SlideSlide(models.Model):
    _inherit = 'slide.slide'

    materia_id = fields.Many2one(
        'cedl.materia',
        string='Matéria',
        index=True,
        ondelete='set null',
        help='Matéria a que este conteúdo pertence dentro da turma. '
             'Deixe em branco para conteúdo geral.',
    )
