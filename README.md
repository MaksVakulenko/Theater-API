# Theater-API
This API allows users to view available shows and book seats online for a theater.
<br>
It makes the booking process easier by letting customers choose seats and make reservations without going to the theater in person.
<br>
Built with Django and Django REST Framework, the API is easy to use and can be connected to any front-end application.



in this practice, ordinary users have access to the operations of only reservation tickets, 
<br>as well as Get requests for all endpoints, 
<br>
and admin users have access to all operations described below


## API Endpoints

### Documentation
- `GET /api/doc/` - API documentation.
- `Get api/doc/swagger/` - Swagger documentation.
- `GET api/doc/redoc/` - Redoc documentation.

### Actors
- `GET /api/theatre/actors/` - Retrieve a list of actors.
- `POST /api/theatre/actors/` - Create a new actor.

### Genres
- `GET /api/theatre/genres/` - Retrieve a list of genres.
- `POST /api/theatre/genres/` - Create a new genre.

### Performances
- `GET /api/theatre/performances/` - Retrieve a list of performances.
- `POST /api/theatre/performances/` - Create a new performance.
- `GET /api/theatre/performances/{id}/` - Retrieve a specific performance.
- `PUT /api/theatre/performances/{id}/` - Update a performance.
- `PATCH /api/theatre/performances/{id}/` - Partially update a performance.
- `DELETE /api/theatre/performances/{id}/` - Delete a performance.

### Plays
- `GET /api/theatre/plays/` - Retrieve a list of plays.
- `POST /api/theatre/plays/` - Create a new play.
- `GET /api/theatre/plays/{id}/` - Retrieve a specific play.
- `PUT /api/theatre/plays/{id}/` - Update a play.
- `PATCH /api/theatre/plays/{id}/` - Partially update a play.
- `DELETE /api/theatre/plays/{id}/` - Delete a play.

### Reservations
- `GET /api/theatre/reservations/` - Retrieve a list of reservations.
- `POST /api/theatre/reservations/` - Create a new reservation.
- `GET /api/theatre/reservations/{id}/` - Retrieve a specific reservation.

### Theatre Halls
- `GET /api/theatre/theater-halls/` - Retrieve a list of theatre halls.
- `POST /api/theatre/theater-halls/` - Create a new theatre halls.

### User Management
- `GET /api/user/me/` - Retrieve the current user’s profile.
- `PUT /api/user/me/` - Update the current user’s profile.
- `PATCH /api/user/me/` - Partially update the current user’s profile.
- `POST /api/user/register/` - Register a new user.
- `POST /api/user/token/` - Obtain a new authentication token.
- `POST /api/user/token/refresh/` - Refresh the authentication token.
- `POST /api/user/token/verify/` - Verify the authentication token.
