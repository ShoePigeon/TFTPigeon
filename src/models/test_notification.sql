-- Assign Tasks to Your User
INSERT INTO Project (project_name, description, user_id, status) VALUES 
('Task Notification Test', 'Testing the email notification system.', 1, 'IN PROGRESS');

-- Assign Tasks to You
INSERT INTO Task (task_name, description, deadline, priority, status, project_id, assignee_id) VALUES 
('Test Task 1', 'First test task for email notification.', '2024-12-01 09:00:00', 1, 'NOT STARTED', 1, 1),
('Test Task 2', 'Second test task for email notification.', '2024-12-01 12:00:00', 2, 'IN PROGRESS', 1, 1),
('Test Task 3', 'Third test task for email notification.', '2024-12-02 10:00:00', 0, 'NOT STARTED', 1, 1),
('Test Task 4', 'Fourth test task for email notification.', '2024-12-03 15:00:00', 1, 'IN PROGRESS', 1, 1);

-- Assign Tags and Priority Levels to Your Tasks
INSERT INTO Tag (tag_name) VALUES 
('Notification Test');

INSERT INTO Task_Tags (task_id, tag_id) VALUES 
(1, 1), -- Tag Task 1
(2, 1), -- Tag Task 2
(3, 1), -- Tag Task 3
(4, 1); -- Tag Task 4

INSERT INTO Priority (priority_id, priority_label) VALUES 
(0, 'Low'),
(1, 'Medium'),
(2, 'High');