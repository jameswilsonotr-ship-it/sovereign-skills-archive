# olette-box SFTP sync

[`olette-box.ssh-config.example`](olette-box.ssh-config.example) contains
OpenSSH aliases for:

```text
100.115.0.111:22
```

The aliases cover the `bunny` and `olivia` accounts. Each `IdentityFile` is a
path placeholder; install the corresponding private key out of band with mode
`0600`. Never paste key bytes into this repository.

[`olette-box.sync.config.example.json`](olette-box.sync.config.example.json)
is the client-neutral manifest used by the offline Pydantic smoke test. It
describes the destination and key paths but does not connect or sync.

Example one-shot checks after keys and host fingerprints are installed:

```sh
sftp -F bridges/sftp/olette-box.ssh-config.example olette-box-bunny
sftp -F bridges/sftp/olette-box.ssh-config.example olette-box-olivia
```

Use the account-specific alias and an explicit remote path for any real sync.
Populate `known_hosts` from a trusted out-of-band fingerprint rather than
disabling host-key checking.
