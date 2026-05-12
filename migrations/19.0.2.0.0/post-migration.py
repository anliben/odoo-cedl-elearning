"""Migrate existing slide.channel records to the new turma/materia model.

For every existing channel without turma_id:
  - create a cedl.turma matching the channel name
  - create (once) the placeholder cedl.materia "Geral"
  - link the channel (without renaming — the Matéria badge is enough)

Idempotent: rerunning skips channels that already have turma_id set.
"""
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    materia_geral = env['cedl.materia'].search(
        [('name', '=', 'Geral')], limit=1
    )
    if not materia_geral:
        materia_geral = env['cedl.materia'].create({
            'name': 'Geral',
            'sequence': 1,
        })

    Turma = env['cedl.turma']
    channels = env['slide.channel'].search([('turma_id', '=', False)])
    for ch in channels:
        original_name = ch.name or f'Turma {ch.id}'
        turma = Turma.search([('name', '=', original_name)], limit=1)
        if not turma:
            turma = Turma.create({'name': original_name, 'sequence': ch.id})
        ch.write({
            'turma_id': turma.id,
            'materia_id': materia_geral.id,
        })
