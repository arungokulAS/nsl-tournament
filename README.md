# NSL Badminton Tournament Management System

A comprehensive Django web application for managing badminton tournaments with real-time score updates and intuitive tournament tracking.

## Features

### Tournament Management
- **Team Management**: Organize teams into groups with player information
- **Group Management**: Create and manage tournament groups
- **Match Scheduling**: Schedule matches with venue and timing information
- **Live Score Updates**: Track ongoing matches with live score updates
- **Results Tracking**: View completed match results with winners highlighted

### Admin Panel
- Full-featured Django admin interface for tournament management
- Add and edit teams, groups, and matches
- Update match scores and status (Scheduled → Live → Completed)
- Filter matches by status and date
- Automatic statistics calculation (wins, losses, points)

### Public Pages (Auto-Refresh)
- **Home**: Tournament overview with key statistics
- **Schedule**: View all upcoming matches
- **Live Games**: Watch live match scores (auto-refreshes every 5 seconds)
- **Point Table**: Team standings by group (auto-refreshes every 10 seconds)
- **Results**: Completed match results with winners

## Screenshots

### Home Page
![Home Page](https://github.com/user-attachments/assets/9b3a6415-1e71-4c9b-af55-9421cf8c9bbe)

### Schedule
![Schedule](https://github.com/user-attachments/assets/b597ee10-a7f2-4b22-aec4-458e4dda227a)

### Live Games (Auto-Refreshing)
![Live Games](https://github.com/user-attachments/assets/cf520f83-27b7-4b20-adce-7ba8572bcc9e)

### Point Table (Auto-Refreshing)
![Point Table](https://github.com/user-attachments/assets/351b9030-356d-4457-a07c-2bb923a558c7)

### Match Results
![Results](https://github.com/user-attachments/assets/a7c9c21b-4ed1-4c14-ab85-60c62cbc8373)

### Admin Panel
![Admin Panel](https://github.com/user-attachments/assets/7ea8f74b-3dd2-4a2f-a7fb-e2d12a0722a7)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/arungokulAS/nsl-tournament.git
   cd nsl-tournament
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set username, email, and password.

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Public pages: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Usage Guide

### Adding Tournament Data

1. **Log in to Admin Panel**
   - Navigate to http://localhost:8000/admin/
   - Log in with your superuser credentials

2. **Create Groups**
   - Go to Tournament → Groups → Add Group
   - Enter group name and optional description
   - Save

3. **Add Teams**
   - Go to Tournament → Teams → Add Team
   - Enter team name, select group, and add player names
   - Statistics (matches played, won, lost, points) are automatically calculated
   - Save

4. **Schedule Matches**
   - Go to Tournament → Matches → Add Match
   - Select home team and away team
   - Set scheduled time and venue
   - Status defaults to "Scheduled"
   - Save

5. **Update Match Scores**
   - Go to Tournament → Matches
   - Click on the match to edit
   - Update status to "Live" when match starts
   - Update home_score and away_score as the match progresses
   - Change status to "Completed" when match finishes
   - Team statistics are automatically updated when match is completed

### Viewing Tournament Information

Navigate to the public pages to view:
- **Home** (`/`): Overview statistics
- **Schedule** (`/schedule/`): Upcoming matches
- **Live Games** (`/live/`): Ongoing matches with real-time scores
- **Point Table** (`/table/`): Team standings by group
- **Results** (`/results/`): Completed matches with winners

## Technical Details

### Technology Stack
- **Framework**: Django 4.2
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Real-time Updates**: AJAX polling (5s for live games, 10s for point table)

### Models

#### Group
- name: Unique group name
- description: Optional description
- Relationship: One-to-many with Team

#### Team
- name: Unique team name
- group: Foreign key to Group
- players: Text field for player names
- Statistics: matches_played, matches_won, matches_lost, points (auto-calculated)

#### Match
- home_team, away_team: Foreign keys to Team
- scheduled_time: DateTime for match timing
- status: Choice field (scheduled, live, completed)
- home_score, away_score: Integer scores
- venue: Match location
- Auto-updates team statistics on completion

### API Endpoints (JSON)
- `/live/data/`: Returns live match data for AJAX refresh
- `/table/data/`: Returns point table data for AJAX refresh

## Project Structure

```
nsl-tournament/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── nsl_tournament/          # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
└── tournament/              # Tournament app
    ├── models.py            # Database models
    ├── views.py             # View functions
    ├── admin.py             # Admin configuration
    ├── urls.py              # App URL routing
    ├── migrations/          # Database migrations
    └── templates/           # HTML templates
        └── tournament/
            ├── base.html           # Base template
            ├── home.html           # Home page
            ├── schedule.html       # Schedule page
            ├── live_games.html     # Live games (auto-refresh)
            ├── point_table.html    # Point table (auto-refresh)
            └── results.html        # Results page
```

## Development

### Running Tests
```bash
python manage.py test tournament
```

### Creating Sample Data
After setting up the database, you can add sample data through the admin panel or create a custom management command.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
