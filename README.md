# Example database setup of fine-grained role-based access control

![Role Based Access Control](https://user-images.githubusercontent.com/60190294/217440446-80a80c1b-c657-42ef-91a0-95acf02fb8cd.png)

This is an example implementation of relational database tables for
fine-grained access control with custom permissions and roles, similar to AWS IAM
roles and policies/permissions.

The example demonstration utilizes Django models as an easier way to interpret.
It is also because I ripped it off my current application for others to inspect.

At [Lazify](https://lazify.ai), we allow roles to be dynamically created for
our enterprise customers. We assume permissions are not allowed to be generated.
This is because permissions, in our application, are baked into our backend logic.
If dynamic permissions are allowed, prefer the method described in point 1 using
a Permission table and an M2M between Permission and your User; just
note that the below Python implementation does not demonstrate this. Our implementation
is more aligned with AWS IAM where custom policies are a set of permissions you
attach directly.

We define three tables:
1. A User table includes information about a user. It is also frequently
accessed application wide and is suitable for performing permissions queries.

> **Note** An alternative is to use a dedicated Permissions table which is an M2M
> relation between UserRole and Permission (which defines a permission) via a connection
> which can be called UserRolePermission. However, in database migration files,
> this can get clumsy by constantly defining permissions. Instead, I prefer
> an Enum based approach as seen in the example Python file below. This may
> not be preferable in large-scale applications which are unable to share
> code. However, for most cases, teams who are able to re-use code benefit
> the most not only because of DRY principles but also code benefits.

2. A Role table which defines roles and the role's permissions. This allows
user-generated roles similar to AWS IAM. Admins are able to create roles and
attach permissions to them which are inherited by users who are given this role.
3. An M2M UserRole table that defines which role(s) are attached to users. For
performance reasons, we also attach permissions to the user table.

#### Groups

We can further expand on this by creating groups. Groups in IAM simply have roles
attached to a Group and users are attached to a group. Policies/roles can also be
directly attached to users.

### Setup and Usage

If you don't want to see the tutorial, you can press the dropdown here.
The code is in [main.py](./main.py)

#### Tutorial Text

<details>
<summary>Click to see results with groups</summary>

```
❯ python main.py with_groups                                                 ─╯
ERROR:  database "testorm" already exists
ERROR:  role "testorm" already exists
GRANT
ERROR:  database "testorm" already exists
ERROR:  role "testorm" already exists
GRANT
(0.006)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
Migrations for 'app':
  app/migrations/0001_initial.py
    - Create model Group
    - Create model GroupRole
    - Create model GroupUser
    - Create model Role
    - Create model User
    - Create model UserRole
    - Add field user to groupuser
    - Add field role to grouprole
(0.005)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.000) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
(0.001)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
Operations to perform:
  Apply all migrations: app
Running migrations:
  No migrations to apply.
(0.002)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.000) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
Create User
(0.026) INSERT INTO "app_user" ("name") VALUES ('User 1') RETURNING "app_user"."id"; args=('User 1',); alias=default
Creating Group 1
(0.001) INSERT INTO "app_group" ("name") VALUES ('Group 1') RETURNING "app_group"."id"; args=('Group 1',); alias=default
Creating four roles:
Role 1: Can Read, Can Create
Role 2 (has Can Create like Role 1): Can Create, Can Update
Role 3 (completely disjoint from other two roles): Can Delete
Role 4 (completely disjoint from other two roles): Can Rule the World
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 1', ARRAY[1,2]::integer[]) RETURNING "app_role"."id"; args=('Role 1', [1, 2]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 2', ARRAY[2,3]::integer[]) RETURNING "app_role"."id"; args=('Role 2', [2, 3]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 3', ARRAY[4]::integer[]) RETURNING "app_role"."id"; args=('Role 3', [4]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 4', ARRAY[5]::integer[]) RETURNING "app_role"."id"; args=('Role 4', [5]); alias=default
Attaching Role 1, 2, and 3 to the user
(0.003) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (7, 25, NULL, NULL, ARRAY[1,2]::integer[]) RETURNING "app_userrole"."id"; args=(7, 25, None, None, [1, 2]); alias=default
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (7, 26, NULL, NULL, ARRAY[2,3]::integer[]) RETURNING "app_userrole"."id"; args=(7, 26, None, None, [2, 3]); alias=default
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (7, 27, NULL, NULL, ARRAY[4]::integer[]) RETURNING "app_userrole"."id"; args=(7, 27, None, None, [4]); alias=default
Attaching Role 2, 3, and 4 to the group
(0.028) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (26, 4) RETURNING "app_grouprole"."id"; args=(26, 4); alias=default
(0.002) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (27, 4) RETURNING "app_grouprole"."id"; args=(27, 4); alias=default
(0.001) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (28, 4) RETURNING "app_grouprole"."id"; args=(28, 4); alias=default
----------------------------------------

Let's get user 1's permissions (in Python, I've converted it into a set)
(0.001) SELECT "app_userrole"."permissions" FROM "app_userrole" WHERE "app_userrole"."user_id" = 7; args=(7,); alias=default
{1, 2, 3, 4}
In Python, we use an IntEnum to represent permissions so that we can get a textual representation of a permission while storing small integers in the database
----------------------------------------

Let's attach User 1 to Group 1
(0.002) INSERT INTO "app_groupuser" ("user_id", "group_id") VALUES (7, 4) RETURNING "app_groupuser"."id"; args=(7, 4); alias=default
We also need to attach the group's roles to the user
Get group roles
(0.002) SELECT "app_grouprole"."id", "app_grouprole"."role_id", "app_role"."permissions" FROM "app_grouprole" INNER JOIN "app_role" ON ("app_grouprole"."role_id" = "app_role"."id") WHERE "app_grouprole"."group_id" = 4; args=(4,); alias=default
Attach group roles to the user via the UserRole table. Note that we attach the group role id to the user role. This allows for a cascading deletion effect if a group role is deleted.
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (7, 26, 10, 4, ARRAY[2,3]::integer[]), (7, 27, 11, 4, ARRAY[4]::integer[]), (7, 28, 12, 4, ARRAY[5]::integer[]) RETURNING "app_userrole"."id"; args=(7, 26, 10, 4, [2, 3], 7, 27, 11, 4, [4], 7, 28, 12, 4, [5]); alias=default
----------------------------------------

Let's get user 1's permissions (in Python, I've converted it into a set)
(0.001) SELECT "app_userrole"."permissions" FROM "app_userrole" WHERE "app_userrole"."user_id" = 7; args=(7,); alias=default
{1, 2, 3, 4, 5}
Let's perform a query to see whether a permission (Can Read) exists for a user
(0.027) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[1])::integer[] AND "app_userrole"."user_id" = 7) LIMIT 1; args=(1, 1, 7); alias=default
User has permission: True
Let's do it for multiple permissions now
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[1, 2])::integer[] AND "app_userrole"."user_id" = 7) LIMIT 1; args=(1, 1, 2, 7); alias=default
User has permissions: True
What if we want to see if the user has two permissions? Use contains instead of overlap
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[1, 2])::integer[] AND "app_userrole"."user_id" = 7) LIMIT 1; args=(1, 1, 2, 7); alias=default
User has permissions: True
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[5, 2])::integer[] AND "app_userrole"."user_id" = 7) LIMIT 1; args=(1, 5, 2, 7); alias=default
User has permissions: False
Let's remove a disjoint Role 3 from user
(0.001) DELETE FROM "app_userrole" WHERE ("app_userrole"."group_role_id" IS NULL AND "app_userrole"."role_id" = 27 AND "app_userrole"."user_id" = 7); args=(27, 7); alias=default
Let's see if the user still has the permission
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[4])::integer[] AND "app_userrole"."user_id" = 7) LIMIT 1; args=(1, 4, 7); alias=default
User has permission: True
The reason the user still has permission is because the group the user is attached to has the permission. Take note of the SQL DELETE query performed. It explicitly states that the group_id is NULL. This is to ensure the group role that was attached wasn't deleted.
Let's delete the group role and see what happens
(0.001) SELECT "app_grouprole"."id", "app_grouprole"."role_id", "app_grouprole"."group_id" FROM "app_grouprole" WHERE ("app_grouprole"."group_id" = 4 AND "app_grouprole"."role_id" = 27); args=(4, 27); alias=default
(0.001) DELETE FROM "app_userrole" WHERE "app_userrole"."group_role_id" IN (11); args=(11,); alias=default
(0.001) DELETE FROM "app_grouprole" WHERE "app_grouprole"."id" IN (11); args=(11,); alias=default
Let's see if the user still has the permission
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[4])::integer[] AND "app_userrole"."user_id" = 7) LIMIT 1; args=(1, 4, 7); alias=default
User has permission: False
The reason the user no longer has permission is because the group role was deleted. The user role was also deleted because the group role was deleted via a database CASCADE.
Let's delete the group and see what happens
(0.001) SELECT "app_group"."id", "app_group"."name" FROM "app_group" WHERE "app_group"."id" = 4; args=(4,); alias=default
(0.001) SELECT "app_grouprole"."id" FROM "app_grouprole" WHERE "app_grouprole"."group_id" IN (4); args=(4,); alias=default
(0.000) SELECT "app_groupuser"."id" FROM "app_groupuser" WHERE "app_groupuser"."group_id" IN (4); args=(4,); alias=default
(0.001) DELETE FROM "app_userrole" WHERE "app_userrole"."group_role_id" IN (10, 12); args=(10, 12); alias=default
(0.001) DELETE FROM "app_userrole" WHERE "app_userrole"."group_user_id" IN (4); args=(4,); alias=default
(0.001) DELETE FROM "app_grouprole" WHERE "app_grouprole"."id" IN (12, 10); args=(12, 10); alias=default
(0.001) DELETE FROM "app_groupuser" WHERE "app_groupuser"."id" IN (4); args=(4,); alias=default
(0.001) DELETE FROM "app_group" WHERE "app_group"."id" IN (4); args=(4,); alias=default
Let's see if the user still has Role 2's permission
(0.026) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[2, 3])::integer[] AND "app_userrole"."user_id" = 7) LIMIT 1; args=(1, 2, 3, 7); alias=default
Since we directly attached Role 2 to the user, the role and its permissionsare still attached to the user
----------------------------------------

Thanks for going through this tutorial
```

</details>

<details>
<summary>Click to open results for without groups</summary>

```
❯ python main.py without_groups                                              ─╯
ERROR:  database "testorm" already exists
ERROR:  role "testorm" already exists
GRANT
ERROR:  database "testorm" already exists
ERROR:  role "testorm" already exists
GRANT
(0.005)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
Migrations for 'app':
  app/migrations/0001_initial.py
    - Create model Role
    - Create model User
    - Create model UserRole
(0.002)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
(0.001)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
Operations to perform:
  Apply all migrations: app
Running migrations:
  No migrations to apply.
(0.022)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001)
            SELECT
                c.relname,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
        ; args=None; alias=default
(0.001) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
Create User
(0.002) INSERT INTO "app_user" ("name") VALUES ('User 1') RETURNING "app_user"."id"; args=('User 1',); alias=default
Creating four roles:
Role 1: Can Read, Can Create
Role 2 (has Can Create like Role 1): Can Create, Can Update
Role 3 (completely disjoint from other two roles): Can Delete
Role 4 (completely disjoint from other two roles): Can Rule the World
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 1', ARRAY[1,2]::integer[]) RETURNING "app_role"."id"; args=('Role 1', [1, 2]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 2', ARRAY[2,3]::integer[]) RETURNING "app_role"."id"; args=('Role 2', [2, 3]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 3', ARRAY[4]::integer[]) RETURNING "app_role"."id"; args=('Role 3', [4]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 4', ARRAY[5]::integer[]) RETURNING "app_role"."id"; args=('Role 4', [5]); alias=default
Attaching Role 1, 2, and 3 to the user
(0.003) INSERT INTO "app_userrole" ("user_id", "role_id", "permissions") VALUES (6, 21, ARRAY[1,2]::integer[]) RETURNING "app_userrole"."id"; args=(6, 21, [1, 2]); alias=default
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "permissions") VALUES (6, 22, ARRAY[2,3]::integer[]) RETURNING "app_userrole"."id"; args=(6, 22, [2, 3]); alias=default
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "permissions") VALUES (6, 23, ARRAY[4]::integer[]) RETURNING "app_userrole"."id"; args=(6, 23, [4]); alias=default
Let's see if the user has Role 4 (disjoint from other roles) permissions
(0.024) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[5])::integer[] AND "app_userrole"."user_id" = 6) LIMIT 1; args=(1, 5, 6); alias=default
User has permission: False
Let's see if the user has one of the permissions from Role 1 that no other role has (Can Read)
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[1])::integer[] AND "app_userrole"."user_id" = 6) LIMIT 1; args=(1, 1, 6); alias=default
User has permission: True
What if we want to see if the user has two permissions? Use contains instead of overlap
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[1, 2])::integer[] AND "app_userrole"."user_id" = 6) LIMIT 1; args=(1, 1, 2, 6); alias=default
User has permissions: True
(0.000) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[5, 2])::integer[] AND "app_userrole"."user_id" = 6) LIMIT 1; args=(1, 5, 2, 6); alias=default
User has permissions: False
Let's see if the user has one of the permissions from Role 1 and 2 (Can Create)
(0.000) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" && (ARRAY[2])::integer[] AND "app_userrole"."user_id" = 6) LIMIT 1; args=(1, 2, 6); alias=default
User has permission: True
----------------------------------------

Thanks for going through this tutorial
```

</details>

### Longer explanation

Assume we have an organization that can dynamically create roles. Each organization has Members. We can create roles for the organization and attach permission IDs (integers) to a role. Let's attach a role to a Member. To do so, we create a MemberRole with a foreign key to Member and Role. We set the groups to null for now; copy the permissions from the role to the MemberRole. On update of Role's permissions, simply update all Roles with a foreign key pointing to that role with the new permissions integer array.

If we want to quickly attach several roles to members in the organization where several members have the same roles/permissions in their current enterprise setting, we create a Group. Create a Group. To attach roles, create a GroupRole that has an FK to Organization and the Role you want to attach. Now let's add members to the group. 1) We create a GroupMember by pointing to the Group and the Member and 2) we create a MemberRole by attaching the Role IDs of the Group you attached the member to. Do this for all group roles. We perform this operation by creating MemberRole the same way we did before but this time we add the FK to GroupMember and GroupRole.

Now to see whether a user has permission to conduct an action, you can perform overlap and contains operations in PostgreSQL on the permissions table with whatever filters you want.

Note: All foreign keys cascade on deletion. This allows for easy resource cleanup. For instance, if a role is deleted, then the role is deleted for MemberRole and GroupRole. If a Member is deleted, then the all Member related materials are also deleted.

### Running it locally

To set up, you will need a PostgreSQL instance on your localhost running.
You cannot use SQLite since it doesn't natively support array attributes
in its database:

```bash
sh bin/create_db.sh
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements/local.txt
```

To use, you can watch the demo by writing `with_groups` or `without_groups`:

```bash
python main.py with_groups
# Or
python main.py without_groups
```

### Credit and License

This repository was generated with [Andrew-Chen-Wang/django-orm-template](https://github.com/Andrew-Chen-Wang/django-orm-template)

This template is based on the repository
by [@dancaron](https://github.com/dancaron/Django-ORM).

This repository/template is licensed under the Apache 2.0 license
which can be found in the [LICENSE](./LICENSE) file.
