# How to Run Migrations on Render

## Quick Fix: Run Migrations via Render Shell

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your backend service (`studymate-tkmw`)
3. Click on the **"Shell"** tab
4. Run the following command:
   ```bash
   python manage.py migrate
   ```
5. Wait for migrations to complete
6. Try logging in again

## Alternative: Update Build Command

I've updated the `render.yaml` file to automatically run migrations during build. If you're using the YAML file, migrations will run automatically.

If you're manually configuring, update your **Build Command** in Render to:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

## Verify Migrations

After running migrations, you can verify tables were created by running in the Shell:
```bash
python manage.py showmigrations
```

All migrations should show `[X]` (checked) if they've been applied.

## Create Superuser (Optional)

If you need an admin user, run in the Shell:
```bash
python manage.py createsuperuser
```

Then follow the prompts to create an admin account.
