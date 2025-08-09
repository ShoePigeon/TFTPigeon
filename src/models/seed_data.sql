INSERT INTO User (user_name, password, email, DOB) VALUES 
('john_doe', 'hashed_password123', 'john.doe@example.com', '1995-06-15'),
('jane_smith', 'hashed_password456', 'jane.smith@example.com', '1998-09-22'),
('alice_walker', 'hashed_password789', 'alice.walker@example.com', '2000-05-20'),
('mike_johnson', 'hashed_password101', 'mike.johnson@example.com', '1993-03-12'),
('emily_davis', 'hashed_password202', 'emily.davis@example.com', '1989-11-08'),
('david_clark', 'hashed_password303', 'david.clark@example.com', '1992-07-17'),
('sophia_lee', 'hashed_password404', 'sophia.lee@example.com', '1997-01-25'),
('oliver_wilson', 'hashed_password505', 'oliver.wilson@example.com', '2001-10-30');

INSERT INTO Project (project_name, description, user_id, status) VALUES 
('Dashboard Redesign', 'UI/UX updates for the company dashboard.', 1, 'IN PROGRESS'),
('Data Analytics Pipeline', 'Implementing a data pipeline for analytics.', 2, 'COMPLETED'),
('AI Chatbot Development', 'Developing a chatbot using GPT models.', 3, 'NOT STARTED'),
('Mobile App Development', 'Creating a mobile app for e-commerce.', 4, 'IN PROGRESS'),
('Website Optimization', 'Improving website speed and performance.', 8, 'COMPLETED'),
('Cloud Infrastructure Setup', 'Setting up scalable cloud infrastructure for the company.', 8, 'NOT STARTED'),
('Internal Chat System', 'Developing a secure internal messaging system.', 2, 'CANCELLED'),
('API Integration', 'Integrating third-party APIs for payment processing.', 3, 'IN PROGRESS');

INSERT INTO Team (team_name, description) VALUES
('Backend Team', 'Handles server-side development'),
('Frontend Team', 'Focuses on client-side development'),
('Design Team', 'Creates visual designs for projects'),
('Marketing Team', 'Handles promotions and outreach');

INSERT INTO Project_Teams (project_id, team_id) VALUES
(1, 1),  -- Project 1 is worked on by the Backend Team
(2, 2),  -- Project 2 is worked on by the Frontend Team
(3, 3),  -- Project 3 is worked on by the Design Team
(4, 4),  -- Project 4 is worked on by the Marketing Team
(5, 2),  -- Project 5 is worked on by the Frontend Team
(6, 3),  -- Project 6 is worked on by the Design Team
(7, 4),  -- Project 7 is worked on by the Marketing Team
(8, 1);  -- Project 8 is worked on by the Backend Team

INSERT INTO Team_Members (team_id, user_id, is_owner) VALUES
-- Backend Team
(1, 1, 1),  -- John is the owner of the Backend Team
(1, 2, 0),  -- Jane is a team member of the Backend Team
(1, 3, 0),  -- Alice is a team member of the Backend Team

-- Frontend Team
(2, 2, 1),  -- Jane is the owner of the Frontend Team
(2, 4, 0),  -- Mike is a team member of the Frontend Team
(2, 5, 0),  -- Emily is a team member of the Frontend Team

-- Design Team
(3, 3, 1),  -- Alice is the owner of the Design Team
(3, 6, 0),  -- David is a team member of the Design Team
(3, 7, 0),  -- Sophia is a team member of the Design Team

-- Marketing Team
(4, 4, 1),  -- Mike is the owner of the Marketing Team
(4, 5, 1),  -- Emily is the owner of the Marketing Team
(4, 6, 0),  -- David is a team member of the Marketing Team
(4, 7, 0),  -- Sophia is a team member of the Marketing Team
(4, 8, 0),  -- Oliver is a team member of the Marketing Team
(4, 1, 0);



INSERT INTO Task (task_name, description, deadline, priority, status, project_id, assignee_id) VALUES 
('Create Wireframes', 'Design wireframes for the new dashboard layout.', '2024-12-07 17:00:00', 0, 'IN PROGRESS', 1, 2), -- Assigned to Jane
('Develop API', 'Develop RESTful APIs for the data pipeline.', '2024-12-01 12:00:00', 1, 'NOT STARTED', 2, 1), -- Assigned to John
('Train Chatbot Model', 'Train an NLP model for chatbot responses.', '2024-12-15 18:00:00', 2, 'IN PROGRESS', 3, 3), -- Assigned to Alice
('Create Database Schema', 'Design the database schema for the mobile app.', '2024-11-30 14:00:00', 1, 'NOT STARTED', 4, 6), -- Assigned to David
('Optimize Loading Speed', 'Optimize the initial loading time of the website.', '2024-11-28 10:00:00', 0, 'IN PROGRESS', 5, 8), -- Assigned to Oliver
('Set Up CI/CD Pipeline', 'Implement Continuous Integration/Continuous Deployment pipeline for project deployment.', '2024-12-10 09:00:00', 1, 'NOT STARTED', 6, 7), -- Assigned to Sophia
('Build Notification System', 'Build a system for sending push notifications in the mobile app.', '2024-12-05 15:00:00', 2, 'IN PROGRESS', 4, 5), -- Assigned to Emily
('User Authentication', 'Implement user authentication for the internal chat system.', '2024-11-27 11:00:00', 1, 'COMPLETED', 7, 7), -- Assigned to Sophia
('Write Unit Tests', 'Write unit tests for the core modules of the data pipeline.', '2024-12-02 16:00:00', 2, 'IN PROGRESS', 2, 1), -- Assigned to John
('Integrate Payment Gateway', 'Integrate a secure payment gateway API for the mobile app.', '2024-12-08 18:00:00', 2, 'NOT STARTED', 4, 6), -- Assigned to David
('Design UI Components', 'Design reusable UI components for the new website.', '2024-12-01 17:00:00', 0, 'IN PROGRESS', 5, 8), -- Assigned to Oliver
('Create API Documentation', 'Write API documentation for the API integration project.', '2024-12-12 13:00:00', 1, 'NOT STARTED', 8, 3), -- Assigned to Alice
('Conduct Performance Tests', 'Test the website’s performance under high load conditions.', '2024-12-05 11:00:00', 2, 'NOT STARTED', 5, 8), -- Assigned to Oliver
('Finalize Design Mockups', 'Finalize the mockups for the new dashboard design.', '2024-12-06 14:00:00', 0, 'COMPLETED', 1, 2), -- Assigned to Jane
('Create User Stories', 'Write user stories and acceptance criteria for the mobile app.', '2024-11-29 09:00:00', 1, 'NOT STARTED', 4, 4), -- Assigned to Mike
('Develop Chatbot API', 'Develop a RESTful API for interacting with the chatbot.', '2024-12-10 17:00:00', 1, 'IN PROGRESS', 3, 3), -- Assigned to Alice
('Conduct User Testing', 'Conduct user testing for the internal chat system.', '2024-12-03 16:00:00', 0, 'IN PROGRESS', 7, 5), -- Assigned to Emily
('Set Up Cloud Monitoring', 'Set up monitoring and alerting for the cloud infrastructure.', '2024-12-07 15:00:00', 2, 'NOT STARTED', 6, 6), -- Assigned to David
('Build Data Models', 'Create machine learning models for data analysis.', '2024-12-15 14:00:00', 2, 'NOT STARTED', 2, 1), -- Assigned to John
('Finalize Dashboard Layout', 'Complete the final design and layout of the new dashboard.', '2024-11-26 09:00:00', 1, 'NOT STARTED', 1, 2), -- Assigned to Jane
('Implement Data Pipeline', 'Build the core components for the data processing pipeline.', '2024-12-03 10:00:00', 1, 'NOT STARTED', 1, 1), -- Assigned to John
('Update Dashboard Mockups', 'Update the mockups with the final data from the client.', '2024-12-04 11:00:00', 1, 'IN PROGRESS', 1, 2), -- Assigned to Jane
('Create Dashboard Widgets', 'Develop the interactive widgets for the dashboard.', '2024-12-07 14:00:00', 1, 'NOT STARTED', 1, 3), -- Assigned to Alice
('Integrate Analytics API', 'Integrate the analytics API with the new dashboard.', '2024-12-12 09:00:00', 1, 'NOT STARTED', 1, 1), -- Assigned to John
('Conduct Stakeholder Review', 'Hold a review session with stakeholders for the dashboard.', '2024-12-14 15:00:00', 1, 'NOT STARTED', 1, 2), -- Assigned to Jane
('Finalize Dashboard Launch', 'Prepare the dashboard for final launch and deployment.', '2024-12-15 16:00:00', 1, 'NOT STARTED', 1, 3); -- Assigned to Alice

INSERT INTO Tag (tag_name) VALUES 
('UI/UX'),
('Backend'),
('Frontend'),
('Design'),
('NLP'),
('Analytics'),
('Performance'),
('Security'),
('Testing'),
('Database'),
('API');

INSERT INTO Task_Tags (task_id, tag_id) VALUES 
(1, 1), -- Task 1 tagged as UI/UX
(1, 4), -- Task 1 tagged as Design
(2, 2), -- Task 2 tagged as Backend
(2, 6), -- Task 2 tagged as Analytics
(3, 5), -- Task 3 tagged as NLP
(4, 10),  -- Task 4 (Create Database Schema) tagged as Database
(5, 7),   -- Task 5 (Optimize Loading Speed) tagged as Performance
(6, 8),   -- Task 6 (Set Up CI/CD Pipeline) tagged as Security
(7, 2),   -- Task 7 (Build Notification System) tagged as Backend
(8, 9),   -- Task 8 (User Authentication) tagged as Testing
(9, 7),   -- Task 9 (Write Unit Tests) tagged as Performance
(10, 10), -- Task 10 (Integrate Payment Gateway) tagged as API
(11, 4),  -- Task 11 (Design UI Components) tagged as Design
(12, 10), -- Task 12 (Create API Documentation) tagged as API
(13, 7),  -- Task 13 (Conduct Performance Tests) tagged as Performance
(14, 4),  -- Task 14 (Finalize Design Mockups) tagged as Design
(15, 6),  -- Task 15 (Create User Stories) tagged as Analytics
(16, 2),  -- Task 16 (Develop Chatbot API) tagged as Backend
(17, 9),  -- Task 17 (Conduct User Testing) tagged as Testing
(18, 8),  -- Task 18 (Set Up Cloud Monitoring) tagged as Security
(19, 6);  -- Task 19 (Build Data Models) tagged as Analytics

INSERT INTO Priority (priority_id, priority_label) VALUES 
(0, 'Low'),
(1, 'Medium'),
(2, 'High'),
(3, 'Very High');