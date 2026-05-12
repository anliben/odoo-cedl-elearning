from odoo import api, fields, models


class CedlMateria(models.Model):
    _name = 'cedl.materia'
    _description = 'Matéria'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    color = fields.Integer()
    active = fields.Boolean(default=True)
    turma_ids = fields.Many2many(
        'cedl.turma',
        'cedl_turma_materia_rel',
        'materia_id',
        'turma_id',
        string='Turmas',
    )
    turma_count = fields.Integer(compute='_compute_turma_count')

    _name_unique = models.Constraint(
        'UNIQUE (name)',
        'Já existe uma matéria com esse nome.',
    )

    @api.depends('turma_ids')
    def _compute_turma_count(self):
        for rec in self:
            rec.turma_count = len(rec.turma_ids)

    def write(self, vals):
        before = {m.id: set(m.turma_ids.ids) for m in self} if 'turma_ids' in vals else None
        res = super().write(vals)
        if before is not None:
            affected = self.env['cedl.turma']
            for m in self:
                added = set(m.turma_ids.ids) - before[m.id]
                if added:
                    affected |= self.env['cedl.turma'].browse(added)
            if affected:
                affected._sync_notas_for_turma()
        return res
