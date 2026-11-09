# Status site on Cloudflare Workers

## Scope

Workers Static Assets hosts the public status page independently of primaryserver.
GitHub Actions retains the Upptime monitoring, incidents, historical data, graphs, and static-site generation.
Do not move the monitoring probes onto the monitored server.
Do not edit template-generated Upptime workflows.

The source branch is `master`.
The generated static branch is `gh-pages`.
The Worker is `uc-status` in account `10bd9b12698da3c8aa30ff9ebfa81c71`.
The canonical hostname is `status.uniclipboard.app`.

## Packaging and routing

`scripts/prepare-assets.sh` exports an exact generated commit into `.build/assets`.
The export excludes the old CNAME control file and GitHub Pages marker.
The Worker serves the static bundle directly.
Only history, incident, and rate-limit client routes invoke the Worker to fetch the root shell.
Missing scripts and unknown paths return 404.
HTML and service-worker files revalidate; hashed client assets cache immutably.
The page reads current service and incident data from GitHub APIs.
A new data sample does not require a Worker deployment.

## Automatic releases

Cloudflare Workers Builds uses the repository's GitHub connection and an existing account-owned Workers build token.
No expiring local OAuth token is copied into GitHub Actions.
The production build trigger watches `gh-pages`.
Monitoring samples remain on `master` and do not cause unnecessary static deployments.
The trigger uses `scripts/worker-build.sh` from the current source branch and package the current generated branch.
The build records the generated commit in `.build/source.json`.
The deployment command pins Wrangler 4.158.0 and runs HTTP acceptance after deployment.

After changing deployment configuration on `master`, run the `uc-status` Cloudflare Workers Builds trigger.
Generated-site commits trigger production deployments automatically.
For an operator deployment from the source checkout:

```sh
bun install --frozen-lockfile
git fetch origin gh-pages
bun run build
bun run deploy
python3 e2e/acceptance.py https://status.uniclipboard.app .build/assets .migration/public-http.json
```

The operator CLI uses the existing authorized Cloudflare account.
Keep generated artifacts and local authorization outside Git.

## Acceptance and recovery

HTTP acceptance verifies the homepage, historical and incident paths, every static asset digest, cache headers, and missing-path behavior.
The JSON receipt contains no incident credentials or deployment tokens.
Browser rendering remains user-owned.

Keep the last Worker version and generated commit identity for rollback.
Use a Workers version rollback to restore the previous static deployment.
The GitHub monitoring history does not roll back with the Worker.
The old Vercel CNAME is `9ef2e5c63d919aee.vercel-dns-017.com`.
The old Vercel site returned HTTP 402 before migration, so verify recovery availability before restoring that route.

Cloudflare manages the custom-domain TLS certificate.
Do not install an origin certificate on primaryserver for this hostname.
