


# CREATE TABLE `maintenances` (
#   `id` int(11) NOT NULL,
#   `id_machine` int(11) NOT NULL,
#   `id_maintenance_staff` int(11) NOT NULL,
#   `start_date` date NOT NULL,
#   `end_date` date DEFAULT NULL,
#   `problem_description` varchar(512) NOT NULL,
#   `solution_description` varchar(512) DEFAULT NULL,
#   `path_report` varchar(64) DEFAULT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;