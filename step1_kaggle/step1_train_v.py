import argparse
import csv
from collections import defaultdict
import re
import os

def parse_feature_range(range_str):
    """Input argument 1: feature range (supports single numbers, comma-separated values, and multi-value ranges)"""
    try:
        features = set()
        parts = range_str.split(',')
        
        for part in parts:
            # range
            if '-' in part:
                start, end = map(int, part.split('-'))
                features.update(range(start, end + 1))
            # single number
            else:
                features.add(int(part))
        # return a list with all input feature numbers (small to large)
        return sorted(features)

    except (ValueError, TypeError) as e:
        print(f"Error: Invalid feature range format '{range_str}': {e}")
        return []

def calculate_frequencies(input_file, selected_features, output_file):
    """Calculate occurrence frequencies for specified categorical features"""

    # Use nested dictionaries
    feature_counts = defaultdict(lambda: defaultdict(int))
    total_data_rows = 0  # Real total data rows
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        
        for row in reader:
            # skip meaningless row (if have)
            if len(row) < 40:  # 1(label) + 13(int) + 26(cat) = 40 column
                continue
            
            total_data_rows += 1
            
            # Process each selected categorical feature
            for feat_index in selected_features:
                if feat_index > 26 or feat_index < 1:
                    continue
                    
                # Calculate absolute column position (0-based indexing)
                # [label] + 13 int + 26 cat → start at index 14
                col_index = 13 + feat_index
                
                # Handle missing values
                if col_index >= len(row):
                    value = "MISSING"
                # empty value
                else:
                    value = row[col_index].strip()
                    if not value:
                        value = "MISSING"
                
                feature_counts[feat_index][value] += 1
    
    if total_data_rows == 0:
        print("Error: No valid data found")
        return total_data_rows
    
    # Write result in csv
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['feature_id', 'feature_value', 'count', 'frequency'])
        
        for feat_id in sorted(feature_counts.keys()):
            # Sort by count descending
            sorted_items = sorted(
                feature_counts[feat_id].items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            for value, count in sorted_items:
                # Calculate frequency
                frequency = count / total_data_rows
                writer.writerow([f'C{feat_id}', value, count, f"{frequency:.9f}"])
    
    return total_data_rows

def display_progress(total_rows, file_path):
    """Display progress information in the terminal"""
    filesize = os.path.getsize(file_path) # get file size

    readable_size = human_readable_size(filesize)
    
    print(f"Processed data: {total_rows:,} rows")
    print(f"Input file size: {readable_size}")
    
def human_readable_size(size, decimal_places=2):
    """Change to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            break
        if unit != 'GB':
            size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Calculate frequency of categorical features')

    # Define input_file as positional argument
    parser.add_argument('input_file', help='Input file path')
    
    # Features range as required option
    parser.add_argument(
        '--features', 
        type=str,
        required=True,
        help='Features to analyze (e.g., 1,3,5-8 or 2-26)'
    )
    
    # Optional output path with default value
    parser.add_argument(
        '--output',
        default='feature_frequencies.csv',
        help='Output CSV file path (default: feature_frequencies.csv)'
    )
    
    args = parser.parse_args()
    
    selected_features = parse_feature_range(args.features)
    
    if not selected_features:
        print("Error: No valid features specified")
        return
    
    print(f"Analyzing features: {[f'C{i}' for i in selected_features]}")
    print("Processing data...")
    
    # Calculate frequency and get total rows
    total_rows = calculate_frequencies(args.input_file, selected_features, args.output)
    
    if total_rows > 0:
        print("\nProcessing completed!")
        print(f"Total data rows processed: {total_rows:,}")
        print(f"Results saved to: {args.output}")
        
        try:
            display_progress(total_rows, args.input_file)
        except FileNotFoundError:
            print("Error: Unable to get input file size information")
        

        try:
            output_size = os.path.getsize(args.output)
            print(f"Output file size:: {human_readable_size(output_size)}")
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    main()
