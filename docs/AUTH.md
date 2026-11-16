# Authentication and Authorization

## Authentication vs Authorization
- **Authentication** = who are you? (login, verifying identity with a password/JWT token)
- **Authorization** = what are you allowed to do? (checking the role's permissions)
A user must be authenticated first; then authorization decides each action.

## Roles
| Action | ADMIN | HR | EMPLOYEE |
|---|---|---|---|
| Create employee | Yes | Yes | No |
| View all employees | Yes | Yes | No |
| View own record | Yes | Yes | Yes |
| Update employee | Yes | Yes | Own contact info only |
| Delete (soft delete) employee | Yes | No | No |
| Create department | Yes | No | No |
| Request leave | Yes | Yes | Own only |
| Approve leave | Yes | Yes | No |

## Design notes
- Login returns a JWT containing user id and role; each request sends it in the `Authorization: Bearer <token>` header.
- A FastAPI dependency (e.g. `require_role("ADMIN", "HR")`) checks the role per endpoint.
- Passwords stored hashed (bcrypt), never plain text.
- Return 401 when not authenticated, 403 when authenticated but not allowed.