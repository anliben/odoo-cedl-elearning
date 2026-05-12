from odoo import api, fields, models


class CedlTurma(models.Model):
    _name = 'cedl.turma'
    _description = 'Turma'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    channel_ids = fields.One2many('slide.channel', 'turma_id', string='Cursos')
    channel_count = fields.Integer(compute='_compute_channel_count')
    materia_ids = fields.Many2many(
        'cedl.materia',
        'cedl_turma_materia_rel',
        'turma_id',
        'materia_id',
        string='Matérias',
    )

    _name_unique = models.Constraint(
        'UNIQUE (name)',
        'Já existe uma turma com esse nome.',
    )

    @api.depends('channel_ids')
    def _compute_channel_count(self):
        for rec in self:
            rec.channel_count = len(rec.channel_ids)

    def write(self, vals):
        res = super().write(vals)
        if 'materia_ids' in vals:
            self._sync_notas_for_turma()
        return res

    def _sync_notas_for_turma(self):
        Nota = self.env['cedl.nota']
        for turma in self:
            channel_partners = self.env['slide.channel.partner'].search([
                ('channel_id.turma_id', '=', turma.id),
            ])
            for materia in turma.materia_ids:
                for cp in channel_partners:
                    existing = Nota.search([
                        ('channel_partner_id', '=', cp.id),
                        ('materia_id', '=', materia.id),
                    ], limit=1)
                    if not existing:
                        Nota.create({
                            'channel_partner_id': cp.id,
                            'materia_id': materia.id,
                        })
