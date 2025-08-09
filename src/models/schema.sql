DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Setting;
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Team_Members;
DROP TABLE IF EXISTS Project_Teams;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Task;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Task_Tags;
DROP TABLE IF EXISTS Priority;



-- Table: User
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    DOB DATE,
    email_verified BOOLEAN DEFAULT 0,
    email_validation_code TEXT
);

-- Table: Setting
CREATE TABLE Setting (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    theme TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Table: Project
CREATE TABLE Project (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    description TEXT,
    create_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_datetime DATETIME,
    user_id INTEGER NOT NULL,
    status TEXT DEFAULT 'NOT STARTED',
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create Team table
CREATE TABLE Team (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    team_name TEXT NOT NULL
);


-- Table: Team_Members
CREATE TABLE Team_Members (
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    is_owner BOOLEAN NOT NULL,  -- e.g. 'owner', 'member', 'lead', etc.
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Project_Teams (
    project_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, team_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

-- Table: Task
CREATE TABLE Task (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    description TEXT,
    create_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_datetime DATETIME,
    deadline DATETIME,
    priority INTEGER DEFAULT 0,
    status TEXT DEFAULT 'NOT STARTED',
    project_id INTEGER NOT NULL,
    assignee_id INTEGER,
    FOREIGN KEY (priority) REFERENCES Priority(priority_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (assignee_id) REFERENCES User(user_id)
);

-- Table: Tag
CREATE TABLE Tag (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT NOT NULL UNIQUE
);

-- Table: Task_Tags
CREATE TABLE Task_Tags (
    task_tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);

-- Create Priority Table
CREATE TABLE Priority (
    priority_id INTEGER PRIMARY KEY,
    priority_label TEXT NOT NULL UNIQUE
);

