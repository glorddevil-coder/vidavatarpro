# Database Setup Guide

## Supabase Setup

### 1. Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Copy project URL and API keys to `.env.local`

### 2. Create Tables
Run the SQL migrations in Supabase SQL Editor:

```sql
-- Copy contents of db/migrations/001_initial_schema.sql
-- Paste in Supabase SQL Editor and execute
```

### 3. Enable Realtime
In Supabase dashboard:
1. Go to Database → Realtime
2. Enable realtime for tables: `projects`, `export_jobs`
3. This enables real-time sync across devices

### 4. Seed Data
```sql
-- Copy contents of db/migrations/002_seed_data.sql
-- Paste and execute
```

## Local PostgreSQL Setup (Alternative)

If running locally:

```bash
# Create database
createdb aurastudio

# Run migrations
psql aurastudio < db/migrations/001_initial_schema.sql
psql aurastudio < db/migrations/002_seed_data.sql

# Verify
psql aurastudio -c "\dt"
```

## Environment Variables

Add to `.env.local`:

```env
# Supabase
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key

# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=aurastudio-assets
```

## Real-time Sync Architecture

**How It Works:**
1. User edits script on Mobile → Supabase realtime listener fires
2. Desktop receives update instantly via `projects` subscription
3. All changes trigger `updated_at` timestamp for cache invalidation

**Listener Example (Next.js):**
```typescript
useEffect(() => {
  const subscription = supabase
    .from('projects')
    .on('*', (payload) => {
      // Update local state
      setProjects(prev => /* merge update */);
    })
    .subscribe();

  return () => subscription.unsubscribe();
}, []);
```
