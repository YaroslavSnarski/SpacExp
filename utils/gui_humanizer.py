def humanize_file_size(size_in_bytes):
    """Преобразует размер файла в байтах в человекочитаемый формат."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = size_in_bytes
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"
