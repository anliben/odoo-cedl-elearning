from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SlideChannelPartner(models.Model):
    _name = 'slide.channel.partner'
    _inherit = ['slide.channel.partner', 'mail.thread']

    grade_p1 = fields.Float(string='1º Bimestre', tracking=True)
    grade_p2 = fields.Float(string='2º Bimestre', tracking=True)
    grade_p3 = fields.Float(string='3º Bimestre', tracking=True)
    grade_p4 = fields.Float(string='4º Bimestre', tracking=True)

    grade_filled_count = fields.Integer(
        compute='_compute_grade_metrics',
        store=True,
    )
    grade_average = fields.Float(
        string='Média',
        compute='_compute_grade_metrics',
        store=True,
    )
    grade_status = fields.Selection(
        [
            ('pending', 'Em andamento'),
            ('passed', 'Aprovado'),
            ('failed', 'Reprovado'),
        ],
        string='Situação',
        compute='_compute_grade_metrics',
        store=True,
        default='pending',
    )

    @api.depends('grade_p1', 'grade_p2', 'grade_p3', 'grade_p4',
                 'channel_id.passing_grade')
    def _compute_grade_metrics(self):
        for rec in self:
            grades = [rec.grade_p1, rec.grade_p2, rec.grade_p3, rec.grade_p4]
            filled = [g for g in grades if g]
            rec.grade_filled_count = len(filled)
            if len(filled) == 4:
                avg = sum(grades) / 4.0
                rec.grade_average = avg
                threshold = rec.channel_id.passing_grade or 0.0
                rec.grade_status = 'passed' if avg >= threshold else 'failed'
            else:
                rec.grade_average = 0.0
                rec.grade_status = 'pending'

    @api.constrains('grade_p1', 'grade_p2', 'grade_p3', 'grade_p4',
                    'channel_id')
    def _check_grades_in_range(self):
        for rec in self:
            ch = rec.channel_id
            lo, hi = ch.grade_min, ch.grade_max
            for label, value in (
                ('1º Bimestre', rec.grade_p1),
                ('2º Bimestre', rec.grade_p2),
                ('3º Bimestre', rec.grade_p3),
                ('4º Bimestre', rec.grade_p4),
            ):
                if value and (value < lo or value > hi):
                    raise ValidationError(_(
                        "Nota do %(period)s (%(value)s) fora da escala "
                        "%(lo)s a %(hi)s configurada para o curso "
                        "%(course)s."
                    ) % {
                        'period': label,
                        'value': value,
                        'lo': lo,
                        'hi': hi,
                        'course': ch.display_name,
                    })
