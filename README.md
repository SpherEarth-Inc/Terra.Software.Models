# Software.Models

Shared Django models for Spherearth platforms (`spherearth` package).

Migration files live here under `spherearth/*/migrations/`.  
**Generate and apply them from** [`Spherearth.Migrations`](../Spherearth.Migrations) (same pattern as Rockae DataMigration) — not from Admin.API.

## Install (API consumers)

```bash
pip install -e /path/to/Software.Models
```

## Imports

```python
from spherearth.news.models import News
from spherearth.platforms.models import Platform
from spherearth.account.models import User
```

## Django settings (consumers)

```python
INSTALLED_APPS = [
    'spherearth.shared',
    'spherearth.account',
    'spherearth.platforms',
    'spherearth.invites',
    'spherearth.news',
    'spherearth.media',
    # ...
]
AUTH_USER_MODEL = 'account.User'
```

## Schema changes

1. Edit models in this repo
2. From `Spherearth.Migrations`:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py seed_spherearth_defaults
   ```

3. Commit the new migration files in **this** repo
4. Bump / reinstall this package in Admin.API
