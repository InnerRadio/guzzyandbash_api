/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ab2583ta_ab2583tarot_lyrical_tarot_db
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_logs`
--

DROP TABLE IF EXISTS `activity_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_logs` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `activity_type` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  `metadata_json` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_logs`
--

LOCK TABLES `activity_logs` WRITE;
/*!40000 ALTER TABLE `activity_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `activity_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affiliate_clicks`
--

DROP TABLE IF EXISTS `affiliate_clicks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `affiliate_clicks` (
  `id` char(36) NOT NULL,
  `affiliate_id` char(36) NOT NULL,
  `timestamp` datetime NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(512) DEFAULT NULL,
  `referer_url` varchar(2048) DEFAULT NULL,
  `click_destination_url` varchar(2048) NOT NULL,
  `campaign_id` char(36) DEFAULT NULL,
  `ad_id` char(36) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_affiliate_clicks_ad_id` (`ad_id`),
  KEY `ix_affiliate_clicks_campaign_id` (`campaign_id`),
  KEY `ix_affiliate_clicks_affiliate_id` (`affiliate_id`),
  CONSTRAINT `affiliate_clicks_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliate_clicks`
--

LOCK TABLES `affiliate_clicks` WRITE;
/*!40000 ALTER TABLE `affiliate_clicks` DISABLE KEYS */;
INSERT INTO `affiliate_clicks` VALUES
('001e806d-dc76-4cfe-8f4e-7496414213d3','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-11-27 08:45:12','222.244.147.203','Opera/9.62.(Windows CE; nds-DE) Presto/2.9.188 Version/12.00',NULL,'https://reyes.com/',NULL,NULL,'2024-11-27 08:45:12','2024-11-27 08:45:12'),
('0066131c-79c5-4b4a-be26-722e7649b694','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-03-07 23:46:44',NULL,'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_8 like Mac OS X) AppleWebKit/532.2 (KHTML, like Gecko) CriOS/40.0.839.0 Mobile/16M994 Safari/532.2','http://wilson.org/bloghomepage.html','https://www.foley.com/',NULL,'6c4755bc-ec80-483f-849a-0827a0fbd981','2025-03-07 23:46:44','2025-03-07 23:46:44'),
('026c915e-0ed7-4e32-95e3-c3aa0316d7f5','d2ee5d26-5b68-43ec-a93f-e742145192fc','2024-09-25 17:44:20','94.35.85.7','Opera/9.96.(X11; Linux i686; nds-DE) Presto/2.9.160 Version/12.00','https://gates.com/main/categories/appabout.htm','http://perez.com/',NULL,'c76601c1-4e21-4c90-b612-b0657aadeff9','2024-09-25 17:44:20','2024-09-25 17:44:20'),
('028de1ab-84dc-4d98-b50f-df68710421ef','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2025-05-27 18:50:03','61.117.154.176','Mozilla/5.0 (Android 1.6; Mobile; rv:5.0) Gecko/5.0 Firefox/5.0','http://harper.com/blog/wp-content/wp-contentmain.html','http://www.aguilar.com/',NULL,NULL,'2025-05-27 18:50:03','2025-05-27 18:50:03'),
('03d15225-88ee-4a80-b61f-8d0327f1cb11','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2025-03-13 20:17:05','39.229.137.118','Opera/8.54.(Windows NT 6.0; mg-MG) Presto/2.9.184 Version/12.00','https://dickerson.com/main/wp-contenthomepage.html','http://www.thompson-garrett.com/','5398e87d-bebb-4241-bf1d-8106e450ce1a','8b47b285-e231-457c-a36d-75cc4cb2ef8c','2025-03-13 20:17:05','2025-03-13 20:17:05'),
('04c0ae4f-23f7-4a3a-b578-6f6b72e0a99e','89356118-12d2-4fde-a7d2-2acd5603f266','2025-03-07 10:43:48','117.106.2.207','Mozilla/5.0 (Android 3.2.5; Mobile; rv:60.0) Gecko/60.0 Firefox/60.0',NULL,'https://www.davis.com/',NULL,NULL,'2025-03-07 10:43:48','2025-03-07 10:43:48'),
('04dda47c-0c17-4a8f-9c4a-4a239bc7247a','d2ee5d26-5b68-43ec-a93f-e742145192fc','2024-08-17 11:39:16','107.83.238.197','Mozilla/5.0 (Windows; U; Windows NT 4.0) AppleWebKit/534.4.3 (KHTML, like Gecko) Version/4.0.3 Safari/534.4.3',NULL,'http://www.ellison-boone.com/',NULL,NULL,'2024-08-17 11:39:16','2024-08-17 11:39:16'),
('0874496e-d986-4e04-9ca7-f7b13720190f','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-01-25 03:39:29',NULL,'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_9 rv:3.0; aa-ER) AppleWebKit/535.36.7 (KHTML, like Gecko) Version/5.0.2 Safari/535.36.7','http://jenkins.com/taghome.asp','http://gonzalez.org/',NULL,NULL,'2025-01-25 03:39:29','2025-01-25 03:39:29'),
('08f8b289-9182-44f9-bdac-1ad38b15dbe0','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-04-15 16:31:54',NULL,'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_10_7 rv:3.0; is-IS) AppleWebKit/534.35.5 (KHTML, like Gecko) Version/4.0 Safari/534.35.5',NULL,'http://www.burton-mcbride.com/','bd5497b1-d520-4edb-99ea-cb0537aa2ee2',NULL,'2025-04-15 16:31:54','2025-04-15 16:31:54'),
('098a0d30-39cc-40d4-af33-5993a34c64bc','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-06-10 01:08:07','17.30.8.189','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_8 rv:5.0; tk-TM) AppleWebKit/534.41.4 (KHTML, like Gecko) Version/5.0 Safari/534.41.4',NULL,'http://www.tran.com/',NULL,NULL,'2025-06-10 01:08:07','2025-06-10 01:08:07'),
('09b61a08-d014-4a7c-a3b0-11aa832af9da','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-09-18 02:34:51','105.53.135.70','Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 11.0; Trident/4.1)','https://www.park-smith.com/blog/categories/tagslogin.html','https://www.moreno.org/','501a1849-3c3d-4bc2-912c-f547fa87e417',NULL,'2024-09-18 02:34:51','2024-09-18 02:34:51'),
('09c1c22b-2e7d-4b05-950e-bf5e9d9926ef','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-03-11 11:26:51','105.1.197.99','Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)','http://lara-johnson.com/main/explore/categoriesterms.jsp','https://santos.net/',NULL,NULL,'2025-03-11 11:26:51','2025-03-11 11:26:51'),
('0a079e69-2b71-4edd-b0d4-18f8b2a0a5b5','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-09-22 16:30:41','177.167.98.66','Opera/8.82.(Windows NT 6.1; ha-NG) Presto/2.9.165 Version/12.00',NULL,'https://mcbride.com/','8b336da7-9240-4f72-b1da-d61c1e88ab1b',NULL,'2024-09-22 16:30:41','2024-09-22 16:30:41'),
('0b6bab14-5285-4038-98f2-e02d1432aad6','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2025-04-23 04:20:36','219.12.142.163','Mozilla/5.0 (X11; Linux i686; rv:1.9.5.20) Gecko/3783-11-26 07:16:55.018127 Firefox/3.8','http://galloway.com/posts/posts/searchauthor.asp','http://www.white.net/',NULL,NULL,'2025-04-23 04:20:36','2025-04-23 04:20:36'),
('0bc7bc8e-31ca-41d9-9961-8aa2ea47954c','8bda9505-912a-4356-ade5-22a8f9484ab9','2024-09-25 12:19:38','88.192.227.107','Opera/9.53.(Windows CE; niu-NZ) Presto/2.9.180 Version/11.00',NULL,'https://www.bryant.com/',NULL,NULL,'2024-09-25 12:19:38','2024-09-25 12:19:38'),
('0cf22734-8be1-4ab0-b03b-7ac511cb0765','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-02-01 05:55:30','48.104.110.212','Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/22.0.867.0 Safari/535.2',NULL,'http://www.blake-hahn.net/',NULL,NULL,'2025-02-01 05:55:30','2025-02-01 05:55:30'),
('0f46b34a-1ceb-4312-9f8f-04dbbd584112','a699f263-3050-44cc-8738-f5002a4b9298','2025-04-09 17:00:40','120.248.126.224','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_12_4 rv:4.0; zh-TW) AppleWebKit/534.26.3 (KHTML, like Gecko) Version/5.1 Safari/534.26.3','http://www.gardner.org/explore/searchmain.html','https://www.williams.biz/',NULL,'44bb057b-6b2f-42e9-a505-cae72c9a4a94','2025-04-09 17:00:40','2025-04-09 17:00:40'),
('0f6784ad-d604-46be-9396-afdf10f09971','a699f263-3050-44cc-8738-f5002a4b9298','2025-05-06 16:21:54','198.131.15.125','Mozilla/5.0 (Windows 98; st-ZA; rv:1.9.2.20) Gecko/9830-03-10 18:37:10.689819 Firefox/3.6.8','http://brown-hardy.com/categories/tagsindex.asp','https://moore-baker.info/',NULL,NULL,'2025-05-06 16:21:54','2025-05-06 16:21:54'),
('0f6af982-fe65-48df-b0ca-4587eda685b4','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-03-20 07:53:09','13.122.129.210','Opera/8.91.(Windows CE; iw-IL) Presto/2.9.187 Version/11.00','http://www.fisher-ford.com/appabout.html','https://hayes.info/',NULL,'7e39a581-9106-4734-a29c-159779c24f0d','2025-03-20 07:53:09','2025-03-20 07:53:09'),
('10eb5d3b-cc7c-41fd-8254-53eff387a9a5','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-05-05 07:50:41','213.39.28.2','Mozilla/5.0 (Windows 98; Win 9x 4.90; fr-CA; rv:1.9.2.20) Gecko/2240-02-08 00:59:52.250331 Firefox/3.6.14',NULL,'https://williams.com/','71738405-b579-4e82-a3fa-e1c2a7708f10',NULL,'2025-05-05 07:50:41','2025-05-05 07:50:41'),
('11db214e-aeb1-4010-8816-aec4228fee3e','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-10-15 01:15:12','190.4.13.198','Opera/8.13.(Windows NT 5.1; cs-CZ) Presto/2.9.162 Version/12.00',NULL,'http://gonzalez-singleton.net/',NULL,NULL,'2024-10-15 01:15:12','2024-10-15 01:15:12'),
('138e0962-a116-45f9-bc32-495ada6a796f','349f7ae0-523f-4093-90db-9b5f13344881','2025-03-18 20:27:11','169.170.154.199','Opera/9.65.(Windows NT 5.01; mag-IN) Presto/2.9.172 Version/12.00','http://johnson-spencer.biz/explore/categories/categoryindex.php','https://www.waters.net/',NULL,NULL,'2025-03-18 20:27:11','2025-03-18 20:27:11'),
('1507aeed-905c-44b5-ace6-02922b5466f4','349f7ae0-523f-4093-90db-9b5f13344881','2025-04-18 05:16:45','203.250.199.201','Mozilla/5.0 (iPad; CPU iPad OS 17_2 like Mac OS X) AppleWebKit/531.1 (KHTML, like Gecko) FxiOS/15.5y9345.0 Mobile/32S687 Safari/531.1',NULL,'https://moon-moore.com/','d2518f2b-b25a-4ff3-892c-a5d520d80eac',NULL,'2025-04-18 05:16:45','2025-04-18 05:16:45'),
('16286c02-5f1c-4d18-8a00-3d8bf199498a','a699f263-3050-44cc-8738-f5002a4b9298','2024-11-07 15:19:07',NULL,'Opera/9.32.(Windows 95; ne-NP) Presto/2.9.187 Version/11.00','https://www.ball.com/app/tags/listcategory.html','http://jackson.info/',NULL,NULL,'2024-11-07 15:19:07','2024-11-07 15:19:07'),
('16f437cd-8a5a-4270-b3c2-5014f64e81c5','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2025-04-26 08:47:57','69.89.95.131','Mozilla/5.0 (compatible; MSIE 7.0; Windows 98; Trident/3.1)','http://www.barrera.org/taghome.asp','http://www.smith.net/',NULL,'cab04651-97be-493e-b191-fed8ca2ee963','2025-04-26 08:47:57','2025-04-26 08:47:57'),
('1700ac95-d49e-4ffc-89a8-330d87ac5d9e','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2025-04-14 12:45:41',NULL,'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_5 rv:2.0; sa-IN) AppleWebKit/533.28.7 (KHTML, like Gecko) Version/5.0 Safari/533.28.7','http://www.berger-duke.com/list/searchterms.htm','http://thomas.com/','5298da11-eb17-4024-8c2b-f5f77cae0af8',NULL,'2025-04-14 12:45:41','2025-04-14 12:45:41'),
('17355d16-28fb-4b78-bb4e-140872eff29f','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-12-01 05:20:13','203.35.84.10','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 10.0; Trident/4.0)','http://www.thomas.info/exploreterms.htm','http://fields.com/',NULL,NULL,'2024-12-01 05:20:13','2024-12-01 05:20:13'),
('17ff11b8-32d1-41ac-804b-3b91ada4b14b','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-04-20 02:43:54','123.114.153.71','Opera/8.53.(X11; Linux i686; oc-FR) Presto/2.9.169 Version/12.00',NULL,'http://www.mccullough.org/','0c88b8b9-1930-4086-9c4a-173ac22c96b7','71fbee8b-1f45-45be-8216-16e25469832c','2025-04-20 02:43:54','2025-04-20 02:43:54'),
('1a0497e3-4984-47f5-95b6-2728dcb44b2b','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-08-27 00:34:08','135.77.210.91','Mozilla/5.0 (X11; Linux i686) AppleWebKit/531.2 (KHTML, like Gecko) Chrome/63.0.845.0 Safari/531.2',NULL,'https://phillips.info/',NULL,'9f003b6c-aad5-4c59-b8a0-f6a4e956bf20','2024-08-27 00:34:08','2024-08-27 00:34:08'),
('1ab1cd59-39cd-4d27-ab41-61def43df550','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-07-31 11:17:06',NULL,'Opera/8.84.(Windows NT 5.2; yue-HK) Presto/2.9.168 Version/12.00','http://smith.com/main/app/categorypost.html','https://www.martinez.com/','d79e7859-04c3-435e-9296-ac0d8c0530d8',NULL,'2024-07-31 11:17:06','2024-07-31 11:17:06'),
('1def3e88-e4d5-4467-9d93-9d452f3907cb','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-03-09 03:21:45',NULL,'Opera/8.13.(X11; Linux x86_64; sd-PK) Presto/2.9.161 Version/11.00',NULL,'http://smith-collins.com/','a88b663a-d57f-4c8a-917f-253520e66c32',NULL,'2025-03-09 03:21:45','2025-03-09 03:21:45'),
('1e1e207d-1e11-4027-b8bd-52cb60417e89','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-08-08 10:15:26',NULL,'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.01; Trident/4.1)','https://www.mccoy.com/blog/appfaq.html','http://www.alexander.com/',NULL,NULL,'2024-08-08 10:15:26','2024-08-08 10:15:26'),
('244a6330-7451-4bc9-9590-5571b579007c','8bda9505-912a-4356-ade5-22a8f9484ab9','2024-09-04 15:33:29',NULL,'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/8070-06-09 00:57:16.120911 Firefox/8.0','https://www.green.biz/explore/tagshomepage.html','http://www.mcconnell.com/','1f72f61f-b7db-4680-a34a-9ec59846b44d',NULL,'2024-09-04 15:33:29','2024-09-04 15:33:29'),
('25ee02a5-b062-4395-ab47-20a47a0a77c6','349f7ae0-523f-4093-90db-9b5f13344881','2025-01-01 09:02:31','125.188.164.216','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 10.0; Trident/4.1)',NULL,'http://gomez.com/',NULL,NULL,'2025-01-01 09:02:31','2025-01-01 09:02:31'),
('279dd74c-155a-4f43-b710-6d333334b9cd','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2025-01-11 21:39:28','147.178.108.143','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/533.0 (KHTML, like Gecko) Chrome/52.0.816.0 Safari/533.0','https://www.bailey.info/explorehome.php','http://www.lawrence-sawyer.com/',NULL,NULL,'2025-01-11 21:39:28','2025-01-11 21:39:28'),
('28caca3d-3f83-442c-99fb-0e71810cea6e','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2024-08-25 15:07:37',NULL,'Mozilla/5.0 (Windows NT 6.2; sq-AL; rv:1.9.1.20) Gecko/4536-03-07 16:35:47.573547 Firefox/3.6.11','https://www.graves-anderson.biz/search/listhome.htm','https://www.smith.com/',NULL,NULL,'2024-08-25 15:07:37','2024-08-25 15:07:37'),
('2912f561-6298-4416-8395-b957d3af2721','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-10-22 08:48:33','111.186.123.62','Mozilla/5.0 (Windows 98; Win 9x 4.90) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/52.0.888.0 Safari/535.2','https://www.martinez.net/search/searchterms.htm','http://www.white.com/',NULL,NULL,'2024-10-22 08:48:33','2024-10-22 08:48:33'),
('295aef9f-8ded-4ae7-a3dd-1cda2b4778dd','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-12-06 15:23:29',NULL,'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.1)',NULL,'http://ramirez.com/',NULL,'a5511b4b-0132-4e09-9228-490978d26358','2024-12-06 15:23:29','2024-12-06 15:23:29'),
('2aa211b0-ac8a-483e-bb07-b4c1fd3ebbd3','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-05-18 04:13:42',NULL,'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/5.1)',NULL,'https://www.lewis-meyer.com/','24884681-8a43-4311-9e09-a17adaad2157',NULL,'2025-05-18 04:13:42','2025-05-18 04:13:42'),
('2d58fe3d-a821-4614-bd5a-a8801a41ba8e','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-10-26 22:35:30','205.195.36.252','Opera/8.31.(X11; Linux x86_64; sd-PK) Presto/2.9.187 Version/10.00',NULL,'https://jordan.net/',NULL,NULL,'2024-10-26 22:35:30','2024-10-26 22:35:30'),
('2d8f904c-7d5a-4e56-b0b1-e684f94f8a7e','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-10-26 13:52:05',NULL,'Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/535.28.6 (KHTML, like Gecko) Version/4.1 Safari/535.28.6','https://www.grant.net/list/wp-contentsearch.php','https://walker.biz/','55102361-20a1-4b28-85e5-e3d95bb9aa7c','21e2144d-e39e-4a08-8cf0-c28c8d360e28','2024-10-26 13:52:05','2024-10-26 13:52:05'),
('2f292989-4902-492c-8e63-6561385e26ba','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-10-09 00:50:43','44.154.168.39','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_10_1; rv:1.9.5.20) Gecko/5049-06-10 22:19:24.461060 Firefox/3.6.17','http://taylor.info/search/app/exploremain.php','http://www.hines-carr.com/',NULL,NULL,'2024-10-09 00:50:43','2024-10-09 00:50:43'),
('2f60dc6f-e5fd-475d-a23e-5c7b35140b1a','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2025-05-22 14:31:39',NULL,'Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/532.47.6 (KHTML, like Gecko) Version/4.0 Safari/532.47.6',NULL,'http://klein-bennett.org/',NULL,NULL,'2025-05-22 14:31:39','2025-05-22 14:31:39'),
('312fe59d-991e-420f-9405-128a4f30b8de','349f7ae0-523f-4093-90db-9b5f13344881','2025-06-25 14:45:12','18.96.84.206','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_7 rv:3.0; tg-TJ) AppleWebKit/531.2.4 (KHTML, like Gecko) Version/5.0.1 Safari/531.2.4',NULL,'https://www.phillips-porter.net/',NULL,NULL,'2025-06-25 14:45:12','2025-06-25 14:45:12'),
('31af2da4-d0cf-4ef4-b30d-77ba5aa4b7d1','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-09-02 22:40:49','83.40.7.198','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_0 rv:6.0; fo-FO) AppleWebKit/534.29.5 (KHTML, like Gecko) Version/5.0.2 Safari/534.29.5','http://johnson.org/main/postsmain.htm','http://www.gibson-baldwin.info/',NULL,NULL,'2024-09-02 22:40:49','2024-09-02 22:40:49'),
('32559db7-adf8-456a-b5c1-1431f107b4fe','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-09-05 04:34:00','32.183.60.209','Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_4 like Mac OS X) AppleWebKit/535.2 (KHTML, like Gecko) FxiOS/10.1o9029.0 Mobile/87F982 Safari/535.2',NULL,'http://bailey.net/',NULL,NULL,'2024-09-05 04:34:00','2024-09-05 04:34:00'),
('326a6afd-9669-4cdb-9267-d825edd43e4f','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-07-12 13:21:37','114.199.173.53','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1 rv:6.0; ts-ZA) AppleWebKit/532.43.5 (KHTML, like Gecko) Version/5.0 Safari/532.43.5','http://www.myers.com/tagsabout.htm','http://lee.com/','bf3e54b0-9e6b-4215-bb3b-c04a62608f00','7af6f3e3-cad4-4c9f-8760-bae7c40792a3','2024-07-12 13:21:37','2024-07-12 13:21:37'),
('327d2a03-847c-4322-b5ac-e292b506b98f','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2024-08-11 21:35:47',NULL,'Mozilla/5.0 (Android 2.2; Mobile; rv:19.0) Gecko/19.0 Firefox/19.0','http://singleton-mason.com/postssearch.html','https://donovan.org/',NULL,NULL,'2024-08-11 21:35:47','2024-08-11 21:35:47'),
('32fc03b8-dac2-4f9c-9ab8-ef84b0257f45','a699f263-3050-44cc-8738-f5002a4b9298','2025-03-03 06:04:13','115.161.32.10','Mozilla/5.0 (compatible; MSIE 6.0; Windows 98; Win 9x 4.90; Trident/5.0)','http://www.sharp.com/wp-contentlogin.php','https://www.chung.com/',NULL,NULL,'2025-03-03 06:04:13','2025-03-03 06:04:13'),
('362fa409-275e-4604-8e78-a44b26986947','349f7ae0-523f-4093-90db-9b5f13344881','2024-12-13 07:47:36','187.184.187.196','Opera/8.15.(X11; Linux i686; cy-GB) Presto/2.9.167 Version/10.00',NULL,'https://www.lopez.net/',NULL,NULL,'2024-12-13 07:47:36','2024-12-13 07:47:36'),
('36f41d7e-afeb-4d01-ae51-c97451996385','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-04-26 13:25:53','191.89.115.150','Mozilla/5.0 (iPod; U; CPU iPhone OS 3_2 like Mac OS X; tl-PH) AppleWebKit/532.7.7 (KHTML, like Gecko) Version/3.0.5 Mobile/8B114 Safari/6532.7.7',NULL,'https://david.com/','1978b01a-6fe0-48a0-aff8-09cacaa87a59',NULL,'2025-04-26 13:25:53','2025-04-26 13:25:53'),
('3780dcfd-5c7d-4c87-8869-b527e056f059','d2ee5d26-5b68-43ec-a93f-e742145192fc','2024-09-02 05:34:04','166.27.63.121','Mozilla/5.0 (compatible; MSIE 8.0; Windows 95; Trident/3.1)',NULL,'http://www.owens-smith.com/',NULL,'97f84a0a-a697-4776-85e0-7c236635dfed','2024-09-02 05:34:04','2024-09-02 05:34:04'),
('3877c008-9d8b-4e21-a390-e6e99975fdf7','a699f263-3050-44cc-8738-f5002a4b9298','2024-09-25 16:20:24',NULL,'Opera/9.11.(X11; Linux i686; ky-KG) Presto/2.9.165 Version/11.00',NULL,'http://www.jennings.info/',NULL,NULL,'2024-09-25 16:20:24','2024-09-25 16:20:24'),
('39a5f54d-0217-4464-9c0b-e6a7a4167034','8bda9505-912a-4356-ade5-22a8f9484ab9','2024-12-20 09:19:48','121.217.192.44','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_2; rv:1.9.2.20) Gecko/9580-02-29 14:46:53.928162 Firefox/3.8','https://duncan.com/main/postssearch.php','https://price.com/','26853fc6-1da7-431d-a9b8-522cecf9a08f',NULL,'2024-12-20 09:19:48','2024-12-20 09:19:48'),
('3aa1c966-eea1-4ef2-8a69-489f67874a33','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-11-16 12:10:06','165.129.210.185','Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/26.0.830.0 Safari/534.1','http://jackson.org/postsprivacy.html','https://robertson.org/',NULL,NULL,'2024-11-16 12:10:06','2024-11-16 12:10:06'),
('408ef711-8526-4771-8cab-02505ad692a5','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-10-15 04:12:50',NULL,'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_4 rv:4.0; ce-RU) AppleWebKit/531.49.7 (KHTML, like Gecko) Version/5.0.3 Safari/531.49.7',NULL,'https://rice.com/',NULL,NULL,'2024-10-15 04:12:50','2024-10-15 04:12:50'),
('40efb486-2102-44e9-b80f-6e515dfcdccb','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-01-05 18:31:27','212.124.112.78','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.1)','https://rivers.com/listprivacy.html','http://mercado.com/',NULL,NULL,'2025-01-05 18:31:27','2025-01-05 18:31:27'),
('4215ad15-5384-41ca-8762-2c455e0088ee','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-10-09 16:52:56','211.246.100.68','Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; ce-RU) AppleWebKit/533.48.3 (KHTML, like Gecko) Version/3.0.5 Mobile/8B113 Safari/6533.48.3','https://www.martin.com/categoryabout.php','https://trujillo.com/','a998526b-c1fc-4060-90bd-2af721e004ce',NULL,'2024-10-09 16:52:56','2024-10-09 16:52:56'),
('42f804f9-84b4-49c3-9750-69de95c28dba','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-06-14 05:16:45','125.108.42.63','Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/531.26.2 (KHTML, like Gecko) Version/5.0 Safari/531.26.2',NULL,'https://www.alvarado.com/','94dbe79d-5316-4977-9eea-dda14e09d8a0',NULL,'2025-06-14 05:16:45','2025-06-14 05:16:45'),
('4407be6d-0ead-41a2-9953-e9e14f11ce02','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-11-20 02:16:00','169.222.134.66','Mozilla/5.0 (Android 4.0.4; Mobile; rv:19.0) Gecko/19.0 Firefox/19.0',NULL,'http://clark-mcdowell.com/',NULL,NULL,'2024-11-20 02:16:00','2024-11-20 02:16:00'),
('44316d2a-964b-42a4-b69d-ae19df21ec53','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2025-04-07 05:46:29','32.81.31.205','Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 5.01; Trident/4.0)',NULL,'https://smith.net/',NULL,NULL,'2025-04-07 05:46:29','2025-04-07 05:46:29'),
('4490d6a3-973a-4cc8-bb04-fb4785f3fdeb','89356118-12d2-4fde-a7d2-2acd5603f266','2024-10-26 10:10:47','206.9.54.134','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_12_4) AppleWebKit/533.0 (KHTML, like Gecko) Chrome/47.0.833.0 Safari/533.0',NULL,'https://www.cooper-gonzales.com/','2deeee99-8373-4cf2-b394-9b7118258531',NULL,'2024-10-26 10:10:47','2024-10-26 10:10:47'),
('44a28b55-be6d-402d-87e0-cfa5f154ce60','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-05-22 12:08:15','84.77.31.181','Mozilla/5.0 (X11; Linux x86_64; rv:1.9.5.20) Gecko/3356-11-29 17:03:13.355820 Firefox/11.0','http://www.mitchell.com/taghome.php','http://caldwell-ross.com/',NULL,NULL,'2025-05-22 12:08:15','2025-05-22 12:08:15'),
('45bd1f64-7276-45f9-9299-84d0e8d45442','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-06-08 13:22:09','15.135.225.47','Mozilla/5.0 (iPod; U; CPU iPhone OS 4_0 like Mac OS X; lij-IT) AppleWebKit/532.44.3 (KHTML, like Gecko) Version/3.0.5 Mobile/8B115 Safari/6532.44.3','http://www.salazar.com/categories/categoriesfaq.php','https://www.campbell-morgan.com/',NULL,'f410c2fd-7771-4d4c-9cc5-7f4aabc04f95','2025-06-08 13:22:09','2025-06-08 13:22:09'),
('4641c15f-fe86-4152-b6bf-b7b318c16022','a699f263-3050-44cc-8738-f5002a4b9298','2025-02-27 01:51:36','155.126.58.72','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4 rv:5.0; ik-CA) AppleWebKit/534.15.4 (KHTML, like Gecko) Version/5.0 Safari/534.15.4','https://pena.com/search/search/searchindex.html','http://www.west-hoffman.com/',NULL,NULL,'2025-02-27 01:51:36','2025-02-27 01:51:36'),
('4674a71e-de25-4059-a009-20220a05ad79','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-06-01 23:12:30','46.127.113.183','Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.0; Trident/3.0)',NULL,'http://ramirez.com/',NULL,NULL,'2025-06-01 23:12:30','2025-06-01 23:12:30'),
('46d7f44e-6899-4348-b817-15ecc92bc48a','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2025-02-17 00:31:13','5.17.228.54','Mozilla/5.0 (Windows; U; Windows NT 4.0) AppleWebKit/532.8.6 (KHTML, like Gecko) Version/5.0 Safari/532.8.6','https://www.brock.net/main/explorecategory.asp','http://www.brown-stewart.com/',NULL,NULL,'2025-02-17 00:31:13','2025-02-17 00:31:13'),
('4778ec83-8cd7-4e76-9a79-603dabfa936c','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-04-11 10:13:41',NULL,'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 6.2; Trident/3.0)','http://larson.info/app/wp-content/postsmain.htm','https://nunez.org/',NULL,NULL,'2025-04-11 10:13:41','2025-04-11 10:13:41'),
('48d7321a-342f-475d-bbdc-668518ce3605','349f7ae0-523f-4093-90db-9b5f13344881','2025-03-12 17:33:56',NULL,'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 4.0; Trident/3.1)',NULL,'http://www.thompson.org/','efb6517a-b820-4661-8a2d-c6468985dbb4',NULL,'2025-03-12 17:33:56','2025-03-12 17:33:56'),
('4a7ef2c1-e399-4109-9509-f28ac31c239e','a699f263-3050-44cc-8738-f5002a4b9298','2024-08-16 03:35:35','116.13.158.18','Mozilla/5.0 (Windows CE; uz-UZ; rv:1.9.1.20) Gecko/3407-07-03 22:42:50.881569 Firefox/6.0',NULL,'https://bailey.net/',NULL,'4723913b-f6d2-4abb-b481-d678e87f1a81','2024-08-16 03:35:35','2024-08-16 03:35:35'),
('4ab044c0-7ab1-4310-be68-f86a1e00a69e','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-05-13 05:36:03','114.222.231.132','Mozilla/5.0 (Linux; Android 2.3.4) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.0.835.0 Safari/535.2',NULL,'https://www.montoya.com/','7b856c76-0651-4a11-90b9-59238ecd40ef',NULL,'2025-05-13 05:36:03','2025-05-13 05:36:03'),
('4be9ac3a-63a9-4416-a020-1db4d1a2e08b','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-06-11 21:57:16','175.90.34.123','Mozilla/5.0 (Windows NT 5.1; mag-IN; rv:1.9.2.20) Gecko/8068-03-07 15:32:57.164459 Firefox/5.0','http://scott-roberts.com/searchauthor.asp','http://morton.com/',NULL,'149e9c9c-87d8-4a11-afba-2405274a9001','2025-06-11 21:57:16','2025-06-11 21:57:16'),
('4cbd1cc9-f96f-4fe4-9047-da7f7ab8526b','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-09-21 12:02:26',NULL,'Opera/9.30.(X11; Linux i686; pap-AW) Presto/2.9.167 Version/12.00','https://www.stein-french.com/explore/tagabout.jsp','https://green-macias.com/','ccd163ca-db79-40b2-89eb-20719f765893','fd83b6e0-1815-47b5-af9d-1a9d1126cc82','2024-09-21 12:02:26','2024-09-21 12:02:26'),
('4fd19c87-a2c9-4968-964a-4b462ccad7a9','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-12-27 01:16:57','52.48.183.30','Mozilla/5.0 (iPod; U; CPU iPhone OS 3_3 like Mac OS X; pap-AN) AppleWebKit/535.9.2 (KHTML, like Gecko) Version/4.0.5 Mobile/8B114 Safari/6535.9.2',NULL,'https://mueller.com/',NULL,NULL,'2024-12-27 01:16:57','2024-12-27 01:16:57'),
('4fd8b450-cf9b-4ed2-a72b-26a80250faa2','349f7ae0-523f-4093-90db-9b5f13344881','2024-12-02 09:15:39','36.239.84.85','Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/8529-04-23 05:54:43.908936 Firefox/3.6.16','http://garcia.biz/appfaq.jsp','https://www.combs.net/',NULL,'7327b185-5993-440e-b575-1681113c8192','2024-12-02 09:15:39','2024-12-02 09:15:39'),
('50093685-8cfc-4022-a7d2-7e3d11254312','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-07-21 21:08:36',NULL,'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/6058-05-24 23:00:30.657272 Firefox/3.6.14',NULL,'https://williams.biz/',NULL,NULL,'2024-07-21 21:08:36','2024-07-21 21:08:36'),
('51db811b-3f52-477e-8ade-95af962cbdf6','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-06-06 07:53:24','10.84.68.26','Mozilla/5.0 (Windows NT 6.1; ce-RU; rv:1.9.1.20) Gecko/8302-03-09 13:13:06.592712 Firefox/14.0','https://www.robbins-lee.biz/tagspost.html','https://taylor.com/','d239f644-1181-4979-9b8e-039393f416c8',NULL,'2025-06-06 07:53:24','2025-06-06 07:53:24'),
('556a5cdd-befb-4830-9da2-c9a8afe24022','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-03-02 07:04:57','120.250.93.159','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_9_4 rv:4.0; kok-IN) AppleWebKit/535.13.3 (KHTML, like Gecko) Version/4.1 Safari/535.13.3',NULL,'https://krueger.com/',NULL,NULL,'2025-03-02 07:04:57','2025-03-02 07:04:57'),
('5a3e1aaa-ded0-42b9-9d70-9343b57a3409','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-01-27 23:50:50','39.29.54.206','Mozilla/5.0 (Windows NT 6.2) AppleWebKit/531.2 (KHTML, like Gecko) Chrome/15.0.846.0 Safari/531.2','http://www.williams.com/categories/explore/searchabout.php','https://fischer.com/',NULL,NULL,'2025-01-27 23:50:50','2025-01-27 23:50:50'),
('5aa41d13-afa3-45f5-966a-2f74afaf9dc1','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-12-15 01:20:03',NULL,'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/3.0)','http://spencer.net/tagsabout.html','http://www.jones.com/','54f1b7d3-821e-435e-8dd7-cee8f0f7a5c9',NULL,'2024-12-15 01:20:03','2024-12-15 01:20:03'),
('5b4acff1-750b-4809-a859-0d079f7edbc2','89356118-12d2-4fde-a7d2-2acd5603f266','2024-10-10 09:58:28','93.231.230.121','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_7 rv:5.0; ur-IN) AppleWebKit/533.13.6 (KHTML, like Gecko) Version/5.1 Safari/533.13.6','https://sanchez.com/tag/blogprivacy.htm','http://phillips.com/',NULL,NULL,'2024-10-10 09:58:28','2024-10-10 09:58:28'),
('5bdb5e5c-fb34-4c08-adbb-98bb0a3b0779','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-05-09 18:53:21','115.77.92.240','Opera/8.99.(X11; Linux i686; az-AZ) Presto/2.9.168 Version/10.00',NULL,'http://prince-robinson.com/',NULL,NULL,'2025-05-09 18:53:21','2025-05-09 18:53:21'),
('5c0f4843-1d89-4a2d-b66c-e94aea00e00f','349f7ae0-523f-4093-90db-9b5f13344881','2024-10-20 09:05:23',NULL,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.0 (KHTML, like Gecko) Chrome/53.0.837.0 Safari/535.0','http://taylor.info/explorepost.asp','https://schmidt.org/',NULL,NULL,'2024-10-20 09:05:23','2024-10-20 09:05:23'),
('5f87944d-f6b8-4ea5-b322-a4f3a2b8c236','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-05-26 09:04:05','221.184.11.131','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_12_6) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/40.0.827.0 Safari/534.1','http://www.moore.com/tag/tagpost.html','http://www.adams.com/',NULL,NULL,'2025-05-26 09:04:05','2025-05-26 09:04:05'),
('5fb2af11-279c-4aa6-ae34-89343f04be7c','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-12-12 05:05:44','77.237.76.183','Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)','https://www.smith-johnson.com/wp-contentfaq.htm','http://www.miller.org/',NULL,NULL,'2024-12-12 05:05:44','2024-12-12 05:05:44'),
('60b442b9-df0a-414b-9500-8c35f466d45e','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-10-02 20:55:52','214.112.31.197','Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.2 (KHTML, like Gecko) Chrome/28.0.861.0 Safari/534.2',NULL,'https://www.romero.com/',NULL,NULL,'2024-10-02 20:55:52','2024-10-02 20:55:52'),
('65ab4124-cd49-47e7-927e-416704552351','349f7ae0-523f-4093-90db-9b5f13344881','2024-10-21 13:19:19','184.66.55.35','Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1 like Mac OS X; lo-LA) AppleWebKit/532.49.3 (KHTML, like Gecko) Version/3.0.5 Mobile/8B114 Safari/6532.49.3','https://www.zimmerman.com/wp-contentpost.asp','http://nelson.com/',NULL,NULL,'2024-10-21 13:19:19','2024-10-21 13:19:19'),
('65de6664-f03a-4df0-9d80-bcf74e4b92ec','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-01-28 16:57:07','30.96.148.177','Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/6040-05-05 04:27:03.100510 Firefox/3.8',NULL,'http://www.gutierrez.com/',NULL,NULL,'2025-01-28 16:57:07','2025-01-28 16:57:07'),
('674c86e2-8c85-427c-b246-579953043b6a','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-05-09 09:49:18',NULL,'Opera/8.88.(X11; Linux i686; ti-ER) Presto/2.9.165 Version/11.00','http://www.ortega.com/appcategory.html','https://garcia-webster.com/',NULL,NULL,'2025-05-09 09:49:18','2025-05-09 09:49:18'),
('685c61a6-8060-4e33-a1d3-d7ff7c18d92d','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-06-09 17:29:36',NULL,'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/19.0.816.0 Safari/532.1','http://rollins-jackson.com/search/categoriesindex.php','http://www.payne-campbell.com/',NULL,'547eab58-feae-4045-a8a2-57cc0628380b','2025-06-09 17:29:36','2025-06-09 17:29:36'),
('68f75f17-3f79-4a1e-83ea-9c911545ff1f','89356118-12d2-4fde-a7d2-2acd5603f266','2024-08-03 19:03:19',NULL,'Mozilla/5.0 (Linux; Android 2.3.7) AppleWebKit/533.0 (KHTML, like Gecko) Chrome/61.0.806.0 Safari/533.0',NULL,'https://www.ramirez.com/',NULL,NULL,'2024-08-03 19:03:19','2024-08-03 19:03:19'),
('693b7518-4e1b-4d26-aae5-7df31f9b503d','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-12-25 12:24:02',NULL,'Mozilla/5.0 (Android 3.2.4; Mobile; rv:58.0) Gecko/58.0 Firefox/58.0',NULL,'http://smith-barnes.com/',NULL,'186420ab-6ee5-47f2-b671-48b1084880be','2024-12-25 12:24:02','2024-12-25 12:24:02'),
('695f3825-cefe-4be9-a162-d77a6d52b146','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-01-02 07:24:58','134.20.160.248','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_10_0; rv:1.9.6.20) Gecko/8051-04-06 06:21:31.793701 Firefox/3.8','http://garcia.com/mainhome.html','https://www.ballard.com/',NULL,NULL,'2025-01-02 07:24:58','2025-01-02 07:24:58'),
('6f4e2ef5-723c-4a69-98ff-5f6b266c72f1','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-07-16 14:09:56','19.72.135.143','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 11.0; Trident/5.1)',NULL,'https://www.douglas-valdez.info/',NULL,NULL,'2024-07-16 14:09:56','2024-07-16 14:09:56'),
('6fdddc81-3ef5-49a2-a413-181106705c24','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-03-05 18:52:38','53.124.200.82','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_11_2 rv:4.0; mhr-RU) AppleWebKit/533.50.1 (KHTML, like Gecko) Version/4.0.1 Safari/533.50.1',NULL,'http://villanueva-cruz.info/',NULL,NULL,'2025-03-05 18:52:38','2025-03-05 18:52:38'),
('719adbb8-92ca-4032-be3f-c4f73daa116f','89356118-12d2-4fde-a7d2-2acd5603f266','2024-08-06 18:27:17','110.77.225.233','Mozilla/5.0 (iPad; CPU iPad OS 17_4_1 like Mac OS X) AppleWebKit/531.2 (KHTML, like Gecko) FxiOS/9.9r4271.0 Mobile/02Y047 Safari/531.2',NULL,'https://www.davis.net/','d65b79a8-9cd0-436f-b444-2b86c47f2bbd',NULL,'2024-08-06 18:27:17','2024-08-06 18:27:17'),
('71dfe29f-310d-4d6e-9c7a-643a9a303782','89356118-12d2-4fde-a7d2-2acd5603f266','2024-11-04 19:47:15',NULL,'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/8527-11-10 16:56:56.725769 Firefox/13.0','https://juarez.biz/posts/list/searchpost.html','http://robinson.net/',NULL,NULL,'2024-11-04 19:47:15','2024-11-04 19:47:15'),
('728c3f26-c10a-4017-9fe3-048555663240','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-03-18 18:51:26',NULL,'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.1)',NULL,'http://malone.biz/',NULL,'6a41a538-b873-4a2c-9874-8e7115181149','2025-03-18 18:51:26','2025-03-18 18:51:26'),
('729bc166-2ddc-4f70-b4cd-83d2148232aa','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-12-10 19:10:32','67.166.192.152','Opera/9.18.(Windows NT 4.0; bo-CN) Presto/2.9.171 Version/10.00','https://www.murray.com/tags/posts/blogcategory.html','https://www.mitchell-carroll.com/',NULL,NULL,'2024-12-10 19:10:32','2024-12-10 19:10:32'),
('72e10b1b-5468-44d7-9f17-073d898217e5','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-10-16 18:22:55','57.50.191.254','Mozilla/5.0 (Windows; U; Windows 98; Win 9x 4.90) AppleWebKit/535.2.4 (KHTML, like Gecko) Version/5.0.5 Safari/535.2.4','https://www.christensen.com/mainlogin.asp','https://lee.com/','eea6d2d9-3394-494b-ab56-2a907c6d88fd',NULL,'2024-10-16 18:22:55','2024-10-16 18:22:55'),
('73749967-1068-4fe3-972c-cd35cc63bfc4','89356118-12d2-4fde-a7d2-2acd5603f266','2024-09-08 18:57:54','85.140.35.114','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_4 rv:5.0; yi-US) AppleWebKit/535.50.5 (KHTML, like Gecko) Version/4.0 Safari/535.50.5','https://www.nolan-johnson.net/tags/exploreindex.html','https://www.ray.com/',NULL,NULL,'2024-09-08 18:57:54','2024-09-08 18:57:54'),
('7590d6f8-4ffb-4398-bb0a-afa1c645b20e','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-11-11 23:12:57','22.134.88.68','Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/533.9.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.9.1','https://www.davis.net/blog/list/wp-contentcategory.html','http://bradford-ochoa.net/',NULL,NULL,'2024-11-11 23:12:57','2024-11-11 23:12:57'),
('75925260-757d-4c0a-bfef-24eee7f787e9','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-02-21 00:13:32','165.110.199.244','Opera/9.42.(X11; Linux i686; ha-NG) Presto/2.9.181 Version/10.00',NULL,'http://www.andrews-french.com/','67d839f0-33ca-4a79-9246-f6633e2c7962','77ca0804-3163-4e5d-b2d1-ed1058496f1d','2025-02-21 00:13:32','2025-02-21 00:13:32'),
('75a71b39-5d6a-4515-8d78-a22bca8b7f28','a699f263-3050-44cc-8738-f5002a4b9298','2025-06-14 00:20:26','118.20.44.220','Opera/8.51.(X11; Linux i686; nan-TW) Presto/2.9.161 Version/10.00',NULL,'https://lester-hill.net/',NULL,NULL,'2025-06-14 00:20:26','2025-06-14 00:20:26'),
('75f1d7cf-aa8f-4459-bf22-7271b810b958','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-09-20 01:12:28',NULL,'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 10.0; Trident/3.1)',NULL,'https://www.johnson.org/',NULL,'532f0883-a050-445a-a3a2-c15bba1b2cbf','2024-09-20 01:12:28','2024-09-20 01:12:28'),
('771580ca-4f8f-4f5b-ad81-19086a12d480','349f7ae0-523f-4093-90db-9b5f13344881','2024-10-30 20:26:39',NULL,'Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/532.11.4 (KHTML, like Gecko) Version/5.1 Safari/532.11.4','http://diaz.com/search/tag/searchcategory.html','https://watson-wilson.com/',NULL,NULL,'2024-10-30 20:26:39','2024-10-30 20:26:39'),
('79a6d6e1-1649-4417-8666-6981803451ca','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-12-10 12:00:19','223.109.183.151','Mozilla/5.0 (iPad; CPU iPad OS 17_1_1 like Mac OS X) AppleWebKit/533.2 (KHTML, like Gecko) CriOS/52.0.804.0 Mobile/89P722 Safari/533.2','https://miller-romero.net/main/search/exploresearch.htm','http://www.brown.net/',NULL,NULL,'2024-12-10 12:00:19','2024-12-10 12:00:19'),
('7bb54be2-3bda-4318-bf4e-5800a5cb9089','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-11-13 11:41:26','1.191.26.169','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_10_7) AppleWebKit/531.1 (KHTML, like Gecko) Chrome/50.0.807.0 Safari/531.1','http://collier-mitchell.com/app/wp-contentmain.html','http://smith.com/','5e95331f-8d84-4558-a532-a94381133d06',NULL,'2024-11-13 11:41:26','2024-11-13 11:41:26'),
('7bfb5662-6d16-41b4-b6ac-cc65f936c8c8','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-02-17 13:42:31','135.151.250.62','Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/535.33.2 (KHTML, like Gecko) Version/5.0 Safari/535.33.2',NULL,'https://www.flores-cuevas.com/',NULL,NULL,'2025-02-17 13:42:31','2025-02-17 13:42:31'),
('7c1ec061-5902-4b89-a1b7-2a1f7dc246e0','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-03-14 21:17:08','123.148.68.177','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_8_8; rv:1.9.4.20) Gecko/4758-06-10 10:45:19.761749 Firefox/10.0','https://www.clark.info/app/searchterms.htm','https://welch.com/',NULL,NULL,'2025-03-14 21:17:08','2025-03-14 21:17:08'),
('7d9cbffe-9b50-4e27-b1d3-d1f969c18103','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-04-13 06:13:21','42.242.139.134','Opera/9.80.(X11; Linux i686; apn-IN) Presto/2.9.174 Version/11.00','http://shah.com/tag/tagssearch.php','http://www.white-chung.info/','f2588f57-820d-4206-9bee-13e522e893bd','9c3b9018-2b0f-4465-8a76-303f27ca7405','2025-04-13 06:13:21','2025-04-13 06:13:21'),
('81fe6133-dda8-4a53-a11f-7bde9981576b','d2ee5d26-5b68-43ec-a93f-e742145192fc','2024-12-07 20:27:18',NULL,'Mozilla/5.0 (Windows; U; Windows NT 4.0) AppleWebKit/534.31.6 (KHTML, like Gecko) Version/4.0.3 Safari/534.31.6','https://www.hamilton.com/exploreindex.html','https://sanders-peck.org/','fcca354b-2113-4fb5-b9af-51566d693c2f',NULL,'2024-12-07 20:27:18','2024-12-07 20:27:18'),
('823c6e01-2d0e-4704-8308-267972284393','a699f263-3050-44cc-8738-f5002a4b9298','2025-06-13 03:20:28','182.219.9.127','Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/531.0 (KHTML, like Gecko) CriOS/23.0.822.0 Mobile/24E445 Safari/531.0',NULL,'https://richardson.com/','ce747f76-8450-4f7e-98ca-ca9820f94f63',NULL,'2025-06-13 03:20:28','2025-06-13 03:20:28'),
('83563bc4-e204-4f12-be1e-edfe3ec01c43','89356118-12d2-4fde-a7d2-2acd5603f266','2025-06-20 02:39:50','174.110.110.68','Mozilla/5.0 (Windows; U; Windows NT 4.0) AppleWebKit/532.42.6 (KHTML, like Gecko) Version/5.1 Safari/532.42.6','https://david.com/explorehomepage.html','https://moss.org/',NULL,NULL,'2025-06-20 02:39:50','2025-06-20 02:39:50'),
('85005238-374b-4448-9e88-c99a1c6f6826','349f7ae0-523f-4093-90db-9b5f13344881','2024-08-26 00:08:43',NULL,'Mozilla/5.0 (iPad; CPU iPad OS 4_2_1 like Mac OS X) AppleWebKit/533.1 (KHTML, like Gecko) FxiOS/15.7i6600.0 Mobile/49E671 Safari/533.1','http://www.barnett.com/explore/listmain.html','http://thompson.com/','54590374-efe3-4783-8bd8-9634b7242535',NULL,'2024-08-26 00:08:43','2024-08-26 00:08:43'),
('852e2a6c-22f4-4e81-9b04-10177d9f8444','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-04-04 18:37:09','112.127.0.50','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.01; Trident/3.0)','http://walker-young.com/explore/tagshomepage.php','https://www.garcia-kirk.com/','06d943bb-7993-4094-86d6-1ed490766ea6','fb3c04b0-4dc3-4f96-97be-45ab23b78013','2025-04-04 18:37:09','2025-04-04 18:37:09'),
('87699c53-ec6b-432d-9007-719505565738','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-06-08 20:46:21','35.43.30.113','Opera/8.48.(X11; Linux i686; mr-IN) Presto/2.9.187 Version/10.00',NULL,'https://www.scott.com/',NULL,'4dbdcc9c-3298-4cb4-8355-4ae07d714502','2025-06-08 20:46:21','2025-06-08 20:46:21'),
('88cd274f-6186-4416-bd15-bfaa3526c256','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-04-01 19:45:08','41.215.199.47','Opera/9.30.(X11; Linux i686; szl-PL) Presto/2.9.190 Version/11.00','https://www.lawson.biz/explore/exploreindex.jsp','http://davis.com/',NULL,NULL,'2025-04-01 19:45:08','2025-04-01 19:45:08'),
('89a6233f-b164-4951-829d-4c46144656ca','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-05-18 07:12:51','207.100.19.115','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_5; rv:1.9.3.20) Gecko/9191-02-21 17:33:29.527130 Firefox/3.8','http://www.aguilar.com/poststerms.asp','https://www.newton.com/',NULL,NULL,'2025-05-18 07:12:51','2025-05-18 07:12:51'),
('8b08e975-9fda-48eb-85b2-d3fab90889b1','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-03-20 14:18:14','9.144.53.231','Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 10.0; Trident/4.1)','https://www.davis.biz/categories/categories/listlogin.html','https://www.duncan-lester.com/',NULL,NULL,'2025-03-20 14:18:14','2025-03-20 14:18:14'),
('8cbe4642-3824-43ee-8876-82e19d15fe25','349f7ae0-523f-4093-90db-9b5f13344881','2025-06-19 06:34:06','149.68.174.217','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_8_1) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/44.0.876.0 Safari/532.1','http://johnson.com/categorysearch.htm','https://walsh.net/','6d650c30-731a-422c-b521-0399573ef44a',NULL,'2025-06-19 06:34:06','2025-06-19 06:34:06'),
('8d963bd2-bbc8-44b6-bba0-4397e33f7e8a','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-09-16 14:16:00','103.52.152.137','Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8 rv:6.0; cs-CZ) AppleWebKit/535.7.4 (KHTML, like Gecko) Version/5.1 Safari/535.7.4',NULL,'https://bell.com/',NULL,NULL,'2024-09-16 14:16:00','2024-09-16 14:16:00'),
('8e4dab1c-0c7f-4fb5-ad18-ca9de57608fe','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-06-12 04:51:37','93.233.64.127','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0)',NULL,'https://jackson.net/','84f21133-86b7-4d70-9017-51381b48b4da','6c33d6ec-d947-4427-8f48-a9c5a6562da1','2025-06-12 04:51:37','2025-06-12 04:51:37'),
('8e7cbfe3-c80a-47c9-8f2a-1407d56b6a99','89356118-12d2-4fde-a7d2-2acd5603f266','2024-07-09 06:55:57','135.149.208.216','Opera/9.61.(X11; Linux x86_64; mai-IN) Presto/2.9.161 Version/12.00','https://www.lewis.com/tagsregister.jsp','http://www.jones.biz/','3504f416-d4b3-4b1a-8f38-b1891331efeb',NULL,'2024-07-09 06:55:57','2024-07-09 06:55:57'),
('900a2f07-803c-4aa1-b7f6-fc978e9033db','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-11-25 08:16:51',NULL,'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_9) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/61.0.847.0 Safari/532.0','http://juarez.net/search/exploresearch.php','https://www.contreras.com/',NULL,NULL,'2024-11-25 08:16:51','2024-11-25 08:16:51'),
('9022b89a-e50c-4111-ae34-c34860a0757d','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-04-19 07:02:12',NULL,'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_12_5 rv:6.0; wo-SN) AppleWebKit/533.34.2 (KHTML, like Gecko) Version/4.0 Safari/533.34.2','http://watts.info/wp-content/search/taglogin.html','https://www.alexander.com/',NULL,'2c4aa9c5-0636-435d-8076-354229e8ddc0','2025-04-19 07:02:12','2025-04-19 07:02:12'),
('9530aa9b-1ea6-48a0-9da0-6df0b0748011','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-10-14 00:08:51','42.226.108.147','Mozilla/5.0 (Android 1.0; Mobile; rv:5.0) Gecko/5.0 Firefox/5.0','https://rodriguez.org/category/listcategory.html','http://www.moody.com/','0a4acaa0-d747-461f-a080-bbc165d5f4ff','ecd74681-d960-4d69-ae66-bddae90e4145','2024-10-14 00:08:51','2024-10-14 00:08:51'),
('9813c28e-8224-4071-800a-22eb227ac1af','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-08-27 12:32:52','172.96.182.120','Mozilla/5.0 (Windows 98) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/55.0.866.0 Safari/534.1','http://www.lloyd.info/appauthor.html','http://hernandez-buck.com/',NULL,NULL,'2024-08-27 12:32:52','2024-08-27 12:32:52'),
('98a0d676-fc27-4789-bf98-219beea55d73','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2024-11-08 04:54:37','165.145.104.238','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.1)',NULL,'http://www.brown-jennings.org/',NULL,NULL,'2024-11-08 04:54:37','2024-11-08 04:54:37'),
('996da8de-57e4-413e-a11c-80c5e9d01cd2','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-09-03 00:14:49','7.41.238.59','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_7 rv:5.0; kw-GB) AppleWebKit/532.25.5 (KHTML, like Gecko) Version/4.1 Safari/532.25.5','http://www.mcneil.com/app/tagindex.html','https://lester-davis.com/',NULL,NULL,'2024-09-03 00:14:49','2024-09-03 00:14:49'),
('9bc2f21a-3c39-4004-bed1-0bfd012ecc2b','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2024-10-17 06:34:06',NULL,'Mozilla/5.0 (compatible; MSIE 7.0; Windows 98; Trident/5.0)',NULL,'https://castro.com/',NULL,'23d79d6f-7083-4ca1-91b3-90646e2ec272','2024-10-17 06:34:06','2024-10-17 06:34:06'),
('9d30cb3d-5c9e-40cf-ba8c-cc535693e354','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-11-14 12:30:47','80.227.53.227','Opera/9.26.(Windows 98; niu-NZ) Presto/2.9.162 Version/10.00','http://wiggins-wilson.com/posts/blog/searchindex.html','https://hansen.info/',NULL,NULL,'2024-11-14 12:30:47','2024-11-14 12:30:47'),
('9d6835e4-0b05-4e4a-8eac-c6831adca025','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-05-05 05:01:19','210.200.16.240','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_8; rv:1.9.3.20) Gecko/2166-10-10 10:08:53.444658 Firefox/3.6.20','https://richardson-morales.com/tags/postsauthor.php','https://nichols-willis.com/','6959ffaf-35ee-4282-a60e-7fdaad4e4fc5',NULL,'2025-05-05 05:01:19','2025-05-05 05:01:19'),
('a2b48de1-d8de-4628-9fc0-dd7252739caa','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-03-08 19:04:08',NULL,'Mozilla/5.0 (Windows; U; Windows NT 10.0) AppleWebKit/535.6.3 (KHTML, like Gecko) Version/4.0.3 Safari/535.6.3',NULL,'https://www.livingston-jenkins.com/','15f162d5-2a66-4425-88a3-c5b9e71a54bb',NULL,'2025-03-08 19:04:08','2025-03-08 19:04:08'),
('a6be63a6-b6ad-4406-a499-f7dfc09e7acf','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','2025-05-01 16:35:07','66.72.11.30','Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0)',NULL,'https://www.smith.biz/',NULL,NULL,'2025-05-01 16:35:07','2025-05-01 16:35:07'),
('a7a732dc-a232-482b-9df2-aabf3352dd09','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-06-08 01:32:02','134.178.14.53','Opera/8.15.(X11; Linux i686; uk-UA) Presto/2.9.168 Version/11.00','http://martin.info/blogabout.html','http://www.fernandez-sandoval.info/',NULL,NULL,'2025-06-08 01:32:02','2025-06-08 01:32:02'),
('a7cd077e-258f-4ebf-9cfb-e86041b381d7','349f7ae0-523f-4093-90db-9b5f13344881','2024-08-20 15:18:07','109.223.50.77','Mozilla/5.0 (Windows; U; Windows 98) AppleWebKit/531.17.3 (KHTML, like Gecko) Version/4.0 Safari/531.17.3','http://www.boyer.biz/search/list/postshomepage.html','http://www.brown.biz/',NULL,NULL,'2024-08-20 15:18:07','2024-08-20 15:18:07'),
('a9190e02-d00e-4ac2-ad89-e3f462a0089e','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-08-13 02:08:19','113.9.21.71','Mozilla/5.0 (Windows; U; Windows NT 5.0) AppleWebKit/533.49.4 (KHTML, like Gecko) Version/4.0.2 Safari/533.49.4',NULL,'http://www.newton-johnson.net/',NULL,'32d23567-3ff1-4e82-a506-c9329304f92d','2024-08-13 02:08:19','2024-08-13 02:08:19'),
('a943da68-ebc6-4281-80ca-9ca818e34f20','89356118-12d2-4fde-a7d2-2acd5603f266','2025-01-22 08:47:11',NULL,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/33.0.893.0 Safari/533.2','http://arnold-bennett.net/wp-contentindex.html','https://dougherty.com/',NULL,NULL,'2025-01-22 08:47:11','2025-01-22 08:47:11'),
('aa3d49ff-5297-489b-be91-70f188a6bda1','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-01-20 12:39:31','29.18.249.47','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_3 rv:3.0; ce-RU) AppleWebKit/535.29.7 (KHTML, like Gecko) Version/4.0.5 Safari/535.29.7','http://davis-wong.com/list/tags/exploreindex.htm','https://www.james.biz/','d4e39297-6498-48bf-b31d-f6fb77ad16ac',NULL,'2025-01-20 12:39:31','2025-01-20 12:39:31'),
('aa8c4261-6112-4031-a2f1-4e84f4a01007','349f7ae0-523f-4093-90db-9b5f13344881','2024-07-28 21:45:14','146.52.177.155','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_9) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/35.0.880.0 Safari/533.2','http://sanchez.net/tagspost.html','https://thompson-scott.org/',NULL,NULL,'2024-07-28 21:45:14','2024-07-28 21:45:14'),
('ae28b724-9cc8-41fd-a8f4-42f6e70e6530','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-09-16 07:14:35','29.58.13.153','Opera/9.26.(Windows NT 6.1; shs-CA) Presto/2.9.165 Version/11.00','https://lopez.org/explore/wp-content/listterms.html','http://www.rowland-stafford.biz/',NULL,NULL,'2024-09-16 07:14:35','2024-09-16 07:14:35'),
('ae319168-e8b9-4e88-a8c1-52998a047c85','a699f263-3050-44cc-8738-f5002a4b9298','2025-03-03 20:10:38','54.186.77.66','Mozilla/5.0 (compatible; MSIE 9.0; Windows CE; Trident/4.1)','https://mills.com/exploreindex.html','https://beltran-moss.com/',NULL,NULL,'2025-03-03 20:10:38','2025-03-03 20:10:38'),
('ae9ffb69-cdd4-4de2-9050-b157720c68e1','349f7ae0-523f-4093-90db-9b5f13344881','2025-02-07 17:43:25','157.171.74.108','Opera/9.29.(X11; Linux i686; mni-IN) Presto/2.9.185 Version/12.00','http://www.reynolds-gutierrez.com/tagindex.html','http://johnson.com/',NULL,NULL,'2025-02-07 17:43:25','2025-02-07 17:43:25'),
('aecaab4f-938a-4bf1-ba10-e53a57c8fefb','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2024-12-09 05:40:02','172.79.182.140','Opera/8.99.(Windows NT 4.0; the-NP) Presto/2.9.185 Version/12.00',NULL,'http://www.huang.com/','f5fc21a4-33ea-4a75-bcee-25d0b2be765f',NULL,'2024-12-09 05:40:02','2024-12-09 05:40:02'),
('b339ab18-29a2-4619-91c4-75deccee1501','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2025-01-31 22:15:31','19.166.93.139','Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 6.2; Trident/3.0)','http://jenkins.net/blog/search/listhome.htm','https://www.robbins.com/',NULL,'17b86d91-5b11-4888-8951-c640534ffa21','2025-01-31 22:15:31','2025-01-31 22:15:31'),
('b3e4d485-0444-4380-b122-6e69f66a851f','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-01-31 11:43:28',NULL,'Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/5433-10-29 02:12:20.972794 Firefox/3.6.8',NULL,'https://mayer-branch.org/',NULL,NULL,'2025-01-31 11:43:28','2025-01-31 11:43:28'),
('b6576734-8556-4712-a9d0-65b7345a1504','89356118-12d2-4fde-a7d2-2acd5603f266','2025-05-29 03:26:08','77.56.240.116','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4 rv:2.0; zu-ZA) AppleWebKit/532.11.4 (KHTML, like Gecko) Version/5.0.3 Safari/532.11.4','https://www.sanders-valencia.com/tags/wp-contentlogin.htm','http://gutierrez.info/',NULL,NULL,'2025-05-29 03:26:08','2025-05-29 03:26:08'),
('b719e388-cf39-4cd0-b94a-95be52b26aaa','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-08-21 11:38:32','3.205.141.161','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/52.0.816.0 Safari/532.1','http://jones.com/search/searchregister.php','https://www.moore.com/',NULL,NULL,'2024-08-21 11:38:32','2024-08-21 11:38:32'),
('b885a5d2-ec5c-4ec7-a69a-df1005b74428','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-01-04 14:20:57','43.253.74.137','Mozilla/5.0 (Windows NT 5.0; kw-GB; rv:1.9.2.20) Gecko/3312-08-24 23:35:31.625008 Firefox/15.0',NULL,'http://www.hunter-doyle.info/',NULL,NULL,'2025-01-04 14:20:57','2025-01-04 14:20:57'),
('bb18e954-32f7-4343-8fdd-72a3dd433f45','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-10-13 09:11:48','189.189.133.46','Mozilla/5.0 (Linux; Android 3.0) AppleWebKit/534.2 (KHTML, like Gecko) Chrome/45.0.810.0 Safari/534.2',NULL,'http://www.kent.net/',NULL,NULL,'2024-10-13 09:11:48','2024-10-13 09:11:48'),
('bb2fda40-1321-41b0-9b44-b97e4b05f0bb','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2025-01-09 11:43:59','107.103.104.90','Opera/8.38.(X11; Linux x86_64; mk-MK) Presto/2.9.183 Version/12.00',NULL,'https://www.campbell.com/',NULL,'9885e5a0-e0e7-4b0d-8e42-6f26e9a26b5d','2025-01-09 11:43:59','2025-01-09 11:43:59'),
('bf4cff2a-90d6-4d65-93cb-e0f99a6464cb','d2ee5d26-5b68-43ec-a93f-e742145192fc','2024-12-18 09:21:14','93.154.4.1','Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/534.23.2 (KHTML, like Gecko) Version/5.0.2 Safari/534.23.2','https://sanchez.net/tags/list/postsabout.htm','http://www.smith-whitaker.com/',NULL,NULL,'2024-12-18 09:21:14','2024-12-18 09:21:14'),
('c010cdb0-5855-4394-9787-26e2d6669f5d','89356118-12d2-4fde-a7d2-2acd5603f266','2025-03-24 16:17:12','98.226.143.169','Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/9655-11-11 23:37:02.466095 Firefox/4.0','https://henderson-gomez.info/categories/tag/wp-contentindex.php','https://hart-mcclain.com/',NULL,NULL,'2025-03-24 16:17:12','2025-03-24 16:17:12'),
('c06d0c93-f26d-49ed-841c-dd40c5410acf','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-05-01 04:36:06','110.150.8.21','Mozilla/5.0 (iPad; CPU iPad OS 1_1_5 like Mac OS X) AppleWebKit/536.2 (KHTML, like Gecko) CriOS/42.0.829.0 Mobile/40V195 Safari/536.2','http://skinner-mullins.com/wp-contentauthor.php','http://harris.com/',NULL,NULL,'2025-05-01 04:36:06','2025-05-01 04:36:06'),
('c3e7a0a6-3f54-40ed-b31f-0d9a0e9561c7','89356118-12d2-4fde-a7d2-2acd5603f266','2025-01-01 19:55:00','136.255.176.123','Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/535.39.7 (KHTML, like Gecko) Version/5.0 Safari/535.39.7','https://smith.com/main/appsearch.php','http://collins-wilson.com/',NULL,NULL,'2025-01-01 19:55:00','2025-01-01 19:55:00'),
('c80fcd32-d006-48d4-a2b7-9bbdace74323','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-06-30 06:31:40','223.141.226.191','Mozilla/5.0 (iPod; U; CPU iPhone OS 3_0 like Mac OS X; kn-IN) AppleWebKit/533.16.2 (KHTML, like Gecko) Version/4.0.5 Mobile/8B111 Safari/6533.16.2',NULL,'https://www.martin.com/',NULL,NULL,'2024-06-30 06:31:40','2024-06-30 06:31:40'),
('caea2d80-9171-4f2e-95f6-4d57b4c9066f','89356118-12d2-4fde-a7d2-2acd5603f266','2024-11-26 11:01:29','6.40.14.34','Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/5.1)',NULL,'http://www.montes-mays.com/',NULL,NULL,'2024-11-26 11:01:29','2024-11-26 11:01:29'),
('cb17a26f-2131-46b4-8e59-a202a1886fca','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-07-13 20:22:51','131.124.38.183','Mozilla/5.0 (iPad; CPU iPad OS 14_2 like Mac OS X) AppleWebKit/531.0 (KHTML, like Gecko) FxiOS/16.8y2538.0 Mobile/97H392 Safari/531.0','http://www.medina.org/tagpost.jsp','https://williams.com/',NULL,NULL,'2024-07-13 20:22:51','2024-07-13 20:22:51'),
('cb54e420-ca6d-4fc2-8f0a-007e92c27985','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-08-05 08:02:12','129.90.7.255','Mozilla/5.0 (X11; Linux x86_64; rv:1.9.6.20) Gecko/6870-03-22 06:55:52.592987 Firefox/3.8',NULL,'http://www.lopez.net/',NULL,NULL,'2024-08-05 08:02:12','2024-08-05 08:02:12'),
('cc75e63e-5e9d-4bdf-b311-2607c2239f37','8bda9505-912a-4356-ade5-22a8f9484ab9','2024-08-02 14:36:40','134.191.173.2','Mozilla/5.0 (Linux; Android 4.4) AppleWebKit/534.2 (KHTML, like Gecko) Chrome/15.0.808.0 Safari/534.2',NULL,'http://baker.com/',NULL,NULL,'2024-08-02 14:36:40','2024-08-02 14:36:40'),
('cd397830-a817-4492-b430-5f2eb13ba8ca','349f7ae0-523f-4093-90db-9b5f13344881','2025-04-25 22:58:07','63.194.62.104','Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/532.1 (KHTML, like Gecko) CriOS/31.0.848.0 Mobile/01M475 Safari/532.1','https://thompson-brown.com/tagsregister.html','http://www.watts-thompson.com/',NULL,NULL,'2025-04-25 22:58:07','2025-04-25 22:58:07'),
('d0825075-0eab-4433-a335-bc683191986a','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-08-17 14:32:33','27.213.51.82','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_9_7) AppleWebKit/533.1 (KHTML, like Gecko) Chrome/41.0.868.0 Safari/533.1',NULL,'http://www.schmidt.com/','2e0ba226-1870-43be-8da0-19b4a43f4976','244ccd32-d50d-4831-be0f-b9994c4b1f4a','2024-08-17 14:32:33','2024-08-17 14:32:33'),
('d0e712d0-57fa-477c-b1a4-213fde255250','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-06-21 19:52:20','34.68.47.186','Mozilla/5.0 (iPod; U; CPU iPhone OS 3_2 like Mac OS X; ce-RU) AppleWebKit/534.17.3 (KHTML, like Gecko) Version/4.0.5 Mobile/8B115 Safari/6534.17.3',NULL,'https://bennett.info/','94d9e18d-7701-4cd0-9697-0fb0dc6ce8b3',NULL,'2025-06-21 19:52:20','2025-06-21 19:52:20'),
('d249b8fe-f332-4d01-998b-347986504d44','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-05-20 13:14:55',NULL,'Opera/8.90.(X11; Linux x86_64; nan-TW) Presto/2.9.163 Version/11.00',NULL,'http://brooks-gallagher.com/',NULL,NULL,'2025-05-20 13:14:55','2025-05-20 13:14:55'),
('d64a994d-f9f7-4a27-a566-191c0fc7d88f','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-10-20 19:20:33',NULL,'Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/532.7.4 (KHTML, like Gecko) Version/4.0.3 Safari/532.7.4','http://allen.com/listindex.html','http://wright.com/','7fc9db96-fee0-492b-bae7-d942ba602fa3','8d85daa1-1507-41e2-a0a8-7475f77c37d6','2024-10-20 19:20:33','2024-10-20 19:20:33'),
('d6ce9ff0-b0a7-4ddc-b67b-2da79b9065c6','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-11-25 01:16:17',NULL,'Mozilla/5.0 (compatible; MSIE 9.0; Windows 98; Trident/4.1)',NULL,'http://daniel-cuevas.net/',NULL,NULL,'2024-11-25 01:16:17','2024-11-25 01:16:17'),
('d8271033-2794-41fd-938d-d5554f1cfd9f','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-12-22 02:10:13','157.246.198.74','Mozilla/5.0 (Macintosh; PPC Mac OS X 10_6_4 rv:5.0; os-RU) AppleWebKit/533.28.3 (KHTML, like Gecko) Version/5.0 Safari/533.28.3','http://www.richardson.com/posts/main/wp-contentpost.php','http://www.davies.info/',NULL,NULL,'2024-12-22 02:10:13','2024-12-22 02:10:13'),
('d87e6972-d2fc-4ffc-81f6-87b6be4775ee','349f7ae0-523f-4093-90db-9b5f13344881','2024-11-02 18:38:10','178.107.9.51','Mozilla/5.0 (Windows NT 4.0) AppleWebKit/536.0 (KHTML, like Gecko) Chrome/47.0.840.0 Safari/536.0',NULL,'https://vaughn-smith.net/','4db28ebd-40f0-4ca1-9af1-6d6709b1dcbd','cf1142c7-42ee-4657-a3de-dca98c641862','2024-11-02 18:38:10','2024-11-02 18:38:10'),
('d9c8a26a-1d30-417b-b85d-0396e263a6d3','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-06-17 22:22:44','29.228.227.144','Mozilla/5.0 (compatible; MSIE 9.0; Windows 98; Trident/3.1)','http://www.martinez.com/search/posts/mainfaq.html','http://www.lopez-acevedo.org/',NULL,NULL,'2025-06-17 22:22:44','2025-06-17 22:22:44'),
('d9f5b4dd-7b99-4f53-819b-605bdc0e837d','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2025-01-19 21:39:12','55.25.61.86','Mozilla/5.0 (compatible; MSIE 6.0; Windows 95; Trident/5.1)',NULL,'https://phillips.com/',NULL,'287fbe43-195e-41ed-8b9c-18dbefbeaca8','2025-01-19 21:39:12','2025-01-19 21:39:12'),
('dcd6b171-2fb7-4895-88f6-bcf5b3764744','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-03-15 04:52:52','166.165.146.252','Mozilla/5.0 (iPad; CPU iPad OS 17_2_1 like Mac OS X) AppleWebKit/533.1 (KHTML, like Gecko) CriOS/51.0.877.0 Mobile/35C469 Safari/533.1','http://www.garcia.com/postsauthor.php','http://flores.com/','ce2974ff-4e69-424f-908e-a0740995e09e',NULL,'2025-03-15 04:52:52','2025-03-15 04:52:52'),
('dd831b4b-495a-4fb3-9635-f59f2e640681','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-01-25 11:20:32','76.203.108.22','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 11.0; Trident/4.0)','https://www.barr.net/blogcategory.asp','http://lewis.com/','7b9ee2ae-6d62-4711-a336-2f47aa8bacf1',NULL,'2025-01-25 11:20:32','2025-01-25 11:20:32'),
('dde28dd7-a742-4649-90f7-ab54a4e0b4fc','a699f263-3050-44cc-8738-f5002a4b9298','2025-06-23 17:49:58','26.99.155.56','Mozilla/5.0 (Linux; Android 6.0.1) AppleWebKit/535.0 (KHTML, like Gecko) Chrome/45.0.832.0 Safari/535.0','https://reed-jackson.com/postspost.php','http://www.navarro.com/','366d13d7-76bc-4e72-ada6-57a005b57305','3f379805-e2b9-4edb-ab83-ae91039e1da3','2025-06-23 17:49:58','2025-06-23 17:49:58'),
('de0c8b1f-1b80-4ece-bc96-37f89dbb823c','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2025-04-13 21:44:08',NULL,'Opera/8.21.(X11; Linux i686; sk-SK) Presto/2.9.166 Version/12.00','https://www.williams-jacobson.biz/posts/postscategory.html','https://marshall-jones.org/',NULL,'af0f3931-5e59-4f1f-b7de-de95178e5417','2025-04-13 21:44:08','2025-04-13 21:44:08'),
('de8aed39-e772-4c56-b8ab-aa8ac360aaac','89356118-12d2-4fde-a7d2-2acd5603f266','2025-06-09 03:23:08','3.154.174.160','Mozilla/5.0 (Windows 98; Win 9x 4.90; sc-IT; rv:1.9.0.20) Gecko/2200-06-14 02:09:17.289942 Firefox/3.6.13','https://www.lang-sanchez.com/explorehome.html','http://daniel.com/',NULL,NULL,'2025-06-09 03:23:08','2025-06-09 03:23:08'),
('deb1da69-7d73-49ef-a57f-5c2f0c5da264','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-03-30 12:00:44','137.196.216.96','Mozilla/5.0 (Macintosh; PPC Mac OS X 10_8_1; rv:1.9.5.20) Gecko/4549-07-07 11:02:13.476807 Firefox/3.8',NULL,'https://woodard.com/',NULL,NULL,'2025-03-30 12:00:44','2025-03-30 12:00:44'),
('deb49878-3540-46b9-9139-39065290a2e6','a699f263-3050-44cc-8738-f5002a4b9298','2024-09-21 10:40:25',NULL,'Opera/8.71.(Windows NT 4.0; ak-GH) Presto/2.9.190 Version/11.00','http://www.peterson-harrison.com/category/postsabout.jsp','http://www.potts-richmond.com/',NULL,'da55ab7f-344f-46d0-97af-c508b79018a4','2024-09-21 10:40:25','2024-09-21 10:40:25'),
('e07f71df-1927-4c2d-acc9-67af691d0ac3','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-05-06 21:25:29','102.113.6.150','Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_12_6) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/53.0.840.0 Safari/532.0',NULL,'https://griffin.info/',NULL,NULL,'2025-05-06 21:25:29','2025-05-06 21:25:29'),
('e3a9383a-0163-4679-b133-1267ca246cee','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-08-01 20:57:53','125.205.232.189','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/45.0.861.0 Safari/532.0',NULL,'http://thomas-hammond.org/',NULL,NULL,'2024-08-01 20:57:53','2024-08-01 20:57:53'),
('e4f4114c-380b-4cd5-a790-1daa00144568','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-10-15 17:19:04',NULL,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8; rv:1.9.2.20) Gecko/7570-05-06 13:09:20.497345 Firefox/3.8','https://www.jackson.com/app/category/exploremain.php','http://smith-taylor.com/',NULL,NULL,'2024-10-15 17:19:04','2024-10-15 17:19:04'),
('e515cd45-b972-4a2e-9c26-e07841fb5075','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','2024-12-19 22:39:21',NULL,'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; fur-IT) AppleWebKit/534.8.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B118 Safari/6534.8.4','http://www.ingram-washington.com/blog/app/listfaq.html','https://anderson.com/',NULL,NULL,'2024-12-19 22:39:21','2024-12-19 22:39:21'),
('e5c509a5-4ce8-4582-b7ac-b92113fda44c','89356118-12d2-4fde-a7d2-2acd5603f266','2024-08-16 19:26:40',NULL,'Opera/9.87.(Windows NT 6.2; te-IN) Presto/2.9.166 Version/11.00','http://martin.com/tags/posts/searchcategory.php','https://www.gordon.net/',NULL,NULL,'2024-08-16 19:26:40','2024-08-16 19:26:40'),
('e677c6f0-b69e-470a-8421-f366041d7c0c','a699f263-3050-44cc-8738-f5002a4b9298','2025-01-18 01:48:55','136.110.175.254','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_9_3) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/43.0.892.0 Safari/532.0',NULL,'http://gomez.com/',NULL,NULL,'2025-01-18 01:48:55','2025-01-18 01:48:55'),
('e867c413-19ec-4c73-8d26-d861427afb85','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-09-08 23:28:34','41.143.4.19','Mozilla/5.0 (Windows NT 6.1; my-MM; rv:1.9.2.20) Gecko/2533-01-26 01:20:05.650146 Firefox/3.8','https://www.diaz.com/category/wp-content/mainregister.php','http://www.burns.net/',NULL,NULL,'2024-09-08 23:28:34','2024-09-08 23:28:34'),
('e927252a-4f9f-46b7-9c9f-3a4b2ec2aaaa','a699f263-3050-44cc-8738-f5002a4b9298','2024-11-21 07:15:58','62.21.73.236','Mozilla/5.0 (X11; Linux x86_64; rv:1.9.5.20) Gecko/8403-05-03 03:11:30.533508 Firefox/12.0','http://miller.com/categories/categorylogin.asp','http://www.garcia.com/',NULL,NULL,'2024-11-21 07:15:58','2024-11-21 07:15:58'),
('ea6ed361-f7a8-4480-8ae6-43af8d9252cd','09abb310-89ee-49aa-b2be-daf234e8efc7','2025-03-07 23:46:04',NULL,'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.1)',NULL,'https://www.cole-melton.org/',NULL,NULL,'2025-03-07 23:46:04','2025-03-07 23:46:04'),
('eb8f7d34-ca09-4d4c-9015-64c3e0ba73cd','8bda9505-912a-4356-ade5-22a8f9484ab9','2025-04-10 15:10:11','105.213.9.102','Mozilla/5.0 (X11; Linux i686; rv:1.9.6.20) Gecko/5468-09-28 15:22:33.110535 Firefox/13.0','https://www.hoffman.biz/category/listcategory.php','http://www.cox-lee.com/',NULL,NULL,'2025-04-10 15:10:11','2025-04-10 15:10:11'),
('ec72d4da-1ec8-4d6b-854d-9e29a5d2217d','d2ee5d26-5b68-43ec-a93f-e742145192fc','2024-12-19 19:40:56','148.39.33.171','Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3 like Mac OS X; sr-RS) AppleWebKit/535.29.7 (KHTML, like Gecko) Version/4.0.5 Mobile/8B118 Safari/6535.29.7','http://www.moss-bishop.info/categories/main/taghome.htm','http://www.sims.info/','ea0ef849-57f2-4b29-8782-420836693980','4aa8fb8d-1ccf-4012-aa69-2b7a8bf3424a','2024-12-19 19:40:56','2024-12-19 19:40:56'),
('edb1123c-3531-4636-9ad1-57f979ea6a1f','a699f263-3050-44cc-8738-f5002a4b9298','2024-12-01 14:06:11','38.134.162.245','Mozilla/5.0 (iPod; U; CPU iPhone OS 3_2 like Mac OS X; hak-TW) AppleWebKit/533.37.7 (KHTML, like Gecko) Version/4.0.5 Mobile/8B118 Safari/6533.37.7','http://www.dean.org/search/searchterms.htm','http://www.miller.com/',NULL,NULL,'2024-12-01 14:06:11','2024-12-01 14:06:11'),
('ede0b061-983b-477f-809c-b881021ecb82','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-10-24 07:53:36','117.103.109.221','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_0 rv:5.0; sk-SK) AppleWebKit/533.37.2 (KHTML, like Gecko) Version/5.0 Safari/533.37.2',NULL,'http://www.ramirez.info/','435f8a03-75ee-4cbe-8361-60feb77b031e','e76eca8b-1170-48ad-b6f7-299d452aab3e','2024-10-24 07:53:36','2024-10-24 07:53:36'),
('ee48109b-87c3-46cd-93d1-c301b958a535','09abb310-89ee-49aa-b2be-daf234e8efc7','2024-12-12 02:36:58',NULL,'Mozilla/5.0 (compatible; MSIE 5.0; Windows 98; Trident/3.1)','http://www.anderson.com/searchregister.html','https://www.valdez.com/',NULL,'e78cd3d4-283b-4c15-b9ee-15529bfd9f2c','2024-12-12 02:36:58','2024-12-12 02:36:58'),
('ee814089-60a6-4cce-88a8-293735891ebb','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','2024-11-17 17:27:51','38.111.111.165','Opera/8.47.(Windows 98; gez-ET) Presto/2.9.170 Version/12.00','https://www.white-ellis.com/appabout.htm','https://www.skinner.net/',NULL,NULL,'2024-11-17 17:27:51','2024-11-17 17:27:51'),
('f12a284e-2c84-4038-9317-f83cc5112ce4','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2025-04-08 10:30:48',NULL,'Mozilla/5.0 (Windows NT 5.1; om-KE; rv:1.9.2.20) Gecko/2404-03-15 11:51:22.991467 Firefox/6.0','http://www.strickland-mcdaniel.com/category/main/wp-contentauthor.html','https://www.buchanan.com/',NULL,NULL,'2025-04-08 10:30:48','2025-04-08 10:30:48'),
('f228619a-75a8-41bf-a305-ce2c0edf14de','d2ee5d26-5b68-43ec-a93f-e742145192fc','2025-05-27 13:04:27',NULL,'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 11.0; Trident/5.1)','https://dunlap.info/categories/categoryauthor.html','https://www.harvey-may.info/',NULL,NULL,'2025-05-27 13:04:27','2025-05-27 13:04:27'),
('f4c5baef-87ee-4054-a15a-4d4b72c0f243','349f7ae0-523f-4093-90db-9b5f13344881','2024-07-15 17:08:58',NULL,'Opera/8.32.(Windows CE; st-ZA) Presto/2.9.188 Version/11.00','https://www.ramirez.com/posts/tag/apppost.php','https://www.cohen.com/','1708ec47-9bf0-4928-bddc-9a835d6530cc',NULL,'2024-07-15 17:08:58','2024-07-15 17:08:58'),
('f4cd4023-98e7-4a12-9f68-9d94757122db','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','2024-09-11 12:27:50','67.200.1.149','Mozilla/5.0 (iPad; CPU iPad OS 7_1_2 like Mac OS X) AppleWebKit/532.0 (KHTML, like Gecko) FxiOS/17.7z0630.0 Mobile/50X234 Safari/532.0','http://thomas.com/app/app/wp-contenthome.asp','https://www.baxter.com/','ac923dfe-2789-4956-84b8-5201c3413a77',NULL,'2024-09-11 12:27:50','2024-09-11 12:27:50'),
('fa587328-e814-4304-8e8d-6f5668e939df','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2024-09-07 03:18:02',NULL,'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)','https://www.young.com/main/blog/categoryabout.html','http://www.rios.com/','ea938e6b-7917-4876-8fb9-985417e4fdfb','defe149c-8e74-4a4d-adef-a7f91399a193','2024-09-07 03:18:02','2024-09-07 03:18:02'),
('fab16c7f-0f60-49fe-ad0b-c9e813610013','a699f263-3050-44cc-8738-f5002a4b9298','2024-10-05 03:29:22','138.186.118.211','Mozilla/5.0 (iPod; U; CPU iPhone OS 3_2 like Mac OS X; yo-NG) AppleWebKit/535.6.1 (KHTML, like Gecko) Version/3.0.5 Mobile/8B118 Safari/6535.6.1','http://serrano.org/searchcategory.html','http://avery-huang.com/',NULL,NULL,'2024-10-05 03:29:22','2024-10-05 03:29:22'),
('fcaf00ad-29ec-4d28-bbfe-d190908de240','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','2025-03-13 13:47:28','116.61.222.46','Mozilla/5.0 (X11; Linux i686) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/34.0.873.0 Safari/533.2',NULL,'https://www.vargas.org/',NULL,'e37eb27f-5688-4bbc-990e-fe622ba67ab2','2025-03-13 13:47:28','2025-03-13 13:47:28');
/*!40000 ALTER TABLE `affiliate_clicks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affiliate_commissions`
--

DROP TABLE IF EXISTS `affiliate_commissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `affiliate_commissions` (
  `id` varchar(36) NOT NULL,
  `affiliate_id` varchar(36) NOT NULL,
  `referred_sale_id` varchar(36) DEFAULT NULL,
  `referred_sale_value` float NOT NULL,
  `commission_amount` float NOT NULL,
  `commission_date` datetime NOT NULL,
  `is_paid` tinyint(1) NOT NULL,
  `paid_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `referred_sale_id` (`referred_sale_id`),
  KEY `affiliate_id` (`affiliate_id`),
  CONSTRAINT `affiliate_commissions_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliates` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliate_commissions`
--

LOCK TABLES `affiliate_commissions` WRITE;
/*!40000 ALTER TABLE `affiliate_commissions` DISABLE KEYS */;
INSERT INTO `affiliate_commissions` VALUES
('064ae5e6-1593-4e09-a6d2-6fb97bfa8bf5','1335e209-b7be-49c5-8b1e-b7155ccda3c8','95fbfc77-ce25-42f0-ae9b-3bd727183f71',58.82,5.22,'2024-10-28 23:46:14',1,'2025-04-01 03:17:12'),
('107b7896-f69c-4269-9ee1-33122b2d1a7d','db6d0f7a-a503-42b7-958e-7681c7d24a26','0589a651-4433-4d7e-992d-52ddb3c9359c',220.56,42.53,'2024-08-28 22:32:01',1,NULL),
('118df019-8ceb-4dfa-8729-eff27e6ccf01','13c0546d-c9c3-47a5-a285-3109fa4f6722','7531a340-4b9f-4e31-a986-a43ba0c5d094',562.62,34.2,'2025-05-08 18:07:10',1,'2025-05-22 21:47:42'),
('13f30819-9ba6-4c5f-96dc-f343270d6e6b','7901dc0e-8ce4-481d-92c1-fc3bc5302276','2cba59cb-9bb4-4d78-ae62-2ba7db09f044',147.23,23.99,'2025-06-25 20:35:15',1,'2025-06-26 12:12:24'),
('1d33abf3-aba3-472c-9073-1279b2442abe','f831e60d-77d0-40f6-8e9b-92f24ea33a03','8699ca41-0203-456c-bb77-7a7879c54e4e',339.03,52.6,'2024-12-28 03:04:23',1,'2025-05-14 12:36:01'),
('240aefb0-cbbd-4056-963f-3e13da2ec545','c4bc375c-f897-4366-bd32-2415996e5169','ce0496b1-fa93-4e5f-8961-41e8a6aad213',810.78,110.12,'2024-07-29 01:44:29',1,'2025-04-22 16:45:32'),
('240c414a-9dd0-428a-b0c1-883e7e14c455','00a047b0-e4e2-4e1c-a765-76607f8be268','8ce74140-fb53-47eb-8c67-f83593809238',725.19,76.74,'2025-03-07 20:47:56',0,'2025-03-19 01:14:03'),
('29e6b534-85fe-490f-804d-3f53d832f700','15aad7b3-1a6f-4ba2-8318-968042be2fe8',NULL,389.42,72.45,'2025-03-16 12:36:27',0,NULL),
('2c3cc6bf-b274-4a84-b173-da9945a8a88c','00a047b0-e4e2-4e1c-a765-76607f8be268','f569f705-ec80-469a-837f-322b5852b767',407.86,43.16,'2024-08-06 14:08:05',1,'2025-01-27 22:35:15'),
('2fcf48fd-5cc5-4950-bb74-b6d40edc70d8','b1d66e0a-2d08-486a-9642-578268d06ac4','9d65dac6-9a45-4a1f-bf02-ff67635d81b7',828.4,145.76,'2025-03-08 14:10:14',1,'2025-03-21 05:54:25'),
('3e5c3174-fdd3-43e8-8e5d-4d8f0535118b','463c2dae-b050-4f5b-942a-3842ed514dbe',NULL,559.69,83.88,'2025-04-22 15:32:20',1,'2025-05-01 09:03:15'),
('3ed5c36e-21e2-4862-9430-02c672a30e8c','1335e209-b7be-49c5-8b1e-b7155ccda3c8','ecd5fbc5-253c-44f8-842c-300ec1871257',23.03,2.04,'2024-12-08 16:36:13',1,'2025-03-10 13:28:34'),
('3f132519-c430-4ea1-9ccf-645d17cd19d1','db6d0f7a-a503-42b7-958e-7681c7d24a26','a5986f53-991d-4291-b06b-78fc3569b28c',446.47,86.1,'2024-12-16 09:34:37',1,'2025-06-20 01:55:38'),
('4d05acea-7386-4849-907b-1cd6d253bd30','463c2dae-b050-4f5b-942a-3842ed514dbe','0ac1dbfa-1819-46c9-bff0-4501f3163ecf',987.46,147.99,'2024-09-21 15:56:52',1,NULL),
('52fe9562-6a11-4bdd-9cfd-6bb19016a5f4','15aad7b3-1a6f-4ba2-8318-968042be2fe8',NULL,57.94,10.78,'2025-06-11 12:01:21',1,'2025-06-15 03:29:01'),
('54c18de2-8930-4b09-bce2-4e0c0aa157f7','1335e209-b7be-49c5-8b1e-b7155ccda3c8',NULL,568.25,50.41,'2024-10-06 08:36:22',1,'2025-06-18 01:47:08'),
('56e80784-1bab-49c0-af74-b4408f46daaa','b18ee6b6-3348-4e7d-8978-9974e552d26f','91ea3dd7-aaad-471a-80d9-4b2086b64f19',330.14,19.55,'2025-06-19 15:06:43',1,'2025-06-20 17:02:00'),
('57a4ed4a-bb14-413d-9db8-fcb7db2fd61a','db6d0f7a-a503-42b7-958e-7681c7d24a26',NULL,418.93,80.78,'2025-02-23 23:04:53',1,NULL),
('5b9a3e08-a70e-4ee2-9466-87f51feeaf35','13c0546d-c9c3-47a5-a285-3109fa4f6722','18a1176e-095a-46b8-bf80-7060deb9a99c',565.26,34.36,'2025-04-05 15:50:53',0,'2025-05-02 06:37:52'),
('619ff438-da32-41e0-926c-438086d960d7','13c0546d-c9c3-47a5-a285-3109fa4f6722','65e49468-16d7-49d8-856a-73e7def9e6f6',473.36,28.77,'2024-08-21 04:27:51',0,'2025-01-28 05:27:11'),
('64faeeb5-6c93-4c44-9975-65de375d8574','15aad7b3-1a6f-4ba2-8318-968042be2fe8','f9afea0a-e860-4f38-807b-5dc0c40944ab',986.11,183.46,'2025-01-05 22:24:43',1,'2025-04-07 00:10:16'),
('65a90940-60ff-4501-80bd-9b72629aee55','b8d9ac53-e4fe-4d70-9698-fa5ca3d2e157','fd3f012c-a31b-4f43-9325-0e27fc2b644d',268.42,14.83,'2025-06-01 03:48:36',1,'2025-06-07 15:23:02'),
('6ca686a9-df35-48a9-8613-896aa26d6bd3','b1d66e0a-2d08-486a-9642-578268d06ac4','b6adf508-c2eb-4b09-963f-23de2dd17119',29.74,5.23,'2025-02-20 08:43:51',0,'2025-06-03 20:12:38'),
('6fae7f5a-acf1-435a-b210-23ba07d11200','13c0546d-c9c3-47a5-a285-3109fa4f6722',NULL,656.68,39.92,'2024-11-30 17:27:27',1,'2025-02-21 08:34:21'),
('74a78f9f-4af2-4871-afc1-aeacde094f32','7901dc0e-8ce4-481d-92c1-fc3bc5302276','beb2932c-0522-49ae-8ea2-5df525ec3bfd',224.13,36.51,'2025-06-24 04:17:39',1,NULL),
('7a3c1d6d-11b4-4b08-8ca8-7507b7b52599','463c2dae-b050-4f5b-942a-3842ed514dbe','af0b98fc-8228-40bb-abe4-e75df7ef9ddf',667.22,100,'2025-04-01 00:39:40',0,'2025-04-27 02:10:54'),
('7d4dcf0a-50da-45e6-8285-65cecd1bd15d','b18ee6b6-3348-4e7d-8978-9974e552d26f','836942d5-d0bc-4897-bca3-8f80635b937d',18.05,1.07,'2025-04-16 20:12:36',1,NULL),
('7e04b597-5a8d-4bd1-86b3-c14ff30f321a','1335e209-b7be-49c5-8b1e-b7155ccda3c8','340cb0cf-59c0-4195-a033-917c5556cede',715.08,63.44,'2024-12-17 00:57:07',0,NULL),
('7fc950ba-d733-4532-9102-76355669612f','bcd819f0-63e0-4f6d-8f73-604e5a04d027','678ec266-7635-4145-8c72-66b4358584b7',847.57,138.48,'2024-10-08 05:52:13',1,'2025-05-10 19:53:25'),
('98f4514e-19ce-4d0b-8178-a80803e1b827','db6d0f7a-a503-42b7-958e-7681c7d24a26','905993af-3358-47af-8723-255731f26970',674.1,129.99,'2024-12-30 15:23:12',1,'2025-03-31 12:47:40'),
('9cf94e7e-3e1c-426e-9c71-f8449b26f553','db6d0f7a-a503-42b7-958e-7681c7d24a26','2acbc05c-bc34-4be8-b545-815b8c2a9246',734.52,141.64,'2024-08-19 20:50:09',0,NULL),
('9db75f46-e73e-4751-85b5-1dd11cf986cd','b1d66e0a-2d08-486a-9642-578268d06ac4',NULL,783.44,137.85,'2024-06-29 12:45:50',1,NULL),
('9f6f42ef-dd8e-4492-b93a-1ccd3606ead2','463c2dae-b050-4f5b-942a-3842ed514dbe','b1ecc06a-15ba-4c9b-aa02-dfe3b47174b7',187.87,28.16,'2025-02-24 20:16:52',1,'2025-04-08 19:22:58'),
('a609a545-db21-4f6f-a2dc-4cee9a290832','c4bc375c-f897-4366-bd32-2415996e5169','3904acb4-abbd-44c7-bc94-6ff57007b111',59.27,8.05,'2024-10-30 22:26:52',0,'2024-11-24 17:30:15'),
('b36a06d7-c9e0-4a99-9670-345e4eb1ebd1','b8d9ac53-e4fe-4d70-9698-fa5ca3d2e157','a6b5eabf-acf6-4168-947f-791f57e45abf',73.79,4.08,'2024-09-02 16:22:21',0,'2024-12-24 01:19:25'),
('b5d1c9b9-1f99-4158-bd15-98927cb2e98b','1335e209-b7be-49c5-8b1e-b7155ccda3c8','7c619c1c-c7ae-4aba-bf3a-2c9b5faa61f6',57.74,5.12,'2024-12-06 08:10:48',1,'2025-01-14 03:50:52'),
('b5d4bd1b-107b-4fbc-be5d-38bb7239a059','00a047b0-e4e2-4e1c-a765-76607f8be268',NULL,726.57,76.88,'2024-09-02 05:27:17',1,'2025-02-26 12:37:52'),
('b7289330-412e-4791-9414-e5721841aeb4','db6d0f7a-a503-42b7-958e-7681c7d24a26',NULL,345.07,66.54,'2024-11-17 13:13:27',1,'2025-03-14 16:17:09'),
('c64504a7-467a-4079-8b3a-fa8d5c3d6998','c4bc375c-f897-4366-bd32-2415996e5169',NULL,750.91,101.99,'2025-03-29 15:16:08',1,'2025-04-24 08:16:31'),
('c75a8032-83e9-476a-a08d-eaa1dc803b57','1335e209-b7be-49c5-8b1e-b7155ccda3c8','ace42141-1a76-48cb-9f09-e8768677a5cd',987.22,87.58,'2025-06-20 06:04:53',0,'2025-06-27 00:09:20'),
('c8a91c22-ed8d-42d8-9198-2f7206555e79','15aad7b3-1a6f-4ba2-8318-968042be2fe8','bf17e1a9-6f7b-48dd-bbbd-88ae76a7c8f1',738.93,137.47,'2024-12-16 23:39:58',1,'2025-01-23 13:23:21'),
('d451315f-dc90-4905-a3cf-039c4a26ccdf','7901dc0e-8ce4-481d-92c1-fc3bc5302276',NULL,121.08,19.73,'2025-01-22 02:22:20',1,NULL),
('d6ec4d15-c9cb-41fc-8e86-d14f80b582b1','bcd819f0-63e0-4f6d-8f73-604e5a04d027',NULL,279.41,45.65,'2025-03-08 08:45:38',1,'2025-05-29 06:53:35'),
('dcbcf36b-aa81-4caf-b091-0c02aee26446','b8d9ac53-e4fe-4d70-9698-fa5ca3d2e157',NULL,198.87,10.98,'2025-01-19 23:56:32',1,'2025-02-20 16:59:08'),
('e14fef59-0c44-4222-8a72-11a0b5dd7168','db6d0f7a-a503-42b7-958e-7681c7d24a26','ad1deb6e-32fe-4bce-802e-736f585d4392',963.45,185.79,'2024-08-03 13:55:17',1,'2025-04-11 10:28:49'),
('e3133780-c2f7-4fba-804d-008b39eb2820','f831e60d-77d0-40f6-8e9b-92f24ea33a03','c136d02f-f5ea-46fd-baa6-6abc2e56f892',670.63,104.05,'2024-11-08 09:47:00',1,'2024-12-05 14:00:25'),
('e3a6c4f4-0612-4dab-8a20-2226f8cdc413','bcd819f0-63e0-4f6d-8f73-604e5a04d027','fc09cfe3-971f-4732-a437-f149d8d0a330',934.51,152.69,'2025-03-07 23:48:01',1,'2025-06-06 03:35:29'),
('ef6c4d8c-587a-42c5-9a7b-150cf3e611b8','7901dc0e-8ce4-481d-92c1-fc3bc5302276',NULL,504.46,82.18,'2024-09-03 13:16:39',1,NULL),
('fb0b4bb3-cc82-415f-8f2c-d9fa36ca3619','15aad7b3-1a6f-4ba2-8318-968042be2fe8',NULL,848.21,157.8,'2025-05-02 03:37:27',1,NULL),
('fc9ed548-c5af-4da8-a0d9-46ec103dc382','463c2dae-b050-4f5b-942a-3842ed514dbe','f4c0034a-ae3d-4a8b-a706-eb9700a811b4',95.52,14.32,'2025-05-07 21:01:06',0,NULL);
/*!40000 ALTER TABLE `affiliate_commissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affiliates`
--

DROP TABLE IF EXISTS `affiliates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `affiliates` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `referral_code` varchar(50) NOT NULL,
  `commission_rate` float NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `ix_affiliates_referral_code` (`referral_code`),
  CONSTRAINT `affiliates_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliates`
--

LOCK TABLES `affiliates` WRITE;
/*!40000 ALTER TABLE `affiliates` DISABLE KEYS */;
INSERT INTO `affiliates` VALUES
('00a047b0-e4e2-4e1c-a765-76607f8be268','17a7a39c-3c0a-4ea7-a277-be32020f5b1f','fVItFLFKSf',0.105818,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('1335e209-b7be-49c5-8b1e-b7155ccda3c8','b4b4bb65-782e-403b-9ba3-7f5a74327c0b','tUsi66',0.0887183,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('13c0546d-c9c3-47a5-a285-3109fa4f6722','09abb310-89ee-49aa-b2be-daf234e8efc7','TYzotcZWFK',0.0607876,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('15aad7b3-1a6f-4ba2-8318-968042be2fe8','349f7ae0-523f-4093-90db-9b5f13344881','UbUy97',0.186042,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('463c2dae-b050-4f5b-942a-3842ed514dbe','89356118-12d2-4fde-a7d2-2acd5603f266','TGFA17',0.149869,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('7901dc0e-8ce4-481d-92c1-fc3bc5302276','a699f263-3050-44cc-8738-f5002a4b9298','WTTs16',0.162909,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('b18ee6b6-3348-4e7d-8978-9974e552d26f','931cc4a3-929a-41ca-8719-1a83c115907e','CzBcvtwfEJ',0.0592322,0,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('b1d66e0a-2d08-486a-9642-578268d06ac4','1e29163d-fe45-4bb0-b543-a37d12aa3a91','GOgu34',0.175949,0,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('b8d9ac53-e4fe-4d70-9698-fa5ca3d2e157','d2ee5d26-5b68-43ec-a93f-e742145192fc','KqOZvEUmsW',0.0552366,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('bcd819f0-63e0-4f6d-8f73-604e5a04d027','ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','kzgY21',0.163389,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('c4bc375c-f897-4366-bd32-2415996e5169','16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','glAW54',0.135816,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('db6d0f7a-a503-42b7-958e-7681c7d24a26','8bda9505-912a-4356-ade5-22a8f9484ab9','mpbm34',0.192836,1,'2025-06-29 02:02:53','2025-06-29 02:02:53'),
('f831e60d-77d0-40f6-8e9b-92f24ea33a03','607b3ab7-f43a-4b20-8d1f-86c05b985bcc','UrfAwFipQD',0.155149,1,'2025-06-29 02:02:53','2025-06-29 02:02:53');
/*!40000 ALTER TABLE `affiliates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES
('3765d6635686');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_items`
--

DROP TABLE IF EXISTS `content_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `content_items` (
  `id` char(36) NOT NULL,
  `uuid` char(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` varchar(2048) DEFAULT NULL,
  `content_type` varchar(11) NOT NULL,
  `content_status` varchar(9) NOT NULL DEFAULT 'draft',
  `views` int(11) NOT NULL DEFAULT 0,
  `likes` int(11) NOT NULL DEFAULT 0,
  `sales` decimal(10,2) NOT NULL DEFAULT 0.00,
  `tags` varchar(2048) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `last_updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `owner_user_id` char(36) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_content_items_owner_user_id` (`owner_user_id`),
  CONSTRAINT `content_items_ibfk_1` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `content_items_ibfk_2` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `content_items_ibfk_3` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `content_items_ibfk_4` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `content_items_ibfk_5` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `content_items_ibfk_6` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `content_items_ibfk_7` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_items`
--

LOCK TABLES `content_items` WRITE;
/*!40000 ALTER TABLE `content_items` DISABLE KEYS */;
INSERT INTO `content_items` VALUES
('a1b2c3d4-e5f6-7890-1234-567890abcdef','a1b2c3d4-e5f6-7890-1234-567890abcdef','Test Memorial Entry for NFT Mint Fix',NULL,'memorial','published',0,0,0.00,NULL,'2025-10-07 23:37:27','2025-10-07 23:37:27','cdcf9bce-1970-4356-a37e-ddb1ff66f621');
/*!40000 ALTER TABLE `content_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nfts`
--

DROP TABLE IF EXISTS `nfts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `nfts` (
  `id` char(36) NOT NULL,
  `token_id` int(11) NOT NULL,
  `uuid` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(2048) DEFAULT NULL,
  `image_url` varchar(512) NOT NULL,
  `metadata_url` varchar(512) DEFAULT NULL,
  `owner_id` char(36) NOT NULL,
  `content_id` char(36) NOT NULL,
  `minted_at` datetime NOT NULL,
  `last_updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `ix_nfts_token_id` (`token_id`),
  KEY `ix_nfts_content_id` (`content_id`),
  KEY `ix_nfts_owner_id` (`owner_id`),
  CONSTRAINT `nfts_ibfk_1` FOREIGN KEY (`content_id`) REFERENCES `content_items` (`id`),
  CONSTRAINT `nfts_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nfts`
--

LOCK TABLES `nfts` WRITE;
/*!40000 ALTER TABLE `nfts` DISABLE KEYS */;
/*!40000 ALTER TABLE `nfts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_type_options`
--

DROP TABLE IF EXISTS `user_type_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_type_options` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `last_updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_type_options`
--

LOCK TABLES `user_type_options` WRITE;
/*!40000 ALTER TABLE `user_type_options` DISABLE KEYS */;
INSERT INTO `user_type_options` VALUES
('11be8dd3-46ba-4c9d-a27b-c362ab8859a8','SuperTestType_1752516970','A superuser created test type.',1,'2025-07-14 18:16:10','2025-07-14 18:16:10'),
('28d33d71-3f6b-4978-b81a-c00441967a10','SuperTestType_1752517335','A superuser created test type.',1,'2025-07-14 18:22:15','2025-07-14 18:22:15'),
('31728b4b-710e-40ff-aab7-9b08f26c9fd1','Super User','Standard Super User role.',1,'2025-06-29 02:02:43','2025-06-29 02:02:43'),
('65577db6-078e-4abd-baac-ee84e9cdf58f','SuperTestType_1752523460','A superuser created test type.',1,'2025-07-14 20:04:20','2025-07-14 20:04:20'),
('7e47ac15-a7f3-410e-8b36-b288543f1187','SuperTestType_1752523791','A superuser created test type.',1,'2025-07-14 20:09:51','2025-07-14 20:09:51'),
('8cddc4fb-4e44-479b-b09a-7bb93df696a1','Creator','Standard Creator role.',1,'2025-06-29 02:02:43','2025-06-29 02:02:43'),
('8deed136-b7a0-4484-99fb-b8fd4de77926','SuperTestType_1752523859','A superuser created test type.',1,'2025-07-14 20:10:59','2025-07-14 20:10:59'),
('9c4c78fd-dcf7-4973-90a8-45200dc2aa6c','Admin','Standard Admin role.',1,'2025-06-29 02:02:43','2025-06-29 02:02:43'),
('a7666389-a07f-4e0d-b86b-9d7992368359','Consumer','Standard Consumer role.',1,'2025-06-29 02:02:43','2025-06-29 02:02:43'),
('ba15fe7d-9792-4710-9f3b-ef21ddf8d836','Affiliate','Standard Affiliate role.',1,'2025-06-29 02:02:43','2025-06-29 02:02:43'),
('d1cc9f3f-7a50-43f2-b051-4f0691731f91','SuperTestType_1752579193','A superuser created test type.',1,'2025-07-15 11:33:14','2025-07-15 11:33:14'),
('e39946d3-ce79-4650-a794-9e78f96d431b','Registered User','Standard Registered User role.',1,'2025-06-29 02:02:43','2025-06-29 02:02:43'),
('f06463bd-7a99-4a6c-839c-755eb4766602','UpdatedSuperTestType','This superuser test type has been updated.',0,'2025-07-14 18:18:11','2025-07-14 18:18:11');
/*!40000 ALTER TABLE `user_type_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_types`
--

DROP TABLE IF EXISTS `user_user_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user_types` (
  `user_id` char(36) NOT NULL,
  `user_type_option_id` char(36) NOT NULL,
  PRIMARY KEY (`user_id`,`user_type_option_id`),
  KEY `user_type_option_id` (`user_type_option_id`),
  CONSTRAINT `user_user_types_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_user_types_ibfk_2` FOREIGN KEY (`user_type_option_id`) REFERENCES `user_type_options` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_types`
--

LOCK TABLES `user_user_types` WRITE;
/*!40000 ALTER TABLE `user_user_types` DISABLE KEYS */;
INSERT INTO `user_user_types` VALUES
('04cc04e0-51c6-4309-b006-b2673e0a42dc','a7666389-a07f-4e0d-b86b-9d7992368359'),
('07a5d439-d35b-470b-88da-581d3b58628c','a7666389-a07f-4e0d-b86b-9d7992368359'),
('0e59c5c6-6e68-486f-9c61-c9d7838baf1d','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('112eb06a-4d92-46d0-928d-d66aa671639a','8cddc4fb-4e44-479b-b09a-7bb93df696a1'),
('16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','ba15fe7d-9792-4710-9f3b-ef21ddf8d836'),
('17a7a39c-3c0a-4ea7-a277-be32020f5b1f','a7666389-a07f-4e0d-b86b-9d7992368359'),
('1e29163d-fe45-4bb0-b543-a37d12aa3a91','ba15fe7d-9792-4710-9f3b-ef21ddf8d836'),
('2b714597-e4f6-4659-94d3-c1b7b3b809ca','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('2c6f802a-ee5a-4211-9514-4d3c866b1636','9c4c78fd-dcf7-4973-90a8-45200dc2aa6c'),
('32bfeacd-de61-42a8-8dc0-9011c126086f','e39946d3-ce79-4650-a794-9e78f96d431b'),
('349f7ae0-523f-4093-90db-9b5f13344881','ba15fe7d-9792-4710-9f3b-ef21ddf8d836'),
('42f111ee-e96c-48d3-bbe6-8f4a818c7ca0','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('4ab1a1f1-13f4-4ce0-832c-6ae231886ec5','e39946d3-ce79-4650-a794-9e78f96d431b'),
('503c0512-d022-4cf3-acd0-895cf37cca40','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('5197cf24-7039-4135-824c-9640c2f76223','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('607b3ab7-f43a-4b20-8d1f-86c05b985bcc','9c4c78fd-dcf7-4973-90a8-45200dc2aa6c'),
('70d6dca0-5fdf-42ea-ab17-94cc5ba60bfe','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('7fa4e695-7e23-4200-b83e-16fc51cf267b','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('861f0881-9bc5-4286-bea8-decd4a997ecc','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('86578149-9359-4097-959b-b4ba732893b4','e39946d3-ce79-4650-a794-9e78f96d431b'),
('89356118-12d2-4fde-a7d2-2acd5603f266','ba15fe7d-9792-4710-9f3b-ef21ddf8d836'),
('8bda9505-912a-4356-ade5-22a8f9484ab9','ba15fe7d-9792-4710-9f3b-ef21ddf8d836'),
('8e93820c-b834-43e2-9cef-8e1d88db2d2d','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('a699f263-3050-44cc-8738-f5002a4b9298','8cddc4fb-4e44-479b-b09a-7bb93df696a1'),
('ac5b586b-af58-494a-b16a-1e31208718e7','e39946d3-ce79-4650-a794-9e78f96d431b'),
('ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','ba15fe7d-9792-4710-9f3b-ef21ddf8d836'),
('b4b4bb65-782e-403b-9ba3-7f5a74327c0b','ba15fe7d-9792-4710-9f3b-ef21ddf8d836'),
('b9d5e3c8-0d3e-4309-b7b6-944253ca8953','8cddc4fb-4e44-479b-b09a-7bb93df696a1'),
('c1638330-fc15-4242-aa58-878ec07b17e8','e39946d3-ce79-4650-a794-9e78f96d431b'),
('cd8cb54a-abea-435c-ae89-6bc2b1b438a5','31728b4b-710e-40ff-aab7-9b08f26c9fd1'),
('d2ee5d26-5b68-43ec-a93f-e742145192fc','a7666389-a07f-4e0d-b86b-9d7992368359'),
('df8a9980-1e7c-4728-80b2-805f0abec7f8','a7666389-a07f-4e0d-b86b-9d7992368359'),
('e362c58c-d26e-4ec2-822c-980afeac3d3f','9c4c78fd-dcf7-4973-90a8-45200dc2aa6c'),
('e3938f63-873f-4867-b045-0fdf9d4e5fcb','8cddc4fb-4e44-479b-b09a-7bb93df696a1'),
('e7dfc948-0690-4c21-861b-528ac0438d62','8cddc4fb-4e44-479b-b09a-7bb93df696a1'),
('e8750671-c441-43f7-9150-275266de9333','e39946d3-ce79-4650-a794-9e78f96d431b'),
('eed54e26-2f32-4757-81d2-fc1c7c2fed52','a7666389-a07f-4e0d-b86b-9d7992368359'),
('f9af7a4b-c6a6-43b0-9a31-72e2c62b8376','a7666389-a07f-4e0d-b86b-9d7992368359');
/*!40000 ALTER TABLE `user_user_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` char(36) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(120) NOT NULL,
  `hashed_password` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `last_updated_at` datetime NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `bio` varchar(1024) DEFAULT NULL,
  `profile_picture_url` varchar(2048) DEFAULT NULL,
  `social_links` varchar(2048) DEFAULT NULL,
  `role` varchar(15) NOT NULL,
  `permissions_level` int(11) NOT NULL,
  `affiliate_id` char(36) DEFAULT NULL,
  `referring_affiliate_id` char(36) DEFAULT NULL,
  `referral_code` varchar(50) DEFAULT NULL,
  `referral_code_used` varchar(255) DEFAULT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `has_api_access` tinyint(1) NOT NULL,
  `api_key_hashed` varchar(128) DEFAULT NULL,
  `api_key_salt` varchar(64) DEFAULT NULL,
  `referred_by_user_id` char(36) DEFAULT NULL,
  `referred_by_referral_code` varchar(50) DEFAULT NULL,
  `uuid` char(36) NOT NULL DEFAULT uuid(),
  `is_superuser` tinyint(1) NOT NULL DEFAULT 0,
  `user_type_id` char(36) DEFAULT NULL,
  `referred_by_id` char(36) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `ix_users_uuid` (`uuid`),
  UNIQUE KEY `ix_users_referral_code` (`referral_code`),
  UNIQUE KEY `ix_users_affiliate_id` (`affiliate_id`),
  KEY `fk_referring_affiliate_id` (`referring_affiliate_id`),
  KEY `ix_users_referral_code_used` (`referral_code_used`),
  KEY `ix_users_user_type_id` (`user_type_id`),
  KEY `ix_users_referred_by_id` (`referred_by_id`),
  CONSTRAINT `fk_referring_affiliate_id` FOREIGN KEY (`referring_affiliate_id`) REFERENCES `users` (`affiliate_id`) ON DELETE SET NULL,
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`user_type_id`) REFERENCES `user_type_options` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
('04cc04e0-51c6-4309-b006-b2673e0a42dc','justinmorrison26','joseking@example.org','$2b$12$Fk.vh4DXsyeRLYX8LB8kPOjFTkanQS4k5aAnS/RgoLdue5rG5CiPq',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Zachary Nelson','Impact real should believe now. Leave one name course common.',NULL,'http://www.jefferson.com/','CONSUMER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c761fd2-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('06a01a82-7b26-42f1-849c-4cc7e48a4fc7','test_new_user_1752582363','test_new_user_1752582363@example.com','$2b$12$K387udcXY4.HRgr23XqVa.XE8yyoFs668bvEe0wcysg3pPL4j/Tki',1,'2025-07-15 12:26:03','2025-07-15 12:26:03','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'5c07114a-6864-47a4-b0b4-a1fb016902f8',NULL,'6e233a1e',NULL,0,0,NULL,NULL,NULL,NULL,'5c7633ad-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('07a5d439-d35b-470b-88da-581d3b58628c','thomasmatthew0','destiny24@example.org','$2b$12$Bkjw4rHLUK9DLzObDiHtruT.T6jsgvc12opFzrsJi6uvSosOX48hO',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Ethan Ward','Table tell consumer between so south husband.','https://dummyimage.com/659x760','http://www.hughes.com/','CONSUMER',0,NULL,'de1b0610-be08-4676-a0ba-0c2811078393',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c7633ed-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('09abb310-89ee-49aa-b2be-daf234e8efc7','dennisjohnson39','wandaross@example.org','$2b$12$YE.A5cKlh8sHsLCV9kQkTu4r9jxnnVDvEUhwzKWpyQdeAvSvGTygK',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','James Barry','Little along father about budget.','https://placekitten.com/567/603','https://green-williams.com/','GUEST_PLAYER',0,'35daf452-7b5d-45f5-a78a-df68a3665fec','4a404b12-3975-4d03-8617-76550920914b',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76340c-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('0e59c5c6-6e68-486f-9c61-c9d7838baf1d','fergusonbob40','emiles@example.net','$2b$12$ylUnXWVCLRx6KRCzqr8YZuOxczGUVyHGMmm7ua0hEaiTN.5vJBe2q',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Brian Palmer','True form dream if play official. Pass property sit us into remain understand director.','https://picsum.photos/391/45',NULL,'SUPER_USER',0,NULL,'35daf452-7b5d-45f5-a78a-df68a3665fec',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76342f-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('112eb06a-4d92-46d0-928d-d66aa671639a','mcdowelldiana22','kayla94@example.org','$2b$12$2NfYPJMRm/XefcX6x28EC.GRuXHkk2G8ldLuliX8J7bPGx0sgFTSC',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Elizabeth Bailey','Town discussion save race allow myself.','https://dummyimage.com/380x25',NULL,'CREATOR',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76344f-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('13f80d6c-8b0d-4fab-b5f6-b8e84da5bf69','guzzy_superuser222','superuser@example223.com','$2b$12$GGo0XuEv5VaeI.pkjF1j8epxG5KjMYAsTW3jJHe1HD9sUhkrfbv4q',1,'2025-07-14 19:44:30','2025-07-14 19:44:30','Guzzy Superuser223',NULL,'http://example.com/profiles/guzzy1.jpg','{\"linkedin\": \"guzzy_official1\", \"twitter\": \"guzzytweets1\"}','REGISTERED_USER',0,'eda9e0f2-e5d8-49e7-9a8e-84cbb94be8b5',NULL,'48ae1f3b',NULL,0,0,NULL,NULL,NULL,NULL,'5c763469-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('1432edd7-55fe-4f80-87ea-7b00c4fda731','test_ravi_user_28','test_ravi_28@example.com','$2b$12$sDmsKy3kfajEfbf6mVbf5OzCo.3g6TwERzY3QBvSWlDkvIsHEHCXe',1,'2025-07-13 20:03:43','2025-07-13 20:03:43','Ravi Test User Twenty-Eight','This is a test user for retesting auth.',NULL,'{}','REGISTERED_USER',0,NULL,NULL,'4b8979fc',NULL,0,0,NULL,NULL,NULL,NULL,'5c763482-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('16af89f1-c0dc-42bb-b7b5-c76e2f9540ac','frankkim46','deborahkennedy@example.org','$2b$12$kbfUtJBZMIe6LriFCOFwTemVfMLlITQRDAcioXk2NGOxLCRLLpKkK',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Charles Ochoa','May term defense different law center.',NULL,'http://www.eaton-spears.biz/','AFFILIATE',0,'60e4015e-c6bf-455d-ba37-cec98ff23d93',NULL,'glAW54',NULL,0,0,NULL,NULL,NULL,NULL,'5c763499-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('17a7a39c-3c0a-4ea7-a277-be32020f5b1f','craig324','penny46@example.net','$2b$12$rFqdliJzEAVWVdNcYfHTAOZmk1YgUsTem/vnSOUO1c5jY70wcIpwu',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Kevin Hansen','Lose town majority type.',NULL,NULL,'CONSUMER',0,'70f74435-99dd-4812-8045-4c7fc05b2645','de1b0610-be08-4676-a0ba-0c2811078393',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c7634b2-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('1e29163d-fe45-4bb0-b543-a37d12aa3a91','georgeleslie11','richardstravis@example.com','$2b$12$YbMej8aDACCewjKjJsCrueeXbXqE/92itt92EJhD0v6/pAqsnO3aO',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Christopher Williams','Near week itself either per factor person work.','https://placekitten.com/228/550','https://garner-ramirez.net/','AFFILIATE',0,'61fda4f0-5834-4761-bad3-4afebf313572','de1b0610-be08-4676-a0ba-0c2811078393','GOgu34',NULL,0,0,NULL,NULL,NULL,NULL,'5c7634c8-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('2418d91f-584b-48de-893a-c13c782de1bc','agarcia23','gabriellegallagher@example.org','$2b$12$5ouU0GXtPXlCzcZVJT/8N.yoHAqyvV8kIC1bBYGgg/rgTHcy/OTK6',0,'2025-06-29 02:02:53','2025-06-29 02:02:53','Rachel Houston','Loss to none lay gun western although attention.',NULL,'http://www.jones-wilcox.com/','GUEST_PLAYER',0,NULL,'539c8cb0-a9e5-4415-b664-7900f55dc226',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c7634de-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('2b714597-e4f6-4659-94d3-c1b7b3b809ca','guzzy_superuser','admin@guzzyandbash.com','$argon2id$v=19$m=65536,t=3,p=4$MeYcI6S01vr/nxNCSCnFmA$LO//w9tOEq7CtYGWVsOvFI2xyf4We2GXAyw+jTmvhU8',1,'2025-06-29 02:02:43','2025-07-17 17:07:19','Guz The Grand Master',NULL,NULL,NULL,'SUPERUSER',100,'guzzy_superuser_id',NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c763e66-62e7-11f0-b97c-1ee8d4b1fc0e',1,NULL,NULL,NULL,NULL,NULL),
('2c6f802a-ee5a-4211-9514-4d3c866b1636','deborah9631','emily90@example.org','$2b$12$aGeI1lDnX8AmkkN6vRPP3uslVMC2/eY2pwA7Hhh.dJiIlmRHlQgUi',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Brittany Sanchez','Debate bill listen nice understand church north.','https://dummyimage.com/46x449',NULL,'ADMIN',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c763ea2-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('2dcc6ad7-f06e-4785-ab96-199d851a4352','floresmelissa13','tina41@example.com','$2b$12$eT35Kjsehy9X.NOZhgd.ye8qz7dczcGe3gbGA7OMerPCFusfpu21u',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Edward Miller','Nice several help. Power outside again structure measure sense maintain law.',NULL,'https://abbott-hubbard.org/','GUEST_PLAYER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c763ee4-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('2f37414d-974a-4372-80f1-d71fc72e1770','test_new_user_1752591039','test_new_user_1752591039@example.com','$2b$12$cXfiKJEil7OHUjQs1dZmT.VftxPo5l8cOCo.cOlgmjpairjt2oSgu',1,'2025-07-15 14:50:40','2025-07-15 14:50:40','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'c3ce8b05-3c47-4746-9bc9-a7b7c462c01c',NULL,'b60feb09',NULL,0,0,NULL,NULL,NULL,NULL,'5c7647da-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('32bfeacd-de61-42a8-8dc0-9011c126086f','blakemorgan43','shawnferguson@example.net','$2b$12$8ZIVmuWCzj82MpPnC3MDDuUqaNkU5NRtfuyyFhVvNWEpb73AETNq2',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Brianna Bryant','Will who until hotel tax quite PM upon. Laugh shoulder fund could yeah what year skill.','https://dummyimage.com/935x796','http://carroll.info/','REGISTERED_USER',0,NULL,'f88e5d80-c786-491b-b6c6-fdd29dbe5515','hjLo45',NULL,0,0,NULL,NULL,NULL,NULL,'5c764814-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('349f7ae0-523f-4093-90db-9b5f13344881','rebecca2818','cynthia34@example.net','$2b$12$/X.llULcL/I.8FmVZQ8u..17BBYlu3BYxNA1StG/d9J3vlpqtXeXu',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Jennifer Barton','Begin idea first star kind. Stop read reason lose increase foot guess.','https://picsum.photos/366/840','http://www.wheeler.com/','AFFILIATE',0,'7e87bb44-f913-4bed-8c60-04933c29f9db','f88e5d80-c786-491b-b6c6-fdd29dbe5515','UbUy97',NULL,0,0,NULL,NULL,NULL,NULL,'5c764835-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('353b0049-50fc-4c65-837c-138d9366d62c','test_new_user_1752524915','test_new_user_1752524915@example.com','$2b$12$EvvFol7TGl.gQK/BIGW41eJ4FTbYKjEh7IdglG1pFhXgpkBi97YAu',1,'2025-07-14 20:28:35','2025-07-14 20:28:35','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'d4d7dcf4-4a07-45c4-9255-40a5cfd43c18',NULL,'04fe49fb',NULL,0,0,NULL,NULL,NULL,NULL,'5c764e1f-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('3d194221-dfbe-4345-b32e-86a0d0311404','test_new_user_1752582833','test_new_user_1752582833@example.com','$2b$12$xz46WBGeoNHaBTYEqJ3Ol.fDy00jvw6MNQ.EAAOd3LN6ah3hnlACW',1,'2025-07-15 12:33:53','2025-07-15 12:33:53','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'ac432161-b6ab-4c48-bfc1-0863f56df5e9',NULL,'e4d78e47',NULL,0,0,NULL,NULL,NULL,NULL,'5c764e62-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('42f111ee-e96c-48d3-bbe6-8f4a818c7ca0','rgibson10','david33@example.com','$2b$12$s.wlADrv1vUXXbcM13rGeufaTAgDgXiQvwoGHlfFEN6BIuuHiziUC',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Candace Whitney','Matter new entire share person thousand what.',NULL,NULL,'SUPER_USER',0,NULL,'70f74435-99dd-4812-8045-4c7fc05b2645',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c764e89-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('465e5e4f-e949-41a9-b121-99e3f2e2cc63','test_new_user_1752585665','test_new_user_1752585665@example.com','$2b$12$dEdqOHsNTaGak/xUfY/nnut6kovW1jC.7KYyerXNieLHUQmjW3w3K',1,'2025-07-15 13:21:05','2025-07-15 13:21:05','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'3b13c7fd-3c95-457e-b08f-3f6b57e6420f',NULL,'0d23934b',NULL,0,0,NULL,NULL,NULL,NULL,'5c764eac-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('4ab1a1f1-13f4-4ce0-832c-6ae231886ec5','fkennedy24','amanda98@example.com','$2b$12$zwTj9dYRmtSqH7A1eaw..uz05LeVX6k6dNH3svHftmo1eTv1ebaca',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Nicholas Underwood','Single current southern list few age opportunity collection.',NULL,NULL,'REGISTERED_USER',0,NULL,NULL,'mNCb30',NULL,0,0,NULL,NULL,NULL,NULL,'5c764ecd-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('4d9d5942-11de-4fa5-b61b-66ef9f5a8884','test_new_user_1752779622','test_new_user_1752779622@example.com','$argon2id$v=19$m=65536,t=3,p=4$aU0pxfj/HwMgZAzBmFOKEQ$r8TETMro95C8FoFqjOt1UFmQ0drnhlxoF2Ka8VAl3sg',1,'2025-07-17 19:13:52','2025-07-17 19:13:52',NULL,NULL,NULL,NULL,'REGISTERED_USER',1,'a367d82f-9408-4abd-8f0f-2c8ea787741d',NULL,'f8ea7c57',NULL,0,0,NULL,NULL,NULL,NULL,'6fb4e427-57c6-49b7-a90b-ef0df137448a',0,NULL,NULL,'New','Registered Test User',NULL),
('4dd53636-b41f-4bcf-97b3-364a42be92af','abigail906','castilloalexis@example.com','$2b$12$oCNLN7KD3TqyGJDFngdoWeG0XRyem4bd9dx3AKf19i6JkBRRpWB4.',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Mary Petersen','Difficult if nation everybody huge same tree.',NULL,NULL,'GUEST_PLAYER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c764eee-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('503c0512-d022-4cf3-acd0-895cf37cca40','joseph7033','ochristensen@example.net','$2b$12$TVkOGuOm.mR/.qP7i4bGH.twFwSDDRPghVPJLwtKCBOARAfWCFTha',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Melissa Schultz','Wonder relate continue turn final. Daughter south plant day.','https://picsum.photos/847/1002','http://crane-white.info/','SUPER_USER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c764f0a-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('5197cf24-7039-4135-824c-9640c2f76223','kramerkaren27','jason01@example.net','$2b$12$wcl3vvgfp2k/HV7C0i0TPOPJnznIH33/oK8RnAKdSCt4DY1uAUCOS',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','John Johnson','Model its create environment idea. Door east laugh company yeah speak small trial.',NULL,NULL,'SUPER_USER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c764f2a-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('530e57bc-1ab3-4436-9c2d-a346b96f831f','bennetterica44','figueroapeter@example.org','$2b$12$/JgTpvKui7eDvulretPYyOtjSWyIXGAVON/4gLkYhPPer5YVRx7ui',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Sara Contreras','Far its simply though people take.','https://placekitten.com/965/179',NULL,'GUEST_PLAYER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c765569-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('591544b9-78d3-48a3-8c9a-532ada558dd4','test_new_user_1752525009','test_new_user_1752525009@example.com','$2b$12$Qzu1QdjQjwAHVy3tdLSEPOi6vjfySRN4WKOZI4jiUimrKIL421WWa',1,'2025-07-14 20:30:10','2025-07-14 20:30:10','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'0bb0c87c-e38f-49bd-8220-de0c2b55d647',NULL,'93200680',NULL,0,0,NULL,NULL,NULL,NULL,'5c7655c6-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('607b3ab7-f43a-4b20-8d1f-86c05b985bcc','stevenholt2','phillipwallace@example.net','$2b$12$8rXWRsaPIXOmvCxAbVCIMeYHUk3ldqyhUO7h2QxdTRytCBmlue1uC',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Patrick Finley','Brother show state growth.','https://picsum.photos/435/242',NULL,'ADMIN',0,'0d6e739f-6c26-47c8-be7d-ca9f9786f0b2',NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c7655e9-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('627f242e-f64b-4fdd-be88-858c63fdf687','dlandry14','oadkins@example.org','$2b$12$sVcYyfVbI2HGRPg.tOI21eXjN2X8iFZSgUbItHhb3Xm9yPEJHFg72',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Carlos Beard','Article late why center production budget system teacher. Building lawyer eye rather allow agency that.','https://picsum.photos/40/656','http://www.carroll.com/','GUEST_PLAYER',0,NULL,'61fda4f0-5834-4761-bad3-4afebf313572',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76582f-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('70d6dca0-5fdf-42ea-ab17-94cc5ba60bfe','scottrobinson29','qbarber@example.org','$2b$12$xiltpBo6gh8jBW.gm26H/uc9KgKU1S6bnt6sxKFEl7BC6KEpUkf/m',0,'2025-06-29 02:02:53','2025-06-29 02:02:53','Julie Chen','Risk single job wife build far treat. Charge long concern will black can.','https://dummyimage.com/451x463','https://mccoy.com/','SUPER_USER',0,NULL,'4a404b12-3975-4d03-8617-76550920914b','vdOf00',NULL,0,0,NULL,NULL,NULL,NULL,'5c765852-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('781c5289-97bc-4649-ab6d-33e20e3dac8c','test_new_user_1752590398','test_new_user_1752590398@example.com','$2b$12$8mqcVLPoacV84XDgUfRMAOlkB6zF6oneX/JW12pixUn/P6XODDDWC',1,'2025-07-15 14:39:58','2025-07-15 14:39:58','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'cdc99327-801e-4709-a784-f81b3a603f08',NULL,'5ed13107',NULL,0,0,NULL,NULL,NULL,NULL,'5c765876-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('7fa4e695-7e23-4200-b83e-16fc51cf267b','bradleymejia7','hallkimberly@example.com','$2b$12$P0b9lMcc3Y1d3CcptO5gyOkQ6mXYhyJqo7srx8UKePucL8S/KneVC',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Rachel Robinson','Hope front magazine later simple animal.',NULL,'http://www.neal.net/','SUPER_USER',0,NULL,'4a404b12-3975-4d03-8617-76550920914b','dlgT57',NULL,0,0,NULL,NULL,NULL,NULL,'5c76588e-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('80abaf5a-bcc9-4263-9282-c736f4f6a9c7','anotheruser','another@example.com','$argon2id$v=19$m=65536,t=3,p=4$qbUWwlhL6b035vxfK0VozQ$1LfOOa4T53PCzmIKjdKp5B0GYDZSdMWakRKGYKRjfp8',1,'2025-07-17 18:23:05','2025-07-17 18:23:05',NULL,NULL,NULL,NULL,'REGISTERED_USER',1,'b6012c1b-4c8e-41d6-ae64-cca0b305e276',NULL,'7632d6b1',NULL,0,0,NULL,NULL,NULL,NULL,'7922cad6-9ba3-4e57-bf31-b388ff991359',0,NULL,NULL,'Another','Test User',NULL),
('81e5afdd-3d86-477f-b536-68da505575f7','test_new_user_1752585759','test_new_user_1752585759@example.com','$2b$12$OvZBS1u5fzEFZqUlHRmUruT35B/CG.INQWqKBsYuu9L0TI2viyXfe',1,'2025-07-15 13:22:40','2025-07-15 13:22:40','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'9c08fc93-b740-4025-960e-848405e091c0',NULL,'cb068e36',NULL,0,0,NULL,NULL,NULL,NULL,'5c765cdf-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('844df998-c4a5-4d54-b4ff-217018f3dcd6','test_new_user_1752585333','test_new_user_1752585333@example.com','$2b$12$hTefsxJ6M0kIb.Zy7XbmwO1lcs.TFR6SPrKNERlh/wH2wjt6Sc8Mi',1,'2025-07-15 13:15:33','2025-07-15 13:15:33','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'64a642db-298a-4c53-9c7f-81b80aa04d23',NULL,'d5119977',NULL,0,0,NULL,NULL,NULL,NULL,'5c765d01-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('85c0fc34-927c-46fb-b907-a2c253759ac7','test_new_user_1752524717','test_new_user_1752524717@example.com','$2b$12$0JbKeCQGQENIIVPorth3Nu1L3.g7I5C0h.ucNucpTHvDnL6HF9uSu',1,'2025-07-14 20:25:18','2025-07-14 20:25:18','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'50d89bed-041b-4377-912e-39524e4bc91a',NULL,'fb212667',NULL,0,0,NULL,NULL,NULL,NULL,'5c765ec5-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('861f0881-9bc5-4286-bea8-decd4a997ecc','hjohnson20','branchaustin@example.com','$2b$12$sQZPiv/7y5LQKzkiKv2cj.GT9g8AWB9juO108f32wzgRKsVw/Dzd2',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Sarah Rowland','Management once identify and since wind soon. Left teacher song identify owner.','https://dummyimage.com/861x131','http://www.sawyer.com/','SUPER_USER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c7667bc-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('86578149-9359-4097-959b-b4ba732893b4','lauratorres32','madisonmorales@example.org','$2b$12$tzlSnbikWTBiMEmoLfGaTOKlqbNz5jx24ezJINL4p1cwTOicJrIcK',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Desiree Kidd','Security politics other culture middle expect.','https://dummyimage.com/405x37','https://calhoun.org/','REGISTERED_USER',0,NULL,'60e4015e-c6bf-455d-ba37-cec98ff23d93','nsPo09',NULL,0,0,NULL,NULL,NULL,NULL,'5c766c20-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('868fca54-ed83-48d2-ae1c-a72c8bf4f856','dsmith16','flambert@example.net','$2b$12$Ph9c/aiisADGGfuG1/x5dOo9/SqbXO9tKpQ6ljt4DQp41Of1z.qoS',0,'2025-06-29 02:02:53','2025-06-29 02:02:53','Matthew Little','Tax whether sometimes could final television bed.','https://dummyimage.com/1007x906','https://www.buckley.info/','GUEST_PLAYER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c766cfc-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('89356118-12d2-4fde-a7d2-2acd5603f266','ggutierrez17','harrisjames@example.org','$2b$12$V1q40p53k7epPdtLRyyQIOf/YuLs9lZ0qjsnfpQ8kNkYdcIae9zAe',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Theresa Davila','Return speak prevent left. Field international family memory myself.','https://placekitten.com/867/705',NULL,'AFFILIATE',0,'16e79888-765d-42fa-b990-97009821fc7d',NULL,'TGFA17',NULL,0,0,NULL,NULL,NULL,NULL,'5c76723c-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('8bda9505-912a-4356-ade5-22a8f9484ab9','angelawhitehead42','kristine80@example.org','$2b$12$GXPwSI0FDHYouqkgBQNDzemr0ZbGUf4WMfntPjeZygt/1Bs5A2P7W',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Adam Olson','Admit probably name test food.','https://placekitten.com/475/557',NULL,'AFFILIATE',0,'f88e5d80-c786-491b-b6c6-fdd29dbe5515','7b094133-c11e-4cee-8724-80c3944f7792','mpbm34',NULL,0,0,NULL,NULL,NULL,NULL,'5c76726e-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('8e93820c-b834-43e2-9cef-8e1d88db2d2d','ojohnson15','hmartinez@example.org','$2b$12$4hH8SZhQixPHL5DJGq9C2e1A3TD3SONnWr3lBmatxyx8cm0qxZhG6',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Emily Daniel','Receive coach bed.','https://dummyimage.com/772x213','http://www.stanley-bowers.biz/','SUPER_USER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76728a-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('931cc4a3-929a-41ca-8719-1a83c115907e','hernandezkristie47','wjackson@example.org','$2b$12$fIqoeNTp2TzzRGrEU6biP.t5tqrLO0fQv1qUq19BKi7kP4MBO4Xoy',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Larry Gray','Modern score sure glass career.','https://dummyimage.com/926x760',NULL,'GUEST_PLAYER',0,'13fa4749-d38f-42b2-9bd6-f1f117442fa8','60e4015e-c6bf-455d-ba37-cec98ff23d93',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c7672a8-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('96b4f4b1-3086-48ca-bba3-fa01c105946f','testuser2','test2@example.com','$argon2id$v=19$m=65536,t=3,p=4$GUOIsbZ2DqG0tnYOgfA+pw$f/ynwVqlAuXlQvLy7yntqoEAUNBFAukqRMzwT/DrCnQ',1,'2025-10-25 20:36:48','2025-10-25 20:36:48',NULL,NULL,NULL,NULL,'REGISTERED_USER',1,'ccc9c9df-4607-45ab-97e0-d1843fcc5854',NULL,'ee71ebc7',NULL,0,0,NULL,NULL,NULL,NULL,'79cb072e-1943-4b55-9ed9-6e29d949d6d6',0,NULL,NULL,NULL,NULL,NULL),
('a699f263-3050-44cc-8738-f5002a4b9298','charlesgregory35','xguzman@example.org','$2b$12$Q5OX30IMbe//Ig7nx0aXl.tQ6KIdXZToT9EwGYXyUEmMwE7wtbIQi',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Michelle Jackson','Easy red little then there.',NULL,'http://www.alvarez-schmitt.org/','CREATOR',0,'7b094133-c11e-4cee-8724-80c3944f7792',NULL,'WTTs16',NULL,0,0,NULL,NULL,NULL,NULL,'5c76799b-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('a95f3d58-0e2f-48ee-8807-6c54dcd36066','test_ravi_user_34','test_ravi_34@example.com','$2b$12$CUyIKrbx5rt9aYhWxyu0EOZnKhn8.EMeXK4cq5eKPs1O3xj/Dhv8a',1,'2025-07-13 20:32:13','2025-07-13 20:32:13','Ravi Test User Thirty-Four','This is a test user for retesting auth.',NULL,'{}','REGISTERED_USER',0,'9603e0a2-1229-4396-ae8f-4abcf98539d5',NULL,'3dd61f6e',NULL,0,0,NULL,NULL,NULL,NULL,'5c767e97-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('ac5b586b-af58-494a-b16a-1e31208718e7','browncheryl8','fisherautumn@example.org','$2b$12$PSvDvcmfLmXaH91GnbOSP.QW4bh2f.v9OYWRAGey0F7q8cw1zN4Zq',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Melissa Valdez','Add maybe surface spend relationship. Wait pull special sign word sort month above.','https://picsum.photos/656/503','http://www.oneal-rodriguez.com/','REGISTERED_USER',0,NULL,NULL,'xYpw02',NULL,0,0,NULL,NULL,NULL,NULL,'5c768345-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('ad403f0b-32cc-4c94-b9a9-ef29a0edc8fa','kpugh3','jasonharris@example.net','$2b$12$JWfDRCHWhzfCK83ZcERY.OYkSZVOjhfTKLINRhLTHWqm8cLBgdt/a',0,'2025-06-29 02:02:53','2025-06-29 02:02:53','Brandon Schultz','He wall maybe necessary book. Sea lead truth bag design live.','https://dummyimage.com/707x526',NULL,'AFFILIATE',0,'4a404b12-3975-4d03-8617-76550920914b','16e79888-765d-42fa-b990-97009821fc7d','kzgY21',NULL,0,0,NULL,NULL,NULL,NULL,'5c768365-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('ad8313ce-5449-4cec-bf66-eb35c3e4f287','georgejohnson19','mramirez@example.net','$2b$12$OoF0VkDnHEZEa00xeMHeVOzXF.U7wTsP5Tqj7sbZQ.reYQhVbra26',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Ernest Hicks','Exactly hope between house instead.','https://placekitten.com/954/134',NULL,'GUEST_PLAYER',0,NULL,'16e79888-765d-42fa-b990-97009821fc7d',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76837f-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('affb3747-ff61-465c-bf2a-11e72febc795','johnwright45','melissa26@example.com','$2b$12$HhN4iwrLlxeOXEesRudPiuhDBJMRXMm2VxsyALNd3UsN6/EKqJ5eS',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Samuel Martin','Dark force skill standard poor meeting must eight.',NULL,'https://www.collins.info/','GUEST_PLAYER',0,NULL,'35daf452-7b5d-45f5-a78a-df68a3665fec',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76891e-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('b4b4bb65-782e-403b-9ba3-7f5a74327c0b','brooke4412','pvasquez@example.org','$2b$12$KDboKBTSRpad7Wkklf.EiOWNde4SPnA6CEQospxlu3jfcK1xggyou',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Barbara Cohen','Although clear fill.','https://dummyimage.com/319x901',NULL,'AFFILIATE',0,'de1b0610-be08-4676-a0ba-0c2811078393',NULL,'tUsi66',NULL,0,0,NULL,NULL,NULL,NULL,'5c76897a-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('b61c32db-418f-425e-a3b3-e66e6680570c','test_new_user_1752590727','test_new_user_1752590727@example.com','$2b$12$8FfmO/CKbz.fO5wPAybmL.MlbMrFBfo69hh8qpjgc5980u60QXo.O',1,'2025-07-15 14:45:28','2025-07-15 14:45:28','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'0e8364e5-dd25-4109-81ed-fb6c80a2d046',NULL,'378c5f82',NULL,0,0,NULL,NULL,NULL,NULL,'5c768f2f-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('b9d5e3c8-0d3e-4309-b7b6-944253ca8953','whitneycook25','rebeccapoole@example.com','$2b$12$luCKVAZJY3xYVvHsLFY0TuGW9eZ/tfBOTch1V0/jQVZMcb.7MqyEq',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Barbara Williams','Method current couple show staff book watch.','https://placekitten.com/961/450',NULL,'CREATOR',0,NULL,'7b094133-c11e-4cee-8724-80c3944f7792',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c768f5e-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('ba749dde-10f1-4e17-b4be-e9a1d5e07381','test_new_user_1752524808','test_new_user_1752524808@example.com','$2b$12$8y6Xx9yGCuexbUrRi5CoeujXfOqdYDnlBXUIJyY2vekyUWur0aRn2',1,'2025-07-14 20:26:48','2025-07-14 20:26:48','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'30bf0145-de81-47db-aa69-ae3c2a6a0651',NULL,'d3457d68',NULL,0,0,NULL,NULL,NULL,NULL,'5c7694ff-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('bb007402-bf56-4611-bb27-1d7d987181bf','testuser','test@example.com','$argon2id$v=19$m=65536,t=3,p=4$tTam9F6r1fo/p7RWqtUaww$aPsw/OCfHEfpn6yHKlDztT+7nRsc4qVPVKXL+KhJ4Ow',1,'2025-07-17 18:06:22','2025-07-17 18:06:22',NULL,NULL,NULL,NULL,'REGISTERED_USER',1,'7c4c84ed-c62b-46cd-866e-0fb91e1649e6',NULL,'1727acb9',NULL,0,0,NULL,NULL,NULL,NULL,'d339ec2f-5f20-4682-9964-8778646ddae8',0,NULL,NULL,'Test','User',NULL),
('bb6fd780-e1d2-4116-b18d-951ddf5ee52c','swansonroberto41','jeffreysims@example.com','$2b$12$4NDyIUW3DrCG84At.Pe9QOnyTPdZtgHh3VN81FYEi2d5YbMUtFrt2',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Victoria Long','Offer chance heart. Significant wife skin hospital.','https://dummyimage.com/1000x859','https://rodriguez.com/','GUEST_PLAYER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76952d-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('c1638330-fc15-4242-aa58-878ec07b17e8','thansen36','wigginsmark@example.com','$2b$12$3wwgbe54RwlOeYl.NQtPQ.sXjz0a4BTCeC3h/52rwWRjinn9GrnPq',0,'2025-06-29 02:02:53','2025-06-29 02:02:53','Debbie Burns','Onto boy decide appear along far already.','https://dummyimage.com/206x689',NULL,'REGISTERED_USER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76954e-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('cd8cb54a-abea-435c-ae89-6bc2b1b438a5','draymond34','ohill@example.net','$2b$12$Jh3Y14ARtVgL.lI4RPltF.7mA.JwYfkJ5nmHUZ43yGCdhkP5On3hm',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Sherry Whitehead','Debate everyone trial leg tax toward. Daughter thousand rather newspaper science.','https://placekitten.com/334/193','http://www.matthews.com/','SUPER_USER',0,NULL,NULL,'NvRl49',NULL,0,0,NULL,NULL,NULL,NULL,'5c76956b-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('cdcf9bce-1970-4356-a37e-ddb1ff66f621','test_new_user_1752834222','test_new_user_1752834222@example.com','$argon2id$v=19$m=65536,t=3,p=4$mrO2NiaEUMrZWyvF2Nv7Xw$uJ41xICQ+oHNIvRTZgFshNcEhYhmuL+XcnGZ9XaJTV0',1,'2025-07-18 10:23:44','2025-07-18 10:23:44',NULL,NULL,NULL,NULL,'REGISTERED_USER',1,'24a85d9a-3338-4d2d-9322-83d717a9068e',NULL,'7bbe03fc',NULL,0,0,NULL,NULL,NULL,NULL,'46474fac-1597-4c03-9115-07d33cab9e89',0,NULL,NULL,'New','Registered Test User',NULL),
('ce82ba5b-ccf9-4782-b103-22415fc85cbc','test_new_user_1752590851','test_new_user_1752590851@example.com','$2b$12$gW05sRVU6Nj6Afr3sxM9COe/1dvUlhgRQcamN70dbco4cjzR87P/i',1,'2025-07-15 14:47:32','2025-07-15 14:47:32','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'903e681d-7635-4626-bc83-a5121d474fa8',NULL,'66a2aa52',NULL,0,0,NULL,NULL,NULL,NULL,'5c769590-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('d2ee5d26-5b68-43ec-a93f-e742145192fc','hhill1','abanks@example.net','$2b$12$mECyBIUkC9H8XirKHeVNQeoS4SQQO8aLC8nBH/xQr7x2eevKgv3hG',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','David West','With price believe station team maybe. Answer true involve eight about upon really one.',NULL,NULL,'CONSUMER',0,'539c8cb0-a9e5-4415-b664-7900f55dc226','de1b0610-be08-4676-a0ba-0c2811078393',NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c7695b1-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('df8a9980-1e7c-4728-80b2-805f0abec7f8','nicolesolis5','mistyalvarado@example.org','$2b$12$hH7Cb0s0cqU7SkDKCWg5jOmWL7x.LgUY7oQEzy9VwQRaTv2QJtw0m',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Jill Nguyen','Staff position give commercial would picture.','https://picsum.photos/433/901',NULL,'CONSUMER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c769b48-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('e362c58c-d26e-4ec2-822c-980afeac3d3f','admin_bash','admin@example.com','$2b$12$ctXKZIbc2F/1gmhEcBQ07eMNUjVvAasOqg.3b9NhkwTXkE.FXNhqm',1,'2025-06-29 02:02:44','2025-06-29 02:02:44','Bash The Admin',NULL,NULL,NULL,'ADMIN',50,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c769b82-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('e3938f63-873f-4867-b045-0fdf9d4e5fcb','mharrison38','hayneschristine@example.net','$2b$12$1ONUmH9ilrjIzG2LRNTqpuF3N7GlfNOAviTKj97qcgF3VkqrcTP32',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Mary Oconnor','Seat call skill charge brother already his away. Mother there course medical.','https://picsum.photos/527/939',NULL,'CREATOR',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76a142-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('e3970000-9b97-4e1f-8422-a8ccdd53d27d','test_new_user_1752585495','test_new_user_1752585495@example.com','$2b$12$HHTOn7ECe942Tp2sahFYE.BCgTWB7TzNGG.bU8PyVt6/1O7Eyok/m',1,'2025-07-15 13:18:16','2025-07-15 13:18:16','New Registered Test User',NULL,NULL,'{}','REGISTERED_USER',0,'acb2d60f-4fde-4ba1-a5b5-b7786c26070c',NULL,'40bc5781',NULL,0,0,NULL,NULL,NULL,NULL,'5c76a68a-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('e7dfc948-0690-4c21-861b-528ac0438d62','anasmith37','jennifer22@example.com','$2b$12$C89zpvOe8miVkpXnN64b3.I.nxiDfl88ptfF2GlRITIV2x0L0tGd2',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Spencer Bauer','Explain once fly. These use reveal southern.',NULL,'http://www.park-fowler.com/','CREATOR',0,NULL,NULL,'xrkc14',NULL,0,0,NULL,NULL,NULL,NULL,'5c76a6d8-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('e8750671-c441-43f7-9150-275266de9333','wnolan30','laurengonzalez@example.org','$2b$12$3NGDl2WcT4JHwqds22drlO4S2p54e5FAnNBYqyxnYvs6U6Ad4TJaS',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Melissa Lee','Pass right culture building since read on.','https://placekitten.com/9/808','https://www.pacheco-perez.com/','REGISTERED_USER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76a6f6-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('ea2984b5-d8ab-4dbe-b50c-2f457de6a3a7','test_ravi_user_32','test_ravi_32@example.com','$2b$12$cF8hho85G0a4mtEwIJApiOey4TaYqDLz7DNrLg9kwPF2npKi/D8ni',1,'2025-07-13 20:19:24','2025-07-13 20:19:24','Ravi Test User Thirty-Two','This is a test user for retesting auth.',NULL,'{}','REGISTERED_USER',0,'a13bf4ee-8d5a-4d59-a7bd-8e0ccc1a7566',NULL,'694cdb39',NULL,0,0,NULL,NULL,NULL,NULL,'5c76a715-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('eed54e26-2f32-4757-81d2-fc1c7c2fed52','jessicathornton9','mcollier@example.org','$2b$12$KNp4Mx8TzeBJJirVAky9xuWkUY9q9rUVDJjVvZ8TpGbovn/YSEfQG',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Charles Yates','Try budget compare doctor yard officer kitchen.','https://picsum.photos/699/290',NULL,'CONSUMER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76a738-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('f2cf62c1-8e70-4a13-81bf-78c2e36ae711','plucero21','davidbrown@example.org','$2b$12$fXwcnBiiiLH9UNlrn076/eF0woJfkit0/x1xPIUzj.0GlE9HaXCmO',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Peter Holmes','West at strategy statement.',NULL,'https://www.reid.biz/','GUEST_PLAYER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76abe7-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL),
('f9af7a4b-c6a6-43b0-9a31-72e2c62b8376','martinchristopher28','richardvasquez@example.net','$2b$12$SG45n44U6Z0UHQfUjplhBOC1dxJXHol.gRl.lLS0JCvlNqo8nybWm',1,'2025-06-29 02:02:53','2025-06-29 02:02:53','Jeremy Miller','Yourself fund song war hotel enjoy.','https://picsum.photos/92/1001',NULL,'CONSUMER',0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,'5c76ac04-62e7-11f0-b97c-1ee8d4b1fc0e',0,NULL,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2025-10-25 20:50:35
