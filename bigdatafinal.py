import argparse
import csv

def color_gen(file_path, error_color):
    color_counts = {}
    broken_cells = []

    error_color = error_color.strip().lower()
    try:
        with open(file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            print("Reading CSV file")
            for row_num, row in enumerate(csv_reader, start=1):
                if row:
                    for col_num, cell in enumerate(row, start=1):
                        cleaned_cell = cell.strip().lower()
                        broken_type = None

                        if not cleaned_cell:
                            broken_type = "empty"
                        elif cleaned_cell == error_color:
                            broken_type = "error"

                        if broken_type:
                            broken_cells.append((broken_type, row_num, col_num))
                            color_counts[broken_type] = color_counts.get(broken_type, 0) + 1
                        else:
                            color_counts[cleaned_cell] = color_counts.get(cleaned_cell, 0) + 1

            for broken_type, row_num, col_num in broken_cells:
                if broken_type == "empty":
                    yield f"Found an empty cell at row {row_num} col {col_num}"
                elif broken_type == "error":
                    yield f"Found an {error_color.capitalize()} broken cell at row {row_num} col {col_num}"

            yield "\nDone Reading CSV file"

    except FileNotFoundError:
        yield f"Error: File '{file_path}' not found."
    except Exception as e:
        yield f"An error occurred: {e}"

    for color, count in color_counts.items():
        if color not in {"empty", "error"}:
            yield f"Color: {color.capitalize()}, Number of Cells: {count}"

def main():
    parser = argparse.ArgumentParser(description="Read CSV file and count colors / count broken cells.")
    parser.add_argument("-error", help="Specify the error color", required=True)

    args = parser.parse_args()
    error_trigger_color = args.error

    csv_file_path = "ColorsUpD.csv"

    for message in color_gen(csv_file_path, error_trigger_color):
        print(message)

if __name__ == "__main__":
    main()
