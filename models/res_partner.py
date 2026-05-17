from odoo import api, models

PROFESSOR_TAG_NAME = 'Professor'
GROUP_XMLID = 'cedl_elearning.group_professor'


def _professor_tag(env):
    return env['res.partner.category'].search(
        [('name', '=', PROFESSOR_TAG_NAME)], limit=1
    )


def _professor_group(env):
    return env.ref(GROUP_XMLID, raise_if_not_found=False)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _sync_professor_group(self):
        """For each partner in self, ensure linked internal users are in
        the professor group iff the partner currently has the Professor tag.
        """
        tag = _professor_tag(self.env)
        group = _professor_group(self.env)
        if not tag or not group:
            return
        for partner in self:
            users = partner.user_ids.filtered(lambda u: not u.share)
            if not users:
                continue
            should_have = tag in partner.category_id
            in_group = users.filtered(lambda u: group in u.groups_id)
            if should_have:
                missing = users - in_group
                if missing:
                    group.sudo().write(
                        {'user_ids': [(4, u.id) for u in missing]}
                    )
            else:
                if in_group:
                    group.sudo().write(
                        {'user_ids': [(3, u.id) for u in in_group]}
                    )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._sync_professor_group()
        return partners

    def write(self, vals):
        res = super().write(vals)
        if 'category_id' in vals or 'user_ids' in vals:
            self._sync_professor_group()
        return res
