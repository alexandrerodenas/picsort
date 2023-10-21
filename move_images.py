from shutil import move


def move_images(source_images, target_dir):
    for image in source_images:
        move(image, target_dir)