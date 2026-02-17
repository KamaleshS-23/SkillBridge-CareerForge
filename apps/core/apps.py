from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

{
    "python.linting.pylintArgs": [
        "--init-hook",
        "import sys; sys.path.append('${workspaceFolder}')"
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}"
    ]
}
