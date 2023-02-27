-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: db
-- Tiempo de generación: 17-12-2021 a las 01:17:32
-- Versión del servidor: 8.0.27
-- Versión de PHP: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


--
-- Estructura de tabla para la tabla `Components`
--

CREATE TABLE `Components` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(256) NOT NULL,
  `type` varchar(20) NOT NULL,
  `id_subclass` int NOT NULL,
  `brand` varchar(64) DEFAULT NULL,
  `model` varchar(64) DEFAULT NULL,
  `id_plc` int NOT NULL,
  `plc_in` int NOT NULL,
  `plc_out` int NOT NULL,
  `id_machine` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Hubs`
--

CREATE TABLE `Hubs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand` varchar(64) NOT NULL,
  `model` varchar(64) NOT NULL,
  `n_ports` int NOT NULL,
  `net_mask` varchar(25) DEFAULT NULL,
  `gateway` varchar(25) DEFAULT NULL,
  `mac_address` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Lines`
--

CREATE TABLE `Lines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(256) NOT NULL,
  `id_user_in_charge` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lmi_maintenances`
--

CREATE TABLE `lmi_maintenances` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_machine` int NOT NULL,
  `id_maintenance_staff` int NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `problem_description` varchar(512) NOT NULL,
  `solution_description` varchar(512) DEFAULT NULL,
  `path_report` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lmi_outofservice_machine`
--

CREATE TABLE `lmi_outofservice_machine` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_machine` int NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `description` varchar(512) NOT NULL,
  `has_solution` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lmi_parts`
--

CREATE TABLE `lmi_parts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_machine` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `working_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lmi_rework_parts`
--

CREATE TABLE `lmi_rework_parts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_machine` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `working_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Machines`
--

CREATE TABLE `Machines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nickname` varchar(45) NOT NULL,
  `description` varchar(256) NOT NULL,
  `brand` varchar(64) DEFAULT NULL,
  `model` varchar(64) DEFAULT NULL,
  `voltage` int NOT NULL,
  `amperage` float NOT NULL,
  `serie` varchar(45) DEFAULT NULL,
  `id_line` int NOT NULL,
  `manufacturing_date` datetime NOT NULL,
  `instalation_date` datetime NOT NULL,
  `id_supplier` int NOT NULL,
  `run_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Machine_PLCs`
--

CREATE TABLE `Machine_PLCs` (
  `id_machine` int NOT NULL,
  `id_plc` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Modules`
--

CREATE TABLE `Modules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand` varchar(64) NOT NULL,
  `model` varchar(64) NOT NULL,
  `n_in` int NOT NULL,
  `n_out` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `PLCs`
--

CREATE TABLE `PLCs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `n_in` int NOT NULL,
  `n_out` int NOT NULL,
  `ip` varchar(25) DEFAULT NULL,
  `net` varchar(25) DEFAULT NULL,
  `gateway` varchar(25) DEFAULT NULL,
  `model` varchar(64) NOT NULL,
  `brand` varchar(64) NOT NULL,
  `serie` varchar(45) NOT NULL,
  `id_module` int NOT NULL,
  `id_hub` int NOT NULL,
  `id_router` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Roles`
--

CREATE TABLE `Roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(256) NOT NULL,
  `access_level` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Routers`
--

CREATE TABLE `Routers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand` varchar(64) NOT NULL,
  `model` varchar(64) NOT NULL,
  `n_ports` int NOT NULL,
  `net_mask` varchar(25) DEFAULT NULL,
  `gateway` varchar(25) DEFAULT NULL,
  `mac_address` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `SubcalssComponents`
--

CREATE TABLE `SubcalssComponents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Suppliers`
--

CREATE TABLE `Suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `adress` varchar(80) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Users`
--

CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(64) NOT NULL,
  `id_rol` int NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `id_employee` varchar(45) NOT NULL,
  `cell_phone` varchar(20) DEFAULT NULL,
  `cubicle` varchar(5) NOT NULL,
  `ext` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Components`
--   ADD PRIMARY KEY (`id`,`id_plc`,`id_subclass`),
ALTER TABLE `Components`

  ADD KEY `fk_Components_SubcalssComponents1_idx` (`id_subclass`),
  ADD KEY `fk_Components_PLCs1_idx` (`id_plc`);

--
-- Indices de la tabla `Hubs`
--
-- ALTER TABLE `Hubs`
--   ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `Lines`
-- ADD PRIMARY KEY (`id`),
ALTER TABLE `Lines`
  ADD UNIQUE KEY `name_UNIQUE` (`name`),
  ADD KEY `fk_Lines_Users1_idx` (`id_user_in_charge`);

--
-- Indices de la tabla `lmi_maintenances`
-- ADD PRIMARY KEY (`id`),
ALTER TABLE `lmi_maintenances`
  ADD KEY `fk_lmi_maintenances_1` (`id_machine`),
  ADD KEY `fk_lmi_maintenances_2` (`id_maintenance_staff`);

--
-- Indices de la tabla `lmi_outofservice_machine`
-- ADD PRIMARY KEY (`id`),
ALTER TABLE `lmi_outofservice_machine`
  ADD KEY `fk_lmi_outofservice_machine_1` (`id_machine`);

--
-- Indices de la tabla `lmi_parts`
-- ADD PRIMARY KEY (`id`),
ALTER TABLE `lmi_parts`
  ADD KEY `fk_lmi_parts_1` (`id_machine`);

--
-- Indices de la tabla `lmi_rework_parts`
-- ADD PRIMARY KEY (`id`),
ALTER TABLE `lmi_rework_parts`
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `fk_lmi_rework_parts_1` (`id`),
  ADD KEY `fk_lmi_rework_parts_2` (`id_machine`);

--
-- Indices de la tabla `Machines`
-- ADD PRIMARY KEY (`id`,`id_line`,`id_supplier`),
ALTER TABLE `Machines`
  ADD KEY `fk_Machines_Lines1_idx` (`id_line`),
  ADD KEY `fk_Machines_Suppliers1_idx` (`id_supplier`);

--
-- Indices de la tabla `Machine_PLCs`
--
ALTER TABLE `Machine_PLCs`
  ADD PRIMARY KEY (`id_machine`,`id_plc`),
  ADD KEY `fk_Machine_PLCs_PLCs1_idx` (`id_plc`);

--
-- Indices de la tabla `Modules`
--
-- ALTER TABLE `Modules`
--   ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `PLCs`
-- ADD PRIMARY KEY (`id`),
ALTER TABLE `PLCs`
  ADD KEY `fk_PLCs_Modules1_idx` (`id_module`),
  ADD KEY `fk_PLCs_Hubs1_idx` (`id_hub`),
  ADD KEY `fk_PLCs_Routers1_idx` (`id_router`);

--
-- Indices de la tabla `Roles`
-- ADD PRIMARY KEY (`id`),
ALTER TABLE `Roles`
  ADD UNIQUE KEY `name_UNIQUE` (`name`);

--
-- Indices de la tabla `Routers`
--
-- ALTER TABLE `Routers`
--  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `SubcalssComponents`
--
-- ALTER TABLE `SubcalssComponents`
--   ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `Suppliers`
--  ADD PRIMARY KEY (`id`),
ALTER TABLE `Suppliers`
  ADD UNIQUE KEY `name_UNIQUE` (`name`);

--
-- Indices de la tabla `Users`
--  ADD PRIMARY KEY (`id`,`id_rol`),
ALTER TABLE `Users`
  ADD UNIQUE KEY `email_UNIQUE` (`email`),
  ADD UNIQUE KEY `id_employee_UNIQUE` (`id_employee`),
  ADD UNIQUE KEY `cubicle_UNIQUE` (`cubicle`),
  ADD UNIQUE KEY `cell_phone_UNIQUE` (`cell_phone`),
  ADD KEY `fk_Users_Roles1_idx` (`id_rol`);


--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Components`
--
ALTER TABLE `Components`
  ADD CONSTRAINT `fk_Components_PLCs1` FOREIGN KEY (`id_plc`) REFERENCES `PLCs` (`id`),
  ADD CONSTRAINT `fk_Components_SubcalssComponents1` FOREIGN KEY (`id_subclass`) REFERENCES `SubcalssComponents` (`id`);

--
-- Filtros para la tabla `Lines`
--
ALTER TABLE `Lines`
  ADD CONSTRAINT `fk_Lines_Users1` FOREIGN KEY (`id_user_in_charge`) REFERENCES `Users` (`id`);

--
-- Filtros para la tabla `lmi_maintenances`
--
ALTER TABLE `lmi_maintenances`
  ADD CONSTRAINT `fk_lmi_maintenances_1` FOREIGN KEY (`id_machine`) REFERENCES `Machines` (`id`),
  ADD CONSTRAINT `fk_lmi_maintenances_2` FOREIGN KEY (`id_maintenance_staff`) REFERENCES `Users` (`id`);

--
-- Filtros para la tabla `lmi_outofservice_machine`
--
ALTER TABLE `lmi_outofservice_machine`
  ADD CONSTRAINT `fk_lmi_outofservice_machine_1` FOREIGN KEY (`id_machine`) REFERENCES `Machines` (`id`);

--
-- Filtros para la tabla `lmi_parts`
--
ALTER TABLE `lmi_parts`
  ADD CONSTRAINT `fk_lmi_parts_1` FOREIGN KEY (`id_machine`) REFERENCES `Machines` (`id`);

--
-- Filtros para la tabla `lmi_rework_parts`
--
ALTER TABLE `lmi_rework_parts`
  ADD CONSTRAINT `fk_lmi_rework_parts_1` FOREIGN KEY (`id`) REFERENCES `lmi_parts` (`id`),
  ADD CONSTRAINT `fk_lmi_rework_parts_2` FOREIGN KEY (`id_machine`) REFERENCES `Machines` (`id`);

--
-- Filtros para la tabla `Machines`
--
ALTER TABLE `Machines`
  ADD CONSTRAINT `fk_Machines_Lines1` FOREIGN KEY (`id_line`) REFERENCES `Lines` (`id`),
  ADD CONSTRAINT `fk_Machines_Suppliers1` FOREIGN KEY (`id_supplier`) REFERENCES `Suppliers` (`id`);

--
-- Filtros para la tabla `Machine_PLCs`
--
ALTER TABLE `Machine_PLCs`
  ADD CONSTRAINT `fk_Machine_PLCs_Machines` FOREIGN KEY (`id_machine`) REFERENCES `Machines` (`id`),
  ADD CONSTRAINT `fk_Machine_PLCs_PLCs1` FOREIGN KEY (`id_plc`) REFERENCES `PLCs` (`id`);

--
-- Filtros para la tabla `PLCs`
--
ALTER TABLE `PLCs`
  ADD CONSTRAINT `fk_PLCs_Hubs1` FOREIGN KEY (`id_hub`) REFERENCES `Hubs` (`id`),
  ADD CONSTRAINT `fk_PLCs_Modules1` FOREIGN KEY (`id_module`) REFERENCES `Modules` (`id`),
  ADD CONSTRAINT `fk_PLCs_Routers1` FOREIGN KEY (`id_router`) REFERENCES `Routers` (`id`);

--
-- Filtros para la tabla `Users`
--
ALTER TABLE `Users`
  ADD CONSTRAINT `fk_Users_Roles1` FOREIGN KEY (`id_rol`) REFERENCES `Roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
