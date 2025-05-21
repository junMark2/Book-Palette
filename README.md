# Book-Palette

## Project Description and Overview

Project Name: “Book Palette” (Django REST Framework + Vue.js)

This project is a student-level web application designed to visualize users’ reading preferences as distinct colors based on book genres. It uses Django REST Framework (backend) and Vue.js (frontend).

### Project Overview

Build a functional book community application. Users mark books as read, generating a unique color profile based on book genres. Fetch book data directly from the Aladin API. Use the Aladin API key provided below.

Aladin API Key: ttbjhpark9706021328002

## Requirements & Detailed Tasks

### Step 1: ERD and Database Modeling

Create an ERD with the following simplified database structure:
  - User: id, email, username, password, profile_image, represent_color (HEX), created_at
  - Book: id, title, author, publisher, isbn, published_at, cover_image, description
  - Genre: id, name, color (HEX code provided below)
  - BookGenre: id, book_id (FK), genre_id (FK) (many-to-many)
  - UserBook: id, user_id (FK), book_id (FK), status (‘reading’, ‘completed’, ‘wishlist’), finished_at, personal_note
  - Thread: id, book_id (FK, nullable), user_id (FK), content, created_at
  - Comment: id, thread_id (FK), user_id (FK), content, created_at
  - Like: id, thread_id (FK), user_id (FK)
  - ColorHistory: id, user_id (FK), genre_id (FK), count (number of books read in that genre)

Genre Colors (HEX Codes):
  - Romance: #FF9AA2
  - Fantasy/Adventure: #B5A1DD
  - Mystery/Thriller: #355C7D
  - Horror: #23272A
  - Social/Culture: #BCAAA4
  - Essay/Self-development: #A7C7E7
  - Poetry/Literature: #D6CDEA
  - Science/Technology: #61C0BF
  - History: #8B3A3A
  - Humanities/Philosophy: #7B8D8E
  - Youth/Growth: #FFA64D
  - Children: #FFF176
  - Nature/Travel: #A8D5BA
  - Science Fiction: #76FF7A
  - Business/Economics: #256D1B
  - Health/Medicine: #C1E1C1

If ERD generation is not supported by Copilot Tasks, explicitly inform me so I can provide the ERD manually using erdcloud.com.

### Step 2: Backend (Django REST Framework)

#### Initial Setup
  - Create Django apps for authentication (users), books (books), and community (community).

#### Aladin API Integration (Books & Genres)
  - Implement a backend service to fetch book data from the Aladin API using the provided key: ttbjhpark9706021328002.
  - Parse and save the fetched data into the database, including title, author, cover image, description, ISBN, genre information, and publisher details.
  - Automatically associate fetched genres with the predefined genre colors as defined above.

#### API Endpoints
  - CRUD for UserBook, Thread, Comment, Like, and ColorHistory models.
  - /api/users/{id}/color-profile:
    Calculate user’s primary genre color based on their ColorHistory and return HEX value.
  - /api/books/search:
    Search endpoint connected to Aladin API. Return results with associated genre colors.

#### Authentication
  - Simple authentication using DRF tokens or JWT.
  - Registration, login, logout functionality.
  - Basic permissions (authenticated users for protected endpoints).

#### File Uploads
  - Simple image upload functionality for profile and book cover images (local storage).

### Step 3: Frontend (Vue.js)

#### Project Setup
  - Initialize Vue.js app using Vue Router, Axios, and Pinia or Vuex.

#### Pages and Features
  - Home Page: Display user’s primary color profile and recommended books (fetched via Aladin API).
  - Book List/Detail Page:
    - Display books with their genres using the assigned genre colors.
    - Allow users to update reading status and add personal notes.
  - Community (Threads/Comments): Basic posting and commenting functionality.
  - Profile Page: Display user’s reading color palette and statistics visually (SVG or Chart.js).
  - Login/Signup Page: Basic form validation.

#### Visualization
  - Implement a simple, dynamic wave animation around user profile images.
  - Wave color must match user’s primary genre color fetched via API.

### Step 4: Basic Performance & Security
  - Optimize queries minimally (use select_related, prefetch_related only when necessary).
  - Implement pagination for long lists if needed.
  - Use Django’s built-in password hashing and basic input sanitization to prevent SQL injections or XSS.

### Step 5: Testing & Refactoring
  - Basic unit tests for critical backend endpoints (login, user color-profile, book search).
  - Frontend testing only if necessary.
  - Ensure consistent variable naming conventions (snake_case Python, camelCase JavaScript).
  - Remove unused imports and variables.
  - Conduct a final basic refactoring to improve readability and fix obvious syntax errors.

### Final Notes
  - Skip advanced security features and highly complex optimizations.
  - Omit detailed visual design considerations for now; these will be addressed separately.
  - Notify me explicitly if tasks, particularly ERD generation or external API integrations, cannot be completed directly by Copilot. I will provide assistance manually.
