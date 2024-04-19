-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 14, 2024 at 07:14 PM
-- Server version: 10.3.39-MariaDB-0ubuntu0.20.04.2
-- PHP Version: 7.4.3-4ubuntu2.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Drop existing database and recreate
DROP DATABASE IF EXISTS barchart_scraper;
CREATE DATABASE IF NOT EXISTS barchart_scraper;
USE barchart_scraper;

-- --------------------------------------------------------

-- Table structure for table `barchart`
CREATE TABLE `barchart` (
  `id` int(11) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `currency_id` smallint(6) DEFAULT NULL,
  `ind_name_id` smallint(6) DEFAULT NULL,
  `strength_id` tinyint(4) DEFAULT NULL,
  `direction_id` tinyint(4) DEFAULT NULL,
  `ind_signal_id` tinyint(4) DEFAULT NULL,
  `overall_percentage` tinyint UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Indexes for table `barchart`
ALTER TABLE `barchart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `currency_id` (`currency_id`);

-- AUTO_INCREMENT for table `barchart`
ALTER TABLE `barchart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------

-- Table structure for table `currency`
CREATE TABLE `currency` (
  `id` smallint(6) NOT NULL,
  `currency_name` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table `currency`
INSERT INTO `currency` (`id`, `currency_name`) VALUES
(31, 'AUD'),
(7, 'AUD_CAD'),
(3, 'AUD_CHF'),
(1, 'AUD_JPY'),
(4, 'AUD_NZD'),
(2, 'AUD_USD'),
(30, 'CAD'),
(9, 'CAD_CHF'),
(8, 'CAD_JPY'),
(36, 'CHF'),
(10, 'CHF_JPY'),
(32, 'CNY'),
(37, 'DXY_'),
(28, 'EUR'),
(11, 'EUR_AUD'),
(12, 'EUR_CAD'),
(13, 'EUR_CHF'),
(14, 'EUR_GBP'),
(15, 'EUR_JPY'),
(16, 'EUR_NZD'),
(6, 'EUR_USD'),
(33, 'GBP'),
(17, 'GBP_AUD'),
(18, 'GBP_CAD'),
(19, 'GBP_CHF'),
(20, 'GBP_JPY'),
(5, 'GBP_USD'),
(34, 'JPY'),
(35, 'NZD'),
(24, 'NZD_CAD'),
(23, 'NZD_CHF'),
(22, 'NZD_JPY'),
(21, 'NZD_USD'),
(38, 'UAH'),
(29, 'USD'),
(25, 'USD_CAD'),
(26, 'USD_CHF'),
(27, 'USD_JPY');

-- Indexes for table `currency`
ALTER TABLE `currency`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_name` (`currency_name`);

-- AUTO_INCREMENT for table `currency`
ALTER TABLE `currency`
  MODIFY `id` smallint(6) NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------

-- Table structure for table `ind_name`
CREATE TABLE `ind_name` (
  `id` int(11) NOT NULL,
  `ind_name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `ind_name`
INSERT INTO `ind_name` (`id`, `ind_name`) VALUES
(1, 'NEnv4_test'),
(2, 'NStochCrossD_Sell'),
(3, 'NStochCrossD'),
(4, 'NashMACDcrossH1_Sell'),
(5, 'NashMACDcrossH1'),
(6, 'NStochCrossH1'),
(7, 'NStochCrossH1_Sell'),
(8, 'N_BBStochRSIOBOSH1'),
(9, 'Test1'),
(10, 'N_testdifftf'),
(11, 'NEnv2025_v2'),
(12, 'NEnv2025_v3'),
(13, 'Pivot Points High Low'),
(14, 'TDI_Alert_H1'),
(15, 'N_OBOS_2024_H1'),
(16, 'N_PivotPointsAlertH1'),
(17, 'N_FLI_H1'),
(18, 'NStochCrossM1'),
(19, '2024_RSI_Stoch_BB_OBOS_v1'),
(20, 'SharkFinOBOS'),
(21, '2024_EMA_1020Cross'),
(22, '2024_SharkFinOBOS'),
(23, '2024_Liquidity'),
(24, '20 day moving avg');

-- Indexes for table `ind_name`
ALTER TABLE `ind_name`
  ADD PRIMARY KEY (`id`);

-- AUTO_INCREMENT for table `ind_name`
ALTER TABLE `ind_name`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------

-- Table structure for table `ind_signal`
CREATE TABLE `ind_signal` (
  `id` tinyint(4) NOT NULL,
  `ind_signal` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `ind_signal`
INSERT INTO `ind_signal` (`id`, `ind_signal`) VALUES
(1, 'BUY SOON'),
(2, 'SELL SOON'),
(3, 'RANGE'),
(4, 'SELL'),
(5, 'BUY'),
(6, 'Stayout'),
(7, 'BUY NOW'),
(8, 'SELL NOW');


-- Indexes for table `ind_signal`
ALTER TABLE `ind_signal`
  ADD PRIMARY KEY (`id`);

-- AUTO_INCREMENT for table `ind_signal`
ALTER TABLE `ind_signal`
  MODIFY `id` tinyint(4) NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------

-- Table structure for table `barchart_strength_direction`
CREATE TABLE `barchart_strength_direction` (
  `id` int(11) NOT NULL,
  `signal_type` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `barchart_strength_direction`

INSERT INTO `barchart_strength_direction` (`id`, `signal_type`) VALUES
(1, 'Maximum'),
(2, 'Strongest'),
(3, 'Average'),
(4, 'Strengthening'),
(5, 'Weak'),
(6, 'Maximum'),
(7, 'Average'),
(8, 'Soft'),
(9, 'Strong');

-- Indexes for table `barchart_strength_direction`
ALTER TABLE `barchart_strength_direction`
  ADD PRIMARY KEY (`id`);

-- AUTO_INCREMENT for table `barchart_strength_direction`
ALTER TABLE `barchart_strength_direction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;