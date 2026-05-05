from odoo import api, SUPERUSER_ID

PROFESSOR_TAG_NAME = 'Professor'


def post_init_sync_professors(env):
    """Sync existing partners with the Professor tag into group_professor."""
    Category = env['res.partner.category']
    tag = Category.search([('name', '=', PROFESSOR_TAG_NAME)], limit=1)
    if not tag:
        return
    group = env.ref('cedl_elearning.group_professor', raise_if_not_found=False)
    if not group:
        return
    users = env['res.users'].search([
        ('partner_id.category_id', 'in', tag.ids),
        ('share', '=', False),
    ])
    if users:
        group.sudo().write({'user_ids': [(4, u.id) for u in users]})
