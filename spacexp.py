
from SpacExp.file_manager import FileManager

#FileManager("/content/my_files", "output.csv").run()

if __name__ == "__main__":
    manager = FileManager("D:\\YandexDisk\\gold_standard_dataset_snarski\\Files", "output_gold_standard_data.csv")
    manager.run()
