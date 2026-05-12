from odoo import fields, models


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    turma_id = fields.Many2one(
        'cedl.turma',
        string='Turma',
        index=True,
        ondelete='restrict',
    )

    grade_min = fields.Float(
        string='Nota mínima da escala',
        default=0.0,
    )
    grade_max = fields.Float(
        string='Nota máxima da escala',
        default=10.0,
    )
    passing_grade = fields.Float(
        string='Média para aprovação',
        default=6.0,
    )
