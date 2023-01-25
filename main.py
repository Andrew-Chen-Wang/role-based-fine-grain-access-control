############################################################################
## Django ORM Standalone Python Template
############################################################################
""" Here we'll import the parts of Django we need. It's recommended to leave
these settings as is, and skip to START OF APPLICATION section below """

# Turn off bytecode generation
import sys


sys.dont_write_bytecode = True

import os
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
demonstrate_with_groups = sys.argv[1] == "with_groups"


def setup():
    subprocess.call(["sh", "./bin/drop_db.sh"])
    subprocess.call(["sh", "./bin/create_db.sh"])
    migrations_dir = BASE_DIR / "app" / "migrations"
    for file in migrations_dir.iterdir():
        if file.is_file() and file.name not in ("__init__.py", ".gitignore"):
            file.unlink()
    migrations_dir.mkdir(exist_ok=True)
    (migrations_dir / "__init__.py").touch(exist_ok=True)
    models_dir = BASE_DIR / "app" / "models"
    (models_dir / "__init__.py").touch(exist_ok=True)
    models_dir = BASE_DIR / "app" / "models"
    (models_dir / "__init__.py").touch(exist_ok=True)
    with_or_without = "with_groups" if demonstrate_with_groups else "without_groups"
    (models_dir / "__init__.py").write_text(f"from .{with_or_without} import *")


setup()


import django


django.setup()


import logging
from itertools import chain

from django.core.management import call_command

from app.permissions import Permission


l = logging.getLogger("django.db.backends")
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())


def create_db(with_group: bool):
    call_command("makemigrations", "app")
    call_command("migrate")


def print_dashes():
    print("----------------------------------------\n")


def with_groups():
    from app.models.with_groups import Group, GroupRole, GroupUser, Role, User, UserRole

    create_db(True)
    print("Create User")
    user = User.objects.create(name="User 1")

    print("Creating Group 1")
    group1 = Group.objects.create(name="Group 1")

    print("Creating four roles:")
    print("Role 1: Can Read, Can Create")
    print("Role 2 (has Can Create like Role 1): Can Create, Can Update")
    print("Role 3 (completely disjoint from other two roles): Can Delete")
    print("Role 4 (completely disjoint from other two roles): Can Rule the World")
    role1 = Role.objects.create(
        name="Role 1",
        permissions=[Permission.CAN_READ.value, Permission.CAN_CREATE.value],
    )
    role2 = Role.objects.create(
        name="Role 2",
        permissions=[Permission.CAN_CREATE.value, Permission.CAN_UPDATE.value],
    )
    role3 = Role.objects.create(
        name="Role 3", permissions=[Permission.CAN_DELETE.value]
    )
    role4 = Role.objects.create(
        name="Role 4", permissions=[Permission.CAN_RULE_THE_WORLD.value]
    )

    print("Attaching Role 1, 2, and 3 to the user")
    UserRole.objects.create(user=user, role=role1, permissions=role1.permissions)
    UserRole.objects.create(user=user, role=role2, permissions=role2.permissions)
    UserRole.objects.create(user=user, role=role3, permissions=role3.permissions)
    print("Attaching Role 2, 3, and 4 to the group")
    GroupRole.objects.create(group=group1, role=role2)
    GroupRole.objects.create(group=group1, role=role3)
    GroupRole.objects.create(group=group1, role=role4)
    print_dashes()

    print("Let's get user 1's permissions (in Python, I've converted it into a set)")
    print(
        set(
            chain.from_iterable(
                UserRole.objects.filter(user=user).values_list("permissions", flat=True)
            )
        )
    )
    print(
        "In Python, we use an IntEnum to represent permissions so that we can get a "
        "textual representation of a permission while storing small integers in the "
        "database"
    )
    print_dashes()
    print("Let's attach User 1 to Group 1")
    group_user = GroupUser.objects.create(user=user, group=group1)
    print("We also need to attach the group's roles to the user")
    print("Get group roles")
    group_roles = list(
        GroupRole.objects.filter(group=group1)
        .select_related("role")
        .values_list("id", "role_id", "role__permissions")
    )
    print(
        "Attach group roles to the user via the UserRole table. "
        "Note that we attach the group role id to the user role. This allows "
        "for a cascading deletion effect if a group role is deleted."
    )
    UserRole.objects.bulk_create(
        [
            UserRole(
                user=user,
                role_id=role_id,
                permissions=role_permissions,
                group_role_id=group_role_id,
                group_user=group_user,
            )
            for group_role_id, role_id, role_permissions in group_roles
        ]
    )
    print_dashes()
    print("Let's get user 1's permissions (in Python, I've converted it into a set)")
    print(
        set(
            chain.from_iterable(
                UserRole.objects.filter(user=user).values_list("permissions", flat=True)
            )
        )
    )
    print(
        "Let's perform a query to see whether a permission (Can Read) exists for a user"
    )
    has_permission = UserRole.objects.filter(
        user=user, permissions__overlap=[Permission.CAN_READ.value]
    ).exists()
    assert has_permission is True, "Strange..."
    print(f"User has permission: {has_permission}")
    print("Let's do it for multiple permissions now")
    has_permissions = UserRole.objects.filter(
        user=user,
        permissions__overlap=[Permission.CAN_READ.value, Permission.CAN_CREATE.value],
    ).exists()
    assert has_permissions is True, "Strange..."
    print(f"User has permissions: {has_permissions}")
    print(
        "What if we want to see if the user has two permissions? Use contains "
        "instead of overlap"
    )
    has_permissions = UserRole.objects.filter(
        user=user,
        permissions__contains=[Permission.CAN_READ.value, Permission.CAN_CREATE.value],
    ).exists()
    assert has_permissions is True, "Strange..."
    print(f"User has permissions: {has_permissions}")
    has_permissions = UserRole.objects.filter(
        user=user,
        permissions__contains=[
            Permission.CAN_RULE_THE_WORLD.value,
            Permission.CAN_CREATE.value,
        ],
    ).exists()
    assert has_permissions is False, "Strange..."
    print(f"User has permissions: {has_permissions}")
    print("Let's remove a disjoint Role 3 from user")
    UserRole.objects.filter(user=user, role=role3, group_role=None).delete()
    print("Let's see if the user still has the permission")
    has_permission = UserRole.objects.filter(
        user=user, permissions__overlap=role3.permissions
    ).exists()
    assert has_permission is True, "Strange..."
    print(f"User has permission: {has_permission}")
    print(
        "The reason the user still has permission is because the group the user is "
        "attached to has the permission. Take note of the SQL DELETE query performed. "
        "It explicitly states that the group_id is NULL. This is to ensure the group "
        "role that was attached wasn't deleted."
    )
    print("Let's delete the group role and see what happens")
    GroupRole.objects.filter(group=group1, role=role3).delete()
    print("Let's see if the user still has the permission")
    has_permission = UserRole.objects.filter(
        user=user, permissions__overlap=role3.permissions
    ).exists()
    assert has_permission is False, "Strange..."
    print(f"User has permission: {has_permission}")
    print(
        "The reason the user no longer has permission is because the group role was "
        "deleted. The user role was also deleted because the group role was deleted "
        "via a database CASCADE."
    )
    print("Let's delete the group and see what happens")
    Group.objects.filter(id=group1.id).delete()
    print("Let's see if the user still has Role 2's permission")
    has_permission = UserRole.objects.filter(
        user=user, permissions__overlap=role2.permissions
    ).exists()
    assert has_permission is True, "Strange..."
    print(
        "Since we directly attached Role 2 to the user, the role and its permissions"
        "are still attached to the user"
    )


def without_groups():
    from app.models.without_groups import Role, User, UserRole

    create_db(False)
    print("Create User")
    user = User.objects.create(name="User 1")

    print("Creating four roles:")
    print("Role 1: Can Read, Can Create")
    print("Role 2 (has Can Create like Role 1): Can Create, Can Update")
    print("Role 3 (completely disjoint from other two roles): Can Delete")
    print("Role 4 (completely disjoint from other two roles): Can Rule the World")
    role1 = Role.objects.create(
        name="Role 1",
        permissions=[Permission.CAN_READ.value, Permission.CAN_CREATE.value],
    )
    role2 = Role.objects.create(
        name="Role 2",
        permissions=[Permission.CAN_CREATE.value, Permission.CAN_UPDATE.value],
    )
    role3 = Role.objects.create(
        name="Role 3", permissions=[Permission.CAN_DELETE.value]
    )
    role4 = Role.objects.create(
        name="Role 4", permissions=[Permission.CAN_RULE_THE_WORLD.value]
    )

    print("Attaching Role 1, 2, and 3 to the user")
    UserRole.objects.create(user=user, role=role1, permissions=role1.permissions)
    UserRole.objects.create(user=user, role=role2, permissions=role2.permissions)
    UserRole.objects.create(user=user, role=role3, permissions=role3.permissions)

    print("Let's see if the user has Role 4 (disjoint from other roles) permissions")
    has_permission = UserRole.objects.filter(
        user=user, permissions__overlap=role4.permissions
    ).exists()
    assert has_permission is False, "Strange..."
    print(f"User has permission: {has_permission}")
    print(
        "Let's see if the user has one of the permissions from Role 1 that no other "
        "role has (Can Read)"
    )
    has_permission = UserRole.objects.filter(
        user=user, permissions__overlap=[Permission.CAN_READ.value]
    ).exists()
    assert has_permission is True, "Strange..."
    print(f"User has permission: {has_permission}")
    print(
        "What if we want to see if the user has two permissions? Use contains "
        "instead of overlap"
    )
    has_permissions = UserRole.objects.filter(
        user=user,
        permissions__contains=[Permission.CAN_READ.value, Permission.CAN_CREATE.value],
    ).exists()
    assert has_permissions is True, "Strange..."
    print(f"User has permissions: {has_permissions}")
    has_permissions = UserRole.objects.filter(
        user=user,
        permissions__contains=[
            Permission.CAN_RULE_THE_WORLD.value,
            Permission.CAN_CREATE.value,
        ],
    ).exists()
    assert has_permissions is False, "Strange..."
    print(f"User has permissions: {has_permissions}")
    print(
        "Let's see if the user has one of the permissions from Role 1 and 2 "
        "(Can Create)"
    )
    has_permission = UserRole.objects.filter(
        user=user, permissions__overlap=[Permission.CAN_CREATE.value]
    ).exists()
    assert has_permission is True, "Strange..."
    print(f"User has permission: {has_permission}")


def main():
    if demonstrate_with_groups:
        with_groups()
    else:
        without_groups()
    print_dashes()
    print("Thanks for going through this tutorial")


if __name__ == "__main__":
    main()
