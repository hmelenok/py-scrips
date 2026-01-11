import os
import cv2
import pandas as pd
from PIL import Image
from fuzzywuzzy import process
import numpy as np
import easyocr


def transliterate_to_ukrainian(text):
    # Hashmap for transliteration
    transliteration_map = {
        'A': 'А', 'B': 'Б', 'C': 'К', 'D': 'Д', 'E': 'Е', 'F': 'Ф', 'G': 'Г',
        'H': 'Х', 'I': 'І', 'J': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н',
        'O': 'О', 'P': 'П', 'Q': 'Ку', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У',
        'V': 'В', 'W': 'В', 'X': 'Кс', 'Y': 'И', 'Z': 'З',
        'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г',
        'h': 'х', 'i': 'і', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н',
        'o': 'о', 'p': 'п', 'q': 'ку', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
        'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'и', 'z': 'з'
    }

    # Transliterate the text
    transliterated_text = ''.join([transliteration_map.get(char, char) for char in text])

    return transliterated_text

def parse_text(text, known_locations, known_drones):
    def get_best_match(matches):
        if matches:
            return max(matches, key=lambda x: x[1])[0]
        return ""

    location_matches = [process.extractOne(word, known_locations, score_cutoff=60) for word in text.split()]
    drone_matches = [process.extractOne(word, known_drones, score_cutoff=90) for word in text.split()]

    best_location = get_best_match([match for match in location_matches if match])
    best_drone = get_best_match([match for match in drone_matches if match])

    result = []
    if best_location or best_drone:
        if best_drone:
            best_drone = transliterate_to_ukrainian(best_drone)
            best_drone = best_drone.capitalize()  
        result.append({'location': best_location, 'drone_type': best_drone})

    return result

def read_locations_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        locations = [line.strip() for line in file if line.strip()]
    return locations

def clahe_contrast(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(img)

def mask_dark_text(img, threshold_value=180):
    _, mask = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY_INV)
    return mask

def isolate_text_with_mask(img):
    mask = mask_dark_text(img)
    if len(img.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    isolated_img = cv2.bitwise_and(img, mask)
    return isolated_img

def color_filter(img, lower_bound, upper_bound):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_bound = np.array(lower_bound)
    upper_bound = np.array(upper_bound)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    filtered_img = cv2.bitwise_and(img, img, mask=mask)
    return filtered_img

def upscale_and_grayscale_image(image_path, save_processed=False):
    img = Image.open(image_path)
    img = img.resize((img.width * 2, img.height * 2), Image.BICUBIC)
    img = img.convert('L')
    
    img_np = np.array(img)
    
    if save_processed:
        processed_dir = '../../output/images/map-parts-processed'
        os.makedirs(processed_dir, exist_ok=True)
        save_path = os.path.join(processed_dir, os.path.basename(image_path))
        cv2.imwrite(save_path, img_np)
        print(f"Processed image saved to: {save_path}")

    return img_np

def extract_text(img):
    reader = easyocr.Reader(['uk', 'en'])
    try:
        result = reader.readtext(img)
        text = ' '.join([res[1] for res in result])
        print(f"OCR completed. Text found: {text[:30]}...")
        return text
    except Exception as e:
        print(f"Failed to extract text: {e}")
        return ""

def process_images(directory_path, known_locations, known_drones):
    results = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(directory_path, filename)
            print(f"Processing file: {full_path}")
            img = upscale_and_grayscale_image(full_path)
            text = extract_text(img)
            parsed_data = parse_text(text, known_locations, known_drones)
            results.extend(parsed_data)
            for entry in parsed_data:
                print(f"{entry['location']} - {entry['drone_type']}")
    df = pd.DataFrame(results)
    df.to_csv('../../output/csv/extracted_data.csv', index=False)
    print("All images processed. Data saved to '../../output/csv/extracted_data.csv'.")

    # Remove processed images
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(directory_path, filename)
            os.remove(full_path)
    print("Processed images removed.")

    return df

# Example usage
if __name__ == "__main__":
    directory_path = '../../data/raw-data/map-parts'
    known_locations = read_locations_from_file('../../data/reference-data/locations.txt')
    known_drones = ["ORLAN", "SUPERCAM", "ZALA", "Орлан", "зала","Зала", "Суперкам"]

    df = process_images(directory_path, known_locations, known_drones)
    print("Data extraction complete. Displaying all results:")
    for index, row in df.iterrows():
        print(f"{row['location']} - {row['drone_type']}")
