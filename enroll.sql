CREATE TABLE `enroll` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_ipaddr` int(11) unsigned DEFAULT NULL COMMENT 'Ukazatel na zaznam v tabulce ''ipaddr'' zatim se tato polozka k nicemu nepouziva',
  `first_name` varchar(50) NOT NULL DEFAULT '',
  `last_name` varchar(50) NOT NULL DEFAULT '',
  `phone` varchar(20) NOT NULL DEFAULT '',
  `mail` varchar(120) NOT NULL DEFAULT '',
  `days` int(3) DEFAULT NULL,
  `mac_addr` varchar(17) NOT NULL DEFAULT '',
  `locality` char(1) DEFAULT NULL,
  `garant_mail` varchar(120) NOT NULL DEFAULT '0',
  `date_registration` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `code_registration` varchar(40) DEFAULT NULL,
  `date_confirm` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `first_name` (`first_name`,`last_name`),
  KEY `id_user_confirm` (`garant_mail`),
  KEY `dat_registration` (`date_registration`),
  KEY `code_registration` (`code_registration`),
  KEY `date_confirm` (`date_confirm`),
  KEY `locality` (`locality`),
  KEY `id_ipaddr` (`id_ipaddr`)
) ENGINE=MyISAM AUTO_INCREMENT=1399 DEFAULT CHARSET=utf8
