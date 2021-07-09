# Generated by Django 3.1.12 on 2021-07-03 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("countries_plus", "0005_auto_20160224_1804"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("DIAMOND", "diamond"),
                            ("GOLD", "gold"),
                            ("BRONZE", "bronze"),
                            ("FREE", "free"),
                        ],
                        default="FREE",
                        max_length=30,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=20),
                ),
            ],
            options={
                "verbose_name": "Membership",
                "verbose_name_plural": "Memberships",
                "ordering": ["-created", "-modified"],
                "managed": True,
            },
        ),
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
        migrations.AddField(
            model_name="user",
            name="accept_terms",
            field=models.BooleanField(default=False, verbose_name="Accept our terms"),
        ),
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.CharField(
                blank=True,
                max_length=600,
                null=True,
                unique=True,
                verbose_name="Residntial Address",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="balance",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=20, null=True
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="city",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Located City"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="country",
            field=models.ForeignKey(
                default="NG",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="countries_plus.country",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="dob",
            field=models.DateField(blank=True, null=True, verbose_name="Date of Birth"),
        ),
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("", "Gender"), ("Male", "MALE"), ("Female", "FEMALE")],
                max_length=7,
                null=True,
                verbose_name="Gender",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="has_paid",
            field=models.BooleanField(default=False, verbose_name="User has Paid"),
        ),
        migrations.AddField(
            model_name="user",
            name="ip",
            field=models.GenericIPAddressField(null=True, verbose_name="User IP"),
        ),
        migrations.AddField(
            model_name="user",
            name="is_field_worker",
            field=models.BooleanField(
                default=False, verbose_name="Are you a field worker"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="last name"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="marital",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Marital"),
                    ("Single", "Single"),
                    ("Married", "Married"),
                    ("Divorced", "Divorced"),
                    ("Seperated", "Seperated"),
                ],
                max_length=10,
                null=True,
                verbose_name="Marital Status",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_no",
            field=models.CharField(
                blank=True, max_length=13, verbose_name="Phone Number"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="state",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "States"),
                    ("Abia", "Abia"),
                    ("Adamawa", "Adamawa"),
                    ("Akwa Ibom", "Akwa Ibom"),
                    ("Anambra", "Anambra"),
                    ("Bauchi", "Bauchi"),
                    ("Bayelsa", "Bayelsa"),
                    ("Benue", "Benue"),
                    ("Borno", "Borno"),
                    ("Cross River", "Cross River"),
                    ("Delta", "Delta"),
                    ("Ebonyi", "Ebonyi"),
                    ("Enugu", "Enugu"),
                    ("Edo", "Edo"),
                    ("Ekiti", "Ekiti"),
                    ("Gombe", "Gombe"),
                    ("Imo", "Imo"),
                    ("Jigawa", "Jigawa"),
                    ("Kaduna", "Kaduna"),
                    ("Kano", "Kano"),
                    ("Katsina", "Katsina"),
                    ("Kebbi", "Kebbi"),
                    ("Kogi", "Kogi"),
                    ("Kwara", "Kwara"),
                    ("Lagos", "Lagos"),
                    ("Nasarawa", "Nasarawa"),
                    ("Niger", "Niger"),
                    ("Ogun", "Ogun"),
                    ("Ondo", "Ondo"),
                    ("Osun", "Osun"),
                    ("Oyo", "Oyo"),
                    ("Plateau", "Plateau"),
                    ("Rivers", "Rivers"),
                    ("Sokoto", "Sokoto"),
                    ("Taraba", "Taraba"),
                    ("Yobe", "Yobe"),
                    ("Zamfara", "Zamfara"),
                ],
                max_length=15,
                null=True,
                verbose_name="State of Origin",
            ),
        ),
        migrations.CreateModel(
            name="UserMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "membership",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="usermembership",
                        to="users.membership",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usermembership",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("active", models.BooleanField(default=False)),
                (
                    "user_membership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscription",
                        to="users.usermembership",
                    ),
                ),
            ],
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
                "ordering": ["-created", "-modified"],
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Investor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "recommended_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ref_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="investorprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Investor",
                "verbose_name_plural": "Investors",
                "ordering": ["-created", "-modified"],
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="FieldWorker",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("is_employed", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fworkerprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "FieldWorker",
                "verbose_name_plural": "FieldWorkers",
                "ordering": ["-created", "-modified"],
                "managed": True,
            },
        ),
    ]