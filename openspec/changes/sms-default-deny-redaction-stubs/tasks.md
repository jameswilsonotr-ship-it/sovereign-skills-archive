# Tasks

- [x] Add an offline SMS sender stub with a default-deny policy.
- [x] Ensure explicit opt-in remains a local simulation with `sent=False`.
- [x] Add fixed recipient/body redaction and recursive metadata redaction.
- [x] Add pytest coverage using fake inputs only.
- [ ] Replace the stub with a separately reviewed provider adapter only when
  production SMS behavior is explicitly authorized.
