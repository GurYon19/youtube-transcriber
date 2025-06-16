#!/usr/bin/env python3
"""
Script to split links.txt into smaller batches for processing.
Helps avoid GitHub Actions time limits and makes processing more manageable.
"""

import os

def create_batches(input_file="links.txt", batch_size=15, output_prefix="links_batch"):
    """
    Split links.txt into smaller batch files.
    
    Args:
        input_file: Path to the original links file
        batch_size: Number of links per batch (default: 15)
        output_prefix: Prefix for batch files
    """
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return
    
    # Read all links
    with open(input_file, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not links:
        print("No valid links found!")
        return
    
    total_links = len(links)
    total_batches = (total_links + batch_size - 1) // batch_size  # Ceiling division
    
    print(f"Found {total_links} links")
    print(f"Creating {total_batches} batches of {batch_size} links each")
    
    # Create batch files
    for i in range(total_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, total_links)
        batch_links = links[start_idx:end_idx]
        
        batch_filename = f"{output_prefix}_{i+1:02d}.txt"
        
        with open(batch_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Batch {i+1}/{total_batches} - Links {start_idx+1}-{end_idx}\n")
            for link in batch_links:
                f.write(f"{link}\n")
        
        print(f"Created {batch_filename} with {len(batch_links)} links")
    
    # Create a summary file
    with open("batches_summary.txt", 'w', encoding='utf-8') as f:
        f.write(f"Batch Processing Summary\n")
        f.write(f"=======================\n\n")
        f.write(f"Total links: {total_links}\n")
        f.write(f"Batch size: {batch_size}\n")
        f.write(f"Total batches: {total_batches}\n\n")
        f.write(f"Batch files created:\n")
        for i in range(total_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, total_links)
            batch_filename = f"{output_prefix}_{i+1:02d}.txt"
            f.write(f"- {batch_filename} (links {start_idx+1}-{end_idx})\n")
        
        f.write(f"\nTo process each batch:\n")
        for i in range(total_batches):
            batch_filename = f"{output_prefix}_{i+1:02d}.txt"
            f.write(f"1. Rename {batch_filename} to links.txt\n")
            f.write(f"2. Run the transcription\n")
            f.write(f"3. Backup/rename the results\n")
            f.write(f"4. Repeat for next batch\n\n")
    
    print(f"\nSummary saved to: batches_summary.txt")
    print(f"\nTo process a batch:")
    print(f"1. Copy {output_prefix}_01.txt to links.txt")  
    print(f"2. Run: docker-compose up --build")
    print(f"3. Backup your transcript files")
    print(f"4. Repeat with next batch")

if __name__ == "__main__":
    # You can adjust the batch size here
    batch_size = 15  # 15 videos per batch - should take ~2-3 hours
    
    print("YouTube Transcription Batch Creator")
    print("===================================")
    
    create_batches(batch_size=batch_size) 