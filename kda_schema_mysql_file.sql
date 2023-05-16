-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema kda_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `kda_schema` ;

-- -----------------------------------------------------
-- Schema kda_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `kda_schema` DEFAULT CHARACTER SET utf8 ;
USE `kda_schema` ;

-- -----------------------------------------------------
-- Table `kda_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kda_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `riot_identification` VARCHAR(22) NOT NULL,
  `favorite_agent` VARCHAR(45) NOT NULL,
  `current_rank` VARCHAR(45) NOT NULL,
  `goal_rank` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kda_schema`.`matches`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kda_schema`.`matches` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `match_date` DATE NOT NULL,
  `agent` VARCHAR(45) NOT NULL,
  `map` VARCHAR(45) NOT NULL,
  `kills` TINYINT(100) NOT NULL,
  `deaths` TINYINT(100) NOT NULL,
  `assists` TINYINT(100) NOT NULL,
  `headshot_percentage` TINYINT(100) NOT NULL,
  `adr` MEDIUMINT(1000) NOT NULL,
  `acs` MEDIUMINT(1000) NOT NULL,
  `diary_entry` TEXT NOT NULL,
  `youtube_link` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_matches_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_matches_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `kda_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kda_schema`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kda_schema`.`category` (
  `category_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`category_id`));


-- -----------------------------------------------------
-- Table `kda_schema`.`category_1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kda_schema`.`category_1` (
  `category_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`category_id`));


-- -----------------------------------------------------
-- Table `kda_schema`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kda_schema`.`user` (
  `username` VARCHAR(16) NOT NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(32) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);


-- -----------------------------------------------------
-- Table `kda_schema`.`timestamps`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kda_schema`.`timestamps` (
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP NULL);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
