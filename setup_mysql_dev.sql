-- CREATE DATABASE --
CREATE DATABASE IF NOT EXISTS 'church_management_system_dev';

-- CREATE USER --
CREATE USER IF NOT EXISTS 'cms_dev'@'localhost' IDENTIFIED BY 'cms_dev';

-- GRANT USER PRIVILEGES --
GRANT ALL PRIVILEGES ON church_management_system.* TO 'cms_dev'@'localhost';

-- Grant SELECT privilege on performance_schema to jerressy
GRANT SELECT ON performance_schema.* TO 'cms_dev'@'localhost';
