# CREATE TABLE `outofservice_machine` (
#   `id` int(11) NOT NULL,
#   `id_machine` int(11) NOT NULL,
#   `start_date` date NOT NULL,
#   `end_date` date DEFAULT NULL,
#   `description` varchar(512) NOT NULL,
#   `has_solution` tinyint(4) DEFAULT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;