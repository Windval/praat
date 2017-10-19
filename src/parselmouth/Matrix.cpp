/*
 * Copyright (C) 2017  Yannick Jadoul
 *
 * This file is part of Parselmouth.
 *
 * Parselmouth is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Parselmouth is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Parselmouth.  If not, see <http://www.gnu.org/licenses/>
 */

#include "Parselmouth.h"

#include "praat/MelderUtils.h"
#include "utils/pybind11/NumericPredicates.h"
#include "utils/pybind11/Optional.h"

#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace py::literals;

namespace parselmouth {

void Binding<Matrix>::init() {
	// TODO Constructors (i.e., from numpy array, ...)

	def_property_readonly("values",
	                      [](Matrix self) { return py::array_t<double, py::array::f_style>({static_cast<size_t>(self->nx), static_cast<size_t>(self->ny)}, &self->z[1][1], py::cast(self)); });

	def("as_array",
	    [](Matrix self) { return py::array_t<double, py::array::f_style>({static_cast<size_t>(self->nx), static_cast<size_t>(self->ny)}, &self->z[1][1], py::cast(self)); });

	def_buffer([](Matrix self) { return py::buffer_info(&self->z[1][1], {static_cast<ssize_t>(self->nx), static_cast<ssize_t>(self->ny)}, {static_cast<ssize_t>(sizeof(double)), static_cast<ssize_t>(self->nx * sizeof(double))}); });

	def("save_as_matrix_text_file",
	    [](Matrix self, const std::u32string &filePath) {
		    auto file = pathToMelderFile(filePath);
		    Matrix_writeToMatrixTextFile(self, &file);
	    },
	    "file_path"_a);

	def("save_as_headerless_spreadsheet_file",
	    [](Matrix self, const std::u32string &filePath) {
		    auto file = pathToMelderFile(filePath);
		    Matrix_writeToHeaderlessSpreadsheetFile(self, &file);
	    },
	    "file_path"_a);

	def("get_lowest_x", [](Matrix self) { return self->xmin; });

	def("get_highest_x", [](Matrix self) { return self->xmax; });

	def("get_lowest_y", [](Matrix self) { return self->ymin; });

	def("get_highest_y", [](Matrix self) { return self->ymax; });

	def("get_number_of_rows", [](Matrix self) { return self->ny; });

	def_readonly("n_rows", &structMatrix::ny);

	def("get_number_of_columns", [](Matrix self) { return self->nx; });

	def_readonly("n_columns", &structMatrix::nx);

	def("get_row_distance", [](Matrix self) { return self->dy; });

	def("get_column_distance", [](Matrix self) { return self->dx; });

	def("get_y_of_row",
	    [](Matrix self, Positive<integer> rowNumber) { return Matrix_rowToY(self, rowNumber); },
	    "row_number"_a);

	def("get_x_of_column",
	    [](Matrix self, Positive<integer> columnNumber) { return Matrix_rowToY(self, columnNumber); },
	    "column_number"_a);

	def("get_value_in_cell",
	    [](Matrix self, Positive<integer> rowNumber, Positive<integer> columnNumber) {
		    if (rowNumber > self->ny) Melder_throw (U"Row number must not exceed number of rows.");
		    if (columnNumber > self->nx) Melder_throw (U"Column number must not exceed number of columns.");
		    return self->z[rowNumber][columnNumber]; },
	    "row_number"_a, "column_number"_a);

	def("get_value_at_xy",
	    &Matrix_getValueAtXY,
	    "x"_a, "y"_a);

	def("at_xy",
	    &Matrix_getValueAtXY,
	    "x"_a, "y"_a);

	def("get_minimum",
		[](Matrix self) {
			double minimum = undefined;
			double maximum = undefined;
			Matrix_getWindowExtrema(self, 0, 0, 0, 0, &minimum, &maximum);
			return minimum;
		});

	def("get_maximum",
	    [](Matrix self) {
		    double minimum = undefined;
		    double maximum = undefined;
		    Matrix_getWindowExtrema(self, 0, 0, 0, 0, &minimum, &maximum);
		    return maximum;
	    });

	def("get_sum",
	    &Matrix_getSum);

	def("formula", // TODO Make formula into some kind of class?
	    [](Matrix self, const std::u32string &formula, optional<double> fromX, optional<double> toX, optional<double> fromY, optional<double> toY) {
		    if (!fromX && !toX && !fromY && !toY) {
			    Matrix_formula(self, formula.c_str(), nullptr, nullptr);
		    }
		    else {
			    Matrix_formula_part(self, fromX.value_or(self->xmin), toX.value_or(self->xmax), fromY.value_or(self->ymin), toY.value_or(self->ymax), formula.c_str(), nullptr, nullptr);
		    }
	    },
	    "formula"_a, "from_x"_a = nullopt, "to_x"_a = nullopt, "from_y"_a = nullopt, "to_y"_a = nullopt);

	def("formula",
	    [](Matrix self, const std::u32string &formula, std::pair<optional<double>, optional<double>> xRange, std::pair<optional<double>, optional<double>> yRange) {
		    Matrix_formula_part(self, xRange.first.value_or(self->xmin), xRange.second.value_or(self->xmax), yRange.first.value_or(self->ymin), yRange.second.value_or(self->ymax), formula.c_str(), nullptr, nullptr);
	    },
	    "formula"_a, "x_range"_a = std::make_pair(nullopt, nullopt), "y_range"_a = std::make_pair(nullopt, nullopt));

	def("set_value",
	    [](Matrix self, Positive<integer> rowNumber, Positive<integer> columnNumber, double newValue) {
		    if (rowNumber > self->ny) Melder_throw (U"Your row number should not be greater than your number of rows.");
		    if (columnNumber > self->nx) Melder_throw (U"Your column number should not be greater than your number of columns.");
		    self->z[rowNumber][columnNumber] = newValue;
	    },
	    "row_number"_a, "column_number"_a, "new_value"_a);

	// TODO But wait, there's more! Analyse, Synthesize, & Cast subsections, and of course praat_David_init...
}

} // namespace parselmouth
