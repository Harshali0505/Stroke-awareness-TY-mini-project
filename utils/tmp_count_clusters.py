
import csv
import collections
import os

base_path = 'clustering_v2'
files = {
    'kmeans_results.csv': 'cluster_kmeans',
    'gmm_results.csv': 'cluster_gmm',
    'hierarchical_results.csv': 'cluster_hierarchical',
    'spectral_results.csv': 'cluster_spectral',
    'dbscan_results.csv': 'cluster_dbscan'
}

with open('cluster_counts.txt', 'w') as out_f:
    for filename, col_name in files.items():
        file_path = os.path.join(base_path, filename)
        if not os.path.exists(file_path):
            out_f.write(f'File {filename} not found.\n')
            continue
            
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                counts = collections.Counter()
                for row in reader:
                    counts[row[col_name]] += 1
                out_f.write(f'-- {filename} --\n')
                for cluster, count in sorted(counts.items(), key=lambda x: (int(x[0]) if x[0].replace("-","").isdigit() else x[0])):
                    out_f.write(f'Cluster {cluster}: {count} respondents\n')
                out_f.write('\n')
        except Exception as e:
            out_f.write(f'Error reading {filename}: {e}\n')
