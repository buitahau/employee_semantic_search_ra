-- =============================================================================
-- LOCAL TEST DATA — owt-employee-app-backend
-- Generated for: ra_minus_g local development & testing
-- Run order: top to bottom (dependencies respected)
-- =============================================================================

-- Clean up (reverse dependency order)
DROP TABLE IF EXISTS task_assignments_labels CASCADE;
DROP TABLE IF EXISTS task_assignments_comments CASCADE;
DROP TABLE IF EXISTS task_assignments_files CASCADE;
DROP TABLE IF EXISTS task_assignments_assignees CASCADE;
DROP TABLE IF EXISTS task_assignments CASCADE;
DROP TABLE IF EXISTS training_coaches CASCADE;
DROP TABLE IF EXISTS trainings CASCADE;
DROP TABLE IF EXISTS training_topics CASCADE;
DROP TABLE IF EXISTS training_levels CASCADE;
DROP TABLE IF EXISTS experience_skills CASCADE;
DROP TABLE IF EXISTS experiences CASCADE;
DROP TABLE IF EXISTS employment_histories CASCADE;
DROP TABLE IF EXISTS educations CASCADE;
DROP TABLE IF EXISTS certifications CASCADE;
DROP TABLE IF EXISTS user_skills CASCADE;
DROP TABLE IF EXISTS user_cvs CASCADE;
DROP TABLE IF EXISTS cv_overview CASCADE;
DROP TABLE IF EXISTS permissions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS skill_groups CASCADE;
DROP TABLE IF EXISTS task_assignments_categories CASCADE;
DROP TABLE IF EXISTS labels CASCADE;
DROP TABLE IF EXISTS user_levels CASCADE;
DROP TABLE IF EXISTS positions CASCADE;

DROP TYPE IF EXISTS gender_type CASCADE;
DROP TYPE IF EXISTS contract_type CASCADE;
DROP TYPE IF EXISTS role_type CASCADE;
DROP TYPE IF EXISTS task_priority CASCADE;
DROP TYPE IF EXISTS task_status CASCADE;
DROP TYPE IF EXISTS task_category_label CASCADE;

-- =============================================================================
-- ENUMS
-- =============================================================================

CREATE TYPE gender_type AS ENUM ('MALE', 'FEMALE');
CREATE TYPE contract_type AS ENUM ('FULLTIME', 'PART_TIME', 'INTERN');
CREATE TYPE role_type AS ENUM ('USER', 'ADMIN', 'EXTERNAL_USER', 'ASSISTANT');
CREATE TYPE task_priority AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW');
CREATE TYPE task_status AS ENUM ('OPEN', 'IN_PROGRESS', 'IN_REVIEW', 'DONE', 'BLOCKED');
CREATE TYPE task_category_label AS ENUM ('ADMIN', 'HR', 'INFRA', 'EMPLOYEE_APP', 'BUDDIES');

-- =============================================================================
-- LOOKUP / REFERENCE TABLES
-- =============================================================================

CREATE TABLE positions (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL UNIQUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_levels (
    id          SERIAL PRIMARY KEY,
    label       VARCHAR(255) NOT NULL UNIQUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skill_groups (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skills (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    skill_group_id  INT NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_skills_skill_group_id FOREIGN KEY (skill_group_id)
        REFERENCES skill_groups(id) ON DELETE RESTRICT
);

CREATE TABLE training_topics (
    id          SERIAL PRIMARY KEY,
    label       VARCHAR(100),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE training_levels (
    id          SERIAL PRIMARY KEY,
    label       VARCHAR(100),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE task_assignments_categories (
    id          SERIAL PRIMARY KEY,
    label       task_category_label,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE labels (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- USERS
-- =============================================================================

CREATE TABLE users (
    id                  SERIAL PRIMARY KEY,
    first_name          VARCHAR(255),
    last_name           VARCHAR(255),
    trigram             VARCHAR(10),
    id_no               INT,
    phone_no            VARCHAR(50),
    qr_code             VARCHAR(25) UNIQUE,
    photo               TEXT,
    company_email       VARCHAR(255) NOT NULL UNIQUE,
    password            VARCHAR(255) NOT NULL,
    gender              gender_type NOT NULL,
    contract_type       contract_type NOT NULL,
    date_of_birth       TIMESTAMP,
    address             VARCHAR(2048),
    university          VARCHAR(255),
    yearly_allowance    FLOAT DEFAULT 0,
    start_date          TIMESTAMP NOT NULL,
    end_date            TIMESTAMP,
    is_active           BOOLEAN DEFAULT TRUE,
    first_login         BOOLEAN,
    employee_id         VARCHAR(50) NOT NULL UNIQUE,
    timekeeper_user_id  INT,
    fcm_token           VARCHAR,
    position_id         INT NOT NULL,
    level_id            INT,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_positions FOREIGN KEY (position_id)
        REFERENCES positions(id) ON DELETE RESTRICT,
    CONSTRAINT fk_user_levels FOREIGN KEY (level_id)
        REFERENCES user_levels(id) ON DELETE RESTRICT
);

-- =============================================================================
-- PERMISSIONS
-- =============================================================================

CREATE TABLE permissions (
    id          SERIAL PRIMARY KEY,
    role        role_type DEFAULT 'USER',
    user_id     INT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_permissions_users FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE RESTRICT
);

-- =============================================================================
-- CV
-- =============================================================================

CREATE TABLE user_cvs (
    id          SERIAL PRIMARY KEY,
    cv          TEXT NOT NULL,
    version     VARCHAR,
    user_id     INT NOT NULL,
    created_by  INT NOT NULL,
    updated_by  INT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE TABLE cv_overview (
    id               SERIAL PRIMARY KEY,
    custom_position  VARCHAR(255),
    introduction     VARCHAR(1024),
    user_id          INT NOT NULL,
    created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =============================================================================
-- EXPERIENCE
-- =============================================================================

CREATE TABLE experiences (
    id                       SERIAL PRIMARY KEY,
    project_name             VARCHAR(256) NOT NULL,
    date_from                DATE NOT NULL,
    date_to                  DATE,
    domain                   VARCHAR(256) NOT NULL,
    description              VARCHAR(1024) NOT NULL,
    roles_and_responsibilities TEXT NOT NULL,
    position                 INT DEFAULT 0,
    is_selected              BOOLEAN DEFAULT FALSE,
    is_currently_working     BOOLEAN DEFAULT FALSE,
    user_id                  INT NOT NULL,
    created_at               TIMESTAMP NOT NULL DEFAULT now(),
    updated_at               TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT experiences_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE experience_skills (
    id             SERIAL PRIMARY KEY,
    experience_id  INT NOT NULL,
    skill_id       INT NOT NULL,
    created_at     TIMESTAMP NOT NULL DEFAULT now(),
    updated_at     TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT experience_skills_experience_id_fkey FOREIGN KEY (experience_id)
        REFERENCES experiences(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT experience_skills_skill_id_fkey FOREIGN KEY (skill_id)
        REFERENCES skills(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX experience_skills_experience_index ON experience_skills(experience_id);
CREATE INDEX experience_skills_skill_index ON experience_skills(skill_id);

-- =============================================================================
-- EMPLOYMENT HISTORY
-- =============================================================================

CREATE TABLE employment_histories (
    id                    SERIAL PRIMARY KEY,
    company               VARCHAR(256) NOT NULL,
    date_from             DATE NOT NULL,
    date_to               DATE,
    position              INT DEFAULT 0,
    is_selected           BOOLEAN DEFAULT FALSE,
    is_currently_working  BOOLEAN DEFAULT FALSE,
    user_id               INT NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT now(),
    updated_at            TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT employments_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =============================================================================
-- EDUCATION & CERTIFICATIONS
-- =============================================================================

CREATE TABLE educations (
    id           SERIAL PRIMARY KEY,
    institution  VARCHAR(256) NOT NULL,
    degree       VARCHAR(256) NOT NULL,
    date_from    DATE NOT NULL,
    date_to      DATE NOT NULL,
    position     INT NOT NULL,
    is_selected  BOOLEAN DEFAULT FALSE,
    user_id      INT,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE certifications (
    id                    SERIAL PRIMARY KEY,
    name                  VARCHAR(256) NOT NULL,
    issuing_organisation  VARCHAR(256) NOT NULL,
    issue_date            DATE,
    expiration_date       DATE,
    credential_id         VARCHAR(256),
    credential_url        VARCHAR,
    position              INT NOT NULL,
    is_selected           BOOLEAN DEFAULT FALSE,
    user_id               INT NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- =============================================================================
-- USER SKILLS
-- =============================================================================

CREATE TABLE user_skills (
    id          SERIAL PRIMARY KEY,
    level       INT DEFAULT 0,  -- 0-5
    is_selected BOOLEAN DEFAULT TRUE,
    user_id     INT NOT NULL,
    skill_id    INT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_skills_user_id FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_user_skills_skill_id FOREIGN KEY (skill_id)
        REFERENCES skills(id) ON DELETE RESTRICT
);

-- =============================================================================
-- TRAINING
-- =============================================================================

CREATE TABLE trainings (
    id                    SERIAL PRIMARY KEY,
    training_date         DATE NOT NULL,
    duration              INT NOT NULL,
    training_title        VARCHAR(256),
    training_description  VARCHAR(1024),
    training_link         VARCHAR(1024),
    user_id               INT NOT NULL,
    topic_id              INT NOT NULL,
    level_id              INT NOT NULL,
    created_by            INT,
    updated_by            INT,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)   REFERENCES users(id),
    CONSTRAINT fk_training_topics FOREIGN KEY (topic_id)
        REFERENCES training_topics(id) ON DELETE RESTRICT,
    CONSTRAINT fk_training_levels FOREIGN KEY (level_id)
        REFERENCES training_levels(id) ON DELETE RESTRICT
);

CREATE TABLE training_coaches (
    id           SERIAL PRIMARY KEY,
    training_id  INT NOT NULL,
    user_id      INT NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_training_coaches_trainings FOREIGN KEY (training_id)
        REFERENCES trainings(id) ON DELETE RESTRICT,
    CONSTRAINT fk_training_coaches_users FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE RESTRICT
);

-- =============================================================================
-- TASK ASSIGNMENTS
-- =============================================================================

-- Custom sequence: YYZZZZ format (e.g. 260001 for first task of 2026)
CREATE SEQUENCE IF NOT EXISTS task_assignments_custom_seq START WITH 260001;

CREATE TABLE task_assignments (
    id               INT PRIMARY KEY DEFAULT nextval('task_assignments_custom_seq'),
    title            VARCHAR(256) NOT NULL,
    priority         task_priority NOT NULL,
    status           task_status NOT NULL,
    details          TEXT NOT NULL,
    due_to           DATE,
    estimation_hours NUMERIC,
    time_spent       NUMERIC DEFAULT 0,
    start_time       NUMERIC DEFAULT 0,
    timer_total      NUMERIC DEFAULT 0,
    parent_id        INT,
    category_id      INT DEFAULT 4,
    created_by       INT NOT NULL,
    updated_by       INT NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT task_assignments_task_assignments_categories_category_id_fkey
        FOREIGN KEY (category_id) REFERENCES task_assignments_categories(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE task_assignments_assignees (
    task_assignment_id  INT NOT NULL,
    user_id             INT NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (task_assignment_id, user_id),
    FOREIGN KEY (task_assignment_id) REFERENCES task_assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE task_assignments_comments (
    id                  SERIAL PRIMARY KEY,
    content             TEXT NOT NULL,
    html_content        TEXT,
    tagged_user_ids     TEXT,
    task_assignment_id  INT NOT NULL,
    created_by          INT NOT NULL,
    updated_by          INT NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_assignment_id) REFERENCES task_assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE task_assignments_files (
    id                  SERIAL PRIMARY KEY,
    url                 TEXT NOT NULL,
    task_assignment_id  INT NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_assignment_id) REFERENCES task_assignments(id) ON DELETE CASCADE
);

CREATE TABLE task_assignments_labels (
    task_assignment_id  INT NOT NULL,
    label_id            INT NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (task_assignment_id, label_id),
    FOREIGN KEY (task_assignment_id) REFERENCES task_assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (label_id) REFERENCES labels(id) ON DELETE CASCADE
);

-- =============================================================================
-- SEED DATA
-- =============================================================================

-- Positions
INSERT INTO positions (name) VALUES
    ('Software Engineer'),
    ('Senior Software Engineer'),
    ('Tech Lead'),
    ('Product Manager'),
    ('DevOps Engineer'),
    ('QA Engineer'),
    ('UX Designer'),
    ('Data Analyst');

-- User Levels
INSERT INTO user_levels (label) VALUES
    ('Junior'),
    ('Middle'),
    ('Senior'),
    ('Expert'),
    ('Intern');

-- Skill Groups
INSERT INTO skill_groups (name) VALUES
    ('Backend'),
    ('Frontend'),
    ('DevOps & Cloud'),
    ('Data & AI'),
    ('Soft Skills'),
    ('Mobile');

-- Skills
INSERT INTO skills (name, skill_group_id) VALUES
    -- Backend (group 1)
    ('Python',          1),
    ('Java',            1),
    ('TypeScript',      1),
    ('Node.js',         1),
    ('PostgreSQL',      1),
    ('Redis',           1),
    ('FastAPI',         1),
    ('NestJS',          1),
    ('REST API Design', 1),
    ('GraphQL',         1),
    -- Frontend (group 2)
    ('React',           2),
    ('Angular',         2),
    ('Vue.js',          2),
    ('HTML/CSS',        2),
    ('TailwindCSS',     2),
    -- DevOps (group 3)
    ('Docker',          3),
    ('Kubernetes',      3),
    ('AWS',             3),
    ('GitHub Actions',  3),
    ('Terraform',       3),
    -- Data & AI (group 4)
    ('pgvector',        4),
    ('PyTorch',         4),
    ('scikit-learn',    4),
    ('SQL Analytics',   4),
    ('LangChain',       4),
    -- Soft Skills (group 5)
    ('Communication',   5),
    ('Leadership',      5),
    ('Agile/Scrum',     5),
    -- Mobile (group 6)
    ('React Native',    6),
    ('Flutter',         6);

-- Training Topics
INSERT INTO training_topics (label) VALUES
    ('Technical'),
    ('Leadership'),
    ('Security'),
    ('Product'),
    ('Communication'),
    ('AI & Machine Learning');

-- Training Levels
INSERT INTO training_levels (label) VALUES
    ('Beginner'),
    ('Intermediate'),
    ('Advanced'),
    ('Expert');

-- Task Categories
INSERT INTO task_assignments_categories (label) VALUES
    ('ADMIN'),
    ('HR'),
    ('INFRA'),
    ('EMPLOYEE_APP'),
    ('BUDDIES');

-- Labels
INSERT INTO labels (name) VALUES
    ('bug'),
    ('feature'),
    ('improvement'),
    ('documentation'),
    ('urgent'),
    ('backend'),
    ('frontend'),
    ('infra');

-- =============================================================================
-- USERS (3 employees for testing)
-- Passwords are bcrypt hashes of 'Password123!' — replace in prod
-- =============================================================================

INSERT INTO users (
    first_name, last_name, trigram, id_no, phone_no, qr_code,
    company_email, password, gender, contract_type,
    date_of_birth, address, university, yearly_allowance,
    start_date, is_active, first_login, employee_id,
    position_id, level_id
) VALUES
    -- User 1: Senior BE engineer (admin)
    ('Alice', 'Nguyen', 'ANG', 1001, '+84901234567', 'QR-ANG-001',
     'alice.nguyen@owt.swiss',
     '$2b$10$xJ8K4mP9qL2vN3wR6tY8uOeZhFgIjKlMnOpQrStUvWxYzABCDEFGH',
     'FEMALE', 'FULLTIME',
     '1992-03-15 00:00:00', '12 Nguyen Hue, District 1, Ho Chi Minh City',
     'Ho Chi Minh City University of Technology',
     20, '2020-01-06 00:00:00', TRUE, FALSE, 'OWT-2020-001',
     2, 3),  -- Senior SE, Senior level

    -- User 2: Middle FE engineer
    ('Bob', 'Tran', 'BTR', 1002, '+84912345678', 'QR-BTR-002',
     'bob.tran@owt.swiss',
     '$2b$10$xJ8K4mP9qL2vN3wR6tY8uOeZhFgIjKlMnOpQrStUvWxYzABCDEFGH',
     'MALE', 'FULLTIME',
     '1995-07-22 00:00:00', '45 Le Loi, District 3, Ho Chi Minh City',
     'University of Science - VNUHCM',
     20, '2021-06-01 00:00:00', TRUE, FALSE, 'OWT-2021-002',
     1, 2),  -- SE, Middle level

    -- User 3: Intern
    ('Carol', 'Le', 'CLE', 1003, '+84923456789', 'QR-CLE-003',
     'carol.le@owt.swiss',
     '$2b$10$xJ8K4mP9qL2vN3wR6tY8uOeZhFgIjKlMnOpQrStUvWxYzABCDEFGH',
     'FEMALE', 'INTERN',
     '2001-11-05 00:00:00', '78 Tran Hung Dao, District 5, Ho Chi Minh City',
     'FPT University',
     5, '2026-02-01 00:00:00', TRUE, TRUE, 'OWT-2026-003',
     1, 5);  -- SE, Intern level

-- Permissions
INSERT INTO permissions (role, user_id) VALUES
    ('ADMIN', 1),
    ('USER',  2),
    ('USER',  3);

-- =============================================================================
-- CV DATA
-- =============================================================================

INSERT INTO cv_overview (custom_position, introduction, user_id) VALUES
    ('Backend Engineer & Tech Lead',
     'Experienced backend engineer with 6+ years building scalable APIs and data pipelines. Passionate about clean architecture and developer productivity.',
     1),
    ('Frontend Engineer',
     'Creative frontend developer specialised in React and modern web tooling. Enjoys turning complex UX problems into elegant, accessible interfaces.',
     2),
    ('Software Engineering Intern',
     'Final-year Computer Science student eager to contribute to real-world projects and grow engineering skills in a fast-paced team.',
     3);

INSERT INTO user_cvs (cv, version, user_id, created_by, updated_by) VALUES
    ('Alice Nguyen — Senior Software Engineer\n\nObjective: To leverage deep backend expertise in distributed systems and data engineering to deliver high-impact features.\n\nExperience: 6 years at OWT Switzerland, working on employee management platforms and internal tooling.',
     'v3.1', 1, 1, 1),
    ('Bob Tran — Software Engineer (Frontend)\n\nObjective: Build performant, accessible web applications using modern JavaScript frameworks.\n\nExperience: 3 years at OWT Switzerland, Angular/React-based employee portal.',
     'v1.4', 2, 2, 2),
    ('Carol Le — Intern\n\nObjective: Apply university knowledge in a professional setting and contribute to the OWT employee app.\n\nExperience: Internship since Feb 2026.',
     'v0.1', 3, 1, 1);

-- =============================================================================
-- EXPERIENCES
-- =============================================================================

INSERT INTO experiences (
    project_name, date_from, date_to, domain, description,
    roles_and_responsibilities, position, is_selected, is_currently_working, user_id
) VALUES
    -- Alice
    ('Employee Skills Search (ra_minus_g)',
     '2025-10-01', NULL,
     'Internal Tooling',
     'ETL pipeline and vector search API to index employee skill data into pgvector, enabling semantic search across the OWT team.',
     'Designed the ETL architecture, implemented the embedding pipeline using all-MiniLM-L6-v2, built the FastAPI query layer, and led code reviews.',
     1, TRUE, TRUE, 1),

    ('OWT Employee Portal — Backend Rewrite',
     '2023-03-01', '2025-09-30',
     'Enterprise Software',
     'Full backend rewrite of the OWT employee portal from Express.js monolith to NestJS modular architecture with PostgreSQL.',
     'Led the migration design, implemented RBAC permissions, refactored authentication module, mentored two junior engineers.',
     2, TRUE, FALSE, 1),

    -- Bob
    ('OWT Employee Portal — Frontend',
     '2021-06-01', NULL,
     'Enterprise Software',
     'Angular and React-based frontend for the OWT employee self-service portal including CV management, task assignments, and time-off requests.',
     'Implemented CV builder UI, integrated REST APIs, led migration from Angular to React for the dashboard module.',
     1, TRUE, TRUE, 2),

    -- Carol
    ('ra_minus_g — Query API Feature',
     '2026-03-01', NULL,
     'Internal Tooling',
     'Contributing to the FastAPI query layer of the skills search module as part of the internship programme.',
     'Implemented unit tests for the query module, fixed bugs in the ETL extract phase, wrote API documentation.',
     1, TRUE, TRUE, 3);

-- Experience Skills (link experiences to skills)
INSERT INTO experience_skills (experience_id, skill_id) VALUES
    -- Alice exp 1: ra_minus_g
    (1, 1),   -- Python
    (1, 5),   -- PostgreSQL
    (1, 7),   -- FastAPI
    (1, 21),  -- pgvector
    (1, 19),  -- GitHub Actions
    -- Alice exp 2: Portal backend
    (2, 3),   -- TypeScript
    (2, 8),   -- NestJS
    (2, 5),   -- PostgreSQL
    (2, 6),   -- Redis
    (2, 9),   -- REST API Design
    -- Bob exp: Frontend
    (3, 3),   -- TypeScript
    (3, 11),  -- React
    (3, 12),  -- Angular
    (3, 14),  -- HTML/CSS
    (3, 15),  -- TailwindCSS
    -- Carol exp: Query API
    (4, 1),   -- Python
    (4, 7),   -- FastAPI
    (4, 5);   -- PostgreSQL

-- =============================================================================
-- EMPLOYMENT HISTORY
-- =============================================================================

INSERT INTO employment_histories (
    company, date_from, date_to, position, is_selected, is_currently_working, user_id
) VALUES
    -- Alice
    ('OWT Switzerland', '2020-01-06', NULL,     1, TRUE,  TRUE,  1),
    ('Axon Active Vietnam', '2018-05-01', '2019-12-31', 2, TRUE,  FALSE, 1),
    -- Bob
    ('OWT Switzerland', '2021-06-01', NULL,     1, TRUE,  TRUE,  2),
    ('Rikkeisoft',      '2020-01-01', '2021-05-31', 2, FALSE, FALSE, 2),
    -- Carol (only internship so far)
    ('OWT Switzerland', '2026-02-01', NULL,     1, TRUE,  TRUE,  3);

-- =============================================================================
-- EDUCATION
-- =============================================================================

INSERT INTO educations (institution, degree, date_from, date_to, position, is_selected, user_id) VALUES
    ('Ho Chi Minh City University of Technology', 'Bachelor of Computer Science', '2010-09-01', '2014-06-30', 1, TRUE, 1),
    ('University of Science - VNUHCM',            'Bachelor of Information Technology', '2013-09-01', '2017-06-30', 1, TRUE, 2),
    ('FPT University',                            'Bachelor of Software Engineering', '2022-09-01', '2026-06-30', 1, TRUE, 3);

-- =============================================================================
-- CERTIFICATIONS
-- =============================================================================

INSERT INTO certifications (
    name, issuing_organisation, issue_date, expiration_date,
    credential_id, credential_url, position, is_selected, user_id
) VALUES
    ('AWS Certified Developer – Associate',
     'Amazon Web Services', '2023-04-10', '2026-04-10',
     'AWS-DEV-ASSOC-2023-ANG', NULL, 1, TRUE, 1),

    ('PostgreSQL Associate Certification',
     'EDB', '2022-08-01', NULL,
     'EDB-PGA-2022-ANG', NULL, 2, TRUE, 1),

    ('Meta React Developer Certificate',
     'Meta / Coursera', '2022-12-01', NULL,
     'META-REACT-2022-BTR', NULL, 1, TRUE, 2);

-- =============================================================================
-- USER SKILLS
-- =============================================================================

INSERT INTO user_skills (level, is_selected, user_id, skill_id) VALUES
    -- Alice
    (5, TRUE,  1, 1),   -- Python — Expert
    (4, TRUE,  1, 5),   -- PostgreSQL — Advanced
    (4, TRUE,  1, 7),   -- FastAPI — Advanced
    (3, TRUE,  1, 8),   -- NestJS — Intermediate
    (4, TRUE,  1, 21),  -- pgvector — Advanced
    (3, TRUE,  1, 16),  -- Docker — Intermediate
    (2, FALSE, 1, 11),  -- React — Beginner (not on CV)
    -- Bob
    (5, TRUE,  2, 11),  -- React — Expert
    (4, TRUE,  2, 12),  -- Angular — Advanced
    (4, TRUE,  2, 3),   -- TypeScript — Advanced
    (3, TRUE,  2, 14),  -- HTML/CSS — Intermediate
    (3, TRUE,  2, 15),  -- TailwindCSS — Intermediate
    (2, TRUE,  2, 1),   -- Python — Beginner
    -- Carol
    (2, TRUE,  3, 1),   -- Python — Beginner
    (2, TRUE,  3, 7),   -- FastAPI — Beginner
    (1, TRUE,  3, 5),   -- PostgreSQL — Novice
    (3, TRUE,  3, 11),  -- React — Intermediate (personal projects)
    (3, TRUE,  3, 14);  -- HTML/CSS — Intermediate

-- =============================================================================
-- TRAINING
-- =============================================================================

INSERT INTO trainings (
    training_date, duration, training_title, training_description, training_link,
    user_id, topic_id, level_id, created_by, updated_by
) VALUES
    -- Alice
    ('2025-11-15', 8,
     'pgvector Deep Dive',
     'Hands-on workshop covering pgvector indexing strategies, HNSW vs IVFFlat, and performance tuning for 384-dim embeddings.',
     'https://internal.owt.swiss/training/pgvector-2025',
     1, 6, 3, 1, 1),

    ('2025-03-10', 4,
     'AWS Solutions Architect Prep',
     'Internal study group session preparing for AWS SA Associate certification.',
     NULL, 1, 1, 2, 1, 1),

    -- Bob
    ('2025-09-20', 6,
     'React 19 — New Features & Migration',
     'Deep dive into React 19 concurrent features, Server Components, and migration strategies from class-based components.',
     'https://internal.owt.swiss/training/react19-2025',
     2, 1, 2, 1, 1),

    -- Carol
    ('2026-03-05', 3,
     'FastAPI for Beginners',
     'Introduction to FastAPI: routing, dependency injection, pydantic models, and async patterns.',
     'https://fastapi.tiangolo.com/tutorial/',
     3, 1, 1, 1, 1);

-- Training Coaches (Alice coaches Bob's React training and Carol's FastAPI training)
INSERT INTO training_coaches (training_id, user_id) VALUES
    (3, 1),  -- Alice coached Bob's React session
    (4, 1),  -- Alice coached Carol's FastAPI session
    (4, 2);  -- Bob also co-coached Carol's FastAPI session

-- =============================================================================
-- TASK ASSIGNMENTS
-- =============================================================================

INSERT INTO task_assignments (
    title, priority, status, details, due_to,
    estimation_hours, category_id, created_by, updated_by
) VALUES
    -- Task 1
    ('Implement ETL Extract Phase — Source DB Queries',
     'HIGH', 'DONE',
     'Build the psycopg2 query functions to pull RawEmployeeData from the source DB. Must cover: users, skills, experience, employment history, training.',
     '2026-01-31', 16, 4, 1, 1),

    -- Task 2
    ('Add pgvector HNSW index to skills_search_index',
     'MEDIUM', 'IN_PROGRESS',
     'Migrate the existing IVFFlat index to HNSW (m=16, ef_construction=64) for better recall at our current data scale (<10k rows).',
     '2026-06-15', 4, 3, 1, 1),

    -- Task 3 (subtask of task 2)
    ('Write migration script for HNSW index swap',
     'MEDIUM', 'OPEN',
     'Write a zero-downtime migration: create new HNSW index concurrently, drop old IVFFlat index. Add to migrations/ folder.',
     '2026-06-10', 2, 3, 2, 2),

    -- Task 4
    ('Fix: user_skills level column allows values > 5',
     'HIGH', 'IN_REVIEW',
     'Add a CHECK constraint (level BETWEEN 0 AND 5) to user_skills. Verify existing data before applying, add migration.',
     '2026-05-25', 2, 4, 1, 1),

    -- Task 5
    ('Document ra_minus_g query API endpoints',
     'LOW', 'OPEN',
     'Write OpenAPI descriptions for /search and /index endpoints. Include request/response examples and error codes.',
     '2026-06-30', 4, 4, 2, 2);

-- Set parent relationship (task 3 is subtask of task 2)
UPDATE task_assignments SET parent_id = 260002 WHERE id = 260003;

-- Task Assignees
INSERT INTO task_assignments_assignees (task_assignment_id, user_id) VALUES
    (260001, 1),  -- Alice owns task 1
    (260002, 1),  -- Alice owns task 2
    (260003, 2),  -- Bob owns task 3
    (260004, 1),  -- Alice owns task 4
    (260004, 2),  -- Bob co-assigned task 4
    (260005, 3);  -- Carol owns task 5

-- Task Comments
INSERT INTO task_assignments_comments (
    content, html_content, task_assignment_id, created_by, updated_by
) VALUES
    ('Extract phase complete. All 5 query functions implemented and unit-tested. PR #12 merged.',
     '<p>Extract phase complete. All 5 query functions implemented and unit-tested. PR #12 merged.</p>',
     260001, 1, 1),

    ('HNSW benchmarks show ~15% recall improvement vs IVFFlat at ef_search=40. Proceeding with migration.',
     '<p>HNSW benchmarks show ~15% recall improvement vs IVFFlat at ef_search=40. Proceeding with migration.</p>',
     260002, 1, 1),

    ('Reviewed the CHECK constraint migration — looks good. Added a test for the boundary condition (level=5).',
     '<p>Reviewed the CHECK constraint migration — looks good. Added a test for the boundary condition (level=5).</p>',
     260004, 2, 2);

-- Task Files
INSERT INTO task_assignments_files (url, task_assignment_id) VALUES
    ('https://internal.owt.swiss/files/etl-extract-design.pdf', 260001),
    ('https://internal.owt.swiss/files/hnsw-benchmark-results.png', 260002);

-- Task Labels
INSERT INTO task_assignments_labels (task_assignment_id, label_id) VALUES
    (260001, 6),   -- task 1: backend
    (260002, 3),   -- task 2: improvement
    (260002, 8),   -- task 2: infra
    (260003, 8),   -- task 3: infra
    (260004, 1),   -- task 4: bug
    (260004, 6),   -- task 4: backend
    (260005, 4);   -- task 5: documentation

-- =============================================================================
-- VERIFICATION QUERIES (run manually to sanity-check)
-- =============================================================================
-- SELECT u.first_name, u.last_name, p.name AS position, l.label AS level
--   FROM users u
--   JOIN positions p  ON p.id = u.position_id
--   JOIN user_levels l ON l.id = u.level_id;
--
-- SELECT u.first_name, sg.name AS skill_group, s.name AS skill, us.level
--   FROM user_skills us
--   JOIN users u ON u.id = us.user_id
--   JOIN skills s ON s.id = us.skill_id
--   JOIN skill_groups sg ON sg.id = s.skill_group_id
--   ORDER BY u.id, sg.name, us.level DESC;
--
-- SELECT t.title, t.status, t.priority, u.first_name AS assignee
--   FROM task_assignments t
--   JOIN task_assignments_assignees ta ON ta.task_assignment_id = t.id
--   JOIN users u ON u.id = ta.user_id
--   ORDER BY t.id;
