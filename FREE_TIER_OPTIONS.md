# Free-tier options for database and shared rate-limit storage

Checked 15 November 2026 against providers' current public documentation. No provider account, database, paid resource, credential, or production setting was created or changed.

## PostgreSQL candidates

### Neon Free

Neon currently lists its Free plan at $0/month with no credit card requirement. Its pricing page lists up to 100 projects, 100 CU-hours per project, up to 2 CU, 1 GB of PostgreSQL storage per project and 20 GB total per account, plus 5 GB public network transfer per project. Compute automatically scales to zero after five minutes of inactivity; there is no CU-hour charge while suspended. The Free plan is described as permanent rather than a trial. The page lists a six-hour history window and one manual snapshot, but no instant restore on Free. Verify current quotas and retention in the account before relying on them; usage or policy can change. Neon is the best low-cost candidate to test for this small Flask community-vote workload, but it is not yet connected, tested with the site's schema, or configured for Preview/Production.

## Supabase Free

Supabase currently lists $0/month, 500 MB database size, 5 GB egress, 1 GB file storage, and up to two active projects. Projects pause after one week of inactivity. Automatic backups are not included on Free (daily backups are listed on Pro). This is a workable alternative for a small trial, but pausing after inactivity and no included backups make it less suitable for an unattended production community store unless those limitations are acceptable and independently addressed.

## Redis-compatible rate-limit storage

### Upstash Redis Free

Upstash currently lists a Free Redis plan with 250 MB maximum data, 10 GB maximum bandwidth, and a FAQ allowance of 500,000 commands per month. The pricing comparison also lists a 10,000 commands/second ceiling, TLS and REST API availability; the Free tier does not list a strong-consistency guarantee, multi-zone high availability, an uptime SLA, IP allowlisting or encryption at rest. Treat it as a development/low-volume candidate only until the application's actual limiter semantics, quota behavior, failure mode and security needs are tested. It is separate from and does not provide durable PostgreSQL data.

Upstash documents standard account creation in its console. It also describes an instant free Redis database endpoint for agents, but unclaimed databases expire after 72 hours. That flow was intentionally not used because this task does not authorize creating resources or receiving credentials.

## Vercel integration and setup outline

Vercel's Postgres documentation says its former Vercel Postgres offering is no longer available; new Postgres connections are made through external providers in the Vercel Marketplace. Providers can inject environment variables into a selected Vercel project. The Vercel account must be reviewed by the owner before installing an integration or selecting Preview/Production environment scopes.

To enable persistent community ratings/likes later, an owner would create or select a Neon/Supabase project, inspect its current limits/backup policy, and add the provider-issued Postgres connection string as `DATABASE_URL` in the **Preview** environment first. Deploy a Preview and verify connection, schema initialization/migrations, writes/reads, connection pooling, SSL, rollback and logs using non-production test data. Only after acceptance should the owner separately authorize production configuration and deployment. Do not copy credentials into repository files or logs. The application currently falls back to SQLite in `/tmp` on Vercel if `DATABASE_URL` is absent; that is temporary per-instance storage, not durable persistence.

To trial shared rate limiting later, create/select a Redis-compatible account and configure the correct provider-issued URL as `REDIS_URL` in **Preview** only. Verify library compatibility, TLS, URL parsing, increment/expiry/atomicity, quota exhaustion, network outages, request latency and fail-open/fail-closed behavior. Do not claim shared limits until runtime behavior is measured. No `REDIS_URL` currently exists in this branch environment, and no credential was supplied.

## Recommendation

Document Neon Free as the PostgreSQL candidate for a controlled Preview experiment, and Upstash Redis Free as an optional low-volume rate-limit experiment. They are genuinely listed at $0 on their official pages, but both have material quotas and limitations. Do not provision them, claim they are connected, move production data, or state that ratings are persistent/shared until the owner explicitly authorizes configuration and integration is proven.

## Sources

[1]: https://neon.com/pricing "Neon pricing"
[2]: https://supabase.com/pricing "Supabase pricing"
[3]: https://upstash.com/pricing/redis "Upstash Redis pricing"
[4]: https://upstash.com/docs/redis/overall/getstarted "Upstash Redis getting started"
[5]: https://vercel.com/docs/postgres "Postgres on Vercel"
