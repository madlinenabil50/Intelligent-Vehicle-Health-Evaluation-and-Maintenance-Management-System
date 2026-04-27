-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 27, 2026 at 02:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Admin_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `Appointment_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Vehicle_ID` int(11) DEFAULT NULL,
  `StartTime` datetime DEFAULT NULL,
  `Status` enum('Scheduled','Confirmed','In Progress','Completed','Cancelled') NOT NULL DEFAULT 'Scheduled',
  `service_type` varchar(500) DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`Appointment_ID`, `User_ID`, `Vehicle_ID`, `StartTime`, `Status`, `service_type`, `notes`) VALUES
(1, 2, 1, '2026-03-18 10:00:00', 'Completed', 'Oil Change & Filter', 'Regular maintenance'),
(2, 2, 2, '2026-03-19 14:00:00', 'Completed', 'Brake Inspection', 'Squeaky brakes'),
(18, 14, 12, '2026-03-20 09:00:00', 'Confirmed', 'Engine Diagnostics', 'Check engine light on'),
(19, 2, 2, '2026-03-19 12:00:00', 'Completed', 'Brake Inspection', ''),
(30, 2, 30, '2026-04-10 10:00:00', 'Confirmed', '', 'System integration test'),
(31, 2, 31, '2026-04-11 10:00:00', 'Cancelled', '', 'System integration test'),
(32, 2, 32, '2026-04-12 10:00:00', 'Confirmed', '', 'System integration test'),
(33, 2, 33, '2026-04-13 10:00:00', 'Completed', 'AC Service', 'System integration test'),
(34, 2, 34, '2026-04-14 10:00:00', 'Cancelled', '', 'System integration test'),
(35, 2, 35, '2026-04-15 10:00:00', 'Cancelled', '', 'System integration test'),
(36, 2, 36, '2026-04-16 10:00:00', 'Cancelled', '', 'System integration test'),
(37, 2, 37, '2026-04-17 10:00:00', 'Cancelled', '', 'System integration test'),
(38, 2, 38, '2026-04-18 10:00:00', 'Cancelled', '', 'System integration test'),
(39, 2, 39, '2026-04-19 10:00:00', 'Cancelled', '', 'System integration test'),
(42, 21, 41, '2026-03-25 09:00:00', 'Completed', 'Tyre Replacement', 'fixxxx'),
(43, 2, 39, '2026-04-07 16:00:00', 'Cancelled', '', ''),
(44, 2, 39, '2026-04-07 15:00:00', 'Cancelled', 'Battery Replacement, Inspection, Suspension Check', ''),
(45, 2, 1, '2026-04-16 16:00:00', 'Cancelled', 'Electrical System Check, Car Detailing', ''),
(46, 2, 39, '2026-04-07 18:00:00', 'Confirmed', 'Electrical System Check, Car Detailing', ''),
(47, 2, 42, '2026-04-09 10:00:00', 'Completed', 'Oil Change & Filter, Brake Inspection, Engine Diagnostics, Inspection, AC Service, Tyre Replacement', ''),
(48, 2, 43, '2026-04-09 10:00:00', 'Completed', 'Oil Change & Filter, Inspection', ''),
(49, 42, 44, '2026-04-10 10:00:00', 'Completed', 'Inspection', ''),
(50, 42, 44, '2026-04-09 19:00:00', 'Confirmed', 'Car Detailing, Electrical System Check, Wheel Alignment, Fuel System Cleaning, Transmission Service', ''),
(54, 2, 43, '2026-04-25 18:00:00', 'Cancelled', 'Oil Change & Filter', ''),
(55, 2, 43, '2026-04-25 18:00:00', 'Cancelled', 'Engine Diagnostics', ''),
(56, 2, 43, '2026-04-25 20:00:00', 'Cancelled', 'Electrical System Check', ''),
(57, 2, 43, '2026-04-25 21:00:00', 'Cancelled', 'Electrical System Check', ''),
(58, 2, 43, '2026-04-25 20:00:00', 'Cancelled', 'AC Service', ''),
(59, 2, 43, '2026-04-25 19:00:00', 'Cancelled', 'AC Service', ''),
(60, 2, 31, '2026-04-28 11:00:00', 'Cancelled', 'Car Wash', ''),
(61, 2, 42, '2026-04-28 15:00:00', 'Cancelled', 'Fuel System Cleaning', ''),
(62, 2, 3, '2026-04-27 08:00:00', 'Cancelled', 'Inspection, Suspension Check, Wheel Alignment', ''),
(63, 2, 47, '2026-04-27 09:00:00', 'Cancelled', 'Brake Inspection, AC Service, Car Wash', ''),
(64, 2, 47, '2026-04-27 08:00:00', 'Cancelled', 'AC Service, Suspension Check', ''),
(65, 2, 47, '2026-04-30 08:00:00', 'Cancelled', 'Suspension Check, Wheel Alignment', ''),
(66, 2, 47, '2026-04-27 09:00:00', 'Cancelled', 'Engine Diagnostics', ''),
(67, 2, 47, '2026-04-27 16:00:00', 'Cancelled', 'Oil Change & Filter, Tyre Replacement, Battery Replacement', ''),
(68, 2, 47, '2026-04-27 08:00:00', 'Cancelled', 'Car Wash, Fuel System Cleaning, Electrical System Check', ''),
(69, 2, 47, '2026-04-27 12:00:00', 'Cancelled', 'Oil Change & Filter', ''),
(70, 2, 39, '2026-04-27 08:00:00', 'Cancelled', 'Inspection, Engine Diagnostics, Transmission Service, Wheel Alignment', ''),
(71, 2, 43, '2026-04-27 12:00:00', 'Cancelled', 'Suspension Check, Tyre Replacement, Car Wash', ''),
(72, 2, 48, '2026-04-27 08:00:00', 'Cancelled', 'Tyre Replacement, Battery Replacement, Car Wash', ''),
(73, 2, 1, '2026-04-27 08:00:00', 'Confirmed', 'Car Wash, AC Service', '');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add admin', 7, 'add_admin'),
(26, 'Can change admin', 7, 'change_admin'),
(27, 'Can delete admin', 7, 'delete_admin'),
(28, 'Can view admin', 7, 'view_admin'),
(29, 'Can add appointment', 8, 'add_appointment'),
(30, 'Can change appointment', 8, 'change_appointment'),
(31, 'Can delete appointment', 8, 'delete_appointment'),
(32, 'Can view appointment', 8, 'view_appointment'),
(33, 'Can add certification', 9, 'add_certification'),
(34, 'Can change certification', 9, 'change_certification'),
(35, 'Can delete certification', 9, 'delete_certification'),
(36, 'Can view certification', 9, 'view_certification'),
(37, 'Can add inspection', 10, 'add_inspection'),
(38, 'Can change inspection', 10, 'change_inspection'),
(39, 'Can delete inspection', 10, 'delete_inspection'),
(40, 'Can view inspection', 10, 'view_inspection'),
(41, 'Can add inventoryitem', 11, 'add_inventoryitem'),
(42, 'Can change inventoryitem', 11, 'change_inventoryitem'),
(43, 'Can delete inventoryitem', 11, 'delete_inventoryitem'),
(44, 'Can view inventoryitem', 11, 'view_inventoryitem'),
(45, 'Can add invoice', 12, 'add_invoice'),
(46, 'Can change invoice', 12, 'change_invoice'),
(47, 'Can delete invoice', 12, 'delete_invoice'),
(48, 'Can view invoice', 12, 'view_invoice'),
(49, 'Can add jobcard', 13, 'add_jobcard'),
(50, 'Can change jobcard', 13, 'change_jobcard'),
(51, 'Can delete jobcard', 13, 'delete_jobcard'),
(52, 'Can view jobcard', 13, 'view_jobcard'),
(53, 'Can add jobcardparts', 14, 'add_jobcardparts'),
(54, 'Can change jobcardparts', 14, 'change_jobcardparts'),
(55, 'Can delete jobcardparts', 14, 'delete_jobcardparts'),
(56, 'Can view jobcardparts', 14, 'view_jobcardparts'),
(57, 'Can add payment', 15, 'add_payment'),
(58, 'Can change payment', 15, 'change_payment'),
(59, 'Can delete payment', 15, 'delete_payment'),
(60, 'Can view payment', 15, 'view_payment'),
(61, 'Can add timelog', 16, 'add_timelog'),
(62, 'Can change timelog', 16, 'change_timelog'),
(63, 'Can delete timelog', 16, 'delete_timelog'),
(64, 'Can view timelog', 16, 'view_timelog'),
(65, 'Can add topmanager', 17, 'add_topmanager'),
(66, 'Can change topmanager', 17, 'change_topmanager'),
(67, 'Can delete topmanager', 17, 'delete_topmanager'),
(68, 'Can view topmanager', 17, 'view_topmanager'),
(69, 'Can add vehicle', 18, 'add_vehicle'),
(70, 'Can change vehicle', 18, 'change_vehicle'),
(71, 'Can delete vehicle', 18, 'delete_vehicle'),
(72, 'Can view vehicle', 18, 'view_vehicle'),
(73, 'Can add technician', 19, 'add_technician'),
(74, 'Can change technician', 19, 'change_technician'),
(75, 'Can delete technician', 19, 'delete_technician'),
(76, 'Can view technician', 19, 'view_technician'),
(77, 'Can add financemanager', 20, 'add_financemanager'),
(78, 'Can change financemanager', 20, 'change_financemanager'),
(79, 'Can delete financemanager', 20, 'delete_financemanager'),
(80, 'Can view financemanager', 20, 'view_financemanager'),
(81, 'Can add client', 21, 'add_client'),
(82, 'Can change client', 21, 'change_client'),
(83, 'Can delete client', 21, 'delete_client'),
(84, 'Can view client', 21, 'view_client'),
(85, 'Can add stockkeeper', 22, 'add_stockkeeper'),
(86, 'Can change stockkeeper', 22, 'change_stockkeeper'),
(87, 'Can delete stockkeeper', 22, 'delete_stockkeeper'),
(88, 'Can view stockkeeper', 22, 'view_stockkeeper'),
(89, 'Can add dataanalyst', 23, 'add_dataanalyst'),
(90, 'Can change dataanalyst', 23, 'change_dataanalyst'),
(91, 'Can delete dataanalyst', 23, 'delete_dataanalyst'),
(92, 'Can view dataanalyst', 23, 'view_dataanalyst'),
(93, 'Can add servicemanager', 24, 'add_servicemanager'),
(94, 'Can change servicemanager', 24, 'change_servicemanager'),
(95, 'Can delete servicemanager', 24, 'delete_servicemanager'),
(96, 'Can view servicemanager', 24, 'view_servicemanager'),
(97, 'Can add users', 25, 'add_users'),
(98, 'Can change users', 25, 'change_users'),
(99, 'Can delete users', 25, 'delete_users'),
(100, 'Can view users', 25, 'view_users'),
(101, 'Can add supplier', 26, 'add_supplier'),
(102, 'Can change supplier', 26, 'change_supplier'),
(103, 'Can delete supplier', 26, 'delete_supplier'),
(104, 'Can view supplier', 26, 'view_supplier'),
(105, 'Can add supplier part', 27, 'add_supplierpart'),
(106, 'Can change supplier part', 27, 'change_supplierpart'),
(107, 'Can delete supplier part', 27, 'delete_supplierpart'),
(108, 'Can view supplier part', 27, 'view_supplierpart'),
(109, 'Can add purchase order', 28, 'add_purchaseorder'),
(110, 'Can change purchase order', 28, 'change_purchaseorder'),
(111, 'Can delete purchase order', 28, 'delete_purchaseorder'),
(112, 'Can view purchase order', 28, 'view_purchaseorder');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `certification`
--

CREATE TABLE `certification` (
  `Certification_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Vehicle_ID` int(11) DEFAULT NULL,
  `Inspection_ID` int(11) DEFAULT NULL,
  `IssueDate` date DEFAULT NULL,
  `Next_Maint_Date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `Client_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `RegistrationDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`Client_ID`, `User_ID`, `RegistrationDate`) VALUES
(2, 2, '2024-02-15'),
(7, 21, '2026-04-09'),
(8, 42, '2026-04-09');

-- --------------------------------------------------------

--
-- Table structure for table `dataanalyst`
--

CREATE TABLE `dataanalyst` (
  `DataAnalyst_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'core', 'admin'),
(8, 'core', 'appointment'),
(9, 'core', 'certification'),
(21, 'core', 'client'),
(23, 'core', 'dataanalyst'),
(20, 'core', 'financemanager'),
(10, 'core', 'inspection'),
(11, 'core', 'inventoryitem'),
(12, 'core', 'invoice'),
(13, 'core', 'jobcard'),
(14, 'core', 'jobcardparts'),
(15, 'core', 'payment'),
(28, 'core', 'purchaseorder'),
(24, 'core', 'servicemanager'),
(22, 'core', 'stockkeeper'),
(26, 'core', 'supplier'),
(27, 'core', 'supplierpart'),
(19, 'core', 'technician'),
(16, 'core', 'timelog'),
(17, 'core', 'topmanager'),
(25, 'core', 'users'),
(18, 'core', 'vehicle'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-03-17 17:56:21.854304'),
(2, 'auth', '0001_initial', '2026-03-17 17:56:22.346196'),
(3, 'admin', '0001_initial', '2026-03-17 17:56:22.454788'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-03-17 17:56:22.465624'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-03-17 17:56:22.475080'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-03-17 17:56:22.544254'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-03-17 17:56:22.597085'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-03-17 17:56:22.614311'),
(9, 'auth', '0004_alter_user_username_opts', '2026-03-17 17:56:22.623695'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-03-17 17:56:22.679667'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-03-17 17:56:22.688051'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-03-17 17:56:22.697711'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-03-17 17:56:22.716486'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-03-17 17:56:22.734465'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-03-17 17:56:22.753273'),
(16, 'auth', '0011_update_proxy_permissions', '2026-03-17 17:56:22.763760'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-03-17 17:56:22.776423'),
(18, 'sessions', '0001_initial', '2026-03-17 17:56:22.803975'),
(19, 'core', '0001_initial', '2026-04-07 16:45:58.888836'),
(20, 'core', '0002_supplierpart', '2026-04-07 17:18:09.113316'),
(21, 'core', '0003_alter_supplierpart_price', '2026-04-07 18:01:48.778582'),
(22, 'core', '0004_purchaseorder', '2026-04-07 18:18:00.689710');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('487regon5ajahkxy3dtofg3d1dkr2ade', '.eJw1yTEKgDAMRuGryD8XwbWTN5HYRg2kqUQ7iXcXBafH47vQDnbE6-skGXEI4EKiiChk5OP6Xp9qQYBR4R86mjPrRlkQ4FVfODltJknIELB7XUR52iWdzRnRmup9P-1GKDc:1wADgc:-G8BEcUo0YvGanqtsGOOtARnjCJd06z2QGOVM6IqFyI', '2026-04-08 21:10:14.762141'),
('5ph2milge7sdg6wtm8so8vu8b1e5h1m4', 'eyJ1c2VyIjp7InVzZXJfaWQiOjEsInJvbGUiOiJhZG1pbiIsImVtYWlsIjoiYUBhLmNvbSJ9fQ:1wAvHv:GoEm1RLOKMKEERZMQKRo5zwASO4O9DSzwDXzPziV35Q', '2026-04-10 19:43:39.926715'),
('6er3bvcrk9nxtgulwl3i64kl6g6cpb9p', '.eJwdyDEKhEAMRuGrLH89a7VVKm9gsQeQMBslkMxIdAQR775o9fjeibZKgM6no_5AnwRxVgOhOkc_3-hydSQUdgFhcI7Xl_1AQlS71yqxa5a3c-FZAglL1ElNxkXz1kJApZld1x-MkydJ:1w2aoM:4cs9g-m5EeY8QrEym4IMpqOQhMi45Z-d4Gupd4nsVWU', '2026-03-18 20:14:42.084918'),
('8suisb1fjcnk7tleie54mh7w6hhts4af', '.eJyrViotTi1SsqoG0_GZKUpWRjpKqbmJmTlKVkoFiaU5icWJuZWmRg7pIDG95PxcJR2lvMTcVCUrpQCQtEJwYm6lko5SUX4OSMw5JzM1r0SpthYAV9Ad5Q:1wFEzC:QyUqMZA-4o36eyHpDJ5oLYw4lpiUC58aVqVWacN_T2g', '2026-04-22 17:34:10.088989'),
('amc63nkqrh0q6bo0ptvs3ka5p3hfy5vp', '.eJwlyTsOgCAQRdGtmKmNjR2VvXENhMAokwyfIFSEvTtq9fLO7dBuLKD6t5ocqHUGDIYYFITkTUC3Xe9fbAowQxSRdPxp2r1hdOIl8esVrY9kyUSxXNJJjDqTra1Ijo15jAcR8ihs:1w2d51:lUL4_EoGVDyluFt_KRk3qhjTPsbFieNG_DkkQtAZBu8', '2026-03-18 22:40:03.512106'),
('bcrpkwjc45g7ekyt2fo8esgihri9h3ri', '.eJwtjUEKwyAQRa9S_lpiGlIEVz1CoQeQIZkGi0Zx4iKE3L0Yuvrw3oN_oAoX2ONa52fYQYEj-QCLTDWQUNwfw3NprJtShMJKkWHxavr2prhDoaTQ2BQ8rxsUckkfH9hlP221NKVJhDfRNYdEs-h_Ifq6HtzdGNOb0Yx998284Dx_kSg1eQ:1wGnVd:5INkFb_t0Fd4vQDO4nSSrRbPm7rI913jGS9cgPhMOP4', '2026-04-27 00:38:05.114425'),
('fpg6f5m4l8b12hhy3wgw253z4rbqo6op', '.eJwdzMEKg0AMBNBfKXPe9irsyR9of0GCbnUh2SzRnMR_b-xpmDcwJ3wvhnz-c6oL8pBQhCojo6nbuN7lNasgoZGU8E_4402bqC-hpnzrof0p1GiNw4Ru-q1cpl7nwy325szX9QNzdicJ:1wAbOv:C3TgBPsNblHjTsg6rcKA7sRW6Eb8olYBBgn55ppD_fQ', '2026-04-09 22:29:33.492232'),
('g12xvidqjsjln2n67chste239294qejl', '.eJw1yTEKgDAMRuGryD8XwbWTN5HYRg2kqUQ7iXcXBafH47vQDnbE6-skGXEI4EKiiChk5OP6Xp9qQYBR4R86mjPrRlkQ4FVfODltJknIELB7XUR52iWdzRnRmup9P-1GKDc:1wGRh4:sZVaiMS_zuluUCJM2u-t94WY8EWKUk4CwXXnMZ8P8yE', '2026-04-26 01:20:26.423335'),
('k41l7mkhwxzlxz8x6fj5a6jdw5qytpxq', '.eJwdijEKwCAQwP6SWQpdb2pfUqTeIHgKaifx70WnkJDB17QiY_OJATkdaj4mBB8s5qtr68dbDEf2pgj36jhqSUv3xpw_4vEZVQ:1wFF76:aDDAN5yrZ2jTBPtijsElZWEdbsw-3g-G4cueA_tMXeA', '2026-04-22 17:42:20.660970'),
('royjg8tb710sg8v7pzatehr11ntghufw', '.eJwlyDEKwCAMBdCrlD9Lty6Zegj3ImnAgFHQdBLvXminB2_iGdJB8_PSG3QEiCUtILhwPl2G79wMATWZgBBl-BaFMwJ6K39xrsqaKtZ6AblDHDw:1wFF6E:hhtY_HwGGiiLY62afaW4S_Ro0A4xg88S46eMwZKD6ug', '2026-04-22 17:41:26.523532'),
('rr0inzjvsywjkvwhlbfmisvjnoc05mis', '.eJwlyDEKwCAMBdCrlD9Lty6Zegj3ImnAgFHQdBLvXminB2_iGdJB8_PSG3QEiCUtILhwPl2G79wMATWZgBBl-BaFMwJ6K39xrsqaKtZ6AblDHDw:1wFF6q:U1Vb5xbC5D3-foOxsYROOQTvioknFVYQz1ePtHMzkro', '2026-04-22 17:42:04.345311'),
('v0zcpezwoqigglq9cfkkk0lp4ymqnku3', '.eJw1yTEKgDAMRuGryD8XB3Hq5E1KsFGCSVuqncS7SwWnB9-70U6u8PfXIBF-nhzYSBQeRkpHOEnisnca12xwSGT836FfONSs3SiaJDiUmjdRDkXWq1WGT031eV5GbCZg:1wFGN4:DDMc6ijQiPnML0TfXl9cEmE-Wz3HPeNc8VMOOyeG8vI', '2026-04-22 19:02:54.852530'),
('w5bpwbyew8exz5gqxffny49ixttql7b3', '.eJwtyDEKgDAMRuGryD8XJxc7eZNS2qiBtCnRTuLdRXF6vO9CP8jgr6-BM_w0O1CJLPCoqrZs74xJCxxqLPT7EPdCGQ6m8loSpnrCoZmuLBQap7Mbwdcuct8PhNYkqw:1wFE2I:qcAH2dF-qkuWpVNrBTCvXItAw2PkfKaY4h5-Fnj_apA', '2026-04-22 16:33:18.729883'),
('xavtu50bj6njuuez7wky0etgop64n68n', '.eJw1yTEKgDAMRuGryD8XB3Hq5E1KsFGCSVuqncS7SwWnB9-70U6u8PfXIBF-nhzYSBQeRkpHOEnisnca12xwSGT836FfONSs3SiaJDiUmjdRDkXWq1WGT031eV5GbCZg:1wFEvM:PyZlDEpYpVwK2dwb78k9r6omacYaitI173JqrM8z0-4', '2026-04-22 17:30:12.810860');

-- --------------------------------------------------------

--
-- Table structure for table `financemanager`
--

CREATE TABLE `financemanager` (
  `FinanceManager_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `financemanager`
--

INSERT INTO `financemanager` (`FinanceManager_ID`, `User_ID`) VALUES
(1, 5),
(3, 48);

-- --------------------------------------------------------

--
-- Table structure for table `inspection`
--

CREATE TABLE `inspection` (
  `Inspection_ID` int(11) NOT NULL,
  `Vehicle_ID` int(11) DEFAULT NULL,
  `JobCard_ID` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `HealthScore` int(11) DEFAULT NULL,
  `HealthCategory` varchar(50) DEFAULT NULL,
  `Results` text DEFAULT NULL,
  `DiagnosticData` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inspection`
--

INSERT INTO `inspection` (`Inspection_ID`, `Vehicle_ID`, `JobCard_ID`, `Date`, `HealthScore`, `HealthCategory`, `Results`, `DiagnosticData`) VALUES
(7, 2, 11, '2026-03-18', 99, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Fair\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(10, 41, 15, '2026-03-19', 97, 'Excellent', '', '{\"td1\": \"Poor\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Fair\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(11, 12, 12, '2026-04-07', 98, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Poor\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(12, 12, 12, '2026-04-07', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(13, 12, 12, '2026-04-07', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(14, 12, 12, '2026-04-07', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(15, 41, 15, '2026-04-07', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(16, 12, 12, '2026-04-07', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(17, 12, 12, '2026-04-07', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(18, 2, 16, '2026-04-08', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(19, 42, 17, '2026-04-08', 78, 'Operational', 'check now', '{\"td1\": \"Fair\", \"td2\": \"Fair\", \"td3\": \"Fair\", \"td4\": \"Fair\", \"td5\": \"Fair\", \"td6\": \"Fair\", \"td7\": \"Fair\", \"td8\": \"Fair\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Poor\", \"el2\": \"Poor\", \"el3\": \"Poor\", \"el4\": \"Poor\", \"el5\": \"Poor\", \"el6\": \"Poor\", \"el7\": \"Poor\", \"el8\": \"Poor\", \"el9\": \"Poor\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(20, 43, 18, '2026-04-09', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(21, 43, 18, '2026-04-09', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(22, 43, 18, '2026-04-09', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(23, 43, 18, '2026-04-09', 100, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Good\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(24, 44, 19, '2026-04-09', 98, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Fair\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Fair\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Good\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}'),
(28, 33, 23, '2026-04-27', 97, 'Excellent', '', '{\"td1\": \"Good\", \"td2\": \"Good\", \"td3\": \"Good\", \"td4\": \"Good\", \"td5\": \"Good\", \"td6\": \"Good\", \"td7\": \"Fair\", \"td8\": \"Good\", \"ex1\": \"Good\", \"ex2\": \"Good\", \"ex3\": \"Poor\", \"ex4\": \"Good\", \"ex5\": \"Good\", \"ex6\": \"Good\", \"ex7\": \"Good\", \"el1\": \"Good\", \"el2\": \"Good\", \"el3\": \"Good\", \"el4\": \"Good\", \"el5\": \"Good\", \"el6\": \"Good\", \"el7\": \"Good\", \"el8\": \"Good\", \"el9\": \"Good\", \"uh1\": \"Good\", \"uh2\": \"Good\", \"uh3\": \"Good\", \"uh4\": \"Good\", \"uh5\": \"Good\", \"uh6\": \"Good\", \"in1\": \"Good\", \"in2\": \"Good\", \"in3\": \"Good\", \"in4\": \"Good\", \"in5\": \"Good\", \"in6\": \"Good\", \"in7\": \"Good\", \"in8\": \"Good\", \"bb1\": \"Good\", \"bb2\": \"Good\", \"bb3\": \"Good\", \"bb4\": \"Good\", \"bb5\": \"Good\"}');

-- --------------------------------------------------------

--
-- Table structure for table `inventoryitem`
--

CREATE TABLE `inventoryitem` (
  `Item_ID` int(11) NOT NULL,
  `ItemNumber` int(11) DEFAULT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `UnitPrice` int(11) DEFAULT NULL,
  `StockQty` int(11) DEFAULT NULL,
  `MinStockLevel` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventoryitem`
--

INSERT INTO `inventoryitem` (`Item_ID`, `ItemNumber`, `User_ID`, `Name`, `UnitPrice`, `StockQty`, `MinStockLevel`) VALUES
(34, 2277, 6, '3/15 AGM Battery', 9810, 21, 10),
(36, 2279, 6, '3/15 Wiper Blades', 2120, 21, 10),
(37, 2280, 6, '3/15 Air Filter', 1760, 39, 10),
(38, 2281, 6, '3/15 Front Brake Pads', 6170, 33, 10),
(39, 2282, 6, '3/15 Spark Plugs (Set)', 3350, 25, 10),
(40, 2283, 6, '303 Front Brake Pads', 5220, 19, 10),
(41, 2284, 6, '303 Air Filter', 1260, 21, 10),
(42, 2285, 6, '303 Cabin Microfilter', 2220, 19, 10),
(43, 2286, 6, '315 Spark Plugs (Set)', 2570, 33, 10),
(44, 2287, 6, '315 Wiper Blades', 2500, 34, 10),
(45, 2288, 6, '315 Cabin Microfilter', 2320, 45, 10),
(46, 2289, 6, '319 Oil Filter', 1690, 13, 10),
(47, 2290, 6, '319 Wiper Blades', 2480, 30, 10),
(48, 2291, 6, '319 Spark Plugs (Set)', 2550, 35, 10),
(49, 2292, 6, '319 Cabin Microfilter', 2690, 16, 10),
(50, 2293, 6, '319 Rear Brake Pads', 2880, 16, 10),
(51, 2294, 6, '319 AGM Battery', 13500, 35, 10),
(52, 2295, 6, '319 Front Brake Pads', 6120, 29, 10),
(53, 2296, 6, '319 Air Filter', 2180, 45, 10),
(54, 2297, 6, '326 Wiper Blades', 2840, 14, 10),
(55, 2298, 6, '326 Cabin Microfilter', 1420, 50, 10),
(56, 2299, 6, '326 AGM Battery', 14340, 1000, 10),
(57, 2300, 6, '326 Oil Filter', 840, 17, 10),
(58, 2301, 6, '326 Spark Plugs (Set)', 3390, 14, 10),
(59, 2302, 6, '326 Rear Brake Pads', 4650, 40, 10),
(60, 2303, 6, '326 Air Filter', 1980, 49, 10),
(61, 2304, 6, '326 Front Brake Pads', 5840, 31, 10),
(62, 2305, 6, '327 AGM Battery', 9740, 70, 10),
(63, 2306, 6, '327 Wiper Blades', 3270, 25, 10),
(64, 2307, 6, '327 Rear Brake Pads', 4060, 26, 10),
(65, 2308, 6, '327 Air Filter', 2240, 43, 10),
(66, 2309, 6, '327 Oil Filter', 1160, 27, 10),
(67, 2310, 6, '327 Spark Plugs (Set)', 4240, 26, 10),
(68, 2311, 6, '328 Front Brake Pads', 3700, 13, 10),
(69, 2312, 6, '328 Cabin Microfilter', 2530, 35, 10),
(70, 2313, 6, '328 Air Filter', 1690, 10, 10),
(71, 2314, 6, '328 Wiper Blades', 3100, 27, 10),
(72, 2315, 6, '328 Spark Plugs (Set)', 2790, 27, 10),
(73, 2316, 6, '328 AGM Battery', 13020, 8, 10),
(74, 2317, 6, '328 Oil Filter', 1630, 9, 10),
(75, 2318, 6, '335 Wiper Blades', 2140, 9, 10),
(76, 2319, 6, '335 Oil Filter', 1760, 23, 10),
(77, 2320, 6, '335 Cabin Microfilter', 1290, 13, 10),
(78, 2321, 6, '335 Spark Plugs (Set)', 3080, 47, 10),
(79, 2322, 6, '335 Front Brake Pads', 5480, 5, 10),
(80, 2323, 6, '335 Air Filter', 2020, 36, 10),
(81, 2324, 6, '335 Rear Brake Pads', 4050, 49, 10),
(82, 2325, 6, '335 AGM Battery', 11820, 38, 10),
(83, 2326, 6, '340 AGM Battery', 12110, 45, 10),
(84, 2327, 6, '340 Cabin Microfilter', 2680, 17, 10),
(85, 2328, 6, '340 Oil Filter', 1040, 13, 10),
(86, 2329, 6, '340 Wiper Blades', 1760, 9, 10),
(87, 2330, 6, '340 Front Brake Pads', 3950, 27, 10),
(88, 2331, 6, '340 Spark Plugs (Set)', 3290, 17, 10),
(89, 2332, 6, '340 Air Filter', 2120, 5, 10),
(90, 2333, 6, '501 Spark Plugs (Set)', 3190, 50, 10),
(91, 2334, 6, '501 Front Brake Pads', 7120, 46, 10),
(92, 2335, 6, '501 Wiper Blades', 1830, 41, 10),
(93, 2336, 6, '501 Air Filter', 1840, 23, 10),
(94, 2337, 6, '501 Rear Brake Pads', 3410, 50, 10),
(95, 2338, 6, '502 Spark Plugs (Set)', 2340, 43, 10),
(96, 2339, 6, '502 Oil Filter', 1080, 11, 10),
(97, 2340, 6, '502 Front Brake Pads', 3480, 18, 10),
(98, 2341, 6, '502 Wiper Blades', 2450, 13, 10),
(99, 2342, 6, '503 Oil Filter', 1670, 30, 10),
(100, 2343, 6, '503 AGM Battery', 11580, 16, 10),
(101, 2344, 6, '503 Wiper Blades', 2530, 42, 10),
(102, 2345, 6, '503 Cabin Microfilter', 2690, 50, 10),
(103, 2346, 6, '503 Front Brake Pads', 7070, 44, 10),
(104, 2347, 6, '503 Air Filter', 2230, 30, 10),
(105, 2348, 6, '503 Spark Plugs (Set)', 4300, 17, 10),
(106, 2349, 6, '507 Wiper Blades', 2290, 16, 10),
(107, 2350, 6, '507 AGM Battery', 12670, 29, 10),
(108, 2351, 6, '507 Rear Brake Pads', 4700, 47, 10),
(109, 2352, 6, '507 Oil Filter', 1720, 6, 10),
(110, 2353, 6, '507 Spark Plugs (Set)', 3170, 7, 10),
(111, 2354, 6, '507 Air Filter', 1410, 42, 10),
(112, 2355, 6, '507 Front Brake Pads', 6100, 13, 10),
(113, 2356, 6, 'Isetta Spark Plugs (Set)', 2240, 10, 10),
(114, 2357, 6, 'Isetta Wiper Blades', 2020, 20, 10),
(115, 2358, 6, 'Isetta Front Brake Pads', 4300, 29, 10),
(116, 2359, 6, 'Isetta Oil Filter', 1200, 47, 10),
(117, 2360, 6, 'Isetta Cabin Microfilter', 1990, 40, 10),
(118, 2361, 6, 'Isetta Rear Brake Pads', 6570, 47, 10),
(119, 2362, 6, '600 Front Brake Pads', 7840, 16, 10),
(120, 2363, 6, '600 Wiper Blades', 2510, 46, 10),
(121, 2364, 6, '600 Cabin Microfilter', 2570, 21, 10),
(122, 2365, 6, '600 Oil Filter', 980, 34, 10),
(123, 2366, 6, '700 Rear Brake Pads', 7130, 17, 10),
(124, 2367, 6, '700 AGM Battery', 12610, 30, 10),
(125, 2368, 6, '700 Front Brake Pads', 6920, 33, 10),
(126, 2369, 6, '700 Wiper Blades', 2780, 11, 10),
(127, 2370, 6, '700 Oil Filter', 1480, 24, 10),
(128, 2371, 6, '1500 AGM Battery', 14550, 43, 10),
(129, 2372, 6, '1500 Spark Plugs (Set)', 4040, 36, 10),
(130, 2373, 6, '1500 Wiper Blades', 2440, 46, 10),
(131, 2374, 6, '1500 Rear Brake Pads', 6830, 42, 10),
(132, 2375, 6, '1500 Cabin Microfilter', 2420, 11, 10),
(133, 2376, 6, '1500 Oil Filter', 1610, 28, 10),
(134, 2377, 6, '1600 Air Filter', 1720, 17, 10),
(135, 2378, 6, '1600 Wiper Blades', 1630, 24, 10),
(136, 2379, 6, '1600 Spark Plugs (Set)', 2770, 8, 10),
(137, 2380, 6, '1600 Cabin Microfilter', 1400, 37, 10),
(138, 2381, 6, '1800 Wiper Blades', 3230, 49, 10),
(139, 2382, 6, '1800 Air Filter', 2010, 38, 10),
(140, 2383, 6, '1800 AGM Battery', 10590, 21, 10),
(141, 2384, 6, '1800 Rear Brake Pads', 4450, 36, 10),
(142, 2385, 6, '2000 Front Brake Pads', 6430, 37, 10),
(143, 2386, 6, '2000 AGM Battery', 12380, 33, 10),
(144, 2387, 6, '2000 Air Filter', 2110, 47, 10),
(145, 2388, 6, '2000 Rear Brake Pads', 5940, 20, 10),
(146, 2389, 6, '2000 Wiper Blades', 2920, 21, 10),
(147, 2390, 6, '2000 Oil Filter', 1010, 16, 10),
(148, 2391, 6, '2000 Cabin Microfilter', 2230, 34, 10),
(149, 2392, 6, '2002 Air Filter', 2110, 9, 10),
(150, 2393, 6, '2002 Oil Filter', 1130, 38, 10),
(151, 2394, 6, '2002 Front Brake Pads', 6160, 10, 10),
(152, 2395, 6, '2002 Cabin Microfilter', 2390, 16, 10),
(153, 2396, 6, '2002 Spark Plugs (Set)', 2320, 21, 10),
(154, 2397, 6, '2002 Rear Brake Pads', 4370, 22, 10),
(155, 2398, 6, 'E3 Front Brake Pads', 6000, 15, 10),
(156, 2399, 6, 'E3 AGM Battery', 10970, 23, 10),
(157, 2400, 6, 'E3 Wiper Blades', 1860, 11, 10),
(158, 2401, 6, 'E9 Rear Brake Pads', 3390, 24, 10),
(159, 2402, 6, 'E9 Front Brake Pads', 5200, 8, 10),
(160, 2403, 6, 'E9 Wiper Blades', 3220, 22, 10),
(161, 2404, 6, 'E9 Cabin Microfilter', 2290, 21, 10),
(162, 2405, 6, 'E9 Spark Plugs (Set)', 2280, 25, 10),
(163, 2406, 6, 'E9 Oil Filter', 1240, 28, 10),
(164, 2407, 6, '1 Series Wiper Blades', 2010, 35, 10),
(165, 2408, 6, '1 Series Spark Plugs (Set)', 3390, 20, 10),
(166, 2409, 6, '1 Series AGM Battery', 9260, 18, 10),
(167, 2410, 6, '1 Series Oil Filter', 1150, 21, 10),
(168, 2411, 6, '1 Series Cabin Microfilter', 2510, 48, 10),
(169, 2412, 6, '2 Series Cabin Microfilter', 1330, 14, 10),
(170, 2413, 6, '2 Series Wiper Blades', 3110, 48, 10),
(171, 2414, 6, '2 Series Front Brake Pads', 4700, 29, 10),
(172, 2415, 6, '2 Series AGM Battery', 10020, 8, 10),
(173, 2416, 6, '2 Series Air Filter', 1210, 46, 10),
(174, 2417, 6, '3 Series Rear Brake Pads', 6160, 24, 10),
(175, 2418, 6, '3 Series Cabin Microfilter', 2350, 10, 10),
(176, 2419, 6, '3 Series Front Brake Pads', 5060, 19, 10),
(177, 2420, 6, '4 Series Oil Filter', 1330, 40, 10),
(178, 2421, 6, '4 Series AGM Battery', 9290, 39, 10),
(179, 2422, 6, '4 Series Cabin Microfilter', 1460, 5, 10),
(180, 2423, 6, '5 Series Spark Plugs (Set)', 2280, 29, 10),
(181, 2424, 6, '5 Series Rear Brake Pads', 4510, 30, 10),
(182, 2425, 6, '5 Series AGM Battery', 8490, 26, 10),
(183, 2426, 6, '5 Series Air Filter', 2020, 40, 10),
(184, 2427, 6, '5 Series Wiper Blades', 1740, 30, 10),
(185, 2428, 6, '5 Series Oil Filter', 800, 45, 10),
(186, 2429, 6, '6 Series Air Filter', 1930, 5, 10),
(187, 2430, 6, '6 Series Wiper Blades', 1880, 28, 10),
(188, 2431, 6, '6 Series AGM Battery', 14370, 48, 10),
(189, 2432, 6, '7 Series Wiper Blades', 2540, 30, 10),
(190, 2433, 6, '7 Series Rear Brake Pads', 5300, 19, 10),
(191, 2434, 6, '7 Series AGM Battery', 10360, 23, 10),
(192, 2435, 6, '8 Series Spark Plugs (Set)', 3450, 27, 10),
(193, 2436, 6, '8 Series Wiper Blades', 1910, 47, 10),
(194, 2437, 6, '8 Series Oil Filter', 830, 11, 10),
(195, 2438, 6, '1 Series Wiper Blades', 2230, 42, 10),
(196, 2439, 6, '1 Series Front Brake Pads', 4300, 13, 10),
(197, 2440, 6, '1 Series AGM Battery', 8970, 6, 10),
(198, 2441, 6, '1 Series Spark Plugs (Set)', 2350, 48, 10),
(199, 2442, 6, '1 Series Cabin Microfilter', 2580, 8, 10),
(200, 2443, 6, '1 Series Oil Filter', 1420, 32, 10),
(201, 2444, 6, '1 Series Air Filter', 2100, 11, 10),
(202, 2445, 6, '2 Series Cabin Microfilter', 2300, 13, 10),
(203, 2446, 6, '2 Series AGM Battery', 14110, 33, 10),
(204, 2447, 6, '2 Series Oil Filter', 1050, 19, 10),
(205, 2448, 6, '3 Series Wiper Blades', 3200, 12, 10),
(206, 2449, 6, '3 Series AGM Battery', 10420, 46, 10),
(207, 2450, 6, '3 Series Front Brake Pads', 7620, 46, 10),
(208, 2451, 6, '4 Series Cabin Microfilter', 2530, 38, 10),
(209, 2452, 6, '4 Series AGM Battery', 13120, 7, 10),
(210, 2453, 6, '4 Series Spark Plugs (Set)', 4050, 46, 10),
(211, 2454, 6, '5 Series Spark Plugs (Set)', 3280, 28, 10),
(212, 2455, 6, '5 Series Front Brake Pads', 4540, 49, 10),
(213, 2456, 6, '5 Series Wiper Blades', 1660, 7, 10),
(214, 2457, 6, '5 Series Oil Filter', 1530, 46, 10),
(215, 2458, 6, '5 Series Air Filter', 1720, 26, 10),
(216, 2459, 6, '5 Series Cabin Microfilter', 2380, 50, 10),
(217, 2460, 6, '5 Series AGM Battery', 11950, 35, 10),
(218, 2461, 6, '6 Series Cabin Microfilter', 1730, 25, 10),
(219, 2462, 6, '6 Series Wiper Blades', 1760, 6, 10),
(220, 2463, 6, '6 Series Front Brake Pads', 8160, 12, 10),
(221, 2464, 6, '6 Series Rear Brake Pads', 6230, 17, 10),
(222, 2465, 6, '6 Series Oil Filter', 1640, 16, 10),
(223, 2466, 6, '6 Series Spark Plugs (Set)', 2080, 25, 10),
(224, 2467, 6, '6 Series Air Filter', 1240, 44, 10),
(225, 2468, 6, '7 Series Rear Brake Pads', 7060, 7, 10),
(226, 2469, 6, '7 Series AGM Battery', 9750, 44, 10),
(227, 2470, 6, '7 Series Oil Filter', 1730, 16, 10),
(228, 2471, 6, '8 Series Rear Brake Pads', 4850, 25, 10),
(229, 2472, 6, '8 Series Air Filter', 1580, 36, 10),
(230, 2473, 6, '8 Series Front Brake Pads', 4740, 34, 10),
(231, 2474, 6, '1 Series Front Brake Pads', 7840, 44, 10),
(232, 2475, 6, '1 Series Spark Plugs (Set)', 2800, 8, 10),
(233, 2476, 6, '1 Series Oil Filter', 1630, 31, 10),
(234, 2477, 6, '1 Series Cabin Microfilter', 1610, 15, 10),
(235, 2478, 6, '1 Series Rear Brake Pads', 4640, 24, 10),
(236, 2479, 6, '1 Series AGM Battery', 8820, 39, 10),
(237, 2480, 6, '1 Series Air Filter', 1910, 7, 10),
(238, 2481, 6, '1 Series Wiper Blades', 1770, 35, 10),
(239, 2482, 6, '2 Series Spark Plugs (Set)', 3920, 21, 10),
(240, 2483, 6, '2 Series Wiper Blades', 2810, 31, 10),
(241, 2484, 6, '2 Series Front Brake Pads', 7640, 19, 10),
(242, 2485, 6, '2 Series Air Filter', 1340, 24, 10),
(243, 2486, 6, '3 Series AGM Battery', 13790, 20, 10),
(244, 2487, 6, '3 Series Cabin Microfilter', 2200, 36, 10),
(245, 2488, 6, '3 Series Rear Brake Pads', 2950, 9, 10),
(246, 2489, 6, '3 Series Wiper Blades', 3010, 33, 10),
(247, 2490, 6, '3 Series Air Filter', 1530, 35, 10),
(248, 2491, 6, '3 Series Spark Plugs (Set)', 4100, 23, 10),
(249, 2492, 6, '4 Series Oil Filter', 1220, 34, 10),
(250, 2493, 6, '4 Series Front Brake Pads', 5920, 49, 10),
(251, 2494, 6, '4 Series Air Filter', 1490, 13, 10),
(252, 2495, 6, '4 Series Rear Brake Pads', 3650, 41, 10),
(253, 2496, 6, '4 Series Wiper Blades', 1620, 35, 10),
(254, 2497, 6, '4 Series Spark Plugs (Set)', 2090, 25, 10),
(255, 2498, 6, '4 Series Cabin Microfilter', 1940, 9, 10),
(256, 2499, 6, '5 Series Wiper Blades', 2210, 48, 10),
(257, 2500, 6, '5 Series Spark Plugs (Set)', 3040, 30, 10),
(258, 2501, 6, '5 Series Oil Filter', 1460, 12, 10),
(259, 2502, 6, '5 Series Rear Brake Pads', 3900, 30, 10),
(260, 2503, 6, '6 Series AGM Battery', 11690, 34, 10),
(261, 2504, 6, '6 Series Front Brake Pads', 7300, 32, 10),
(262, 2505, 6, '6 Series Oil Filter', 1650, 20, 10),
(263, 2506, 6, '7 Series Rear Brake Pads', 4380, 46, 10),
(264, 2507, 6, '7 Series Wiper Blades', 2300, 7, 10),
(265, 2508, 6, '7 Series Air Filter', 2140, 32, 10),
(266, 2509, 6, '7 Series Front Brake Pads', 6230, 33, 10),
(267, 2510, 6, '8 Series Air Filter', 1850, 38, 10),
(268, 2511, 6, '8 Series Rear Brake Pads', 6130, 50, 10),
(269, 2512, 6, '8 Series Wiper Blades', 2330, 9, 10),
(270, 2513, 6, '1 Series Wiper Blades', 2380, 35, 10),
(271, 2514, 6, '1 Series AGM Battery', 9360, 43, 10),
(272, 2515, 6, '1 Series Front Brake Pads', 8290, 31, 10),
(273, 2516, 6, '1 Series Rear Brake Pads', 5360, 13, 10),
(274, 2517, 6, '1 Series Air Filter', 1610, 42, 10),
(275, 2518, 6, '1 Series Oil Filter', 1430, 29, 10),
(276, 2519, 6, '1 Series Spark Plugs (Set)', 2600, 31, 10),
(277, 2520, 6, '2 Series AGM Battery', 11890, 30, 10),
(278, 2521, 6, '2 Series Cabin Microfilter', 2740, 35, 10),
(279, 2522, 6, '2 Series Oil Filter', 970, 48, 10),
(280, 2523, 6, '2 Series Rear Brake Pads', 6550, 15, 10),
(281, 2524, 6, '2 Series Front Brake Pads', 4100, 27, 10),
(282, 2525, 6, '3 Series Oil Filter', 960, 31, 10),
(283, 2526, 6, '3 Series AGM Battery', 13050, 18, 10),
(284, 2527, 6, '3 Series Wiper Blades', 2600, 21, 10),
(285, 2528, 6, '3 Series Rear Brake Pads', 5280, 31, 10),
(286, 2529, 6, '3 Series Cabin Microfilter', 2040, 16, 10),
(287, 2530, 6, '3 Series Air Filter', 2170, 42, 10),
(288, 2531, 6, '4 Series Spark Plugs (Set)', 2490, 27, 10),
(289, 2532, 6, '4 Series Rear Brake Pads', 3680, 24, 10),
(290, 2533, 6, '4 Series Cabin Microfilter', 1750, 12, 10),
(291, 2534, 6, '4 Series Front Brake Pads', 7600, 35, 10),
(292, 2535, 6, '4 Series Wiper Blades', 1670, 15, 10),
(293, 2536, 6, '5 Series AGM Battery', 12710, 8, 10),
(294, 2537, 6, '5 Series Air Filter', 1900, 27, 10),
(295, 2538, 6, '5 Series Oil Filter', 1650, 43, 10),
(296, 2539, 6, '5 Series Cabin Microfilter', 1960, 44, 10),
(297, 2540, 6, '5 Series Front Brake Pads', 5790, 37, 10),
(298, 2541, 6, '6 Series Spark Plugs (Set)', 3810, 20, 10),
(299, 2542, 6, '6 Series Rear Brake Pads', 5770, 33, 10),
(300, 2543, 6, '6 Series Wiper Blades', 2410, 16, 10),
(301, 2544, 6, '6 Series Cabin Microfilter', 1590, 26, 10),
(302, 2545, 6, '6 Series Front Brake Pads', 6900, 5, 10),
(303, 2546, 6, '6 Series AGM Battery', 13270, 13, 10),
(304, 2547, 6, '7 Series Spark Plugs (Set)', 2050, 40, 10),
(305, 2548, 6, '7 Series Front Brake Pads', 7490, 21, 10),
(306, 2549, 6, '7 Series Oil Filter', 1100, 41, 10),
(307, 2550, 6, '7 Series AGM Battery', 13890, 42, 10),
(308, 2551, 6, '7 Series Rear Brake Pads', 6670, 16, 10),
(309, 2552, 6, '8 Series Oil Filter', 1190, 33, 10),
(310, 2553, 6, '8 Series Air Filter', 1260, 40, 10),
(311, 2554, 6, '8 Series Spark Plugs (Set)', 1940, 47, 10),
(312, 2555, 6, '8 Series Wiper Blades', 2150, 50, 10),
(313, 2556, 6, 'M1 Air Filter', 1910, 23, 10),
(314, 2557, 6, 'M1 Front Brake Pads', 8070, 42, 10),
(315, 2558, 6, 'M1 Spark Plugs (Set)', 2880, 8, 10),
(316, 2559, 6, 'M1 Rear Brake Pads', 2990, 22, 10),
(317, 2560, 6, 'M1 Cabin Microfilter', 2320, 37, 10),
(318, 2561, 6, 'M1 Oil Filter', 810, 13, 10),
(319, 2562, 6, 'M2 AGM Battery', 12020, 26, 10),
(320, 2563, 6, 'M2 Air Filter', 2140, 47, 10),
(321, 2564, 6, 'M2 Front Brake Pads', 4990, 34, 10),
(322, 2565, 6, 'M2 Rear Brake Pads', 3370, 43, 10),
(323, 2566, 6, 'M3 Spark Plugs (Set)', 2310, 25, 10),
(324, 2567, 6, 'M3 Rear Brake Pads', 4790, 41, 10),
(325, 2568, 6, 'M3 AGM Battery', 9030, 15, 10),
(326, 2569, 6, 'M3 Front Brake Pads', 4310, 48, 10),
(327, 2570, 6, 'M4 Front Brake Pads', 4860, 27, 10),
(328, 2571, 6, 'M4 Cabin Microfilter', 1430, 35, 10),
(329, 2572, 6, 'M4 AGM Battery', 10150, 15, 10),
(330, 2573, 6, 'M4 Spark Plugs (Set)', 1960, 24, 10),
(331, 2574, 6, 'M4 Rear Brake Pads', 5820, 32, 10),
(332, 2575, 6, 'M4 Air Filter', 2030, 19, 10),
(333, 2576, 6, 'M4 Oil Filter', 950, 37, 10),
(334, 2577, 6, 'M4 Wiper Blades', 2100, 47, 10),
(335, 2578, 6, 'M5 Wiper Blades', 2180, 25, 10),
(336, 2579, 6, 'M5 Rear Brake Pads', 4950, 27, 10),
(337, 2580, 6, 'M5 Front Brake Pads', 4720, 24, 10),
(338, 2581, 6, 'M5 AGM Battery', 9410, 39, 10),
(339, 2582, 6, 'M5 Cabin Microfilter', 2780, 42, 10),
(340, 2583, 6, 'M6 Rear Brake Pads', 6240, 35, 10),
(341, 2584, 6, 'M6 Cabin Microfilter', 1310, 17, 10),
(342, 2585, 6, 'M6 Air Filter', 1550, 7, 10),
(343, 2586, 6, 'M6 Spark Plugs (Set)', 2930, 30, 10),
(344, 2587, 6, 'M6 AGM Battery', 11450, 6, 10),
(345, 2588, 6, 'M6 Front Brake Pads', 3700, 15, 10),
(346, 2589, 6, 'M8 Front Brake Pads', 6980, 38, 10),
(347, 2590, 6, 'M8 Spark Plugs (Set)', 3390, 24, 10),
(348, 2591, 6, 'M8 AGM Battery', 13740, 37, 10),
(349, 2592, 6, 'M8 Wiper Blades', 3080, 21, 10),
(350, 2593, 6, 'M8 Cabin Microfilter', 1250, 48, 10),
(351, 2594, 6, 'M8 Oil Filter', 1310, 27, 10),
(352, 2595, 6, 'M8 Air Filter', 1270, 13, 10),
(353, 2596, 6, 'X5 M Rear Brake Pads', 6090, 20, 10),
(354, 2597, 6, 'X5 M AGM Battery', 11160, 19, 10),
(355, 2598, 6, 'X5 M Wiper Blades', 1730, 29, 10),
(356, 2599, 6, 'X5 M Front Brake Pads', 7230, 49, 10),
(357, 2600, 6, 'X5 M Cabin Microfilter', 1400, 12, 10),
(358, 2601, 6, 'X5 M Oil Filter', 1640, 14, 10),
(359, 2602, 6, 'X5 M Air Filter', 1240, 14, 10),
(360, 2603, 6, 'X6 M Cabin Microfilter', 1980, 10, 10),
(361, 2604, 6, 'X6 M Spark Plugs (Set)', 2000, 23, 10),
(362, 2605, 6, 'X6 M AGM Battery', 9420, 41, 10),
(363, 2606, 6, 'XM Front Brake Pads', 7120, 28, 10),
(364, 2607, 6, 'XM Oil Filter', 1800, 6, 10),
(365, 2608, 6, 'XM Air Filter', 1400, 14, 10),
(366, 2609, 6, 'XM AGM Battery', 13320, 33, 10),
(367, 2610, 6, 'XM Spark Plugs (Set)', 2730, 6, 10),
(368, 2611, 6, 'XM Rear Brake Pads', 4920, 17, 10),
(369, 2612, 6, '2 Series Active Tourer Oil Filter', 1660, 46, 10),
(370, 2613, 6, '2 Series Active Tourer Wiper Blades', 3280, 8, 10),
(371, 2614, 6, '2 Series Active Tourer Air Filter', 1760, 41, 10),
(372, 2615, 6, '2 Series Active Tourer Spark Plugs (Set)', 1860, 31, 10),
(373, 2616, 6, '2 Series Gran Tourer Oil Filter', 860, 23, 10),
(374, 2617, 6, '2 Series Gran Tourer Cabin Microfilter', 1740, 13, 10),
(375, 2618, 6, '2 Series Gran Tourer Air Filter', 1570, 7, 10),
(376, 2619, 6, '2 Series Gran Tourer Rear Brake Pads', 4410, 38, 10),
(377, 2620, 6, '2 Series Gran Tourer Spark Plugs (Set)', 3340, 44, 10),
(378, 2621, 6, '2 Series Gran Tourer Wiper Blades', 3030, 30, 10),
(379, 2622, 6, '2 Series Gran Tourer Front Brake Pads', 3420, 22, 10),
(380, 2623, 6, '3 Series GT Wiper Blades', 1610, 21, 10),
(381, 2624, 6, '3 Series GT Oil Filter', 1490, 30, 10),
(382, 2625, 6, '3 Series GT Cabin Microfilter', 1280, 27, 10),
(383, 2626, 6, '3 Series GT Rear Brake Pads', 6900, 31, 10),
(384, 2627, 6, '3 Series GT AGM Battery', 9850, 16, 10),
(385, 2628, 6, '3 Series GT Spark Plugs (Set)', 3750, 9, 10),
(386, 2629, 6, '3 Series GT Air Filter', 1690, 23, 10),
(387, 2630, 6, '5 Series GT Wiper Blades', 2310, 11, 10),
(388, 2631, 6, '5 Series GT Oil Filter', 1280, 36, 10),
(389, 2632, 6, '5 Series GT Front Brake Pads', 3830, 24, 10),
(390, 2633, 6, '5 Series GT Cabin Microfilter', 2300, 5, 10),
(391, 2634, 6, '5 Series GT Rear Brake Pads', 5790, 33, 10),
(392, 2635, 6, '5 Series GT AGM Battery', 13770, 11, 10),
(393, 2636, 6, '5 Series GT Air Filter', 2060, 48, 10),
(394, 2637, 6, '5 Series GT Spark Plugs (Set)', 3830, 44, 10),
(395, 224036, 6, 'MA', 50, 90, 10),
(396, 1000, 42, 'Aquila Norman', 348, 665, 10),
(397, 100068, 42, 'abc', 100, 100, 10);

-- --------------------------------------------------------

--
-- Table structure for table `invoice`
--

CREATE TABLE `invoice` (
  `Invoice_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `InvoiceDate` date DEFAULT NULL,
  `SubtotalLabor` decimal(10,2) DEFAULT NULL,
  `SubtotalParts` decimal(10,2) DEFAULT NULL,
  `Tax` decimal(10,2) DEFAULT NULL,
  `Discount` decimal(10,2) DEFAULT NULL,
  `Total` decimal(10,2) DEFAULT NULL,
  `Status` varchar(50) DEFAULT NULL,
  `JobCard_ID` int(11) DEFAULT NULL,
  `DueDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `invoice`
--

INSERT INTO `invoice` (`Invoice_ID`, `User_ID`, `InvoiceDate`, `SubtotalLabor`, `SubtotalParts`, `Tax`, `Discount`, `Total`, `Status`, `JobCard_ID`, `DueDate`) VALUES
(1, 2, '2026-03-18', 100.00, 50.00, 21.00, 0.00, 171.00, 'Paid', 1, '2026-04-01'),
(2, 3, '2025-03-11', 100.00, 120.00, 22.00, 10.00, 232.00, 'Paid', NULL, NULL),
(3, 3, '2025-03-12', 200.00, 150.00, 30.00, 0.00, 380.00, 'Paid', NULL, NULL),
(8, 2, '2026-03-11', 200.00, 150.00, 49.00, 10.00, 389.00, 'Paid', 1, '2026-03-25'),
(10, 2, '2026-03-18', 650.00, 150.00, 112.00, 12.00, 900.00, 'Paid', 11, '2026-03-18'),
(13, 21, '2026-03-19', 800.00, 9000.00, 1372.00, 172.00, 11000.00, 'Paid', 15, '2026-03-20'),
(14, 2, '2026-04-07', 300.00, 0.00, 42.00, 3.42, 338.58, 'Paid', 16, '2026-04-10'),
(15, 2, '2026-04-08', 750.00, 20300.00, 2947.00, 2399.70, 21597.30, 'Paid', 17, '2026-04-09'),
(16, 2, '2026-04-09', 750.00, 95000.00, 13405.00, 109155.00, 0.00, 'Paid', 18, '2026-04-10'),
(17, 42, '2026-04-09', 500.00, 26160.00, 3732.40, 6078.48, 24313.92, 'Paid', 19, '2026-04-10'),
(19, 2, '2026-04-27', 750.00, 2690.00, 481.60, 0.00, 3921.60, 'Unpaid', 23, '2026-04-28');

-- --------------------------------------------------------

--
-- Table structure for table `jobcard`
--

CREATE TABLE `jobcard` (
  `JobCard_ID` int(11) NOT NULL,
  `Appointment_ID` int(11) DEFAULT NULL,
  `Vehicle_ID` int(11) DEFAULT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Invoice_ID` int(11) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  `UpdatedAt` datetime DEFAULT NULL,
  `ReportedIssues` text DEFAULT NULL,
  `Status` varchar(50) DEFAULT NULL,
  `TotalLaborCost` decimal(10,2) DEFAULT NULL,
  `TotalPartsCost` decimal(10,2) DEFAULT NULL,
  `Technician_ID` int(11) DEFAULT NULL,
  `Technician_Notes` text DEFAULT NULL,
  `TotalHours` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobcard`
--

INSERT INTO `jobcard` (`JobCard_ID`, `Appointment_ID`, `Vehicle_ID`, `User_ID`, `Invoice_ID`, `CreatedAt`, `UpdatedAt`, `ReportedIssues`, `Status`, `TotalLaborCost`, `TotalPartsCost`, `Technician_ID`, `Technician_Notes`, `TotalHours`) VALUES
(1, 1, 1, 2, 1, '2026-03-18 10:30:00', '2026-03-18 11:30:00', 'Oil change needed', 'Completed', 100.00, 50.00, 1, 'Performed oil and filter change.', 1.50),
(11, 19, 2, 2, 10, '2026-03-18 18:50:08', NULL, NULL, 'Completed', NULL, NULL, NULL, '[2026-03-18 18:51] manar abdelhadi: IHD\n', 0.11),
(12, 18, 12, 14, NULL, '2026-03-20 09:15:00', NULL, 'Engine diagnostic', 'Completed', 0.00, 0.00, 3, NULL, 0.00),
(15, 42, 41, 21, 13, '2026-03-19 11:35:56', NULL, NULL, 'Completed', NULL, NULL, 3, NULL, 0.61),
(16, 2, 2, 2, 14, '2026-04-07 22:50:11', NULL, NULL, 'Completed', NULL, NULL, 1, NULL, 0.11),
(17, 47, 42, 2, 15, '2026-04-08 23:17:58', NULL, NULL, 'Completed', NULL, NULL, 1, NULL, 0.30),
(18, 48, 43, 2, 16, '2026-04-09 01:18:17', NULL, NULL, 'Completed', NULL, NULL, 3, NULL, 0.25),
(19, 49, 44, 42, 17, '2026-04-09 16:11:57', NULL, NULL, 'Completed', NULL, NULL, 3, NULL, 0.00),
(20, 50, 44, 42, NULL, '2026-04-09 16:51:35', NULL, NULL, 'Completed', NULL, NULL, 3, NULL, 0.05),
(23, 33, 33, 2, 19, '2026-04-25 00:25:50', NULL, NULL, 'Completed', NULL, NULL, 3, '[2026-04-27 03:50] Mohamed Khaled: hi\n[2026-04-27 03:51] Mohamed Khaled: باي\n', 0.00),
(24, 32, 32, 2, NULL, '2026-04-25 00:26:15', NULL, NULL, 'In Progress', NULL, NULL, 14, NULL, 0.00),
(28, 30, 30, 2, NULL, '2026-04-25 23:30:56', NULL, NULL, 'In Progress', NULL, NULL, 47, NULL, 0.00),
(29, 73, 1, 2, NULL, '2026-04-27 02:32:57', NULL, NULL, 'In Progress', NULL, NULL, 1, NULL, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `jobcardparts`
--

CREATE TABLE `jobcardparts` (
  `id` int(11) NOT NULL,
  `JobCard_ID` int(11) NOT NULL,
  `Item_ID` int(11) NOT NULL,
  `QuantityUsed` int(11) DEFAULT NULL,
  `Status` varchar(50) DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobcardparts`
--

INSERT INTO `jobcardparts` (`id`, `JobCard_ID`, `Item_ID`, `QuantityUsed`, `Status`) VALUES
(21, 1, 48, 1, 'Approved'),
(22, 11, 41, 1, 'Rejected'),
(23, 16, 48, 1, 'Rejected'),
(24, 16, 49, 1, 'Rejected'),
(26, 16, 49, 1, 'Rejected'),
(27, 17, 329, 2, 'Approved'),
(28, 18, 333, 100, 'Rejected'),
(29, 19, 335, 12, 'Approved'),
(30, 17, 329, 1, 'Approved'),
(34, 17, 332, 1, 'Approved'),
(35, 23, 49, 1, 'Pending'),
(36, 20, 336, 100, 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `Payment_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Invoice_ID` int(11) DEFAULT NULL,
  `PaymentDate` date DEFAULT NULL,
  `Amount` decimal(10,2) DEFAULT NULL,
  `Method` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`Payment_ID`, `User_ID`, `Invoice_ID`, `PaymentDate`, `Amount`, `Method`) VALUES
(1, 2, 2, '2025-03-11', 232.00, 'CreditCard'),
(2, 2, 10, '2026-03-18', 900.00, 'CreditCard'),
(3, 2, 1, '2026-03-19', 171.00, 'CreditCard'),
(6, 21, 13, '2026-03-19', 11000.00, 'CreditCard'),
(7, 2, 10, '2026-04-07', 900.00, 'CreditCard'),
(8, 2, 10, '2026-04-07', 900.00, 'CreditCard'),
(9, 2, 10, '2026-04-07', 900.00, 'CreditCard'),
(10, 2, 15, '2026-04-08', 21597.30, 'CreditCard'),
(11, 2, 15, '2026-04-08', 21597.30, 'CreditCard'),
(12, 2, 15, '2026-04-08', 21597.30, 'CreditCard'),
(13, 2, 15, '2026-04-08', 21597.30, 'CreditCard'),
(14, 2, 16, '2026-04-09', 1000.00, 'CreditCard'),
(15, 42, 17, '2026-04-09', 24313.92, 'CreditCard'),
(17, 2, 14, '2026-04-25', 338.58, 'CreditCard'),
(18, 2, 10, '2026-04-27', 900.00, 'CreditCard'),
(19, 2, 8, '2026-04-27', 389.00, 'CreditCard');

-- --------------------------------------------------------

--
-- Table structure for table `purchase_order`
--

CREATE TABLE `purchase_order` (
  `order_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_price` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `order_date` datetime(6) NOT NULL,
  `stock_keeper_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `supplier_part_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchase_order`
--

INSERT INTO `purchase_order` (`order_id`, `quantity`, `total_price`, `status`, `order_date`, `stock_keeper_id`, `supplier_id`, `supplier_part_id`) VALUES
(13, 10, 12300, 'Pending', '2026-04-21 20:07:06.854686', 6, 16, 1457),
(14, 1, 1040, 'Pending', '2026-04-26 00:01:03.528621', 42, 13, 1278),
(15, 1, 2500, 'Pending', '2026-04-26 23:57:13.944419', 42, 17, 1475);

-- --------------------------------------------------------

--
-- Table structure for table `servicemanager`
--

CREATE TABLE `servicemanager` (
  `ServiceManager_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `Department` varchar(100) DEFAULT NULL,
  `Shift` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `servicemanager`
--

INSERT INTO `servicemanager` (`ServiceManager_ID`, `User_ID`, `Department`, `Shift`) VALUES
(1, 4, 'General', 'Day');

-- --------------------------------------------------------

--
-- Table structure for table `stockkeeper`
--

CREATE TABLE `stockkeeper` (
  `StockKeeper_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stockkeeper`
--

INSERT INTO `stockkeeper` (`StockKeeper_ID`, `User_ID`) VALUES
(1, 6);

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

CREATE TABLE `supplier` (
  `Supplier_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `Company_Name` varchar(100) DEFAULT NULL,
  `Category` varchar(50) DEFAULT NULL,
  `Status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier`
--

INSERT INTO `supplier` (`Supplier_ID`, `User_ID`, `Company_Name`, `Category`, `Status`) VALUES
(13, 33, 'Ahmed Classic Models Auto Parts', 'General', 'Active'),
(15, 35, 'Mahmoud Series (Main Auto Parts', 'General', 'Active'),
(16, 36, 'Khaled X Series Auto Parts', 'General', 'Active'),
(17, 37, 'Ali Z Series Auto Parts', 'General', 'Active'),
(18, 38, 'Omar i Series Auto Parts', 'General', 'Active'),
(19, 39, 'Youssef M Models Auto Parts', 'General', 'Active'),
(20, 40, 'Tarek Other / Auto Parts', 'General', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `supplier_part`
--

CREATE TABLE `supplier_part` (
  `part_id` int(11) NOT NULL,
  `car_model` varchar(100) NOT NULL,
  `name` varchar(200) NOT NULL,
  `code` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier_part`
--

INSERT INTO `supplier_part` (`part_id`, `car_model`, `name`, `code`, `price`, `quantity`, `supplier_id`) VALUES
(1277, '3/15', '3/15 AGM Battery', '6121-7039-998', 9510, 49, 13),
(1278, '3/15', '3/15 Oil Filter', '1142-9785-428', 1040, 10, 13),
(1279, '3/15', '3/15 Wiper Blades', '6161-7102-175', 1820, 21, 13),
(1280, '3/15', '3/15 Air Filter', '1371-6214-987', 1460, 39, 13),
(1281, '3/15', '3/15 Front Brake Pads', '3411-2455-260', 5870, 33, 13),
(1282, '3/15', '3/15 Spark Plugs (Set)', '1212-1960-160', 3050, 25, 13),
(1283, '303', '303 Front Brake Pads', '3411-2485-856', 4920, 19, 13),
(1284, '303', '303 Air Filter', '1371-9177-460', 960, 21, 13),
(1285, '303', '303 Cabin Microfilter', '6411-3879-219', 1920, 19, 13),
(1286, '315', '315 Spark Plugs (Set)', '1212-7905-827', 2270, 33, 13),
(1287, '315', '315 Wiper Blades', '6161-2513-392', 2200, 34, 13),
(1288, '315', '315 Cabin Microfilter', '6411-6320-654', 2020, 45, 13),
(1289, '319', '319 Oil Filter', '1142-7837-573', 1390, 13, 13),
(1290, '319', '319 Wiper Blades', '6161-5872-848', 2180, 30, 13),
(1291, '319', '319 Spark Plugs (Set)', '1212-8639-293', 2250, 36, 13),
(1292, '319', '319 Cabin Microfilter', '6411-2122-570', 2390, 16, 13),
(1293, '319', '319 Rear Brake Pads', '3421-9860-681', 2580, 16, 13),
(1294, '319', '319 AGM Battery', '6121-1561-172', 13200, 35, 13),
(1295, '319', '319 Front Brake Pads', '3411-8610-497', 5820, 29, 13),
(1296, '319', '319 Air Filter', '1371-7959-820', 1880, 45, 13),
(1297, '326', '326 Wiper Blades', '6161-9576-247', 2540, 14, 13),
(1298, '326', '326 Cabin Microfilter', '6411-9023-677', 1120, 50, 13),
(1299, '326', '326 AGM Battery', '6121-6968-344', 14040, 10, 13),
(1300, '326', '326 Oil Filter', '1142-1138-107', 540, 17, 13),
(1301, '326', '326 Spark Plugs (Set)', '1212-4558-716', 3090, 14, 13),
(1302, '326', '326 Rear Brake Pads', '3421-3802-393', 4350, 40, 13),
(1303, '326', '326 Air Filter', '1371-1445-614', 1680, 49, 13),
(1304, '326', '326 Front Brake Pads', '3411-4583-825', 5540, 31, 13),
(1305, '327', '327 AGM Battery', '6121-3804-594', 9440, 7, 13),
(1306, '327', '327 Wiper Blades', '6161-2675-485', 2970, 25, 13),
(1307, '327', '327 Rear Brake Pads', '3421-2084-943', 3760, 26, 13),
(1308, '327', '327 Air Filter', '1371-6521-344', 1940, 43, 13),
(1309, '327', '327 Oil Filter', '1142-9890-822', 860, 27, 13),
(1310, '327', '327 Spark Plugs (Set)', '1212-8971-200', 3940, 26, 13),
(1311, '328', '328 Front Brake Pads', '3411-1369-254', 3400, 13, 13),
(1312, '328', '328 Cabin Microfilter', '6411-5368-603', 2230, 35, 13),
(1313, '328', '328 Air Filter', '1371-6813-614', 1390, 10, 13),
(1314, '328', '328 Wiper Blades', '6161-4803-586', 2800, 27, 13),
(1315, '328', '328 Spark Plugs (Set)', '1212-1904-946', 2490, 27, 13),
(1316, '328', '328 AGM Battery', '6121-8997-825', 12720, 8, 13),
(1317, '328', '328 Oil Filter', '1142-5956-894', 1330, 9, 13),
(1318, '335', '335 Wiper Blades', '6161-3223-173', 1840, 9, 13),
(1319, '335', '335 Oil Filter', '1142-3734-311', 1460, 23, 13),
(1320, '335', '335 Cabin Microfilter', '6411-1649-327', 990, 13, 13),
(1321, '335', '335 Spark Plugs (Set)', '1212-4509-207', 2780, 47, 13),
(1322, '335', '335 Front Brake Pads', '3411-6832-262', 5180, 5, 13),
(1323, '335', '335 Air Filter', '1371-7817-729', 1720, 36, 13),
(1324, '335', '335 Rear Brake Pads', '3421-2755-228', 3750, 49, 13),
(1325, '335', '335 AGM Battery', '6121-7873-693', 11520, 38, 13),
(1326, '340', '340 AGM Battery', '6121-6635-987', 11810, 45, 13),
(1327, '340', '340 Cabin Microfilter', '6411-8755-663', 2380, 17, 13),
(1328, '340', '340 Oil Filter', '1142-4275-395', 740, 13, 13),
(1329, '340', '340 Wiper Blades', '6161-1487-370', 1460, 9, 13),
(1330, '340', '340 Front Brake Pads', '3411-2516-435', 3650, 27, 13),
(1331, '340', '340 Spark Plugs (Set)', '1212-7001-771', 2990, 17, 13),
(1332, '340', '340 Air Filter', '1371-1173-664', 1820, 5, 13),
(1333, '501', '501 Spark Plugs (Set)', '1212-2503-556', 2890, 50, 13),
(1334, '501', '501 Front Brake Pads', '3411-3874-263', 6820, 46, 13),
(1335, '501', '501 Wiper Blades', '6161-7699-506', 1530, 41, 13),
(1336, '501', '501 Air Filter', '1371-8066-747', 1540, 23, 13),
(1337, '501', '501 Rear Brake Pads', '3421-5786-582', 3110, 50, 13),
(1338, '502', '502 Spark Plugs (Set)', '1212-3970-141', 2040, 43, 13),
(1339, '502', '502 Oil Filter', '1142-1876-691', 780, 11, 13),
(1340, '502', '502 Front Brake Pads', '3411-1854-171', 3180, 18, 13),
(1341, '502', '502 Wiper Blades', '6161-3343-637', 2150, 13, 13),
(1342, '503', '503 Oil Filter', '1142-9761-776', 1370, 30, 13),
(1343, '503', '503 AGM Battery', '6121-5071-275', 11280, 16, 13),
(1344, '503', '503 Wiper Blades', '6161-2763-840', 2230, 42, 13),
(1345, '503', '503 Cabin Microfilter', '6411-3818-370', 2390, 50, 13),
(1346, '503', '503 Front Brake Pads', '3411-6940-577', 6770, 44, 13),
(1347, '503', '503 Air Filter', '1371-2717-738', 1930, 30, 13),
(1348, '503', '503 Spark Plugs (Set)', '1212-7916-293', 4000, 17, 13),
(1349, '507', '507 Wiper Blades', '6161-6510-245', 1990, 16, 13),
(1350, '507', '507 AGM Battery', '6121-6710-124', 12370, 29, 13),
(1351, '507', '507 Rear Brake Pads', '3421-7127-711', 4400, 47, 13),
(1352, '507', '507 Oil Filter', '1142-1576-742', 1420, 6, 13),
(1353, '507', '507 Spark Plugs (Set)', '1212-4988-752', 2870, 7, 13),
(1354, '507', '507 Air Filter', '1371-8024-213', 1110, 42, 13),
(1355, '507', '507 Front Brake Pads', '3411-7225-569', 5800, 13, 13),
(1356, 'Isetta', 'Isetta Spark Plugs (Set)', '1212-8537-931', 1940, 10, 13),
(1357, 'Isetta', 'Isetta Wiper Blades', '6161-4632-973', 1720, 20, 13),
(1358, 'Isetta', 'Isetta Front Brake Pads', '3411-4231-759', 4000, 29, 13),
(1359, 'Isetta', 'Isetta Oil Filter', '1142-5860-580', 900, 47, 13),
(1360, 'Isetta', 'Isetta Cabin Microfilter', '6411-6320-102', 1690, 40, 13),
(1361, 'Isetta', 'Isetta Rear Brake Pads', '3421-4297-943', 6270, 47, 13),
(1362, '600', '600 Front Brake Pads', '3411-1453-297', 7540, 16, 13),
(1363, '600', '600 Wiper Blades', '6161-9540-864', 2210, 46, 13),
(1364, '600', '600 Cabin Microfilter', '6411-5852-948', 2270, 21, 13),
(1365, '600', '600 Oil Filter', '1142-3140-840', 680, 34, 13),
(1366, '700', '700 Rear Brake Pads', '3421-8570-113', 6830, 17, 13),
(1367, '700', '700 AGM Battery', '6121-8315-478', 12310, 30, 13),
(1368, '700', '700 Front Brake Pads', '3411-4842-433', 6620, 33, 13),
(1369, '700', '700 Wiper Blades', '6161-6469-871', 2480, 11, 13),
(1370, '700', '700 Oil Filter', '1142-7198-791', 1180, 24, 13),
(1407, '1 Series', '1 Series Wiper Blades', '6161-9165-540', 1710, 35, 15),
(1408, '1 Series', '1 Series Spark Plugs (Set)', '1212-8898-411', 3090, 20, 15),
(1409, '1 Series', '1 Series AGM Battery', '6121-3980-744', 8960, 18, 15),
(1410, '1 Series', '1 Series Oil Filter', '1142-8660-520', 850, 21, 15),
(1411, '1 Series', '1 Series Cabin Microfilter', '6411-7188-808', 2210, 48, 15),
(1412, '2 Series', '2 Series Cabin Microfilter', '6411-6791-232', 1030, 14, 15),
(1413, '2 Series', '2 Series Wiper Blades', '6161-8137-186', 2810, 48, 15),
(1414, '2 Series', '2 Series Front Brake Pads', '3411-5561-978', 4400, 29, 15),
(1415, '2 Series', '2 Series AGM Battery', '6121-5571-791', 9720, 8, 15),
(1416, '2 Series', '2 Series Air Filter', '1371-2525-166', 910, 46, 15),
(1417, '3 Series', '3 Series Rear Brake Pads', '3421-1540-468', 5860, 24, 15),
(1418, '3 Series', '3 Series Cabin Microfilter', '6411-3188-461', 2050, 10, 15),
(1419, '3 Series', '3 Series Front Brake Pads', '3411-3962-178', 4760, 19, 15),
(1420, '4 Series', '4 Series Oil Filter', '1142-4724-592', 1030, 40, 15),
(1421, '4 Series', '4 Series AGM Battery', '6121-4645-415', 8990, 39, 15),
(1422, '4 Series', '4 Series Cabin Microfilter', '6411-8176-696', 1160, 5, 15),
(1423, '5 Series', '5 Series Spark Plugs (Set)', '1212-3430-408', 1980, 29, 15),
(1424, '5 Series', '5 Series Rear Brake Pads', '3421-7422-777', 4210, 30, 15),
(1425, '5 Series', '5 Series AGM Battery', '6121-7958-110', 8190, 26, 15),
(1426, '5 Series', '5 Series Air Filter', '1371-6310-183', 1720, 40, 15),
(1427, '5 Series', '5 Series Wiper Blades', '6161-8352-281', 1440, 30, 15),
(1428, '5 Series', '5 Series Oil Filter', '1142-9222-249', 500, 45, 15),
(1429, '6 Series', '6 Series Air Filter', '1371-2763-392', 1630, 5, 15),
(1430, '6 Series', '6 Series Wiper Blades', '6161-6530-628', 1580, 28, 15),
(1431, '6 Series', '6 Series AGM Battery', '6121-3887-783', 14070, 48, 15),
(1432, '7 Series', '7 Series Wiper Blades', '6161-5747-225', 2240, 30, 15),
(1433, '7 Series', '7 Series Rear Brake Pads', '3421-2615-534', 5000, 19, 15),
(1434, '7 Series', '7 Series AGM Battery', '6121-9942-218', 10060, 23, 15),
(1435, '8 Series', '8 Series Spark Plugs (Set)', '1212-5272-373', 3150, 27, 15),
(1436, '8 Series', '8 Series Wiper Blades', '6161-6638-876', 1610, 47, 15),
(1437, '8 Series', '8 Series Oil Filter', '1142-9879-748', 530, 11, 15),
(1438, '1 Series', '1 Series Wiper Blades', '6161-8584-272', 1930, 42, 16),
(1439, '1 Series', '1 Series Front Brake Pads', '3411-5930-852', 4000, 13, 16),
(1440, '1 Series', '1 Series AGM Battery', '6121-5704-724', 8670, 6, 16),
(1441, '1 Series', '1 Series Spark Plugs (Set)', '1212-6054-728', 2050, 48, 16),
(1442, '1 Series', '1 Series Cabin Microfilter', '6411-4562-491', 2280, 8, 16),
(1443, '1 Series', '1 Series Oil Filter', '1142-6164-101', 1120, 32, 16),
(1444, '1 Series', '1 Series Air Filter', '1371-3991-570', 1800, 11, 16),
(1445, '2 Series', '2 Series Cabin Microfilter', '6411-4423-440', 2000, 13, 16),
(1446, '2 Series', '2 Series AGM Battery', '6121-7021-859', 13810, 33, 16),
(1447, '2 Series', '2 Series Oil Filter', '1142-3619-270', 750, 19, 16),
(1448, '3 Series', '3 Series Wiper Blades', '6161-1066-367', 2900, 12, 16),
(1449, '3 Series', '3 Series AGM Battery', '6121-8330-797', 10120, 46, 16),
(1450, '3 Series', '3 Series Front Brake Pads', '3411-8101-782', 7320, 46, 16),
(1451, '4 Series', '4 Series Cabin Microfilter', '6411-6232-599', 2230, 38, 16),
(1452, '4 Series', '4 Series AGM Battery', '6121-4120-703', 12820, 7, 16),
(1453, '4 Series', '4 Series Spark Plugs (Set)', '1212-9010-909', 3750, 46, 16),
(1454, '5 Series', '5 Series Spark Plugs (Set)', '1212-4263-698', 2980, 28, 16),
(1455, '5 Series', '5 Series Front Brake Pads', '3411-5425-208', 4240, 49, 16),
(1456, '5 Series', '5 Series Wiper Blades', '6161-3792-758', 1360, 7, 16),
(1457, '5 Series', '5 Series Oil Filter', '1142-2903-520', 1230, 46, 16),
(1458, '5 Series', '5 Series Air Filter', '1371-4418-787', 1420, 26, 16),
(1459, '5 Series', '5 Series Cabin Microfilter', '6411-6553-931', 2080, 50, 16),
(1460, '5 Series', '5 Series AGM Battery', '6121-4337-156', 11650, 35, 16),
(1461, '6 Series', '6 Series Cabin Microfilter', '6411-1705-397', 1430, 25, 16),
(1462, '6 Series', '6 Series Wiper Blades', '6161-7976-130', 1460, 6, 16),
(1463, '6 Series', '6 Series Front Brake Pads', '3411-1964-626', 7860, 12, 16),
(1464, '6 Series', '6 Series Rear Brake Pads', '3421-3785-955', 5930, 17, 16),
(1465, '6 Series', '6 Series Oil Filter', '1142-1628-271', 1340, 16, 16),
(1466, '6 Series', '6 Series Spark Plugs (Set)', '1212-4035-690', 1780, 25, 16),
(1467, '6 Series', '6 Series Air Filter', '1371-9750-829', 940, 44, 16),
(1468, '7 Series', '7 Series Rear Brake Pads', '3421-9369-147', 6760, 7, 16),
(1469, '7 Series', '7 Series AGM Battery', '6121-5843-343', 9450, 44, 16),
(1470, '7 Series', '7 Series Oil Filter', '1142-6637-817', 1430, 16, 16),
(1471, '8 Series', '8 Series Rear Brake Pads', '3421-5998-383', 4550, 25, 16),
(1472, '8 Series', '8 Series Air Filter', '1371-6785-947', 1280, 36, 16),
(1473, '8 Series', '8 Series Front Brake Pads', '3411-1032-566', 4440, 34, 16),
(1474, '1 Series', '1 Series Front Brake Pads', '3411-9786-462', 7540, 44, 17),
(1475, '1 Series', '1 Series Spark Plugs (Set)', '1212-4460-417', 2500, 8, 17),
(1476, '1 Series', '1 Series Oil Filter', '1142-7530-130', 1330, 31, 17),
(1477, '1 Series', '1 Series Cabin Microfilter', '6411-3204-357', 1310, 15, 17),
(1478, '1 Series', '1 Series Rear Brake Pads', '3421-7319-554', 4340, 24, 17),
(1479, '1 Series', '1 Series AGM Battery', '6121-6159-368', 8520, 39, 17),
(1480, '1 Series', '1 Series Air Filter', '1371-1109-841', 1610, 7, 17),
(1481, '1 Series', '1 Series Wiper Blades', '6161-3739-540', 1470, 35, 17),
(1482, '2 Series', '2 Series Spark Plugs (Set)', '1212-8873-729', 3620, 21, 17),
(1483, '2 Series', '2 Series Wiper Blades', '6161-5119-878', 2510, 31, 17),
(1484, '2 Series', '2 Series Front Brake Pads', '3411-9178-223', 7340, 19, 17),
(1485, '2 Series', '2 Series Air Filter', '1371-8386-507', 1040, 24, 17),
(1486, '3 Series', '3 Series AGM Battery', '6121-8777-559', 13490, 20, 17),
(1487, '3 Series', '3 Series Cabin Microfilter', '6411-5777-736', 1900, 36, 17),
(1488, '3 Series', '3 Series Rear Brake Pads', '3421-1432-572', 2650, 9, 17),
(1489, '3 Series', '3 Series Wiper Blades', '6161-4605-180', 2710, 33, 17),
(1490, '3 Series', '3 Series Air Filter', '1371-5983-292', 1230, 35, 17),
(1491, '3 Series', '3 Series Spark Plugs (Set)', '1212-3552-745', 3800, 23, 17),
(1492, '4 Series', '4 Series Oil Filter', '1142-2087-358', 920, 34, 17),
(1493, '4 Series', '4 Series Front Brake Pads', '3411-4767-179', 5620, 49, 17),
(1494, '4 Series', '4 Series Air Filter', '1371-8689-240', 1190, 13, 17),
(1495, '4 Series', '4 Series Rear Brake Pads', '3421-5946-493', 3350, 41, 17),
(1496, '4 Series', '4 Series Wiper Blades', '6161-3386-787', 1320, 35, 17),
(1497, '4 Series', '4 Series Spark Plugs (Set)', '1212-7665-967', 1790, 25, 17),
(1498, '4 Series', '4 Series Cabin Microfilter', '6411-3780-469', 1640, 9, 17),
(1499, '5 Series', '5 Series Wiper Blades', '6161-2336-918', 1910, 48, 17),
(1500, '5 Series', '5 Series Spark Plugs (Set)', '1212-4514-635', 2740, 30, 17),
(1501, '5 Series', '5 Series Oil Filter', '1142-1299-194', 1160, 12, 17),
(1502, '5 Series', '5 Series Rear Brake Pads', '3421-6968-546', 3600, 30, 17),
(1503, '6 Series', '6 Series AGM Battery', '6121-3146-806', 11390, 34, 17),
(1504, '6 Series', '6 Series Front Brake Pads', '3411-9233-572', 7000, 32, 17),
(1505, '6 Series', '6 Series Oil Filter', '1142-8733-259', 1350, 20, 17),
(1506, '7 Series', '7 Series Rear Brake Pads', '3421-4941-977', 4080, 46, 17),
(1507, '7 Series', '7 Series Wiper Blades', '6161-8115-705', 2000, 7, 17),
(1508, '7 Series', '7 Series Air Filter', '1371-7408-292', 1840, 32, 17),
(1509, '7 Series', '7 Series Front Brake Pads', '3411-9616-347', 5930, 33, 17),
(1510, '8 Series', '8 Series Air Filter', '1371-4539-828', 1550, 38, 17),
(1511, '8 Series', '8 Series Rear Brake Pads', '3421-4206-112', 5830, 50, 17),
(1512, '8 Series', '8 Series Wiper Blades', '6161-7093-382', 2030, 9, 17),
(1513, '1 Series', '1 Series Wiper Blades', '6161-8375-913', 2080, 35, 18),
(1514, '1 Series', '1 Series AGM Battery', '6121-6277-208', 9060, 43, 18),
(1515, '1 Series', '1 Series Front Brake Pads', '3411-6555-636', 7990, 31, 18),
(1516, '1 Series', '1 Series Rear Brake Pads', '3421-4505-519', 5060, 13, 18),
(1517, '1 Series', '1 Series Air Filter', '1371-5935-733', 1310, 42, 18),
(1518, '1 Series', '1 Series Oil Filter', '1142-3252-886', 1130, 29, 18),
(1519, '1 Series', '1 Series Spark Plugs (Set)', '1212-3816-256', 2300, 31, 18),
(1520, '2 Series', '2 Series AGM Battery', '6121-9406-845', 11590, 30, 18),
(1521, '2 Series', '2 Series Cabin Microfilter', '6411-8928-569', 2440, 35, 18),
(1522, '2 Series', '2 Series Oil Filter', '1142-8697-453', 670, 48, 18),
(1523, '2 Series', '2 Series Rear Brake Pads', '3421-4092-603', 6250, 15, 18),
(1524, '2 Series', '2 Series Front Brake Pads', '3411-9727-250', 3800, 27, 18),
(1525, '3 Series', '3 Series Oil Filter', '1142-4508-356', 660, 31, 18),
(1526, '3 Series', '3 Series AGM Battery', '6121-7767-188', 12750, 18, 18),
(1527, '3 Series', '3 Series Wiper Blades', '6161-9356-787', 2300, 21, 18),
(1528, '3 Series', '3 Series Rear Brake Pads', '3421-5141-863', 4980, 31, 18),
(1529, '3 Series', '3 Series Cabin Microfilter', '6411-5143-181', 1740, 16, 18),
(1530, '3 Series', '3 Series Air Filter', '1371-8183-935', 1870, 42, 18),
(1531, '4 Series', '4 Series Spark Plugs (Set)', '1212-9767-263', 2190, 27, 18),
(1532, '4 Series', '4 Series Rear Brake Pads', '3421-9306-576', 3380, 24, 18),
(1533, '4 Series', '4 Series Cabin Microfilter', '6411-9593-949', 1450, 12, 18),
(1534, '4 Series', '4 Series Front Brake Pads', '3411-2168-359', 7300, 35, 18),
(1535, '4 Series', '4 Series Wiper Blades', '6161-3661-667', 1370, 15, 18),
(1536, '5 Series', '5 Series AGM Battery', '6121-8585-587', 12410, 8, 18),
(1537, '5 Series', '5 Series Air Filter', '1371-1416-696', 1600, 27, 18),
(1538, '5 Series', '5 Series Oil Filter', '1142-2218-158', 1350, 43, 18),
(1539, '5 Series', '5 Series Cabin Microfilter', '6411-6292-386', 1660, 44, 18),
(1540, '5 Series', '5 Series Front Brake Pads', '3411-5529-246', 5490, 37, 18),
(1541, '6 Series', '6 Series Spark Plugs (Set)', '1212-3160-704', 3510, 20, 18),
(1542, '6 Series', '6 Series Rear Brake Pads', '3421-8611-776', 5470, 33, 18),
(1543, '6 Series', '6 Series Wiper Blades', '6161-1950-659', 2110, 16, 18),
(1544, '6 Series', '6 Series Cabin Microfilter', '6411-5375-296', 1290, 26, 18),
(1545, '6 Series', '6 Series Front Brake Pads', '3411-2624-596', 6600, 5, 18),
(1546, '6 Series', '6 Series AGM Battery', '6121-3085-870', 12970, 13, 18),
(1547, '7 Series', '7 Series Spark Plugs (Set)', '1212-6245-188', 1750, 40, 18),
(1548, '7 Series', '7 Series Front Brake Pads', '3411-4408-202', 7190, 21, 18),
(1549, '7 Series', '7 Series Oil Filter', '1142-4752-939', 800, 41, 18),
(1550, '7 Series', '7 Series AGM Battery', '6121-9448-822', 13590, 42, 18),
(1551, '7 Series', '7 Series Rear Brake Pads', '3421-9796-684', 6370, 16, 18),
(1552, '8 Series', '8 Series Oil Filter', '1142-8201-292', 890, 33, 18),
(1553, '8 Series', '8 Series Air Filter', '1371-1425-271', 960, 40, 18),
(1554, '8 Series', '8 Series Spark Plugs (Set)', '1212-7783-997', 1640, 47, 18),
(1555, '8 Series', '8 Series Wiper Blades', '6161-9174-552', 1850, 50, 18),
(1556, 'M1', 'M1 Air Filter', '1371-6600-907', 1610, 23, 19),
(1557, 'M1', 'M1 Front Brake Pads', '3411-3349-947', 7770, 42, 19),
(1558, 'M1', 'M1 Spark Plugs (Set)', '1212-8208-425', 2580, 8, 19),
(1559, 'M1', 'M1 Rear Brake Pads', '3421-6847-109', 2690, 22, 19),
(1560, 'M1', 'M1 Cabin Microfilter', '6411-4950-745', 2020, 37, 19),
(1561, 'M1', 'M1 Oil Filter', '1142-9103-174', 510, 13, 19),
(1562, 'M2', 'M2 AGM Battery', '6121-3560-733', 11720, 26, 19),
(1563, 'M2', 'M2 Air Filter', '1371-7562-922', 1840, 47, 19),
(1564, 'M2', 'M2 Front Brake Pads', '3411-7293-691', 4690, 34, 19),
(1565, 'M2', 'M2 Rear Brake Pads', '3421-7902-301', 3070, 43, 19),
(1566, 'M3', 'M3 Spark Plugs (Set)', '1212-5396-774', 2010, 25, 19),
(1567, 'M3', 'M3 Rear Brake Pads', '3421-9143-658', 4490, 41, 19),
(1568, 'M3', 'M3 AGM Battery', '6121-3869-435', 8730, 15, 19),
(1569, 'M3', 'M3 Front Brake Pads', '3411-3957-945', 4010, 48, 19),
(1570, 'M4', 'M4 Front Brake Pads', '3411-2410-132', 4560, 27, 19),
(1571, 'M4', 'M4 Cabin Microfilter', '6411-5431-740', 1130, 35, 19),
(1572, 'M4', 'M4 AGM Battery', '6121-6067-131', 9850, 20, 19),
(1573, 'M4', 'M4 Spark Plugs (Set)', '1212-2191-712', 1660, 24, 19),
(1574, 'M4', 'M4 Rear Brake Pads', '3421-7135-741', 5520, 32, 19),
(1575, 'M4', 'M4 Air Filter', '1371-6693-393', 1730, 20, 19),
(1576, 'M4', 'M4 Oil Filter', '1142-1975-643', 650, 37, 19),
(1577, 'M4', 'M4 Wiper Blades', '6161-9227-925', 1800, 47, 19),
(1578, 'M5', 'M5 Wiper Blades', '6161-7172-932', 1880, 47, 19),
(1579, 'M5', 'M5 Rear Brake Pads', '3421-4871-626', 4650, 27, 19),
(1580, 'M5', 'M5 Front Brake Pads', '3411-8973-693', 4420, 24, 19),
(1581, 'M5', 'M5 AGM Battery', '6121-3523-633', 9110, 40, 19),
(1582, 'M5', 'M5 Cabin Microfilter', '6411-5742-959', 2480, 42, 19),
(1583, 'M6', 'M6 Rear Brake Pads', '3421-1455-235', 5940, 35, 19),
(1584, 'M6', 'M6 Cabin Microfilter', '6411-6836-752', 1010, 17, 19),
(1585, 'M6', 'M6 Air Filter', '1371-6552-498', 1250, 7, 19),
(1586, 'M6', 'M6 Spark Plugs (Set)', '1212-9692-351', 2630, 30, 19),
(1587, 'M6', 'M6 AGM Battery', '6121-2010-954', 11150, 6, 19),
(1588, 'M6', 'M6 Front Brake Pads', '3411-1613-677', 3400, 15, 19),
(1589, 'M8', 'M8 Front Brake Pads', '3411-9249-967', 6680, 38, 19),
(1590, 'M8', 'M8 Spark Plugs (Set)', '1212-7773-894', 3090, 24, 19),
(1591, 'M8', 'M8 AGM Battery', '6121-5530-147', 13440, 37, 19),
(1592, 'M8', 'M8 Wiper Blades', '6161-3992-807', 2780, 21, 19),
(1593, 'M8', 'M8 Cabin Microfilter', '6411-8480-923', 950, 48, 19),
(1594, 'M8', 'M8 Oil Filter', '1142-1427-197', 1010, 27, 19),
(1595, 'M8', 'M8 Air Filter', '1371-7622-641', 970, 13, 19),
(1596, 'X5 M', 'X5 M Rear Brake Pads', '3421-5188-597', 5790, 20, 19),
(1597, 'X5 M', 'X5 M AGM Battery', '6121-7625-174', 10860, 19, 19),
(1598, 'X5 M', 'X5 M Wiper Blades', '6161-3017-671', 1430, 29, 19),
(1599, 'X5 M', 'X5 M Front Brake Pads', '3411-7452-394', 6930, 49, 19),
(1600, 'X5 M', 'X5 M Cabin Microfilter', '6411-3771-961', 1100, 12, 19),
(1601, 'X5 M', 'X5 M Oil Filter', '1142-6508-689', 1340, 14, 19),
(1602, 'X5 M', 'X5 M Air Filter', '1371-2053-735', 940, 14, 19),
(1603, 'X6 M', 'X6 M Cabin Microfilter', '6411-2072-172', 1680, 10, 19),
(1604, 'X6 M', 'X6 M Spark Plugs (Set)', '1212-3990-207', 1700, 23, 19),
(1605, 'X6 M', 'X6 M AGM Battery', '6121-6519-170', 9120, 41, 19),
(1606, 'XM', 'XM Front Brake Pads', '3411-4609-803', 6820, 28, 19),
(1607, 'XM', 'XM Oil Filter', '1142-7833-517', 1500, 6, 19),
(1608, 'XM', 'XM Air Filter', '1371-6161-965', 1100, 14, 19),
(1609, 'XM', 'XM AGM Battery', '6121-7166-561', 13020, 33, 19),
(1610, 'XM', 'XM Spark Plugs (Set)', '1212-7432-552', 2430, 6, 19),
(1611, 'XM', 'XM Rear Brake Pads', '3421-9760-359', 4620, 17, 19),
(1612, '2 Series Active Tourer', '2 Series Active Tourer Oil Filter', '1142-5419-199', 1360, 46, 20),
(1613, '2 Series Active Tourer', '2 Series Active Tourer Wiper Blades', '6161-8709-906', 2980, 8, 20),
(1614, '2 Series Active Tourer', '2 Series Active Tourer Air Filter', '1371-1617-357', 1460, 41, 20),
(1615, '2 Series Active Tourer', '2 Series Active Tourer Spark Plugs (Set)', '1212-5393-654', 1560, 31, 20),
(1616, '2 Series Gran Tourer', '2 Series Gran Tourer Oil Filter', '1142-7370-362', 560, 23, 20),
(1617, '2 Series Gran Tourer', '2 Series Gran Tourer Cabin Microfilter', '6411-5094-554', 1440, 13, 20),
(1618, '2 Series Gran Tourer', '2 Series Gran Tourer Air Filter', '1371-7861-168', 1270, 7, 20),
(1619, '2 Series Gran Tourer', '2 Series Gran Tourer Rear Brake Pads', '3421-5632-627', 4110, 38, 20),
(1620, '2 Series Gran Tourer', '2 Series Gran Tourer Spark Plugs (Set)', '1212-2845-886', 3040, 44, 20),
(1621, '2 Series Gran Tourer', '2 Series Gran Tourer Wiper Blades', '6161-8071-948', 2730, 30, 20),
(1622, '2 Series Gran Tourer', '2 Series Gran Tourer Front Brake Pads', '3411-5597-488', 3120, 22, 20),
(1623, '3 Series GT', '3 Series GT Wiper Blades', '6161-2295-973', 1310, 21, 20),
(1624, '3 Series GT', '3 Series GT Oil Filter', '1142-1668-274', 1190, 30, 20),
(1625, '3 Series GT', '3 Series GT Cabin Microfilter', '6411-5251-452', 980, 27, 20),
(1626, '3 Series GT', '3 Series GT Rear Brake Pads', '3421-5775-903', 6600, 31, 20),
(1627, '3 Series GT', '3 Series GT AGM Battery', '6121-3910-485', 9550, 16, 20),
(1628, '3 Series GT', '3 Series GT Spark Plugs (Set)', '1212-7367-659', 3450, 9, 20),
(1629, '3 Series GT', '3 Series GT Air Filter', '1371-3889-871', 1390, 23, 20),
(1630, '5 Series GT', '5 Series GT Wiper Blades', '6161-5609-922', 2010, 11, 20),
(1631, '5 Series GT', '5 Series GT Oil Filter', '1142-8836-365', 980, 36, 20),
(1632, '5 Series GT', '5 Series GT Front Brake Pads', '3411-9379-552', 3530, 24, 20),
(1633, '5 Series GT', '5 Series GT Cabin Microfilter', '6411-3307-773', 2000, 5, 20),
(1634, '5 Series GT', '5 Series GT Rear Brake Pads', '3421-9331-466', 5490, 33, 20),
(1635, '5 Series GT', '5 Series GT AGM Battery', '6121-2792-733', 13470, 11, 20),
(1636, '5 Series GT', '5 Series GT Air Filter', '1371-7229-857', 1760, 48, 20),
(1637, '5 Series GT', '5 Series GT Spark Plugs (Set)', '1212-3033-283', 3530, 44, 20);

-- --------------------------------------------------------

--
-- Table structure for table `technician`
--

CREATE TABLE `technician` (
  `Technician_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `CurrentStatus` varchar(50) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `Specialization` varchar(100) DEFAULT NULL,
  `YearsOfExperience` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `technician`
--

INSERT INTO `technician` (`Technician_ID`, `User_ID`, `CurrentStatus`, `HireDate`, `Specialization`, `YearsOfExperience`) VALUES
(3, 3, 'Available', '2023-05-01', 'Engine Repair', 5),
(5, 14, 'Active', '2026-04-09', NULL, NULL),
(9, 47, 'Active', '2026-04-09', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `timelog`
--

CREATE TABLE `timelog` (
  `TimeLog_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `JobCard_ID` int(11) DEFAULT NULL,
  `StartTime` datetime DEFAULT NULL,
  `EndTime` datetime DEFAULT NULL,
  `TotalHours` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `timelog`
--

INSERT INTO `timelog` (`TimeLog_ID`, `User_ID`, `JobCard_ID`, `StartTime`, `EndTime`, `TotalHours`) VALUES
(8, 3, 15, '2026-03-19 09:37:54', '2026-03-19 10:14:24', 0.61),
(9, 3, 12, '2026-04-07 13:56:50', '2026-04-07 13:56:52', 0.00),
(15, 3, 18, '2026-04-08 23:29:54', '2026-04-08 23:44:56', 0.25),
(16, 3, 19, '2026-04-09 14:13:33', '2026-04-09 14:13:42', 0.00),
(17, 3, 20, '2026-04-09 14:52:22', '2026-04-09 14:55:31', 0.05),
(23, 3, 18, '2026-04-25 20:55:17', NULL, NULL),
(24, 3, 23, '2026-04-27 00:48:34', '2026-04-27 00:48:37', 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `topmanager`
--

CREATE TABLE `topmanager` (
  `Manager_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `topmanager`
--

INSERT INTO `topmanager` (`Manager_ID`, `User_ID`) VALUES
(1, 7);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `User_ID` int(11) NOT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Role` enum('Client','Technician','FinanceManager','ServiceManager','StockKeeper','DataAnalyst','Admin','TopManager') DEFAULT NULL,
  `ProfilePicture` varchar(255) DEFAULT NULL,
  `ResetToken` varchar(255) DEFAULT NULL,
  `ResetTokenExpiry` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`User_ID`, `FirstName`, `LastName`, `Password`, `Email`, `Phone`, `Address`, `Role`, `ProfilePicture`, `ResetToken`, `ResetTokenExpiry`) VALUES
(1, 'manar', 'abdelhadi', '$2b$12$.rl2GuZsPEBMCuwbD4cQRuNmv1CF5JQOWGInnER6ET9uoXcCQsxwi', 'manar@gmail.com', '0100', 'Cairo', 'Technician', NULL, NULL, NULL),
(2, 'Paula', 'Samy', '$2b$12$WnXfP4HXHxbbSUFZu5um6eW23SxqE3Lg1Rz7u4uTKEhQaTk9ev./2', 'paulasamy52@gmail.com', '01123456789', 'Alexandria', 'Client', '/assets/uploads/profiles/user_2_1777241697.jpeg', NULL, NULL),
(3, 'Mohamed', 'Khaled', '$2b$12$UUosTEJ1vEZj4wY.dF0TDexV7hYSxEPrMTr5MaU7F1X18qP2nlYr2', 'mohamed@gmail.com', '01234567890', 'Giza', 'Technician', NULL, NULL, NULL),
(4, 'Omar', 'Samy', '123456', 'omar@gmail.com', '01098765432', 'Cairo', 'ServiceManager', NULL, NULL, NULL),
(5, 'Mona', 'Adel', '123456', 'mona@gmail.com', '01111222333', 'Mansoura', 'FinanceManager', NULL, NULL, NULL),
(6, 'Hany', 'Mostafa', '123456', 'hany@gmail.com', '01222333444', 'Tanta', 'StockKeeper', '/assets/uploads/profiles/user_6_1775753476.png', NULL, NULL),
(7, 'Nour', 'Mahmoud', '123456', 'nour@gmail.com', '01033334444', 'Alexandria', 'TopManager', NULL, NULL, NULL),
(14, 'fgjhj', 'Cochran', '$2b$12$R239iu15fr1UHe7gijPCSOH/1uaU4D1k0auMAa8UMr..macpel4Rq', 'synugil@mailinator.com', '+1 (424) 815-6846', 'Dolore temporibus cu', 'Technician', NULL, NULL, NULL),
(21, 'hend', 'mahmoud', '$2b$12$7wCSCEVAqLUxB0.hgmPp.O4GsaUw.cD0VqR4gPIinIHNPQe6TxYL2', 'elbardisihend@gmail.com', '01023456789', 'cairo', 'Client', NULL, 'wKzVCaCp8ABtidnQ7OfPr5_sOQ_vzJ65CQzGLrsfsPA', '2026-03-19 12:27:59'),
(33, 'Ahmed', 'Supplier', NULL, 'supplier33@example.com', NULL, NULL, '', NULL, NULL, NULL),
(35, 'Mahmoud', 'Supplier', NULL, 'supplier35@example.com', NULL, NULL, '', NULL, NULL, NULL),
(36, 'Khaled', 'X Series', '$2b$12$gU4l6Gx0eR8/wkx2GnTJdu7LrHbj3qvaKYH2hVRJDCj19OxHmd79.', 'x_series@example.com', NULL, NULL, '', NULL, NULL, NULL),
(37, 'Ali', 'Z Series', '$2b$12$gU4l6Gx0eR8/wkx2GnTJdu7LrHbj3qvaKYH2hVRJDCj19OxHmd79.', 'z_series@example.com', NULL, NULL, '', NULL, NULL, NULL),
(38, 'Omar', 'Supplier', NULL, 'supplier38@example.com', NULL, NULL, '', NULL, NULL, NULL),
(39, 'Youssef', 'M Models', '$2b$12$gU4l6Gx0eR8/wkx2GnTJdu7LrHbj3qvaKYH2hVRJDCj19OxHmd79.', 'm_models@example.com', NULL, NULL, '', NULL, NULL, NULL),
(40, 'Tarek', 'Supplier', NULL, 'supplier40@example.com', NULL, NULL, '', NULL, NULL, NULL),
(42, 'malak', 'said', '$2b$12$ukxHR1s9X7Abhui7KtcNduCjtetof273xs/zImv.jnApR/mvS581e', 'malak_said@gmail.com', '01012345678', '10th of Ramadan', 'Admin', NULL, NULL, NULL),
(47, 'Yousef', 'Samy', '$2b$12$/kcUvEl4TpAzqHWGANBNCuXFbrUnLuSNXoxnQpXv/VMP25EOqpe/K', 'yousafsamy50@gmail.com', '01002422293', 'Cairo', 'Technician', NULL, 'GVdLgcrQQxNWWqVzgXWSg4LCSi9HBKY11mtgZGnwcp4', '2026-04-27 03:54:56'),
(48, 'Martha', 'Reyes', '$2b$12$auk9pXM6pih5JA.ov04mU.I4y.E/6/8oDgJUp49OHpQCmfWu7da9C', 'xupojiqel@mailinator.com', '19544724494', 'In ipsum velit unde', 'FinanceManager', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `Vehicle_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `VIN` varchar(50) DEFAULT NULL,
  `PlateNumber` varchar(20) DEFAULT NULL,
  `Model` varchar(50) DEFAULT NULL,
  `Year` int(11) DEFAULT NULL,
  `Mileage` int(11) DEFAULT NULL,
  `Make` varchar(50) DEFAULT NULL,
  `Color` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`Vehicle_ID`, `User_ID`, `VIN`, `PlateNumber`, `Model`, `Year`, `Mileage`, `Make`, `Color`) VALUES
(1, 2, 'VIN123', 'ABC-123', 'Camry', 2020, 50000, 'Toyota', 'Blue'),
(2, 2, 'VIN456', 'XYZ-789', 'Civic', 2021, 30000, 'Honda', 'Red'),
(3, 2, 'VIN789', 'GHI-456', 'Corolla', 2018, 80000, 'Toyota', 'White'),
(4, 6, 'VIN126', 'BBB222', 'Sunny', 2018, 70000, 'Nissan', 'Black'),
(7, 5, 'VIN129', 'EEE555', 'Octavia', 2020, 45000, 'Skoda', 'Black'),
(12, 14, 'VIN101', 'JKL-001', 'Altima', 2022, 10000, 'Nissan', 'Black'),
(30, 2, 'VIN_30', 'ABC-30', 'Model 30', 2020, 30000, 'Ford', 'Silver'),
(31, 2, 'VIN_31', 'ABC-31', 'Model 31', 2021, 31000, 'Ford', 'Silver'),
(32, 2, 'VIN_32', 'ABC-32', 'Model 32', 2022, 32000, 'Ford', 'Silver'),
(33, 2, 'VIN_33', 'ABC-33', 'Model 33', 2023, 33000, 'Ford', 'Silver'),
(34, 2, 'VIN_34', 'ABC-34', 'Model 34', 2024, 34000, 'Ford', 'Silver'),
(35, 2, 'VIN_35', 'ABC-35', 'Model 35', 2020, 35000, 'Ford', 'Silver'),
(36, 2, 'VIN_36', 'ABC-36', 'Model 36', 2021, 36000, 'Ford', 'Silver'),
(37, 2, 'VIN_37', 'ABC-37', 'Model 37', 2022, 37000, 'Ford', 'Silver'),
(38, 2, 'VIN_38', 'ABC-38', 'Model 38', 2023, 38000, 'Ford', 'Silver'),
(39, 2, 'VIN_39', 'ABC-39', 'Model 39', 2024, 39000, 'Ford', 'Silver'),
(41, 21, '54675876909867564', 'HAN1234', 'AG', 2019, 20000, 'mercedes', 'Black'),
(42, 2, 'WBS4Y9C05NFM41234', 'ABC1234', 'M4', 2022, 32000, 'BMW', 'Black'),
(43, 2, '12345678901234567', 'qwe1234', 'M4', 2014, 2000, 'BMW', 'red'),
(44, 42, '12345678901234567', 'mal1234', 'M5', 2022, 50000, 'BMW', 'blue'),
(47, 2, '11111111111111111', 'MAN1234', 'C55', 2026, 98, 'BMW', 'BLACK'),
(48, 2, 'Quae quo qui ad e', 'ABC1234', 'Aute et nisi Nam dui', 2011, 91, 'Itaque ullamco reici', 'Aute quia ut pariatu');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Admin_ID`),
  ADD KEY `User_ID` (`User_ID`);

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`Appointment_ID`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `Vehicle_ID` (`Vehicle_ID`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `certification`
--
ALTER TABLE `certification`
  ADD PRIMARY KEY (`Certification_ID`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `Vehicle_ID` (`Vehicle_ID`),
  ADD KEY `Inspection_ID` (`Inspection_ID`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`Client_ID`),
  ADD UNIQUE KEY `uq_client_user` (`User_ID`);

--
-- Indexes for table `dataanalyst`
--
ALTER TABLE `dataanalyst`
  ADD PRIMARY KEY (`DataAnalyst_ID`),
  ADD UNIQUE KEY `uq_dataanalyst_user` (`User_ID`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `financemanager`
--
ALTER TABLE `financemanager`
  ADD PRIMARY KEY (`FinanceManager_ID`),
  ADD UNIQUE KEY `uq_financemanager_user` (`User_ID`);

--
-- Indexes for table `inspection`
--
ALTER TABLE `inspection`
  ADD PRIMARY KEY (`Inspection_ID`),
  ADD KEY `Vehicle_ID` (`Vehicle_ID`),
  ADD KEY `JobCard_ID` (`JobCard_ID`);

--
-- Indexes for table `inventoryitem`
--
ALTER TABLE `inventoryitem`
  ADD PRIMARY KEY (`Item_ID`),
  ADD KEY `User_ID` (`User_ID`);

--
-- Indexes for table `invoice`
--
ALTER TABLE `invoice`
  ADD PRIMARY KEY (`Invoice_ID`),
  ADD KEY `User_ID` (`User_ID`);

--
-- Indexes for table `jobcard`
--
ALTER TABLE `jobcard`
  ADD PRIMARY KEY (`JobCard_ID`),
  ADD KEY `Vehicle_ID` (`Vehicle_ID`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `fk_jobcard_technician` (`Technician_ID`);

--
-- Indexes for table `jobcardparts`
--
ALTER TABLE `jobcardparts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Item_ID` (`Item_ID`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`Payment_ID`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `Invoice_ID` (`Invoice_ID`);

--
-- Indexes for table `purchase_order`
--
ALTER TABLE `purchase_order`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `purchase_order_stock_keeper_id_3831b2f4_fk_users_User_ID` (`stock_keeper_id`),
  ADD KEY `purchase_order_supplier_id_f3ce40ee_fk_supplier_User_ID` (`supplier_id`),
  ADD KEY `purchase_order_supplier_part_id_dca39bfe_fk_supplier_` (`supplier_part_id`);

--
-- Indexes for table `servicemanager`
--
ALTER TABLE `servicemanager`
  ADD PRIMARY KEY (`ServiceManager_ID`),
  ADD UNIQUE KEY `uq_servicemanager_user` (`User_ID`);

--
-- Indexes for table `stockkeeper`
--
ALTER TABLE `stockkeeper`
  ADD PRIMARY KEY (`StockKeeper_ID`),
  ADD UNIQUE KEY `uq_stockkeeper_user` (`User_ID`);

--
-- Indexes for table `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`Supplier_ID`),
  ADD UNIQUE KEY `uq_supplier_user` (`User_ID`);

--
-- Indexes for table `supplier_part`
--
ALTER TABLE `supplier_part`
  ADD PRIMARY KEY (`part_id`),
  ADD KEY `supplier_part_supplier_id_a64f012d_fk_supplier_User_ID` (`supplier_id`);

--
-- Indexes for table `technician`
--
ALTER TABLE `technician`
  ADD PRIMARY KEY (`Technician_ID`),
  ADD UNIQUE KEY `uq_technician_user` (`User_ID`);

--
-- Indexes for table `timelog`
--
ALTER TABLE `timelog`
  ADD PRIMARY KEY (`TimeLog_ID`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `JobCard_ID` (`JobCard_ID`);

--
-- Indexes for table `topmanager`
--
ALTER TABLE `topmanager`
  ADD PRIMARY KEY (`Manager_ID`),
  ADD KEY `fk_topmanager_user` (`User_ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`User_ID`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`Vehicle_ID`),
  ADD KEY `User_ID` (`User_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `Admin_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `Appointment_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `certification`
--
ALTER TABLE `certification`
  MODIFY `Certification_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `Client_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `dataanalyst`
--
ALTER TABLE `dataanalyst`
  MODIFY `DataAnalyst_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `financemanager`
--
ALTER TABLE `financemanager`
  MODIFY `FinanceManager_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `inspection`
--
ALTER TABLE `inspection`
  MODIFY `Inspection_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `inventoryitem`
--
ALTER TABLE `inventoryitem`
  MODIFY `Item_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=398;

--
-- AUTO_INCREMENT for table `invoice`
--
ALTER TABLE `invoice`
  MODIFY `Invoice_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `jobcard`
--
ALTER TABLE `jobcard`
  MODIFY `JobCard_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `jobcardparts`
--
ALTER TABLE `jobcardparts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `Payment_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `purchase_order`
--
ALTER TABLE `purchase_order`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `servicemanager`
--
ALTER TABLE `servicemanager`
  MODIFY `ServiceManager_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `stockkeeper`
--
ALTER TABLE `stockkeeper`
  MODIFY `StockKeeper_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `supplier`
--
ALTER TABLE `supplier`
  MODIFY `Supplier_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `supplier_part`
--
ALTER TABLE `supplier_part`
  MODIFY `part_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1638;

--
-- AUTO_INCREMENT for table `technician`
--
ALTER TABLE `technician`
  MODIFY `Technician_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `timelog`
--
ALTER TABLE `timelog`
  MODIFY `TimeLog_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `topmanager`
--
ALTER TABLE `topmanager`
  MODIFY `Manager_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `User_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `Vehicle_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `appointment`
--
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `certification`
--
ALTER TABLE `certification`
  ADD CONSTRAINT `certification_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `certification_ibfk_2` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`),
  ADD CONSTRAINT `certification_ibfk_3` FOREIGN KEY (`Inspection_ID`) REFERENCES `inspection` (`Inspection_ID`);

--
-- Constraints for table `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `client_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `dataanalyst`
--
ALTER TABLE `dataanalyst`
  ADD CONSTRAINT `dataanalyst_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `financemanager`
--
ALTER TABLE `financemanager`
  ADD CONSTRAINT `financemanager_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `inspection`
--
ALTER TABLE `inspection`
  ADD CONSTRAINT `inspection_ibfk_1` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`),
  ADD CONSTRAINT `inspection_ibfk_2` FOREIGN KEY (`JobCard_ID`) REFERENCES `jobcard` (`JobCard_ID`);

--
-- Constraints for table `inventoryitem`
--
ALTER TABLE `inventoryitem`
  ADD CONSTRAINT `inventoryitem_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `invoice`
--
ALTER TABLE `invoice`
  ADD CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `jobcard`
--
ALTER TABLE `jobcard`
  ADD CONSTRAINT `fk_jobcard_technician` FOREIGN KEY (`Technician_ID`) REFERENCES `users` (`User_ID`) ON DELETE SET NULL,
  ADD CONSTRAINT `jobcard_ibfk_1` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`),
  ADD CONSTRAINT `jobcard_ibfk_2` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`Invoice_ID`) REFERENCES `invoice` (`Invoice_ID`);

--
-- Constraints for table `purchase_order`
--
ALTER TABLE `purchase_order`
  ADD CONSTRAINT `purchase_order_stock_keeper_id_3831b2f4_fk_users_User_ID` FOREIGN KEY (`stock_keeper_id`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `purchase_order_supplier_part_id_dca39bfe_fk_supplier_` FOREIGN KEY (`supplier_part_id`) REFERENCES `supplier_part` (`part_id`);

--
-- Constraints for table `servicemanager`
--
ALTER TABLE `servicemanager`
  ADD CONSTRAINT `servicemanager_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `stockkeeper`
--
ALTER TABLE `stockkeeper`
  ADD CONSTRAINT `stockkeeper_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `supplier`
--
ALTER TABLE `supplier`
  ADD CONSTRAINT `supplier_User_ID_72ec0896_fk_users_User_ID` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `technician`
--
ALTER TABLE `technician`
  ADD CONSTRAINT `technician_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `timelog`
--
ALTER TABLE `timelog`
  ADD CONSTRAINT `timelog_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `timelog_ibfk_2` FOREIGN KEY (`JobCard_ID`) REFERENCES `jobcard` (`JobCard_ID`);

--
-- Constraints for table `topmanager`
--
ALTER TABLE `topmanager`
  ADD CONSTRAINT `fk_topmanager_user` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);

--
-- Constraints for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
