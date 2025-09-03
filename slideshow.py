import pygame
import os
import sys
import time
from moviepy.editor import VideoFileClip
import numpy as np

def load_media(folder):
    exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4', '.mov', '.avi')
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    files.sort()
    return [os.path.join(folder, f) for f in files]

def play_video(screen, clip, slide_duration, hold_duration=10):
    clock = pygame.time.Clock()
    start_time = time.time()

    # Get original clip dimensions and screen dimensions
    screen_w, screen_h = screen.get_size()
    clip_w, clip_h = clip.size
    
    # Calculate scaling to fit screen height while maintaining aspect ratio
    scale = screen_h / clip_h
    new_w = int(clip_w * scale)
    new_h = screen_h

    # If scaled video wider than screen, pan horizontally
    pan_needed = new_w > screen_w
    pan_x = 0
    pan_speed = 25  # pixels per second
    max_pan = max(0, new_w - screen_w)
    pan_finished = False
    pan_end_time = None

    for frame in clip.iter_frames(fps=30, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False

        # Convert frame (numpy array) to pygame surface
        frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
        
        # Scale the frame surface using pygame instead of moviepy
        scaled_surface = pygame.transform.smoothscale(frame_surface, (new_w, new_h))

        if pan_needed and pan_x < max_pan:
            pan_x += pan_speed * clock.get_time() / 1000.0
            pan_x = min(pan_x, max_pan)  # Ensure we don't overshoot
            
            # Check if panning just finished
            if pan_x >= max_pan and not pan_finished:
                pan_finished = True
                pan_end_time = time.time()
        elif not pan_needed:
            pan_x = 0
            if not pan_finished:
                pan_finished = True
                pan_end_time = time.time()

        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, (-int(pan_x), 0))
        pygame.display.flip()
        clock.tick(30)

        # Check if we should exit - either slide duration exceeded or hold time after panning finished
        current_time = time.time()
        if current_time - start_time > slide_duration + hold_duration:
            break

    return True

def main(folder, slide_duration=5, hold_duration=10):
    pygame.init()
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Image/Video Slideshow")

    media_files = load_media(folder)
    if not media_files:
        print("No media files found in folder:", folder)
        return

    clock = pygame.time.Clock()
    idx = 0
    running = True

    while running:
        path = media_files[idx]
        ext = os.path.splitext(path)[1].lower()

        if ext in ('.mp4', '.mov', '.avi'):
            try:
                clip = VideoFileClip(path)
            except Exception as e:
                print(f"Error loading video {path}: {e}")
                idx = (idx + 1) % len(media_files)
                continue

            running = play_video(screen, clip, slide_duration, hold_duration)
            clip.close()
        else:
            # Image handling (similar to before)
            img = pygame.image.load(path).convert()
            img_w, img_h = img.get_size()
            scale = screen_h / img_h
            new_w = int(img_w * scale)
            new_h = screen_h
            img = pygame.transform.smoothscale(img, (new_w, new_h))

            pan_needed = new_w > screen_w
            pan_x = 0
            pan_speed = 25
            max_pan = max(0, new_w - screen_w)
            pan_finished = False
            pan_end_time = None
            start_time = time.time()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                        break
                if not running:
                    break

                if pan_needed and pan_x < max_pan:
                    pan_x += pan_speed * clock.get_time() / 1000.0
                    pan_x = min(pan_x, max_pan)  # Ensure we don't overshoot
                    
                    # Check if panning just finished
                    if pan_x >= max_pan and not pan_finished:
                        pan_finished = True
                        pan_end_time = time.time()
                elif not pan_needed:
                    pan_x = 0
                    if not pan_finished:
                        pan_finished = True
                        pan_end_time = time.time()

                screen.fill((0, 0, 0))
                screen.blit(img, (-int(pan_x), 0))
                pygame.display.flip()
                clock.tick(60)

                # Check if we should exit - either slide duration exceeded or hold time after panning finished
                current_time = time.time()
                if current_time - start_time > slide_duration + hold_duration:
                    break

        idx = (idx + 1) % len(media_files)

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python slideshow.py <media_folder>")
    else:
        main(sys.argv[1])