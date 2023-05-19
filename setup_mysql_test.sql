-- CREATE DATABASE --
CREATE DATABASE IF NOT EXISTS 'church_management_system_test';

-- CREATE USER --
CREATE USER IF NOT EXISTS 'cms_test'@'localhost' IDENTIFIED BY 'cms_test';

-- GRANT USER PRIVILEGES --
GRANT ALL PRIVILEGES ON church_management_system.* TO 'cms_test'@'localhost';

-- Grant SELECT privilege on performance_schema to jerressy
GRANT SELECT ON performance_schema.* TO 'cms_test'@'localhost';
