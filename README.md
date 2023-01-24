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
CREATE DATABASE
ERROR:  role "testorm" already exists
GRANT
ERROR:  database "testorm" already exists
ERROR:  role "testorm" already exists
GRANT
(0.030)
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
Operations to perform:
  Apply all migrations: app
Running migrations:
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
CREATE TABLE "django_migrations" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" timestamp with time zone NOT NULL); (params None)
(0.012) CREATE TABLE "django_migrations" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" timestamp with time zone NOT NULL); args=None; alias=default
  Applying app.0001_initial...CREATE TABLE "app_group" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(100) NOT NULL); (params None)
(0.032) CREATE TABLE "app_group" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(100) NOT NULL); args=None; alias=default
CREATE TABLE "app_grouprole" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "group_id" bigint NOT NULL); (params None)
(0.003) CREATE TABLE "app_grouprole" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "group_id" bigint NOT NULL); args=None; alias=default
CREATE TABLE "app_groupuser" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "group_id" bigint NOT NULL); (params None)
(0.030) CREATE TABLE "app_groupuser" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "group_id" bigint NOT NULL); args=None; alias=default
CREATE TABLE "app_role" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(100) NOT NULL, "permissions" integer[] NOT NULL); (params None)
(0.005) CREATE TABLE "app_role" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(100) NOT NULL, "permissions" integer[] NOT NULL); args=None; alias=default
CREATE TABLE "app_user" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(100) NOT NULL); (params None)
(0.006) CREATE TABLE "app_user" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(100) NOT NULL); args=None; alias=default
CREATE TABLE "app_userrole" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "permissions" integer[] NOT NULL, "group_role_id" bigint NULL, "group_user_id" bigint NULL, "role_id" bigint NOT NULL, "user_id" bigint NOT NULL); (params None)
(0.029) CREATE TABLE "app_userrole" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "permissions" integer[] NOT NULL, "group_role_id" bigint NULL, "group_user_id" bigint NULL, "role_id" bigint NOT NULL, "user_id" bigint NOT NULL); args=None; alias=default
ALTER TABLE "app_groupuser" ADD COLUMN "user_id" bigint NOT NULL CONSTRAINT "app_groupuser_user_id_89d3f803_fk_app_user_id" REFERENCES "app_user"("id") DEFERRABLE INITIALLY DEFERRED; SET CONSTRAINTS "app_groupuser_user_id_89d3f803_fk_app_user_id" IMMEDIATE; (params [])
(0.004) ALTER TABLE "app_groupuser" ADD COLUMN "user_id" bigint NOT NULL CONSTRAINT "app_groupuser_user_id_89d3f803_fk_app_user_id" REFERENCES "app_user"("id") DEFERRABLE INITIALLY DEFERRED; SET CONSTRAINTS "app_groupuser_user_id_89d3f803_fk_app_user_id" IMMEDIATE; args=[]; alias=default
ALTER TABLE "app_grouprole" ADD COLUMN "role_id" bigint NOT NULL CONSTRAINT "app_grouprole_role_id_10d9e643_fk_app_role_id" REFERENCES "app_role"("id") DEFERRABLE INITIALLY DEFERRED; SET CONSTRAINTS "app_grouprole_role_id_10d9e643_fk_app_role_id" IMMEDIATE; (params [])
(0.024) ALTER TABLE "app_grouprole" ADD COLUMN "role_id" bigint NOT NULL CONSTRAINT "app_grouprole_role_id_10d9e643_fk_app_role_id" REFERENCES "app_role"("id") DEFERRABLE INITIALLY DEFERRED; SET CONSTRAINTS "app_grouprole_role_id_10d9e643_fk_app_role_id" IMMEDIATE; args=[]; alias=default
ALTER TABLE "app_grouprole" ADD CONSTRAINT "app_grouprole_group_id_1d91324c_fk_app_group_id" FOREIGN KEY ("group_id") REFERENCES "app_group" ("id") DEFERRABLE INITIALLY DEFERRED; (params ())
(0.002) ALTER TABLE "app_grouprole" ADD CONSTRAINT "app_grouprole_group_id_1d91324c_fk_app_group_id" FOREIGN KEY ("group_id") REFERENCES "app_group" ("id") DEFERRABLE INITIALLY DEFERRED; args=(); alias=default
CREATE INDEX "app_grouprole_group_id_1d91324c" ON "app_grouprole" ("group_id"); (params ())
(0.003) CREATE INDEX "app_grouprole_group_id_1d91324c" ON "app_grouprole" ("group_id"); args=(); alias=default
ALTER TABLE "app_groupuser" ADD CONSTRAINT "app_groupuser_group_id_0b97758b_fk_app_group_id" FOREIGN KEY ("group_id") REFERENCES "app_group" ("id") DEFERRABLE INITIALLY DEFERRED; (params ())
(0.003) ALTER TABLE "app_groupuser" ADD CONSTRAINT "app_groupuser_group_id_0b97758b_fk_app_group_id" FOREIGN KEY ("group_id") REFERENCES "app_group" ("id") DEFERRABLE INITIALLY DEFERRED; args=(); alias=default
CREATE INDEX "app_groupuser_group_id_0b97758b" ON "app_groupuser" ("group_id"); (params ())
(0.003) CREATE INDEX "app_groupuser_group_id_0b97758b" ON "app_groupuser" ("group_id"); args=(); alias=default
ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_group_role_id_5e2f5aa5_fk_app_grouprole_id" FOREIGN KEY ("group_role_id") REFERENCES "app_grouprole" ("id") DEFERRABLE INITIALLY DEFERRED; (params ())
(0.003) ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_group_role_id_5e2f5aa5_fk_app_grouprole_id" FOREIGN KEY ("group_role_id") REFERENCES "app_grouprole" ("id") DEFERRABLE INITIALLY DEFERRED; args=(); alias=default
ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_group_user_id_2e5cca64_fk_app_groupuser_id" FOREIGN KEY ("group_user_id") REFERENCES "app_groupuser" ("id") DEFERRABLE INITIALLY DEFERRED; (params ())
(0.002) ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_group_user_id_2e5cca64_fk_app_groupuser_id" FOREIGN KEY ("group_user_id") REFERENCES "app_groupuser" ("id") DEFERRABLE INITIALLY DEFERRED; args=(); alias=default
ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_role_id_178627fc_fk_app_role_id" FOREIGN KEY ("role_id") REFERENCES "app_role" ("id") DEFERRABLE INITIALLY DEFERRED; (params ())
(0.028) ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_role_id_178627fc_fk_app_role_id" FOREIGN KEY ("role_id") REFERENCES "app_role" ("id") DEFERRABLE INITIALLY DEFERRED; args=(); alias=default
ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_user_id_d61bb2ea_fk_app_user_id" FOREIGN KEY ("user_id") REFERENCES "app_user" ("id") DEFERRABLE INITIALLY DEFERRED; (params ())
(0.003) ALTER TABLE "app_userrole" ADD CONSTRAINT "app_userrole_user_id_d61bb2ea_fk_app_user_id" FOREIGN KEY ("user_id") REFERENCES "app_user" ("id") DEFERRABLE INITIALLY DEFERRED; args=(); alias=default
CREATE INDEX "app_userrole_group_role_id_5e2f5aa5" ON "app_userrole" ("group_role_id"); (params ())
(0.002) CREATE INDEX "app_userrole_group_role_id_5e2f5aa5" ON "app_userrole" ("group_role_id"); args=(); alias=default
CREATE INDEX "app_userrole_group_user_id_2e5cca64" ON "app_userrole" ("group_user_id"); (params ())
(0.003) CREATE INDEX "app_userrole_group_user_id_2e5cca64" ON "app_userrole" ("group_user_id"); args=(); alias=default
CREATE INDEX "app_userrole_role_id_178627fc" ON "app_userrole" ("role_id"); (params ())
(0.002) CREATE INDEX "app_userrole_role_id_178627fc" ON "app_userrole" ("role_id"); args=(); alias=default
CREATE INDEX "app_userrole_user_id_d61bb2ea" ON "app_userrole" ("user_id"); (params ())
(0.002) CREATE INDEX "app_userrole_user_id_d61bb2ea" ON "app_userrole" ("user_id"); args=(); alias=default
CREATE INDEX "app_groupuser_user_id_89d3f803" ON "app_groupuser" ("user_id"); (params ())
(0.003) CREATE INDEX "app_groupuser_user_id_89d3f803" ON "app_groupuser" ("user_id"); args=(); alias=default
CREATE INDEX "app_grouprole_role_id_10d9e643" ON "app_grouprole" ("role_id"); (params ())
(0.036) CREATE INDEX "app_grouprole_role_id_10d9e643" ON "app_grouprole" ("role_id"); args=(); alias=default
(0.038)
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
(0.003) INSERT INTO "django_migrations" ("app", "name", "applied") VALUES ('app', '0001_initial', '2023-01-24T15:42:11.573132'::timestamp) RETURNING "django_migrations"."id"; args=('app', '0001_initial', datetime.datetime(2023, 1, 24, 15, 42, 11, 573132)); alias=default
 OK
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
(0.010) SELECT "django_migrations"."id", "django_migrations"."app", "django_migrations"."name", "django_migrations"."applied" FROM "django_migrations"; args=(); alias=default
Create User
(0.002) INSERT INTO "app_user" ("name") VALUES ('User 1') RETURNING "app_user"."id"; args=('User 1',); alias=default
Creating Group 1
(0.026) INSERT INTO "app_group" ("name") VALUES ('Group 1') RETURNING "app_group"."id"; args=('Group 1',); alias=default
Creating four roles:
Role 1: Can Read, Can Create
Role 2 (has Can Create like Role 1): Can Create, Can Update
Role 3 (completely disjoint from other two roles): Can Delete
Role 4 (completely disjoint from other two roles): Can Rule the World
(0.003) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 1', ARRAY[1,2]::integer[]) RETURNING "app_role"."id"; args=('Role 1', [1, 2]); alias=default
(0.001) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 2', ARRAY[2,3]::integer[]) RETURNING "app_role"."id"; args=('Role 2', [2, 3]); alias=default
(0.002) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 3', ARRAY[4]::integer[]) RETURNING "app_role"."id"; args=('Role 3', [4]); alias=default
(0.010) INSERT INTO "app_role" ("name", "permissions") VALUES ('Role 4', ARRAY[5]::integer[]) RETURNING "app_role"."id"; args=('Role 4', [5]); alias=default
Attaching Role 1, 2, and 3 to the user
(0.030) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (1, 1, NULL, NULL, ARRAY[1,2]::integer[]) RETURNING "app_userrole"."id"; args=(1, 1, None, None, [1, 2]); alias=default
(0.002) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (1, 2, NULL, NULL, ARRAY[2,3]::integer[]) RETURNING "app_userrole"."id"; args=(1, 2, None, None, [2, 3]); alias=default
(0.002) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (1, 3, NULL, NULL, ARRAY[4]::integer[]) RETURNING "app_userrole"."id"; args=(1, 3, None, None, [4]); alias=default
Attaching Role 2, 3, and 4 to the group
(0.002) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (2, 1) RETURNING "app_grouprole"."id"; args=(2, 1); alias=default
(0.001) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (3, 1) RETURNING "app_grouprole"."id"; args=(3, 1); alias=default
(0.002) INSERT INTO "app_grouprole" ("role_id", "group_id") VALUES (4, 1) RETURNING "app_grouprole"."id"; args=(4, 1); alias=default
----------------------------------------

Let's get user 1's permissions (in Python, I've converted it into a set)
(0.001) SELECT "app_userrole"."permissions" FROM "app_userrole" WHERE "app_userrole"."user_id" = 1; args=(1,); alias=default
{1, 2, 3, 4}
In Python, we use an IntEnum to represent permissions so that we can get a textual representation of a permission while storing small integers in the database
----------------------------------------

Let's attach User 1 to Group 1
(0.003) INSERT INTO "app_groupuser" ("user_id", "group_id") VALUES (1, 1) RETURNING "app_groupuser"."id"; args=(1, 1); alias=default
We also need to attach the group's roles to the user
Get group roles
(0.024) SELECT "app_grouprole"."id", "app_grouprole"."role_id", "app_role"."permissions" FROM "app_grouprole" INNER JOIN "app_role" ON ("app_grouprole"."role_id" = "app_role"."id") WHERE "app_grouprole"."group_id" = 1; args=(1,); alias=default
Attach group roles to the user via the UserRole table. Note that we attach the group role id to the user role. This allows for a cascading deletion effect if a group role is deleted.
(0.002) INSERT INTO "app_userrole" ("user_id", "role_id", "group_role_id", "group_user_id", "permissions") VALUES (1, 2, 1, 1, ARRAY[2,3]::integer[]), (1, 3, 2, 1, ARRAY[4]::integer[]), (1, 4, 3, 1, ARRAY[5]::integer[]) RETURNING "app_userrole"."id"; args=(1, 2, 1, 1, [2, 3], 1, 3, 2, 1, [4], 1, 4, 3, 1, [5]); alias=default
----------------------------------------

Let's get user 1's permissions (in Python, I've converted it into a set)
(0.001) SELECT "app_userrole"."permissions" FROM "app_userrole" WHERE "app_userrole"."user_id" = 1; args=(1,); alias=default
{1, 2, 3, 4, 5}
Let's perform a query to see whether a permission (Can Read) exists for a user
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[1])::integer[] AND "app_userrole"."user_id" = 1) LIMIT 1; args=(1, 1, 1); alias=default
User has permission: True
Let's do it for multiple permissions now
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[1, 2])::integer[] AND "app_userrole"."user_id" = 1) LIMIT 1; args=(1, 1, 2, 1); alias=default
User has permissions: True
Let's remove a disjoint Role 3 from user
(0.001) DELETE FROM "app_userrole" WHERE ("app_userrole"."group_role_id" IS NULL AND "app_userrole"."role_id" = 3 AND "app_userrole"."user_id" = 1); args=(3, 1); alias=default
Let's see if the user still has the permission
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[4])::integer[] AND "app_userrole"."user_id" = 1) LIMIT 1; args=(1, 4, 1); alias=default
User has permission: True
The reason the user still has permission is because the group the user is attached to has the permission. Take note of the SQL DELETE query performed. It explicitly states that the group_id is NULL. This is to ensure the group role that was attached wasn't deleted.
Let's delete the group role and see what happens
(0.001) SELECT "app_grouprole"."id", "app_grouprole"."role_id", "app_grouprole"."group_id" FROM "app_grouprole" WHERE ("app_grouprole"."group_id" = 1 AND "app_grouprole"."role_id" = 3); args=(1, 3); alias=default
(0.001) DELETE FROM "app_userrole" WHERE "app_userrole"."group_role_id" IN (2); args=(2,); alias=default
(0.001) DELETE FROM "app_grouprole" WHERE "app_grouprole"."id" IN (2); args=(2,); alias=default
Let's see if the user still has the permission
(0.001) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[4])::integer[] AND "app_userrole"."user_id" = 1) LIMIT 1; args=(1, 4, 1); alias=default
User has permission: False
The reason the user no longer has permission is because the group role was deleted. The user role was also deleted because the group role was deleted via a database CASCADE.
Let's delete the group and see what happens
(0.001) SELECT "app_group"."id", "app_group"."name" FROM "app_group" WHERE "app_group"."id" = 1; args=(1,); alias=default
(0.001) SELECT "app_grouprole"."id" FROM "app_grouprole" WHERE "app_grouprole"."group_id" IN (1); args=(1,); alias=default
(0.001) SELECT "app_groupuser"."id" FROM "app_groupuser" WHERE "app_groupuser"."group_id" IN (1); args=(1,); alias=default
(0.027) DELETE FROM "app_userrole" WHERE "app_userrole"."group_role_id" IN (1, 3); args=(1, 3); alias=default
(0.001) DELETE FROM "app_userrole" WHERE "app_userrole"."group_user_id" IN (1); args=(1,); alias=default
(0.000) DELETE FROM "app_grouprole" WHERE "app_grouprole"."id" IN (3, 1); args=(3, 1); alias=default
(0.001) DELETE FROM "app_groupuser" WHERE "app_groupuser"."id" IN (1); args=(1,); alias=default
(0.000) DELETE FROM "app_group" WHERE "app_group"."id" IN (1); args=(1,); alias=default
Let's see if the user still has Role 2's permission
(0.002) SELECT 1 AS "a" FROM "app_userrole" WHERE ("app_userrole"."permissions" @> (ARRAY[2, 3])::integer[] AND "app_userrole"."user_id" = 1) LIMIT 1; args=(1, 2, 3, 1); alias=default
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
