# sync_module/__manifest__.py
{
    'name': 'Sync Module',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Custom',
    'depends': ['base', 'hr', 'account', 'project', 'hc_community_sync_fields'],
    'data': [
        "data/sync_cron_job.xml",
    ],
    'installable': True,
    'application': True,
}
