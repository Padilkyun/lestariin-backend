

- Django 5.2.7
- Django REST Framework
- Django REST Framework Simple JWT
- Google Generative AI (Gemini)
- SQLite (default database, can be switched to MySQL)
- Pillow (for image handling)


2. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Run migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the development server**:
   ```
   python manage.py runserver
   ```

The server will run at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication

- **POST /api/signup/**: Register a new user.
  - Body: `{"email": "user@example.com", "name": "User Name", "password": "password123"}`
  - Response: User data and JWT tokens.

- **POST /api/login/**: Login an existing user (general login, allows both admin and user).
  - Body: `{"email": "user@example.com", "password": "password123"}`
  - Response: User data and JWT tokens.

- **POST /api/admin/login/**: Login specifically for admin users (staff or superuser).
  - Body: `{"email": "admin@example.com", "password": "password123"}`
  - Response: User data and JWT tokens.
  - Note: Only users with `is_staff=True` or `is_superuser=True` can login via this endpoint.

- **POST /api/user/login/**: Login specifically for regular users (non-admin).
  - Body: `{"email": "user@example.com", "password": "password123"}`
  - Response: User data and JWT tokens.
  - Note: Admin users cannot login via this endpoint.

### Profile Management

- **GET /api/profile/**: Retrieve the authenticated user's profile.
  - Headers: `Authorization: Bearer <access_token>`
  - Response: Profile data including bio and photo URL.

- **PUT /api/profile/**: Update the authenticated user's profile.
  - Headers: `Authorization: Bearer <access_token>`
  - Body: `{"bio": "Updated bio", "photo": <file>}` (use multipart/form-data for photo)
  - Response: Updated profile data.

### Chatbot

- **POST /api/chatbot/**: Send a message to the chatbot.
  - Headers: `Authorization: Bearer <access_token>`
  - Body: `{"message": "Hello, chatbot!"}`
  - Response: `{"response": "Chatbot's reply"}`

### Report Submission

- **POST /api/reports/**: Submit a report with image, description, latitude, and longitude. The image is analyzed using Gemini API for environmental issue classification including water turbidity, forest fires, public fires, trash levels, and illegal logging. Note: Not all classifications may be present in the response, as the analysis focuses on what is actually detected in the image (other fields may be null).
  - Headers: `Authorization: Bearer <access_token>`
  - Body: `{"image": <file>, "description": "Report description", "latitude": 12.345, "longitude": 67.890}` (use multipart/form-data)
  - Response: Report data including image URL, classifications (water_classification, forest_classification, public_fire_classification, trash_classification, illegal_logging_classification may be null if not detected), and verification status.

## Configuration

- **Database**: Configured for SQLite by default. To use MySQL, update `DATABASES` in `backend/settings.py` and install `mysqlclient`.
- **Gemini API Key**: Set your Google Gemini API key in `backend/settings.py` under `GEMINI_API_KEY`.
- **Media Files**: Profile photos are stored in the `media/` directory.

## API Usage Tutorial

For detailed tutorials on all API endpoints, please refer to the dedicated `API_TUTORIAL.txt` file in the project root. It contains comprehensive guides for each endpoint including:

- User registration (signup)
- General login
- Admin login
- User login
- Profile management (get/update)
- Chatbot interaction
- Report submission
- All reports retrieval
- User reports retrieval
- Report verification (admin only)
- Leaderboard retrieval

Each tutorial includes:
- Endpoint description
- Request format
- curl examples
- Success and error responses
- Complete Python requests example

The `API_TUTORIAL.txt` file provides step-by-step instructions for using every API endpoint in the Backend Beyonder project.

## Running with Public Access using Ngrok

To make your API accessible publicly, you can use ngrok:

1. **Install pyngrok**:
   ```
   pip install pyngrok
   ```

2. **Run the server with ngrok**:
   ```
   python run_with_ngrok.py
   ```

   This will start the Django server and create a public tunnel. The output will show the public URL like `https://xxxxx.ngrok-free.app`.

3. **Access the API publicly**:
   Replace `http://127.0.0.1:8000` with your ngrok URL in all API calls.

## Testing the API

You can test the API using tools like Postman or curl. Replace `http://127.0.0.1:8000` with your ngrok URL if using public access.

1. **Signup**:
   ```
   curl -X POST http://127.0.0.1:8000/api/signup/ \
   -H "Content-Type: application/json" \
   -d '{"email": "test@example.com", "name": "Test User", "password": "password123"}'
   ```

2. **Login** (General):
   ```
   curl -X POST http://127.0.0.1:8000/api/login/ \
   -H "Content-Type: application/json" \
   -d '{"email": "test@example.com", "password": "password123"}'
   ```

3. **Admin Login** (for admin users only):
   ```
   curl -X POST http://127.0.0.1:8000/api/admin/login/ \
   -H "Content-Type: application/json" \
   -d '{"email": "admin@example.com", "password": "password123"}'
   ```

4. **User Login** (for regular users only):
   ```
   curl -X POST http://127.0.0.1:8000/api/user/login/ \
   -H "Content-Type: application/json" \
   -d '{"email": "user@example.com", "password": "password123"}'
   ```

5. **Chatbot** (replace `<access_token>` with the token from login):
   ```
   curl -X POST http://127.0.0.1:8000/api/chatbot/ \
   -H "Authorization: Bearer <access_token>" \
   -H "Content-Type: application/json" \
   -d '{"message": "Hello!"}'
   ```

6. **Report Submission** (replace `<access_token>` with the token from login):
   ```
   curl -X POST http://127.0.0.1:8000/api/reports/ \
   -H "Authorization: Bearer <access_token>" \
   -F "image=@/path/to/image.jpg" \
   -F "description=Description of the report" \
   -F "latitude=12.345" \
   -F "longitude=67.890"
   ```

   **Response (Success - 201 Created):**
   ```json
   {
     "id": 1,
     "image_url": "http://127.0.0.1:8000/media/report_images/image.jpg",
     "description": "Description of the report",
     "latitude": 12.345,
     "longitude": 67.890,
     "water_classification": "Air_bersih",
     "forest_classification": "non_fire",
     "public_fire_classification": "no_fire",
     "trash_classification": "sedikit_sampah",
     "illegal_logging_classification": "tidak_penebangan_liar",
     "verified": false,
     "created_at": "2023-10-01T12:00:00Z"
   }
   ```

## Security Notes

- JWT tokens are used for authentication.
- Passwords are hashed using Django's default password hasher.
- Ensure the Gemini API key is kept secure and not committed to version control.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test thoroughly.
5. Submit a pull request.

## License

This project is licensed under the MIT License.
