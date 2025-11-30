# Database Migration Requirements

## Introduction

This document defines requirements for migrating from JSON file storage to Railway's PostgreSQL database for persistent conversation and usage data storage in production.

## Glossary

- **PostgreSQL**: Relational database system for persistent data storage
- **SQLAlchemy**: Python ORM (Object-Relational Mapping) library for database operations
- **Migration**: Process of moving data from JSON files to database
- **Railway PostgreSQL**: Managed PostgreSQL database service provided by Railway
- **Connection Pool**: Reusable database connections for performance
- **DATABASE_URL**: Environment variable containing PostgreSQL connection string

## Requirements

### Requirement 1

**User Story:** As a user, I want my conversations to persist across server restarts, so that I don't lose my chat history

#### Acceptance Criteria

1. THE System SHALL store all conversation data in Railway PostgreSQL database
2. WHEN the backend server restarts, THE System SHALL retain all existing conversations
3. THE System SHALL retrieve conversations from the database on user login
4. THE System SHALL maintain conversation data integrity across deployments
5. THE System SHALL support concurrent access from multiple users without data corruption

### Requirement 2

**User Story:** As a developer, I want to easily switch between local and production databases, so that I can develop and test locally

#### Acceptance Criteria

1. THE System SHALL support PostgreSQL connection via DATABASE_URL environment variable
2. WHEN DATABASE_URL is not provided, THE System SHALL fall back to JSON file storage for local development
3. THE System SHALL use the same API interface regardless of storage backend
4. THE System SHALL log which storage backend is being used on startup
5. WHEN database connection fails, THE System SHALL log the error and fall back to JSON storage

### Requirement 3

**User Story:** As a system administrator, I want automatic database schema creation, so that deployment is simple

#### Acceptance Criteria

1. THE System SHALL automatically create required database tables on first run
2. THE System SHALL create indexes for query performance optimization
3. THE System SHALL handle schema migrations for future updates
4. WHEN tables already exist, THE System SHALL not recreate or drop existing data
5. THE System SHALL log all schema operations for debugging

### Requirement 4

**User Story:** As a user, I want my usage statistics to persist, so that my query limits are accurately tracked

#### Acceptance Criteria

1. THE System SHALL store usage statistics in the database
2. THE System SHALL track daily and monthly query counts per user
3. THE System SHALL reset daily counts at midnight UTC
4. THE System SHALL reset monthly counts on the first day of each month
5. THE System SHALL prevent users from exceeding their query limits

### Requirement 5

**User Story:** As a developer, I want to migrate existing JSON data to the database, so that current users don't lose their data

#### Acceptance Criteria

1. THE System SHALL provide a migration script to import JSON files into the database
2. THE Migration Script SHALL preserve all conversation data including messages and metadata
3. THE Migration Script SHALL preserve usage statistics
4. THE Migration Script SHALL handle errors gracefully and report progress
5. THE Migration Script SHALL be idempotent (safe to run multiple times)

### Requirement 6

**User Story:** As a system, I want efficient database queries, so that the application remains fast

#### Acceptance Criteria

1. THE System SHALL use connection pooling for database connections
2. THE System SHALL create indexes on frequently queried columns (user_id, created_at)
3. THE System SHALL use prepared statements to prevent SQL injection
4. THE System SHALL limit query result sizes to prevent memory issues
5. WHEN database queries take longer than 1 second, THE System SHALL log slow query warnings

### Requirement 7 ✅ IMPLEMENTED

**User Story:** As a user, I want the application to work correctly when I reload the page, so that I don't see 404 errors

#### Acceptance Criteria

1. WHEN a user reloads any application page, THE System SHALL serve the correct page content ✅
2. THE Frontend SHALL handle client-side routing without requiring server routes ✅
3. THE Deployment configuration SHALL redirect all routes to index.html for single-page application support ✅
4. WHEN a user navigates to a conversation URL directly, THE System SHALL load the conversation correctly ✅
5. THE System SHALL maintain application state across page reloads ✅

**Implementation**: Added StaticFiles mounting and catch-all route in `backend/main.py` to serve frontend for all non-API routes.

### Requirement 8 ✅ IMPLEMENTED

**User Story:** As a system administrator, I want PostgreSQL to be the only storage backend in production, so that data is always persisted correctly

#### Acceptance Criteria

1. WHEN DATABASE_URL environment variable is not set in production, THE System SHALL fail to start with a clear error message ✅
2. THE System SHALL not fall back to JSON storage in production environments ✅
3. THE System SHALL log a warning if DATABASE_URL is missing during startup ✅
4. WHEN running in development mode, THE System SHALL allow JSON storage fallback ✅
5. THE System SHALL validate DATABASE_URL format on startup ✅

**Implementation**: Added production environment detection and DATABASE_URL validation in startup event in `backend/main.py`.

### Requirement 9 ✅ IMPLEMENTED

**User Story:** As a user, I want my credit usage to be tracked accurately, so that I know how many queries I have remaining

#### Acceptance Criteria

1. WHEN a user makes a query, THE System SHALL increment their usage count immediately ✅
2. THE System SHALL persist usage data to the database after each query ✅
3. WHEN a user views their usage statistics, THE System SHALL display accurate current usage ✅
4. THE System SHALL enforce rate limits based on accurate usage counts ✅
5. WHEN usage tracking fails, THE System SHALL log the error and retry the operation ✅

**Implementation**: Fixed all import statements across backend modules to use `backend.` prefix, enabling proper module resolution and usage tracking functionality.
