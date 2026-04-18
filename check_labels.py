import csv

def normalize(text):
    return ''.join(text.lower().split())

def check_labels(csv_file):
    inconsistencies = []
    gpu_keywords = ['rtx', 'gtx', 'radeon', 'uhdgraphics', 'intelgraphics', 'iris', 'vega', 'mx550', 'rtxpro1000']
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            name = row['name']
            manual_gpu = row['manual_gpu'].strip()
            name_norm = normalize(name)
            manual_gpu_norm = normalize(manual_gpu)
            if manual_gpu.lower() == 'none':
                # Check if any GPU is mentioned in name
                mentioned = any(normalize(keyword) in name_norm for keyword in gpu_keywords)
                if mentioned:
                    inconsistencies.append(f"Row {row_num}: Label is 'None' but GPU mentioned in name: {row['name'][:50]}...")
            else:
                # Check if the normalized manual_gpu is in the normalized name
                if manual_gpu_norm not in name_norm:
                    inconsistencies.append(f"Row {row_num}: Label '{manual_gpu}' not found in name: {row['name'][:50]}...")
    return inconsistencies

if __name__ == "__main__":
    csv_file = '/home/jovyan/work/data/evaluate_data/gpu_sample.csv'
    issues = check_labels(csv_file)
    if issues:
        print("Inconsistencies found:")
        for issue in issues:
            print(issue)
    else:
        print("All labels appear consistent.")