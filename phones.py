import csv

def compare_and_print_operator(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8-sig') as file1, open(file2_path, 'r', encoding='utf-8-sig') as file2:
            reader1 = csv.DictReader(file1, delimiter=';')
            ranges_data = list(csv.DictReader(file2, delimiter=';'))

            for row1 in reader1:
                phone_number_3_digits = row1['phone_number'][1:4]  # Keep the original comparison
                phone_number_from_5th_digit = int(row1['phone_number'][4:])  # New: from 5th digit to the end

                match_found = False
                for row2 in ranges_data:
                    abc_def_digits = row2['АВС/ DEF']
                    range_from = int(row2['От'])
                    range_to = int(row2['До'])

                    if phone_number_3_digits == abc_def_digits and range_from <= phone_number_from_5th_digit <= range_to:
                        print(row2['АВС/ DEF'], int(row2['От']), int(row2['До']))
                        print(f"Matching Operator for phone number {row1['phone_number']}: {row2['Оператор']}")
                        match_found = True
                        break

                if not match_found:
                    print(f"No matching operator found for phone number {row1['phone_number']}.")

    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
compare_and_print_operator('phones.csv', 'ranges.csv')
