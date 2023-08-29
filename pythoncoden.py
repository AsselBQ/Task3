import csv
import argparse

def csv_generator(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row

def create_color_count(data, error_condition=None):
    color_count = {}
    error_cells = []

    for row_idx, row in enumerate(data, start=1):
        for col_idx, cell_value in enumerate(row, start=1):
            if error_condition and error_condition(cell_value):
                error_cells.append((row_idx, col_idx))
                continue

            if cell_value in color_count:
                color_count[cell_value] += 1
            else:
                color_count[cell_value] = 1

    return color_count, error_cells

def main():
    parser = argparse.ArgumentParser(description="Count color occurrences in a CSV file.")
    parser.add_argument("-error", dest="error_color", help="Color to trigger an error condition")
    args = parser.parse_args()

    error_condition = lambda color: color == args.error_color if args.error_color else None

    file_path = "Colors.csv"
    data_generator = csv_generator(file_path)
    data = list(data_generator)
    color_count, error_cells = create_color_count(data, error_condition)

    print("Reading CSV file\n")
    for row_idx, col_idx in error_cells:
        print(f"Found a broken cell in row {row_idx} col {col_idx}")

    print("\nDone reading CSV file\n")

    for color, count in color_count.items():
        print(f"{count} {color} cells")

if __name__ == "__main__":
    main()
