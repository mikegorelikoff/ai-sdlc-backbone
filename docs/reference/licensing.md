# Licensing and distribution

## User contract

License keys use the `ASDL-...` product namespace. The installer treats the
licensing service as authoritative and fails closed. Keys are not validated
only in the client and no universal secret is embedded in the package.

`POST /v1/install` accepts the key, installer version, requested version, and
platform. A successful response returns product/version metadata, a short-lived
download URL, and the exact SHA-256. The URL is a grant, not private repository
access, and must not contain GitHub credentials.

## Errors

The public error codes are `INVALID_LICENSE`, `EXPIRED_LICENSE`,
`REVOKED_LICENSE`, `VERSION_NOT_ALLOWED`, `INSTALL_LIMIT_REACHED`,
`UNSUPPORTED_PLATFORM`, and `RELEASE_NOT_FOUND`.

## Integrity and installation

The installer rejects redirects, cross-origin download grants, malformed
metadata, oversized downloads, mismatched checksums, path traversal, links,
and unsupported archive members. It cleans temporary data after success or
failure. Installing from an artifact does not require a Git checkout.

See the machine-readable [OpenAPI contract](licensing-api.yaml).
