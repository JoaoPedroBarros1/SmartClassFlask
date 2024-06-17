-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: gerenciador
-- ------------------------------------------------------
-- Server version	8.0.37

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
  `id` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `aluno_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aluno`
--

LOCK TABLES `aluno` WRITE;
/*!40000 ALTER TABLE `aluno` DISABLE KEYS */;
INSERT INTO `aluno` VALUES (3),(4),(5);
/*!40000 ALTER TABLE `aluno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coordenador`
--

DROP TABLE IF EXISTS `coordenador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coordenador` (
  `id` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `coordenador_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordenador`
--

LOCK TABLES `coordenador` WRITE;
/*!40000 ALTER TABLE `coordenador` DISABLE KEYS */;
INSERT INTO `coordenador` VALUES (1),(8);
/*!40000 ALTER TABLE `coordenador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curso`
--

DROP TABLE IF EXISTS `curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curso` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `carga_horaria` int DEFAULT NULL,
  `start_curso` time NOT NULL,
  `end_curso` time NOT NULL,
  `dias_da_semana` int NOT NULL,
  `data_de_inicio` date NOT NULL,
  `id_professor` int NOT NULL,
  `id_sala` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_professor` (`id_professor`),
  KEY `id_sala` (`id_sala`),
  CONSTRAINT `curso_ibfk_1` FOREIGN KEY (`id_professor`) REFERENCES `professor` (`id`),
  CONSTRAINT `curso_ibfk_2` FOREIGN KEY (`id_sala`) REFERENCES `sala` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curso`
--

LOCK TABLES `curso` WRITE;
/*!40000 ALTER TABLE `curso` DISABLE KEYS */;
INSERT INTO `curso` VALUES (1,'Desenvolvimento de Sistemas',1200,'07:30:00','17:30:00',6,'2024-01-01',2,1);
/*!40000 ALTER TABLE `curso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emenda`
--

DROP TABLE IF EXISTS `emenda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emenda` (
  `id` int NOT NULL,
  `emenda` tinyint(1) NOT NULL,
  `data` date NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `emenda_ibfk_1` FOREIGN KEY (`id`) REFERENCES `feriado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emenda`
--

LOCK TABLES `emenda` WRITE;
/*!40000 ALTER TABLE `emenda` DISABLE KEYS */;
INSERT INTO `emenda` VALUES (2,1,'2024-02-12'),(7,1,'2024-05-31');
/*!40000 ALTER TABLE `emenda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feriado`
--

DROP TABLE IF EXISTS `feriado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feriado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feriado`
--

LOCK TABLES `feriado` WRITE;
/*!40000 ALTER TABLE `feriado` DISABLE KEYS */;
INSERT INTO `feriado` VALUES (1,'2024-01-01','Confraternização mundial'),(2,'2024-02-13','Carnaval'),(3,'2024-03-29','Sexta-feira Santa'),(4,'2024-03-31','Páscoa'),(5,'2024-04-21','Tiradentes'),(6,'2024-05-01','Dia do trabalho'),(7,'2024-05-30','Corpus Christi'),(8,'2024-09-07','Independência do Brasil'),(9,'2024-10-12','Nossa Senhora Aparecida'),(10,'2024-11-02','Finados'),(11,'2024-11-15','Proclamação da República'),(12,'2024-11-20','Dia da consciência negra'),(13,'2024-12-25','Natal');
/*!40000 ALTER TABLE `feriado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matricula`
--

DROP TABLE IF EXISTS `matricula`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matricula` (
  `id_aluno` int NOT NULL,
  `id_curso` int NOT NULL,
  PRIMARY KEY (`id_aluno`,`id_curso`),
  KEY `id_curso` (`id_curso`),
  CONSTRAINT `matricula_ibfk_1` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id`),
  CONSTRAINT `matricula_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matricula`
--

LOCK TABLES `matricula` WRITE;
/*!40000 ALTER TABLE `matricula` DISABLE KEYS */;
/*!40000 ALTER TABLE `matricula` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professor`
--

DROP TABLE IF EXISTS `professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professor` (
  `id` int NOT NULL,
  `start_turno` time NOT NULL,
  `end_turno` time NOT NULL,
  `dias_da_semana` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `professor_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professor`
--

LOCK TABLES `professor` WRITE;
/*!40000 ALTER TABLE `professor` DISABLE KEYS */;
INSERT INTO `professor` VALUES (2,'07:30:00','17:30:00',6),(6,'04:00:00','22:00:00',126),(7,'10:00:00','18:00:00',120);
/*!40000 ALTER TABLE `professor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reposicao`
--

DROP TABLE IF EXISTS `reposicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reposicao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `id_curso` int NOT NULL,
  `id_feriado` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_curso` (`id_curso`),
  KEY `id_feriado` (`id_feriado`),
  CONSTRAINT `reposicao_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id`),
  CONSTRAINT `reposicao_ibfk_2` FOREIGN KEY (`id_feriado`) REFERENCES `feriado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sala`
--

LOCK TABLES `sala` WRITE;
/*!40000 ALTER TABLE `sala` DISABLE KEYS */;
INSERT INTO `sala` VALUES (1,'Sala1'),(2,'Sala2'),(3,'Sala3');
/*!40000 ALTER TABLE `sala` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cargo` enum('Coordenador','Professor','Aluno') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'coordenador@gmail.com','$2b$12$we2LfM/0OWav76X2ec6cwOdCeBLUbULSEH6D90niqrGrMYDpJxgPu','default','Coordenador'),(2,'professor1@gmail.com','$2b$12$JmkopzAH7UnjhxsdSOFnJO.gN/WhR9e50VKV0phZoE9RMII5RIl5S','Prof1','Professor'),(3,'aluno1@gmail.com','$2b$12$8sqdjlAW7B0EHeB0FMqh6eNd0.fCMWSUrStPNXr/roJP2SUNRq2ti','Aluno1','Aluno'),(4,'aluno2@gmail.com','$2b$12$MtnbcMIloLF8NoZi79nVB.KIeZTQCyAs5qqQJgNZU.KPhpNFJ7jU.','Aluno2','Aluno'),(5,'aluno3@gmail.com','$2b$12$UpUNRQRpD3b2JGrvxFDy/epN8mZ5OEYs.lWnuEeCiyyD5X1Xx9MXC','Aluno3','Aluno'),(6,'professor2@gmail.com','$2b$12$8NkP.8pXOvG8KG4odKs7F.wqLI4l43uWZ5c8JhGOy8RfIYzCKGjJe','Prof2','Professor'),(7,'professor3@gmail.com','$2b$12$UxyjYhbb6FdX6DuCifOml.OFctYkiGsaewsBSVd2oFcL1YSoiQvKu','Prof3','Professor'),(8,'coordenador1@gmail.com','$2b$12$4me76akx5LeEVpo/Nu5ySOwSbGGlPPn39AbEMwt.JsD05df0gxg1m','Coor1','Coordenador');
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

-- Dump completed on 2024-06-16 22:53:54
