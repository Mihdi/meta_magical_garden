from typing import Tuple

def convert_1d_position_to_2d(
	position,
	column_length
) -> Tuple[int, int]:
	col = position % column_length
	row = position // column_length
	
	return (col, row)


def convert_2d_position_to_1d(
	col_position,
	row_position,
	column_length
) -> int:
	return row_position * column_length + col_position
