CREATE DATABASE  IF NOT EXISTS `tat` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `tat`;
-- MySQL dump 10.13  Distrib 5.6.23, for Win32 (x86)
--
-- Host: localhost    Database: tat
-- ------------------------------------------------------
-- Server version	5.0.18-nt

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Not dumping tablespaces as no INFORMATION_SCHEMA.FILES table on this server
--

--
-- Table structure for table `exceptions`
--

DROP TABLE IF EXISTS `exceptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exceptions` (
  `id` int(32) NOT NULL,
  `timestamp` varchar(24) default NULL,
  `module_id` varchar(24) default NULL,
  `sample_id` varchar(24) default NULL,
  `err_code` varchar(24) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payload`
--

DROP TABLE IF EXISTS `payload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payload` (
  `id` int(32) NOT NULL auto_increment,
  `sample_id` varchar(24) default NULL,
  `module_id` varchar(24) default NULL,
  `module_type` varchar(24) default NULL,
  `timestamp` varchar(24) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='payload of each module.\nEach record is a <RETURNED> message.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `results` (
  `id` int(32) NOT NULL auto_increment,
  `sample_id` varchar(24) NOT NULL,
  `test_code` varchar(24) NOT NULL,
  `analyzer_id` varchar(24) default NULL,
  `value` varchar(24) NOT NULL,
  `timestamp` varchar(24) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tat`
--

DROP TABLE IF EXISTS `tat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tat` (
  `sample_id` varchar(48) NOT NULL,
  `lis_order` varchar(24) default NULL,
  `las_inlab` varchar(24) default NULL,
  `centrifuge_in` varchar(24) default NULL,
  `centrifuge_out` varchar(24) default NULL,
  `decap` varchar(24) default NULL,
  `advia_query` varchar(24) default NULL,
  `advia_result` varchar(24) default NULL,
  `centaur_query` varchar(24) default NULL,
  `centaur_result` varchar(24) default NULL,
  `seal` varchar(24) default NULL,
  `store` varchar(24) default NULL,
  `lis_upload` varchar(24) default NULL,
  `inlab_cat` varchar(24) default NULL,
  `analyzer_type` varchar(24) default NULL,
  `TAT` varchar(24) default NULL,
  `CM_TAT` varchar(24) default NULL,
  `Chem_TAT` varchar(24) default NULL,
  `Immu_TAT` varchar(24) default NULL,
  `Track_TAT` varchar(24) default NULL,
  PRIMARY KEY  (`sample_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tat_last_update_timestamp`
--

DROP TABLE IF EXISTS `tat_last_update_timestamp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tat_last_update_timestamp` (
  `type_id` varchar(16) NOT NULL,
  `last_file_update_timestamp` varchar(24) default '0',
  `last_record_update_timestamp` varchar(24) default '0',
  PRIMARY KEY  (`type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'tat'
--
/*!50003 DROP FUNCTION IF EXISTS `new_function` */;
--
-- WARNING: old server version. The following dump may be incomplete.
--
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER' */ ;
DELIMITER ;;
CREATE FUNCTION `new_function`() RETURNS int(11)
BEGIN

UPDATE tat SET inlab_cat = 'morning'  WHERE HOUR(las_inlab) < 11;
UPDATE tat SET inlab_cat = 'noon'  WHERE HOUR(las_inlab) >= 11 AND HOUR(las_inlab) < 14;
UPDATE tat SET inlab_cat = 'afternoon'  WHERE HOUR(las_inlab) >= 14;

RETURN 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-20 15:34:02
