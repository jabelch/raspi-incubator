CREATE DATABASE temps;
USE temps

CREATE TABLE IF NOT EXISTS `setpoints` (
    `id` int(10) NOT NULL,
    `sp_high` numeric NOT NULL,
    `sp_low` numeric NOT NULL
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
    `id` int(3) NOT NULL,
    `pin` int(2) NOT NULL,
    `name` varchar(64),
    UNIQUE(`pin`),
    PRIMARY KEY(`id`)
);

INSERT INTO `setpoints` (`id`, `sp_high`, `sp_low`)
VALUES(1, 102, 97);

INSERT INTO `pins` (`id`, `pin`, `name`)
VALUES(1, 23, "Lamp"), 
(2, 24, "Fan"), 
(3, 25, "IN3"), 
(4, 8, "IN4");
