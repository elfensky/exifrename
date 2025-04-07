from PIL import Image
import piexif
import os
from datetime import datetime

def update_exif_date(file_path):
    # Extract date and time from the filename
    base_name = os.path.basename(file_path)
    parts = base_name.split(' ')
    date_part = parts[2]
    time_part = parts[4][:8].replace('.', ':') #.replace('.jpeg', '')
    print(f"Date part: {date_part}")
    print(f"Time part: {time_part}")

    # Combine date and time
    date_time_str = f"{date_part} {time_part}"
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Convert to EXIF format
    exif_date = date_time_obj.strftime('%Y:%m:%d %H:%M:%S')

    # Load image and existing EXIF data
    img = Image.open(file_path)
    exif_dict = piexif.load(img.info.get('exif', b''))

    # Update EXIF date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = exif_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = exif_date

    # Save the updated EXIF data back to the image
    exif_bytes = piexif.dump(exif_dict)
    img.save(file_path, "jpeg", exif=exif_bytes)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.startswith("WhatsApp Image") and filename.endswith(".jpeg"):
            file_path = os.path.join(folder_path, filename)
            # print(f"Processing {filename}")
            update_exif_date(file_path)
            print(f"Updated EXIF date for {filename}")


def main():
    print("starting from exifrename!")
    folder_path = "/Users/andrei/Downloads/2024-06 Voltadag/test"
    process_folder(folder_path) 


if __name__ == "__main__":
    main()
