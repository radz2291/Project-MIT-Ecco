# ECCO-051 execution coordination

Owner assignment: 30 October 2026. Master worker `ECCO-051-master-20261030`, run `bcd5c3fa-d07d-4ac6-ba2d-fcd6d6a02a2e`.

Controlling decisions: T-050 at `58013a6f5a907bfdfe9a7c7d63405e3306c2c42c`. All 16 selected native source hashes matched before execution. Local base `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`, main; unrelated modified S04/S05 direction files and untracked work preserved. Remote main initially `5f6b18f642d456815f5779a2f7b3a82964abb97e`. Publication will use an isolated task branch containing permitted task outputs.

The open BHA v007 Blender session is dirty and must remain untouched. Builders inspect and build separate background files. No locked previs files may be overwritten.

| Worker | Exclusive outputs | Scheduling |
|---|---|---|
| ECCO-052 | New ECCO/BHA/finish successors; T-052 records | First wave |
| ECCO-053 | New World/Formation/CasedHole successors; T-053 records | First wave; release interface for 054/055 |
| ECCO-056 | New Acoustics/Waveform package; T-056 records | First wave; visual choice before presentation finalization |
| ECCO-054 | New DigitalEnvironment/MeasurementReveal packages; T-054 records | Integrate stable World release |
| ECCO-055 | New Surface/descent successors; T-055 records | Integrate stable World release |

Master alone owns common manifests, aggregate records and Git operations. Each builder claims and heartbeats its own Work run. Three builder slots are available; later builders start as slots clear. Internal version handoffs do not imply owner acceptance.

All renders require a master queue grant. Only one renderer at a time. Record complete render-to-file times, cold/cache conditions, and settings. Benchmark representative/heaviest frames before a batch; every permitted frame must take strictly less than five seconds. Failed benchmarks remain visible.

Master independently reads saved candidates, checks relevant rendered evidence and source/consumer alignment, and returns bounded defects. A shared edit must propagate into two saved/reopened consumer copies without changing their local camera/timing or behavior. Waveform presentation remains pending Radzi's concrete visual choice. This stage excludes final movie batches and film assembly.
