CREATE DATABASE temps;
USE temps

CREATE TABLE IF NOT EXISTS `setpoints` (
    `id` int(3) NOT NULL AUTO_INCREMENT,
    `sp_high` numeric NOT NULL,
    `sp_low` numeric NOT NULL
);
  
CREATE TABLE IF NOT EXISTS `tempdat` (
    `tdatetime` TIMESTAMP NOT NULL,
    `zone` VARCHAR(64),
    `temperature` NUMERIC NOT NULL,
    `humidity` NUMERIC
);

INSERT INTO `setpoints` (`id`, `sp_high`, `sp_low`)
VALUES(1, 102, 97);
