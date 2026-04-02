import os
import shutil
import random

# --- CONFIGURATION ---
SOURCE_PATH = "other_files/fruit_trainer/FRUIT-16K"   # Path to your extracted Mendeley/Fruit-16K folder
OUTPUT_PATH = "other_files/fruit_trainer/dataset"     # Where the organized data will go
TRAIN_SPLIT = 0.7             # 70% for Training

# Target subdirectories
CATEGORIES = {
    'F_': 'fresh',
    'S_': 'spoiled'
}

def prepare_structure():
    """Creates the train/validation and fresh/spoiled folders."""
    for split in ['train', 'validation']:
        for cat in CATEGORIES.values():
            os.makedirs(os.path.join(OUTPUT_PATH, split, cat), exist_ok=True)

def transfer_images():
    prepare_structure()
    
    # List all subdirectories in the raw dataset (e.g., F_Apple, S_Banana)
    subfolders = [d for d in os.listdir(SOURCE_PATH) if os.path.isdir(os.path.join(SOURCE_PATH, d))]
    
    for folder in subfolders:
        # Identify if folder is Fresh or Spoiled
        prefix = folder[:2]
        if prefix not in CATEGORIES:
            print(f"Skipping unknown folder: {folder}")
            continue
            
        target_cat = CATEGORIES[prefix]
        folder_path = os.path.join(SOURCE_PATH, folder)
        
        # Get all image files
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(images)
        
        # Calculate split
        split_point = int(len(images) * TRAIN_SPLIT)
        train_set = images[:split_point]
        val_set = images[split_point:]
        
        # Helper to copy files with unique names
        def copy_files(file_list, split_name):
            for filename in file_list:
                src = os.path.join(folder_path, filename)
                # Rename file to include folder name to avoid collisions (e.g., Apple_img1.jpg)
                dst_name = f"{folder}_{filename}"
                dst = os.path.join(OUTPUT_PATH, split_name, target_cat, dst_name)
                shutil.copy2(src, dst)

        copy_files(train_set, 'train')
        copy_files(val_set, 'validation')
        print(f"Processed {folder}: {len(train_set)} train, {len(val_set)} validation.")

if __name__ == "__main__":
    transfer_images()
    print("\nDataset split and transfer complete.")