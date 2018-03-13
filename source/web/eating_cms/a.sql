CREATE database N1CTF;
use N1CTF;
DROP TABLE IF EXISTS `albert_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `albert_users` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `username_which_you_do_not_know` varchar(200) NOT NULL DEFAULT '',
  `password_which_you_do_not_know_too` varchar(200) NOT NULL DEFAULT '',
  `isadmin_which_you_do_not_know_too_too` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_which_you_do_not_know` (`username_which_you_do_not_know`)
) ENGINE=MyISAM AUTO_INCREMENT=596 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `albert_users`
--

LOCK TABLES `albert_users` WRITE;
/*!40000 ALTER TABLE `albert_users` DISABLE KEYS */;
INSERT INTO `albert_users` VALUES (1,'admin','2417ca0e6583038191148d03cccad37f','1');
/*!40000 ALTER TABLE `albert_users` ENABLE KEYS */;
UNLOCK TABLES;
