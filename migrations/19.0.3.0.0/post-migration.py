"""Pivot to Opção B: drop materia_id from slide.channel (it lived on the wrong
model) and drop the old grade fields from slide.channel.partner — grades now
live in cedl.nota per (matrícula, matéria).

No grade data existed in slide.channel.partner at the moment of this migration
(verified: 0 rows with grades). Existing slide_channel.materia_id values all
pointed to the placeholder Matéria 'Geral' that this refactor renders moot.
"""


def migrate(cr, version):
    cr.execute("""
        ALTER TABLE slide_channel
        DROP COLUMN IF EXISTS materia_id CASCADE
    """)
    cr.execute("""
        ALTER TABLE slide_channel_partner
        DROP COLUMN IF EXISTS grade_p1 CASCADE,
        DROP COLUMN IF EXISTS grade_p2 CASCADE,
        DROP COLUMN IF EXISTS grade_p3 CASCADE,
        DROP COLUMN IF EXISTS grade_p4 CASCADE,
        DROP COLUMN IF EXISTS grade_filled_count CASCADE,
        DROP COLUMN IF EXISTS grade_average CASCADE,
        DROP COLUMN IF EXISTS grade_status CASCADE,
        DROP COLUMN IF EXISTS turma_id CASCADE,
        DROP COLUMN IF EXISTS materia_id CASCADE
    """)
