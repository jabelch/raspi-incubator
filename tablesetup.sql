CREATE DATABASE temps;
USE temps

CREATE TABLE IF NOT EXISTS `setpoints` (
    `id` int(10) NOT NULL,
    `sp_high` NUMERIC NOT NULL,
    `sp_low` NUMERIC NOT NULL,
    `sp_too_hot` NUMERIC NOT NULL,
    `sp_high_h, NUMERIC NOT NULL,
    `sp_low_h, NUMERIC NOT NULL,
    `sp_too_humid`, NUMERIC NOT NULL,
    UNIQUE (`id`),
    PRIMARY KEY (`id`)
);
  
CREATE TABLE IF NOT EXISTS `tempdat` (
    `tdatetime` TIMESTAMP NOT NULL,
    `zone` VARCHAR(64),
    `temperature` NUMERIC NOT NULL,
    `humidity` NUMERIC
);

CREATE TABLE IF NOT EXISTS `pins` (
    `id` INT(3) NOT NULL,
    `pin` INT(2) NOT NULL,
    `name` VARCHAR(64),
    UNIQUE(`pin`),
    PRIMARY KEY(`id`)
);

INSERT INTO `setpoints` (`id`, `sp_high`, `sp_low`, `sp_too_hot`, `sp_high_h`, `sp_low_h`, `sp_too_humid`)
VALUES(1, 38, 38, 40, 52, 42, 62);

INSERT INTO `pins` (`id`, `pin`, `name`)
VALUES(1, 23, "Lamp"), 
(2, 24, "Circulation Fan"), 
(3, 25, "Emergency Fan"), 
(4, 8, "Humidity Fan");
