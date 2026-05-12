from odoo import api, fields, models


class SlideChannelPartner(models.Model):
    _name = 'slide.channel.partner'
    _inherit = ['slide.channel.partner', 'mail.thread']

    nota_ids = fields.One2many(
        'cedl.nota',
        'channel_partner_id',
        string='Notas por matéria',
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_notas_for_partner()
        return records

    def _sync_notas_for_partner(self):
        Nota = self.env['cedl.nota']
        for cp in self:
            turma = cp.channel_id.turma_id
            if not turma:
                continue
            for materia in turma.materia_ids:
                existing = Nota.search([
                    ('channel_partner_id', '=', cp.id),
                    ('materia_id', '=', materia.id),
                ], limit=1)
                if not existing:
                    Nota.create({
                        'channel_partner_id': cp.id,
                        'materia_id': materia.id,
                    })
