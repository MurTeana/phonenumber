import csv
import os

DELIMITER = ';'
OUTPUT_FOLDER = 'output_files'  # Specify the name of the output folder


def sanitize_filename(filename):
    """
    Replace invalid characters in a filename with underscores.
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def compare_and_print_operator(phones_file, ranges_file):
    """
    Compare phone numbers from 'phones_file' with ranges from 'ranges_file'
    and create separate CSV files for each operator with matching phone numbers.
    """
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        with open(phones_file, 'r', encoding='utf-8-sig') as phones, \
                open(ranges_file, 'r', encoding='utf-8-sig') as ranges:

            phone_reader = csv.DictReader(phones, delimiter=DELIMITER)
            ranges_data = list(csv.DictReader(ranges, delimiter=DELIMITER))

            # Dictionary to store output writers for each operator
            output_writers = {}

            for phone_row in phone_reader:
                phone_number_3_digits = phone_row['phone_number'][1:4]
                phone_number_from_5th_digit = int(phone_row['phone_number'][4:])

                for range_row in ranges_data:
                    abc_def_digits = range_row['АВС/ DEF']
                    range_from = int(range_row['От'])
                    range_to = int(range_row['До'])

                    if (phone_number_3_digits == abc_def_digits and
                            range_from <= phone_number_from_5th_digit <= range_to):

                        operator = range_row['Оператор']

                        # Sanitize the operator's name for use in the filename
                        sanitized_operator = sanitize_filename(operator)

                        # Create a new output file if it doesn't exist in the output folder
                        if sanitized_operator not in output_writers:
                            output_filename = os.path.join(OUTPUT_FOLDER, f'{sanitized_operator}.csv')
                            output_writers[sanitized_operator] = csv.DictWriter(
                                open(output_filename, 'w', newline='', encoding='utf-8-sig'),
                                fieldnames=['phone_number']
                            )
                            output_writers[sanitized_operator].writeheader()

                        # Write the matching phone number to the operator's output file
                        output_writers[sanitized_operator].writerow({'phone_number': phone_row['phone_number']})
                        break

    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
compare_and_print_operator('phones.csv', 'ranges.csv')
