# Endpointy backendu dla modułu dostępu użytkownika

Poniżej znajduje się specyfikacja API, którą frontend może podłączyć zamiast aktualnego mocka.

## POST /api/auth/login

Opis: logowanie użytkownika.

Request JSON:

```json
{
  "emailOrUsername": "admin",
  "password": "admin"
}
```

Response 200 JSON:

```json
{
  "accessToken": "jwt-or-session-token",
  "refreshToken": "refresh-token",
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

Response 401 JSON:

```json
{
  "message": "Niepoprawne dane logowania."
}
```

## POST /api/auth/register

Opis: rejestracja nowego użytkownika.

Request JSON:

```json
{
  "username": "new_user",
  "email": "new_user@example.com",
  "password": "supersecret",
  "confirmPassword": "supersecret"
}
```

Response 201 JSON:

```json
{
  "message": "Konto utworzone.",
  "user": {
    "id": "uuid",
    "username": "new_user",
    "email": "new_user@example.com"
  }
}
```

Response 409 JSON (email lub username zajęty):

```json
{
  "message": "Użytkownik o podanym emailu lub nazwie już istnieje."
}
```

## GET /api/auth/me

Opis: pobiera dane aktualnie zalogowanego użytkownika na podstawie tokena.

Headers:

```text
Authorization: Bearer <accessToken>
```

Response 200 JSON:

```json
{
  "id": "uuid",
  "username": "admin",
  "email": "admin@example.com"
}
```

Response 401 JSON:

```json
{
  "message": "Brak autoryzacji."
}
```

## POST /api/auth/logout

Opis: unieważnienie sesji/tokena po stronie serwera.

Headers:

```text
Authorization: Bearer <accessToken>
```

Response 200 JSON:

```json
{
  "message": "Wylogowano poprawnie."
}
```

## POST /api/auth/refresh

Opis: odświeżenie access tokenu.

Request JSON:

```json
{
  "refreshToken": "refresh-token"
}
```

Response 200 JSON:

```json
{
  "accessToken": "new-access-token"
}
```

## Minimalne wymagania walidacji backendu

- email musi mieć poprawny format.
- password minimum 6 znaków.
- confirmPassword musi być równe password.
- username i email muszą być unikalne.
