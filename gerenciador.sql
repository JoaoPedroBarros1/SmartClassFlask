-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: gerenciador
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aluno`
--

DROP TABLE IF EXISTS `aluno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aluno` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `aluno_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aluno`
--

LOCK TABLES `aluno` WRITE;
/*!40000 ALTER TABLE `aluno` DISABLE KEYS */;
INSERT INTO `aluno` VALUES (3),(5),(6),(7),(9),(11);
/*!40000 ALTER TABLE `aluno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coordenador`
--

DROP TABLE IF EXISTS `coordenador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coordenador` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `coordenador_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordenador`
--

LOCK TABLES `coordenador` WRITE;
/*!40000 ALTER TABLE `coordenador` DISABLE KEYS */;
INSERT INTO `coordenador` VALUES (1);
/*!40000 ALTER TABLE `coordenador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curso`
--

DROP TABLE IF EXISTS `curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `carga_horaria` int(11) NOT NULL,
  `start_curso` time NOT NULL,
  `end_curso` time NOT NULL,
  `dias_da_semana` int(11) NOT NULL,
  `data_de_inicio` date NOT NULL,
  `id_professor` int(11) NOT NULL,
  `id_sala` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_professor` (`id_professor`),
  KEY `id_sala` (`id_sala`),
  CONSTRAINT `curso_ibfk_1` FOREIGN KEY (`id_professor`) REFERENCES `professor` (`id`),
  CONSTRAINT `curso_ibfk_2` FOREIGN KEY (`id_sala`) REFERENCES `sala` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curso`
--

LOCK TABLES `curso` WRITE;
/*!40000 ALTER TABLE `curso` DISABLE KEYS */;
INSERT INTO `curso` VALUES (2,'Vendas',1600,'07:30:00','17:30:00',6,'2025-01-01',2,2),(3,'Logistica',1600,'13:30:00','16:00:00',6,'2024-07-01',4,1),(4,'TI',1600,'08:10:00','16:10:00',13,'2024-06-01',10,3);
/*!40000 ALTER TABLE `curso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emenda`
--

DROP TABLE IF EXISTS `emenda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emenda` (
  `id` int(11) NOT NULL,
  `emenda` tinyint(1) NOT NULL,
  `data` date NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `emenda_ibfk_1` FOREIGN KEY (`id`) REFERENCES `feriado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emenda`
--

LOCK TABLES `emenda` WRITE;
/*!40000 ALTER TABLE `emenda` DISABLE KEYS */;
INSERT INTO `emenda` VALUES (2,1,'2024-02-12'),(7,1,'2024-05-31'),(15,1,'2025-03-03'),(19,1,'2025-05-02'),(20,1,'2025-06-20'),(25,1,'2025-11-21'),(26,1,'2025-12-26'),(27,1,'2026-01-02'),(28,1,'2026-02-16'),(31,1,'2026-04-20'),(33,1,'2026-06-05');
/*!40000 ALTER TABLE `emenda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feriado`
--

DROP TABLE IF EXISTS `feriado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feriado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feriado`
--

LOCK TABLES `feriado` WRITE;
/*!40000 ALTER TABLE `feriado` DISABLE KEYS */;
INSERT INTO `feriado` VALUES (1,'2024-01-01','Confraternização mundial'),(2,'2024-02-13','Carnaval'),(3,'2024-03-29','Sexta-feira Santa'),(4,'2024-03-31','Páscoa'),(5,'2024-04-21','Tiradentes'),(6,'2024-05-01','Dia do trabalho'),(7,'2024-05-30','Corpus Christi'),(8,'2024-09-07','Independência do Brasil'),(9,'2024-10-12','Nossa Senhora Aparecida'),(10,'2024-11-02','Finados'),(11,'2024-11-15','Proclamação da República'),(12,'2024-11-20','Dia da consciência negra'),(13,'2024-12-25','Natal'),(14,'2025-01-01','Confraternização mundial'),(15,'2025-03-04','Carnaval'),(16,'2025-04-18','Sexta-feira Santa'),(17,'2025-04-20','Páscoa'),(18,'2025-04-21','Tiradentes'),(19,'2025-05-01','Dia do trabalho'),(20,'2025-06-19','Corpus Christi'),(21,'2025-09-07','Independência do Brasil'),(22,'2025-10-12','Nossa Senhora Aparecida'),(23,'2025-11-02','Finados'),(24,'2025-11-15','Proclamação da República'),(25,'2025-11-20','Dia da consciência negra'),(26,'2025-12-25','Natal'),(27,'2026-01-01','Confraternização mundial'),(28,'2026-02-17','Carnaval'),(29,'2026-04-03','Sexta-feira Santa'),(30,'2026-04-05','Páscoa'),(31,'2026-04-21','Tiradentes'),(32,'2026-05-01','Dia do trabalho'),(33,'2026-06-04','Corpus Christi'),(34,'2026-09-07','Independência do Brasil'),(35,'2026-10-12','Nossa Senhora Aparecida'),(36,'2026-11-02','Finados'),(37,'2026-11-15','Proclamação da República'),(38,'2026-11-20','Dia da consciência negra'),(39,'2026-12-25','Natal');
/*!40000 ALTER TABLE `feriado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matricula`
--

DROP TABLE IF EXISTS `matricula`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matricula` (
  `id_aluno` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  PRIMARY KEY (`id_aluno`,`id_curso`),
  KEY `id_curso` (`id_curso`),
  CONSTRAINT `matricula_ibfk_1` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id`),
  CONSTRAINT `matricula_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matricula`
--

LOCK TABLES `matricula` WRITE;
/*!40000 ALTER TABLE `matricula` DISABLE KEYS */;
INSERT INTO `matricula` VALUES (3,3),(5,3),(6,2),(7,2),(9,3),(11,2);
/*!40000 ALTER TABLE `matricula` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professor`
--

DROP TABLE IF EXISTS `professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professor` (
  `id` int(11) NOT NULL,
  `start_turno` time NOT NULL,
  `end_turno` time NOT NULL,
  `dias_da_semana` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `professor_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professor`
--

LOCK TABLES `professor` WRITE;
/*!40000 ALTER TABLE `professor` DISABLE KEYS */;
INSERT INTO `professor` VALUES (2,'07:30:00','17:30:00',6),(4,'06:32:00','16:31:00',127),(10,'05:10:00','17:10:00',127);
/*!40000 ALTER TABLE `professor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reposicao`
--

DROP TABLE IF EXISTS `reposicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reposicao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `id_curso` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_curso` (`id_curso`),
  CONSTRAINT `reposicao_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reposicao`
--

LOCK TABLES `reposicao` WRITE;
/*!40000 ALTER TABLE `reposicao` DISABLE KEYS */;
/*!40000 ALTER TABLE `reposicao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sala`
--

DROP TABLE IF EXISTS `sala`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sala` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sala`
--

LOCK TABLES `sala` WRITE;
/*!40000 ALTER TABLE `sala` DISABLE KEYS */;
INSERT INTO `sala` VALUES (1,'Sala de TI'),(2,'Sala2'),(3,'Sala3');
/*!40000 ALTER TABLE `sala` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cargo` enum('Coordenador','Professor','Aluno') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'coordenador@gmail.com','$2b$12$yTeLkx06OJewghGNNrm1C.h2XLNmVOPnUA962On2/8q06U2K6D9km','default','Coordenador'),(2,'igor@gmail.com','$2b$12$fyC67EnMJNhUX9B/JwtbOuMx3n2GeqotCtCuEQJBa1FETb9W05JU6','Igor','Professor'),(3,'bianca@gmail.com','$2b$12$ZJb3RITiYuvTl2XtkIH7suKx6MlEGDqMnxF6g/ikigGHrE8LyxQcK','Bianca','Aluno'),(4,'Lais@gmail.com','$2b$12$VBRGM267Mul7.9kfEXbgHegni9XTthpYUgrHHU/TXK1FY1IPMOSbe','Lais','Professor'),(5,'Miguel@gmail.com','$2b$12$uT/CIM0hAxRtzG8uqnuvOOWGF5NHE3KCGzGobiFYt6HtzXHlop1P.','Miguel','Aluno'),(6,'barros@gmail.com','$2b$12$YNZ801Cw8wDSRx9K/m9D6OwRLdIY5aizVyCLjvOmsRDeGANJfFOFW','Barros','Aluno'),(7,'leticia@gmail.com','$2b$12$3wixcybJi.Z.7enqr1ZwF.J8T6S8.mFEYtT1wJDsaDf/EigeZNMOG','leticia','Aluno'),(9,'sanches@gmail.com','$2b$12$u1MKYX4h7vRJw7kYHXeqeudadS319yt0VIEp104UbVHICOKzezbj2','Sanches','Aluno'),(10,'maikola@gmail.com','$2b$12$7tHLYE0loKQh70Y5ub01LuSEuMkGL4DjDQhe3WVVa.0ENDzdw/XOy','maikola','Professor'),(11,'Caue@gmail.com','$2b$12$tNRMWqByysOwTxCxQCAw5.2sC3fbM04LtKoMD3ENOTVP7.JNdtT0K','Caue','Aluno');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-24 17:25:33
