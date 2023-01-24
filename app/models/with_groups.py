from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    """Defines a user"""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    """Defines a role and the permissions attached to a user"""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    permissions = ArrayField(models.PositiveIntegerField())

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """Defines the roles attached to the user"""

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    group_role = models.ForeignKey("GroupRole", on_delete=models.CASCADE, null=True)
    group_user = models.ForeignKey("GroupUser", on_delete=models.CASCADE, null=True)
    permissions = ArrayField(models.PositiveIntegerField())

    def __str__(self):
        return f"{self.user.name} - {self.role.name}"


class Group(models.Model):
    """A group that users can be attached to"""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GroupRole(models.Model):
    """Defines the roles attached to the group"""

    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.name} - {self.role.name}"


class GroupUser(models.Model):
    """Defines the groups attached to the user"""

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.group.name}"
