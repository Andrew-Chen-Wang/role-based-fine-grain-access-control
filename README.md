# Example database setup of fine-grained role-based access control

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
❯ python main.py with_groups                                                                                                                           ─╯
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
    - Create model Role
    - Create model User
    - Create model UserRole
    - Create model UserGroup
    - Add field role to grouprole
(0.013)
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
(0.003)
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
(0.026)
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
(0.003)
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
(0.003) INSERT INTO "app_user" ("name") VALUES ('User 1') RETURNING "app_user"."id"; args=('User 1',); alias=default
Creating Group 1
(0.001) INSERT INTO "app_group" ("name") VALUES ('Group 1') RETURNING "app_group"."id"; args=('Group 1',); alias=default
Creating four roles:
Role 1: Can Read, Can Create
Role 2 (has Can Create like Role 1): Can Create, Can Update
Role 3 (completely disjoint from other two roles): Can Delete
Role 4 (completely disjoint from other two roles): Can Rule the World
(0.002) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 1', ARRAY[1,2]::integer[]) RETURNING "app_role"."id"; args=('Role 1', [1, 2]); alias=default
(0.002) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 2', ARRAY[2,3]::integer[]) RETURNING "app_role"."id"; args=('Role 2', [2, 3]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 3', ARRAY[4]::integer[]) RETURNING "app_role"."id"; args=('Role 3', [4]); alias=default
(0.002) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 4', ARRAY[5]::integer[]) RETURNING "app_role"."id"; args=('Role 4', [5]); alias=default
Attaching Role 1, 2, and 3 to the user
(0.029) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "permissions") VALUES (11, 41, NULL, ARRAY[1,2]::integer[]) RETURNING "app_userrole"."id"; args=(11, 41, None, [1, 2]); alias=default
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "permissions") VALUES (11, 42, NULL, ARRAY[2,3]::integer[]) RETURNING "app_userrole"."id"; args=(11, 42, None, [2, 3]); alias=default
(0.002) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "permissions") VALUES (11, 43, NULL, ARRAY[4]::integer[]) RETURNING "app_userrole"."id"; args=(11, 43, None, [4]); alias=default
Attaching Role 2, 3, and 4 to the group
(0.006) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (42, 8) RETURNING "app_grouprole"."id"; args=(42, 8); alias=default
(0.001) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (43, 8) RETURNING "app_grouprole"."id"; args=(43, 8); alias=default
(0.002) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (44, 8) RETURNING "app_grouprole"."id"; args=(44, 8); alias=default
----------------------------------------

Let's get user 1's permissions (in Python, I've converted it into a set)
(0.028) SELECT "app_userrole"."permissions" FROM "app_userrole" WHERE "app_userrole"."user_id" = 11; args=(11,); alias=default
{1, 2, 3, 4}
In Python, we use an IntEnum to represent permissions so that we can get a textual representation of a permission while storing small integers in the database
----------------------------------------

Let's attach User 1 to Group 1
(0.005) INSERT INTO "app_usergroup" ("user_id", "group_id") VALUES (11, 8) RETURNING "app_usergroup"."id"; args=(11, 8); alias=default
We also need to attach the group's roles to the user
Get group roles
(0.002) SELECT "app_grouprole"."id", "app_grouprole"."role_id", "app_role"."permissions" FROM "app_grouprole" INNER JOIN "app_role" ON ("app_grouprole"."role_id" = "app_role"."id") WHERE "app_grouprole"."group_id" = 8; args=(8,); alias=default
Attach group roles to the user via the UserRole table. Note that we attach the group role id to the user role. This allows for a cascading deletion effect if a group role is deleted.
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "permissions") VALUES (11, 42, 19, ARRAY[2,3]::integer[]), (11, 43, 20, ARRAY[4]::integer[]), (11, 44, 21, ARRAY[5]::integer[]) RETURNING "app_userrole"."id"; args=(11, 42, 19, [2, 3], 11, 43, 20, [4], 11, 44, 21, [5]); alias=default
----------------------------------------

Let's get user 1's permissions (in Python, I've converted it into a set)
(0.001) SELECT "app_userrole"."permissions" FROM "app_userrole" WHERE "app_userrole"."user_id" = 11; args=(11,); alias=default
{1, 2, 3, 4, 5}
Let's perform a query to see whether a permission (Can Read) exists for a user
(0.027) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[1])::integer[] AND "app_userrole"."user_id" = 11) LIMIT 1; args=(1, 1, 11); alias=default
User has permission: True
Let's do it for multiple permissions now
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[1, 2])::integer[] AND "app_userrole"."user_id" = 11) LIMIT 1; args=(1, 1, 2, 11); alias=default
User has permissions: True
Let's remove a disjoint Role 3 from user
(0.001) DELETE FROM "app_userrole" WHERE ("app_userrole"."group_role_id" IS NULL AND "app_userrole"."role_id" = 43 AND "app_userrole"."user_id" = 11); args=(43, 11); alias=default
Let's see if the user still has the permission
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[4])::integer[] AND "app_userrole"."user_id" = 11) LIMIT 1; args=(1, 4, 11); alias=default
User has permission: True
The reason the user still has permission is because the group the user is attached to has the permission. Take note of the SQL DELETE query performed. It explicitly states that the group_id is NULL. This is to ensure the group role that was attached wasn't deleted.
Let's delete the group role and see what happens
(0.001) SELECT "app_grouprole"."id", "app_grouprole"."role_id", "app_grouprole"."group_id" FROM "app_grouprole" WHERE ("app_grouprole"."group_id" = 8 AND "app_grouprole"."role_id" = 43); args=(8, 43); alias=default
(0.001) DELETE FROM "app_userrole" WHERE "app_userrole"."group_role_id" IN (20); args=(20,); alias=default
(0.001) DELETE FROM "app_grouprole" WHERE "app_grouprole"."id" IN (20); args=(20,); alias=default
Let's see if the user still has the permission
(0.002) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[4])::integer[] AND "app_userrole"."user_id" = 11) LIMIT 1; args=(1, 4, 11); alias=default
User has permission: False
The reason the user no longer has permission is because the group role was deleted. The user role was also deleted because the group role was deleted via a database CASCADE.
Let's delete the group and see what happens
(0.001) SELECT "app_group"."id", "app_group"."name" FROM "app_group" WHERE "app_group"."id" = 8; args=(8,); alias=default
(0.001) SELECT "app_grouprole"."id" FROM "app_grouprole" WHERE "app_grouprole"."group_id" IN (8); args=(8,); alias=default
(0.002) DELETE FROM "app_userrole" WHERE "app_userrole"."group_role_id" IN (19, 21); args=(19, 21); alias=default
(0.003) DELETE FROM "app_usergroup" WHERE "app_usergroup"."group_id" IN (8); args=(8,); alias=default
(0.001) DELETE FROM "app_grouprole" WHERE "app_grouprole"."id" IN (21, 19); args=(21, 19); alias=default
(0.001) DELETE FROM "app_group" WHERE "app_group"."id" IN (8); args=(8,); alias=default
Let's see if the user still has Role 2's permission
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[2, 3])::integer[] AND "app_userrole"."user_id" = 11) LIMIT 1; args=(1, 2, 3, 11); alias=default
Since we directly attached Role 2 to the user, the role and its permissionsare still attached to the user
----------------------------------------

Thanks for going through this tutorial
```

</details>

<details>
<summary>Click to open results for without groups</summary>

```
❯ python main.py without_groups                                                                                                                        ─╯
ERROR:  database "testorm" already exists
ERROR:  role "testorm" already exists
GRANT
ERROR:  database "testorm" already exists
ERROR:  role "testorm" already exists
GRANT
(0.031)
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
(0.004)
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
(0.027) INSERT INTO "app_user" ("name") VALUES ('User 1') RETURNING "app_user"."id"; args=('User 1',); alias=default
Creating four roles:
Role 1: Can Read, Can Create
Role 2 (has Can Create like Role 1): Can Create, Can Update
Role 3 (completely disjoint from other two roles): Can Delete
Role 4 (completely disjoint from other two roles): Can Rule the World
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 1', ARRAY[1,2]::integer[]) RETURNING "app_role"."id"; args=('Role 1', [1, 2]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 2', ARRAY[2,3]::integer[]) RETURNING "app_role"."id"; args=('Role 2', [2, 3]); alias=default
(0.002) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 3', ARRAY[4]::integer[]) RETURNING "app_role"."id"; args=('Role 3', [4]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 4', ARRAY[5]::integer[]) RETURNING "app_role"."id"; args=('Role 4', [5]); alias=default
Attaching Role 1, 2, and 3 to the user
(0.002) INSERT INTO "app_userrole" ("user_id", "role_id", "permissions") VALUES (12, 45, ARRAY[1,2]::integer[]) RETURNING "app_userrole"."id"; args=(12, 45, [1, 2]); alias=default
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "permissions") VALUES (12, 46, ARRAY[2,3]::integer[]) RETURNING "app_userrole"."id"; args=(12, 46, [2, 3]); alias=default
(0.001) INSERT INTO "app_userrole" ("user_id", "role_id", "permissions") VALUES (12, 47, ARRAY[4]::integer[]) RETURNING "app_userrole"."id"; args=(12, 47, [4]); alias=default
Let's see if the user has Role 4 (disjoint from other roles) permissions
(0.002) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[5])::integer[] AND "app_userrole"."user_id" = 12) LIMIT 1; args=(1, 5, 12); alias=default
User has permission: False
Let's see if the user has one of the permissions from Role 1 that no other role has (Can Read)
(0.024) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[1])::integer[] AND "app_userrole"."user_id" = 12) LIMIT 1; args=(1, 1, 12); alias=default
User has permission: True
Let's see if the user has one of the permissions from Role 1 and 2 (Can Create)
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[2])::integer[] AND "app_userrole"."user_id" = 12) LIMIT 1; args=(1, 2, 12); alias=default
User has permission: True
----------------------------------------

Thanks for going through this tutorial
```

</details>

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
