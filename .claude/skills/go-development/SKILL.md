---
name: go-development
description: Conventions and verification steps for writing or changing Go code. Use whenever a task touches .go files or go.mod in a repository with a go.mod. Inspects go.mod and the existing API architecture (net/http, Gin, Fiber, Echo, chi, gRPC), writes idiomatic Go with correct error handling and context use, and runs gofmt, go vet and the applicable tests.
argument-hint: "<Go task>"
---

# Go Development

Task: $ARGUMENTS

A stack overlay used inside `/execute-task`, `/feature-development`, or `/bug-fix`. It adds Go
specifics; it does not replace the lifecycle, approval gates, or delivery report.

**Use when:** the repository has a `go.mod` and the change touches Go code. **Do not use** in
non-Go projects, and do not propose rewriting non-Go services in Go.

## 1. Inspect first

- `go.mod`: module path, `go` directive and `toolchain` (respect them), direct dependencies.
  `go version` to compare with the local toolchain.
- Layout: `cmd/`, `internal/`, `pkg/`, `api/`, existing package boundaries.
- HTTP or RPC framework actually used (`net/http`, `chi`, `gin`, `fiber`, `echo`, gRPC),
  middleware chain, router registration, request/response types, error response format.
- Data access: `database/sql`, `sqlx`, `pgx`, `gorm`, `ent`, `sqlc`; migrations tool.
- Tooling present: `Makefile` targets, `.golangci.yml`, `staticcheck`, `buf`, code
  generation (`go generate`, `sqlc`, `mockgen`, `oapi-codegen`).

## 2. Write idiomatic Go that fits the codebase

- Follow the existing structure and naming. Keep packages cohesive; avoid new top-level layers.
- **Errors:** return errors, do not panic in library or handler code. Wrap with context
  (`fmt.Errorf("load user %d: %w", id, err)`), compare with `errors.Is`/`errors.As`, never
  ignore an error silently, and map errors to the project's existing HTTP/gRPC error format at
  the boundary.
- **Context:** accept `ctx context.Context` as the first parameter for I/O, pass it down,
  respect cancellation, and do not store it in structs.
- **Concurrency:** every goroutine has an owner and an exit path; protect shared state; use
  `errgroup` or channels as the codebase already does; no goroutine leaks in handlers.
- **Resources:** `defer rows.Close()`, `defer resp.Body.Close()`, check `rows.Err()`.
- **Security:** parameterized queries only; validate input at the handler; enforce authz in
  middleware or the service layer as the codebase does; never log tokens or passwords.
- Prefer the standard library and existing dependencies. Adding a module needs justification;
  a new web framework needs owner approval.
- Keep exported API and JSON field names backward compatible unless the change is approved.

## 3. Test

- Table-driven tests with `t.Run`, `httptest` for handlers, interfaces or the existing mock
  approach for dependencies. Use `t.Helper()`, `t.Cleanup()`, and `t.Parallel()` where the
  codebase does.
- Integration tests follow the project's existing approach (build tags, testcontainers,
  docker compose). Do not hit real external services.

## 4. Verify (report each command and result)

```
gofmt -l .            # must print nothing; fix with gofmt -w on changed files
go vet ./...
go build ./...
go test ./...         # or the narrower package first, then ./...
go test -race ./...   # when the code is concurrent and the environment supports it
golangci-lint run     # only if the project configures it
go mod tidy           # only if dependencies changed; review the go.mod/go.sum diff
```

If the project's `Makefile` or CI defines these differently, use the project's commands.
If a tool is not installed, say so rather than claiming it passed.

## Example invocations

```
/go-development Add pagination to GET /patients
/go-development Refactor the order service to propagate context
/feature-development Add JWT authentication to the Go API   (go-development applies inside)
```
