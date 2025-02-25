"""
Module Docstring: test_bus_data_calculations

This module contains includes tests for
 functions for calculating bus data,
such as speed calculation, violation coordinates extraction,
and results saving.
"""
import os
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
import requests

from BusTracker.src.bus_data_calculations import (
    calculate_speed,
    get_violation_coordinates,
    save_results,
)
from BusTracker.utils import conect_to_api, haversine_distance, process_data, convert_to_dict


class TestYourModule(unittest.TestCase):
    """Test cases for functions in the bus_data_calculations module."""

    def setUp(self):
        """Set up any necessary data or configuration for your tests."""
        self.test_output_file = "test_output.csv"
        self.test_results_df = pd.DataFrame(
            {"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]}
        )

    def tearDown(self):
        """Clean up any resources or data created during the tests."""
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

    #New test
    def test_haversine_distance(self):
        """Test the haversine_distance function."""
        lat1, lon1 = 52.2296756, 21.0122287  # Warsaw
        lat2, lon2 = 41.8919300, 12.5113300  # Rome
        distance = haversine_distance(lat1, lon1, lat2, lon2)

        self.assertEqual(distance, 1315510)

    #New test
    def test_process_data_invalid(self):
        """Test the process_data function with invalid data."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "Błędna metoda lub parametry wywołania"}
        output_file_path = "test_output.csv"

        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            process_data(mock_response, output_file_path)

            mock_file.assert_not_called()

    #New test
    def test_convert_to_dict(self):
        """Test the convert_to_dict function."""
        str_dict = "{'key1': 'value1', 'key2': 'value2'}"
        result = convert_to_dict(str_dict)

        self.assertEqual(result, {"key1": "value1", "key2": "value2"})

    def test_calculate_speed(self):
        """Test the calculate_speed function."""
        vehicle = [
            {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
            {"Time": "2022-01-01 12:01:00", "Lat": 0.008994, "Lon": 0},
        ]

        speed = calculate_speed(vehicle, 1)
        self.assertEqual(round(speed), 60.0)


    #New test
    def test_calculate_speed_zero_speed(self):
        """Test for the case where the vehicle does not move."""
        vehicle = [
            {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
            {"Time": "2022-01-01 12:01:00", "Lat": 0, "Lon": 0},
        ]
        speed = calculate_speed(vehicle, 1)
        self.assertEqual(speed, 0.0)

    #New test
    def test_calculate_speed_negative_time(self):
        """Test for negative time difference (invalid case)."""
        vehicle = [
            {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
            {"Time": "2022-01-01 11:59:00", "Lat": 0.008994, "Lon": 0},
        ]
        with self.assertRaises(ValueError):
            calculate_speed(vehicle, 1)

    #New test
    def test_get_violation_coordinates_invalid_gps(self):
        """Test for invalid GPS coordinates."""
        json_data = {
            "vehicle1": [
                {"Time": "2022-01-01 12:00:00", "Lat": 1000, "Lon": 2000},
                {"Time": "2022-01-01 12:01:00", "Lat": 1000, "Lon": 2000},
            ],
        }
        violations_coordinates = get_violation_coordinates(json_data, max_speed=50.0)
        self.assertEqual(violations_coordinates, [])

    def test_get_violation_coordinates(self):
        """Test the get_violation_coordinates function."""
        json_data = {
            "vehicle1": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0.008994, "Lon": 0},
            ],
            "vehicle2": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0, "Lon": 0.001},
            ],
        }

        violations_coordinates = get_violation_coordinates(
            json_data, max_speed=50.0)
        expected_coordinates = [(0.008994, 0, None)]
        self.assertEqual(violations_coordinates, expected_coordinates)

    #New test
    def test_get_violation_coordinates_no_violations(self):
        """Test for no violations in the data."""
        json_data = {
            "vehicle1": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0.008994, "Lon": 0},
            ],
            "vehicle2": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0, "Lon": 0.001},
            ],
        }
        violations_coordinates = get_violation_coordinates(json_data, max_speed=100.0)
        self.assertEqual(violations_coordinates, [])

    # New test
    def test_get_violation_coordinates_multiple_violations(self):
        """Test for multiple violations in the data."""
        json_data = {
            "vehicle1": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0.008994, "Lon": 0},
                {"Time": "2022-01-01 12:02:00", "Lat": 0.017988, "Lon": 0},
            ],
            "vehicle2": [
                {"Time": "2022-01-01 12:00:00", "Lat": 0, "Lon": 0},
                {"Time": "2022-01-01 12:01:00", "Lat": 0, "Lon": 0.001},
            ],
        }
        violations_coordinates = get_violation_coordinates(json_data, max_speed=50.0)
        expected_coordinates = [
            (0.008994, 0, None),
            (0.017988, 0, None),
        ]
        self.assertEqual(violations_coordinates, expected_coordinates)

    # New test
    def test_save_results_invalid_file(self):
        """Test for saving results to an invalid file path."""
        invalid_output_file = "/invalid/path/test_output.csv"
        with self.assertRaises(OSError):
            save_results(self.test_results_df, invalid_output_file)

    def test_save_results(self):
        """Test the save_results function."""
        save_results(self.test_results_df, self.test_output_file)

        self.assertTrue(os.path.exists(self.test_output_file))
        saved_df = pd.read_csv(self.test_output_file)
        pd.testing.assert_frame_equal(self.test_results_df, saved_df)

    #New test
    def test_save_results_overwrite(self):
        """Test for overwriting existing result file."""
        save_results(self.test_results_df, self.test_output_file)
        new_df = pd.DataFrame({"Column1": [4, 5, 6], "Column2": ["D", "E", "F"]})
        save_results(new_df, self.test_output_file)

        saved_df = pd.read_csv(self.test_output_file)
        pd.testing.assert_frame_equal(new_df, saved_df)

    @patch("BusTracker.utils.requests.get")
    def test_conect_to_api(self, mock_get):
        """Test the conect_to_api function."""
        query_params = {"your": "query", "parameters": "here"}
        mock_records = [{"field1": "value1", "field2": "value2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": mock_records}
        mock_get.return_value = mock_response
        records = conect_to_api(query_params)

        mock_get.assert_called_once_with(
            "https://api.um.warszawa.pl/api/action/dbtimetable_get/",
            params=query_params,
            timeout=5,
        )

        self.assertEqual(records, mock_records)

    # New test
    def test_conect_to_api_invalid_url(self):
        """Test for an invalid API URL."""
        with patch("BusTracker.utils.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException
            with self.assertRaises(requests.exceptions.RequestException):
                conect_to_api({"your": "query", "parameters": "here"})



if __name__ == "__main__":
    unittest.main()
