
from SpacExp.file_manager import FileManager

#FileManager("/content/my_files", "output.csv").run()

if __name__ == "__main__":
    manager = FileManager("C:\\Users\\snarski\\Desktop\\methodology_gelman", "output_gold_standard_data.csv")
    manager.run()
