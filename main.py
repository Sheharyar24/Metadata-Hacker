from importlib.metadata import metadata

import PIL.Image
import PIL.ExifTags
import piexif
import os
import time
import sys
from colorama import init, Fore, Style

BANNER = """

███╗   ███╗███████╗████████╗ █████╗ ██████╗  █████╗ ████████╗ █████╗ 
████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
██╔████╔██║█████╗     ██║   ███████║██║  ██║███████║   ██║   ███████║
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║  ██║██╔══██║   ██║   ██╔══██║
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║██████╔╝██║  ██║   ██║   ██║  ██║
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝

"""

class MetadataHacker:
  def __init__(self):
    # Define tags for the user to edit
    self.safe_tags = {
      '1': ('Artist', '0th', 315),
      '2': ('Software', '0th', 305),
      '3': ('Copyright', '0th', 33432),
      '4': ('ImageDescription', '0th', 270)
    }
    
  def print_banner(self):
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + BANNER)
    print(Fore.GREEN + "[+] SYSTEM BOOT... SECURE CONNECTION ESTABLISHED.\n")

  def extract_metadata(self, image_path):
    try:
      img = PIL.Image.open(image_path)
      exif = {PIL.ExifTags.TAGS[key]: value for key, value in img.getexif().items() if key in PIL.ExifTags.TAGS}
      return exif
    except Exception as e:
      print(Fore.RED + f"[-] ERROR EXTRACTING METADATA: {e}")
      return None
    
  def remove_metadata(self, image_path):
    try:
      img = PIL.Image.open(image_path)
      data = img.get_flattened_data()
      img_without_exif = PIL.Image.new(img.mode, img.size)
      img_without_exif.putdata(data)
      new_path = os.path.splitext(image_path)[0] + "_no_metadata" + os.path.splitext(image_path)[1]
      img_without_exif.save(new_path)
      print(Fore.LIGHTGREEN_EX + f"[+] METADATA PURGED. FILE SAVED: {new_path}")
    except Exception as e:
      print(Fore.RED + f"[-] ERROR REMOVING METADATA: {e}")

  def modify_metadata(self, image_path):
    try:
      exif_dict = piexif.load(image_path)
      modifications_made = False
      
      while True:
        print(Fore.GREEN + "\n[!] SELECT TARGET TAG TO OVERWRITE:")
        for key, (name, _, _) in self.safe_tags.items():
          print(Fore.LIGHTGREEN_EX + f"    [{key}] {name}")
        print(Fore.LIGHTGREEN_EX + "    [5] SAVE & EXIT")
        print(Fore.LIGHTGREEN_EX + "    [6] CANCEL (DISCARD ALL CHANGES)")
              
        choice = input(Fore.GREEN + "[?] >> ").strip()
              
        if choice in self.safe_tags:
          tag_name, ifd_name, tag_id = self.safe_tags[choice]
                  
          print(Fore.GREEN + f"\n[?] ENTER NEW STRING FOR '{tag_name}': ")
          new_value = input(Fore.LIGHTGREEN_EX + ">> ").strip()
                  
          if new_value:
            # Inject the new value
            exif_dict[ifd_name][tag_id] = new_value.encode('utf-8')
            modifications_made = True
            print(Fore.LIGHTGREEN_EX + f"[+] '{tag_name}' UPDATED.")
          else:
            print(Fore.YELLOW + "[-] INPUT EMPTY. NO CHANGE FOR THIS TAG.")
        elif choice == '5':
          if modifications_made:
            # Save the new file
            new_path = os.path.splitext(image_path)[0] + "_modified" + os.path.splitext(image_path)[1]
            exif_bytes = piexif.dump(exif_dict)
            img = PIL.Image.open(image_path)
            img.save(new_path, exif=exif_bytes)
            print(Fore.LIGHTGREEN_EX + f"\n[+] METADATA INJECTED. NEW FILE SAVED: {new_path}")
          else:
            print(Fore.YELLOW + "[-] NO CHANGES MADE.")
          break
        elif choice == '6':
          print(Fore.YELLOW + "[-] MODIFICATION CANCELLED. NO CHANGES SAVED.")
          break
        else:
          print(Fore.RED + "[-] INVALID SELECTION.")
                
    except Exception as e:
      print(Fore.RED + f"[-] ERROR MODIFYING METADATA: {e}")  

def main():
  hacker = MetadataHacker()
  hacker.print_banner()

  while True:
    print(Fore.GREEN + "\n[?] ENTER TARGET FILE PATH (OR 'EXIT'): ")
    image_path = input().strip()

    if image_path.lower() == "exit":
      print(Fore.YELLOW + "[+] TERMINATING SESSION...")
      break

    if not os.path.isfile(image_path):
      print(Fore.RED + "[-] ERROR: FILE NOT FOUND. VERIFY PATH.")
      continue

    metadata = hacker.extract_metadata(image_path)
    if metadata:
      print(Fore.LIGHTGREEN_EX + "\n[!] EXTRACTED DATA STREAM:")
      print(Fore.GREEN + "-" * 40)
      for key, value in metadata.items():
        print(Fore.LIGHTGREEN_EX + f" {key:<20} : {value}")
      print(Fore.GREEN + "-" * 40)

      print(Fore.GREEN + '\n[?] SELECT OPERATION:')
      print(Fore.LIGHTGREEN_EX + '    [1] GHOST FILE (REMOVE ALL METADATA)')
      print(Fore.LIGHTGREEN_EX + '    [2] MODIFY METADATA')
      print(Fore.LIGHTGREEN_EX + '    [3] ABORT')

      choice = input(Fore.GREEN + "[?] >> ").strip()

      if choice == '1':
        print(Fore.YELLOW + "\n[+] INITIATING PURGE SEQUENCE...")
        time.sleep(1) # Simulate processing time
        hacker.remove_metadata(image_path)

      elif choice == '2':
        hacker.modify_metadata(image_path)
      elif choice == '3':
        print(Fore.YELLOW + "\n[-] OPERATION CANCELLED.")
      else:
        print(Fore.RED + "[-] INVALID COMMAND.")
    else:
      time.sleep(1)
      print(Fore.YELLOW + "[-] NO METADATA DETECTED IN TARGET FILE.")


if __name__ == "__main__":
  main()