# -*- coding: utf-8 -*-
{
    "name": "Hide Any Menu",
    "author": "Website Technologies",
    "category": "Extra Tools",
    "summary": """
Hide Menu, Disable Menu Item,
Invisible Menu, Remove Menu, Delete Menu Odoo,
Hide Menu Items,Invisible Root Menu ,Company show hide menu,
user hide menu, user limited menu access Odoo
""",
    "description": """
Do you want to hide a specific menu for a specific user?
Do you want to show limited menus to users?
This module will help you to hide the menu to the user.
Go to users, Click on hide menus tab and specify menus
which you want to hide for that user. That's it. cheers!    
Hide Menu In Odoo, Disable Menu Item Odoo..
Invisible Menu /Root Menu Module Odoo,
Remove Menu Items For Users,
Feature Of Temporary  Delete Menu Odoo, Hide Sub Menu Items Odoo.
Delete Menu Items Odoo,
Invisible Root Menu , Hide Specific Menu Item Odoo.
""",
    "version": "16.0.1",
    "depends": [
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/hide_menu_template_wizard.xml",
        "views/base_view.xml",
        "views/hide_menu_template.xml",
    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
}
