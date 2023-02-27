-- MySQL dump 10.19  Distrib 10.3.29-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: historic
-- ------------------------------------------------------
-- Server version	10.3.29-MariaDB-0+deb10u1

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
-- Table structure for table `machines`
--

DROP TABLE IF EXISTS `machines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `machines` (
  `id` int(11) NOT NULL,
  `nickname` varchar(45) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `brand` varchar(64) DEFAULT NULL,
  `model` varchar(64) DEFAULT NULL,
  `voltage` int(11) DEFAULT NULL,
  `amperage` float DEFAULT NULL,
  `serie` varchar(45) DEFAULT NULL,
  `id_line` int(11) DEFAULT NULL,
  `manufacturing_date` datetime DEFAULT NULL,
  `instalation_date` datetime DEFAULT NULL,
  `id_supplier` int(11) DEFAULT NULL,
  `run_date` datetime DEFAULT NULL,
  `path_image` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machines`
--

LOCK TABLES `machines` WRITE;
/*!40000 ALTER TABLE `machines` DISABLE KEYS */;
INSERT INTO `machines` VALUES (13,'Parts Assembler','Join different parts on a big item for car parts .........','ASBajio','1',120,2,'XXX.000.000.001',0,'2021-08-30 00:00:00','2021-09-15 00:00:00',0,'2021-09-16 00:00:00','img/tmp_workstation_01.jpeg');
/*!40000 ALTER TABLE `machines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenances`
--

DROP TABLE IF EXISTS `maintenances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maintenances` (
  `id` int(11) NOT NULL,
  `id_machine` int(11) NOT NULL,
  `id_maintenance_staff` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `problem_description` varchar(512) NOT NULL,
  `solution_description` varchar(512) DEFAULT NULL,
  `path_report` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_maintenances_1` (`id_machine`),
  KEY `fk_maintenances_2` (`id_maintenance_staff`),
  CONSTRAINT `fk_maintenances_1` FOREIGN KEY (`id_machine`) REFERENCES `machines` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_maintenances_2` FOREIGN KEY (`id_maintenance_staff`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenances`
--

LOCK TABLES `maintenances` WRITE;
/*!40000 ALTER TABLE `maintenances` DISABLE KEYS */;
/*!40000 ALTER TABLE `maintenances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outofservice_machine`
--

DROP TABLE IF EXISTS `outofservice_machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outofservice_machine` (
  `id` int(11) NOT NULL,
  `id_machine` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `description` varchar(512) NOT NULL,
  `has_solution` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_outofservice_machine_1` (`id_machine`),
  CONSTRAINT `fk_outofservice_machine_1` FOREIGN KEY (`id_machine`) REFERENCES `machines` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outofservice_machine`
--

LOCK TABLES `outofservice_machine` WRITE;
/*!40000 ALTER TABLE `outofservice_machine` DISABLE KEYS */;
/*!40000 ALTER TABLE `outofservice_machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parts`
--

DROP TABLE IF EXISTS `parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_machine` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `working_time` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`status` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parts`
--

LOCK TABLES `parts` WRITE;
/*!40000 ALTER TABLE `parts` DISABLE KEYS */;
INSERT INTO `parts` VALUES (1,0,'2021-08-09 19:16:20',0,100),(2,0,'2021-08-09 19:16:24',0,100),(3,0,'2021-08-09 19:16:25',0,100),(4,0,'2021-08-09 19:16:26',0,100),(5,0,'2021-08-09 19:29:44',0,100),(6,0,'2021-08-09 19:29:45',0,100),(7,0,'2021-08-09 19:29:46',0,100),(8,0,'2021-08-09 19:52:19',0,100),(9,0,'2021-08-09 19:52:20',0,100),(10,0,'2021-08-09 19:52:20',0,100),(11,0,'2021-08-09 19:52:21',0,100),(12,0,'2021-08-09 19:52:21',0,100),(13,0,'2021-08-09 19:52:22',0,100),(14,0,'2021-08-09 22:23:07',0,1529),(15,0,'2021-08-09 22:23:22',0,1590),(16,0,'2021-08-09 22:23:25',0,254),(17,0,'2021-08-09 22:23:28',0,1306),(18,0,'2021-08-09 22:23:29',0,1631),(19,0,'2021-08-09 22:23:30',1,200),(20,0,'2021-08-09 22:23:31',1,2260),(21,0,'2021-08-09 22:23:32',0,576),(22,0,'2021-08-09 22:23:32',0,1956),(23,0,'2021-08-09 22:23:33',1,1656),(24,0,'2021-08-20 19:24:03',1,2108),(25,0,'2021-08-20 19:24:23',1,2257),(26,0,'2021-08-20 19:24:24',1,2087),(27,0,'2021-08-20 19:24:53',1,2805),(28,0,'2021-08-20 19:24:54',0,1195),(29,0,'2021-08-20 19:24:55',1,2926),(30,0,'2021-08-20 19:24:57',1,1740),(31,0,'2021-08-20 19:24:58',1,1145),(32,0,'2021-08-20 19:42:45',0,698),(33,0,'2021-08-20 19:42:48',1,1156),(34,0,'2021-08-20 19:46:17',0,2544),(35,0,'2021-08-20 19:46:19',0,1662),(36,0,'2021-08-20 19:46:22',0,333),(37,0,'2021-08-20 19:46:23',1,1067),(38,0,'2021-08-20 19:46:24',0,2078),(39,0,'2021-08-20 19:46:26',1,866),(40,0,'2021-08-20 19:46:30',0,1290),(41,0,'2021-08-20 19:46:31',1,1322),(42,0,'2021-08-20 19:46:46',0,1495),(43,0,'2021-08-20 19:46:47',1,656),(44,0,'2021-08-20 19:46:47',0,2666),(45,0,'2021-08-20 19:46:49',0,908),(46,0,'2021-08-20 19:46:49',0,2934),(47,0,'2021-08-20 19:46:50',1,1150),(48,0,'2021-08-20 19:46:52',1,2966),(49,0,'2021-08-20 19:46:53',0,2568),(50,0,'2021-08-20 19:46:54',1,2327),(51,0,'2021-08-20 19:46:55',0,2013),(52,0,'2021-08-20 20:04:11',1,713),(53,0,'2021-08-20 20:04:18',1,1542),(54,0,'2021-08-20 20:04:19',1,2567),(55,0,'2021-08-20 20:04:20',0,157),(56,0,'2021-08-20 20:04:21',1,1457),(57,0,'2021-08-20 20:04:22',0,2422),(58,0,'2021-08-20 20:04:23',1,2356),(59,0,'2021-08-20 20:04:24',1,2508),(60,0,'2021-08-20 20:04:24',0,2807),(61,0,'2021-08-20 20:04:25',0,619),(62,0,'2021-08-20 20:04:26',1,2648),(63,0,'2021-08-20 20:04:27',1,1786),(64,0,'2021-08-20 20:08:04',0,1317),(65,0,'2021-08-20 20:08:37',0,1511),(66,0,'2021-12-01 00:13:25',0,2611),(67,0,'2021-12-01 00:13:32',1,1778),(68,0,'2021-12-01 00:13:32',0,500),(69,0,'2021-12-01 00:13:33',0,2981),(70,0,'2021-12-01 00:13:34',0,701),(71,0,'2021-12-01 00:13:34',0,1549),(72,0,'2021-12-01 00:13:52',1,1309),(73,0,'2021-12-01 00:13:53',0,2700),(74,0,'2021-12-01 00:13:54',0,1628),(75,0,'2021-12-01 00:13:55',0,2593),(76,0,'2021-12-01 00:13:56',0,473),(77,0,'2021-12-01 00:13:56',1,1167),(78,0,'2021-12-01 00:13:57',1,914),(79,0,'2021-12-01 00:13:58',0,1332),(80,0,'2021-12-01 00:13:59',1,2991),(81,0,'2021-12-01 00:14:00',1,515),(82,0,'2021-12-01 00:14:00',0,2568),(83,0,'2021-12-01 00:14:01',0,2341),(84,0,'2021-12-01 00:14:02',1,1700),(85,0,'2021-12-01 00:14:03',1,2750),(86,0,'2021-12-01 00:14:03',1,817),(87,0,'2021-12-01 00:14:04',1,2423),(88,0,'2021-12-01 00:14:05',1,902),(89,0,'2021-12-01 00:14:06',1,2910),(90,0,'2021-12-01 00:14:08',0,498),(91,0,'2021-12-01 00:14:08',0,2342),(92,0,'2021-12-01 00:14:09',1,2604),(93,0,'2021-12-01 00:14:09',1,1847),(94,0,'2021-12-01 00:14:10',1,640),(95,0,'2021-12-01 00:14:11',1,1526),(96,0,'2021-12-01 00:14:12',0,519),(97,0,'2021-12-01 00:14:12',0,1225),(98,0,'2021-12-01 00:14:13',0,1908),(99,0,'2021-12-01 00:14:13',1,2794);
/*!40000 ALTER TABLE `parts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rework_parts`
--

DROP TABLE IF EXISTS `rework_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rework_parts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `working_time` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_2` CHECK (`status` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rework_parts`
--

LOCK TABLES `rework_parts` WRITE;
/*!40000 ALTER TABLE `rework_parts` DISABLE KEYS */;
INSERT INTO `rework_parts` VALUES (1,'2021-08-20 19:24:03',0,1194),(2,'2021-08-20 19:24:24',0,1196),(3,'2021-08-20 19:24:53',1,2895),(4,'2021-08-20 19:24:57',0,1558),(5,'2021-08-20 19:24:58',1,172),(41,'2021-08-20 19:46:31',1,713),(47,'2021-08-20 19:46:50',1,1892),(50,'2021-08-20 19:46:54',0,344),(63,'2021-08-20 20:04:27',0,1598),(72,'2021-12-01 00:13:52',1,1964),(77,'2021-12-01 00:13:56',1,596),(81,'2021-12-01 00:14:00',0,2549),(87,'2021-12-01 00:14:04',0,2500),(93,'2021-12-01 00:14:09',1,2988),(94,'2021-12-01 00:14:10',0,1933),(95,'2021-12-01 00:14:11',0,290),(99,'2021-12-01 00:14:13',1,1237);
/*!40000 ALTER TABLE `rework_parts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(40) DEFAULT NULL,
  `fullname` varchar(256) DEFAULT NULL,
  `pwhash` varchar(256) DEFAULT NULL,
  `id_employee` int(11) DEFAULT NULL,
  `id_role` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'arturo','Arturo Garcia','pbkdf2:sha256:150000$PutYAVBv$ef3b386a0c1778dba4c486bb382b48d7a123e67a81b9e92dcd72311b6700b187',1313,1),(2,'jose055new','Jose Garcia','pbkdf2:sha256:150000$AjTYDZ0M$75d8fa63f0350deec860ea1092a79a1d0bbe7f80627a4d12efbba01c95588631',11041990,110490);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-01 17:34:18
