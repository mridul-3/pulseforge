# Constants
seconds_per_day = 86400
days_per_year = 365
seconds_per_year = seconds_per_day * days_per_year  
metrics_per_record = 4  
bytes_per_point = 16  

# Inputs
n_participants_list = [1, 1000, 10000]
years_list = [1, 2, 5]
compression_rate = 0.80

print("=== Data Volume Estimation ===\n")

for n in n_participants_list:
    for years in years_list:
        total_points = n * metrics_per_record * seconds_per_year * years
        raw_bytes = total_points * bytes_per_point
        compressed_bytes = raw_bytes * (1 - compression_rate)

        raw_gb = raw_bytes / (1024 ** 3)
        compressed_gb = compressed_bytes / (1024 ** 3)

        print(f"Participants: {n}, Years: {years}")
        print(f"  → Total Data Points     : {total_points:,}")
        print(f"  → Raw Size (Uncompressed): {raw_gb:.2f} GB")
        print(f"  → Compressed Size (80%)  : {compressed_gb:.2f} GB\n")