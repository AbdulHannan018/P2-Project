# importing modules
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tk_file
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from tkinter import filedialog, messagebox
import os
import cv2


class GalleryApp:
    def __init__(self):
        self.root = tk.Tk()
        
        self.root.geometry('1280x720')
        self.root.title('Gallery App')
        
        # Set background image
        background_image_path = 'C:\\Users\\user\\Desktop\\practice python\\background.jpg'
        background_image = Image.open(background_image_path)
        background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(self.root, image=background_photo)
        self.background_label.image = background_photo
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
                
        #GUI
        
        # Add a bold heading with a smiley
        heading_label = tk.Label(self.root, text="Welcome To Gallery 😊", font=("Helvetica", 22, "bold"))
        heading_label.pack()

       

        # Open the image using Pillow (PIL)
        image_path = 'C:\\Users\\user\\Desktop\\practice python\\menu.png'
        pil_image = Image.open(image_path)

        # Resize the image to your desired size
        resized_image = pil_image.resize((40, 40))

        # Convert the PIL image to a Tkinter PhotoImage
        self.img = ImageTk.PhotoImage(resized_image)

        # Create a label to display the image
        image_label = tk.Label(self.root, image=self.img)
        image_label.pack()
 
        

        
        
        
        self.media_list = []  # Stores both images and videos
        self.media_vars = []
        self.current_media_index = 0

      # creating menu button
        self.menu_btn = tk.Button(self.root, text='Menu Buttons', bd=3, font=('Bold', 15))
        self.menu_btn.pack(side=tk.TOP, anchor=tk.W, pady=20, padx=20)
        self.menu_btn.configure(bg="lightgreen")
        self.attach_logo(self.menu_btn, "C:\\Users\\user\\Desktop\\practice python\\menu.png")
        self.menu_btn.bind('<Button-1>', self.popup_menu)
        
        
        self.album_button = tk.Button(self.root, text="Album", bd=3, font=('Bold', 15), command=self.album_options)
        self.album_button.pack(side=tk.TOP, anchor=tk.W, pady=20, padx=20)
        
        self.album_button.configure(bg="lightblue")
        self.attach_logo(self.album_button, 'C:\\Users\\user\\Desktop\\practice python\\album.png')
       

        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.menu_bar.add_command(label='Open Folder', command=self.load_media)
        self.menu_bar.add_command(label='Open Media', command=self.add_media)
        self.menu_bar.add_command(label='Delete Media', command=self.delete_media)

        self.filter_btn = tk.Button(self.root, text='Filter Options', bd=3, font=('Bold', 15), command=self.show_filter_options)
        self.filter_btn.pack(side=tk.TOP, anchor=tk.W, pady=20, padx=20)
        self.filter_btn.configure(bg="lightcoral")
        self.attach_logo(self.filter_btn, "C:\\Users\\user\\Desktop\\practice python\\filter.png")
        self.media_display_lb = tk.Label(self.root)
        self.media_display_lb.pack(anchor=tk.CENTER)

        self.canvas = tk.Canvas(self.root, height=60, width=500)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.X)

        self.x_scroll_bar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.x_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.x_scroll_bar.config(command=self.canvas.xview)

        self.canvas.config(xscrollcommand=self.x_scroll_bar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.slider = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.slider, anchor=tk.NW)

        self.filter_options = {
            'blur': 0,
            'contrast': 0,
            'emboss': False,
            'contour': False,
            'flipx': False,
            'flipy': False,
            'sharpen': False,
            'rotation': 0
        }

        self.root.mainloop()

    def popup_menu(self, e):
        self.menu_bar.tk_popup(e.x_root, e.y_root)
     
 
        
    def attach_logo(self, button, logo_path):
        # Attach a logo image to the button
        pil_logo = Image.open(logo_path)
        resized_logo = pil_logo.resize((30, 30))
        logo_img = ImageTk.PhotoImage(resized_logo)
        button.config(image=logo_img, compound=tk.LEFT)
        button.logo_img = logo_img 


    def display_media(self, index):
        self.current_media_index = index
        media = self.media_list[index][1]

        if self.media_list[index][0] == 'image':
            filtered_media = self.apply_filters(media)
            self.media_display_lb.configure(image=filtered_media)
            self.media_display_lb.image = filtered_media
        elif self.media_list[index][0] == 'video':
            self.play_video(media)

    def apply_filters(self, image):
        filtered_image = image.copy()

        if self.filter_options['blur'] > 0:
            filtered_image = filtered_image.filter(ImageFilter.GaussianBlur(self.filter_options['blur']))

        if self.filter_options['contrast'] > 0:
            factor = 1 + self.filter_options['contrast'] / 10.0
            enhancer = ImageEnhance.Contrast(filtered_image)
            filtered_image = enhancer.enhance(factor)

        if self.filter_options['emboss']:
            filtered_image = filtered_image.filter(ImageFilter.EMBOSS)

        if self.filter_options['contour']:
            filtered_image = filtered_image.filter(ImageFilter.CONTOUR)

        if self.filter_options['sharpen']:
            filtered_image = filtered_image.filter(ImageFilter.SHARPEN)

        if self.filter_options['flipx']:
            filtered_image = filtered_image.transpose(Image.FLIP_LEFT_RIGHT)

        if self.filter_options['flipy']:
            filtered_image = filtered_image.transpose(Image.FLIP_TOP_BOTTOM)

        rotation_angle = self.filter_options['rotation']
        if rotation_angle != 0:
            filtered_image = filtered_image.rotate(rotation_angle)

        return ImageTk.PhotoImage(filtered_image)

    def play_video(self, video_path):
        try:
            cv2.namedWindow("Video Player", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Video Player", 640, 480)
            cap = cv2.VideoCapture(video_path)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow("Video Player", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        except ImportError:
            print("OpenCV library is not installed. Video playback is not supported.")


    def load_media(self):
        dir_path = tk_file.askdirectory()

        if dir_path:
            try:
                media_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

                if not media_files:
                    print("No media files found in the selected directory.")
                    return

                for r in range(len(media_files)):
                    media_path = os.path.join(dir_path, media_files[r])

                    if media_files[r].lower().endswith(('.png', '.jpg', '.jpeg')):
                        try:
                            image = Image.open(media_path).resize((480, 360), resample=Image.Resampling.LANCZOS)
                            thumbnail = ImageTk.PhotoImage(image.resize((50, 50), resample=Image.Resampling.LANCZOS))
                            self.media_list.append(['image', image, thumbnail])
                            self.media_vars.append(f'media_{r}')
                        except (IOError, OSError) as e:
                            print(f"Error loading image: {media_path}. {str(e)}")
                    elif media_files[r].lower().endswith(('.mp4', '.avi', '.mkv')):
                        self.media_list.append(['video', media_path])
                        self.media_vars.append(f'media_{r}')
                    else:
                        print(f"Unsupported file format: {media_path}")

                self.update_slider()

            except OSError as e:
                print(f"Error accessing directory: {dir_path}. {str(e)}")
        else:
            print("No directory selected.")

    def add_media(self):
        file_path = tk_file.askopenfilename(filetypes=[('Image Files', '.png; .jpg; .jpeg'), ('Video Files', '.mp4; .avi; .mkv')])
        if file_path:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                image = Image.open(file_path)
                self.media_list.append([
                    'image',
                    image.resize((480, 360), resample=Image.LANCZOS),
                    ImageTk.PhotoImage(image.resize((50, 50), resample=Image.LANCZOS))
                ])
                self.media_vars.append(f'media_{len(self.media_vars)}')
            elif file_path.lower().endswith(('.mp4', '.avi', '.mkv')):
                self.media_list.append(['video', file_path])

            self.update_slider()
            self.display_media(len(self.media_list) - 1)

    def delete_media(self):
        if len(self.media_list) > 0:
            del self.media_list[self.current_media_index]
            del self.media_vars[self.current_media_index]

            if len(self.media_list) == 0:
                self.current_media_index = 0
                self.media_display_lb.configure(image='')
                self.media_display_lb.image = None
            elif self.current_media_index == len(self.media_list):
                self.current_media_index -= 1

            self.update_slider()
            self.display_media(self.current_media_index)

    def update_slider(self):
        for widget in self.slider.winfo_children():
            widget.destroy()

        for n in range(len(self.media_vars)):
            if self.media_list[n][0] == 'image':
                button = tk.Button(self.slider, image=self.media_list[n][2], bd=0,
                                   command=lambda n=n: self.display_media(self.media_vars.index(f'media_{n}')))
            elif self.media_list[n][0] == 'video':
                button = tk.Button(self.slider, text='Play Video', bd=0,
                                   command=lambda n=n: self.play_video(self.media_list[n][1]))
            else:
                continue

            button.pack(side=tk.LEFT)


            button.pack(side=tk.LEFT)

    def show_filter_options(self):
        filter_window = tk.Toplevel(self.root)
        filter_window.title('Filter Options')

        blur_frame = tk.Frame(filter_window)
        blur_frame.pack(padx=10, pady=10)
        blur_slider = tk.Scale(blur_frame, from_=0, to=10, orient=tk.HORIZONTAL, label='Blur',
                               command=lambda value: self.update_filter_options('blur', int(value)))
        blur_slider.pack()

        contrast_frame = tk.Frame(filter_window)
        contrast_frame.pack(padx=10, pady=10)
        contrast_slider = tk.Scale(contrast_frame, from_=0, to=10, orient=tk.HORIZONTAL, label='Contrast',
                                   command=lambda value: self.update_filter_options('contrast', int(value)))
        contrast_slider.pack()

        emboss_var = tk.BooleanVar()
        emboss_checkbox = tk.Checkbutton(filter_window, text='Emboss', variable=emboss_var,
                                         command=lambda: self.update_filter_options('emboss', emboss_var.get()))
        emboss_checkbox.pack()

        contour_var = tk.BooleanVar()
        contour_checkbox = tk.Checkbutton(filter_window, text='Contour', variable=contour_var,
                                          command=lambda: self.update_filter_options('contour', contour_var.get()))
        contour_checkbox.pack()

        sharpen_var = tk.BooleanVar()
        sharpen_checkbox = tk.Checkbutton(filter_window, text='Sharpen', variable=sharpen_var,
                                        command=lambda: self.update_filter_options('sharpen', sharpen_var.get()))
        sharpen_checkbox.pack()

        flipx_var = tk.BooleanVar()
        flipx_checkbox = tk.Checkbutton(filter_window, text='Flip x', variable=flipx_var,
                                        command=lambda: self.update_filter_options('flipx', flipx_var.get()))
        flipx_checkbox.pack()

        flipy_var = tk.BooleanVar()
        flipy_checkbox = tk.Checkbutton(filter_window, text='Flip y', variable=flipy_var,
                                        command=lambda: self.update_filter_options('flipy', flipy_var.get()))
        flipy_checkbox.pack()

        rotation_frame = tk.Frame(filter_window)
        rotation_frame.pack(padx=10, pady=10)
        rotation_slider = tk.Scale(rotation_frame, from_=-180, to=180, orient=tk.HORIZONTAL, label='Rotation (degrees)',
                                command=lambda value: self.update_filter_options('rotation', int(value)))
        rotation_slider.pack()

        save_button = tk.Button(filter_window, text='Save Image', command=self.save_image)
        save_button.pack(pady=20)

    def update_filter_options(self, option, value):
        self.filter_options[option] = value
        self.display_media(self.current_media_index)

    def save_image(self):
        media = self.media_list[self.current_media_index]
        if media[0] == 'image':
            image = media[1]
            if image:
                file_path = tk_file.asksaveasfilename(defaultextension='.png',
                                                  filetypes=[('PNG', '.png')])
                if file_path:
                    image_path = os.path.join(file_path)
                    image.save(image_path)
        elif media[0] == 'video':
            print("Saving video is not supported.")

    def play_video(self, video_path):
        try:

            cv2.namedWindow("Video Player", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Video Player", 1280, 720)
            cap = cv2.VideoCapture(video_path)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow("Video Player", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        except ImportError:
            print("OpenCV library is not installed. Video playback is not supported.")

    def album_options(self):
        options_window = tk.Toplevel(self.root)
        options_window.title("Album Options")

        create_button = tk.Button(options_window, text="Create Album", command=self.create_album)
        create_button.pack()

        delete_button = tk.Button(options_window, text="Delete Album", command=self.delete_album)
        delete_button.pack()
        
        favorites_button = tk.Button(options_window, text="Show Favorites", command=self.show_favorites)
        favorites_button.pack()
        
    def show_favorites(self):
        if not self.favorites_list:
            messagebox.showinfo("Favorites", "No favorites selected.")
        else:
            messagebox.showinfo("Favorites", f"Favorites List: {', '.join(self.favorites_list)}")

    def create_album(self):
        folder_path = filedialog.askdirectory(title="Select Location to Create Album")
        if folder_path:
            album_name = tk.simpledialog.askstring("Create Album", "Enter Album Name:")
            if album_name:
                album_path = os.path.join(folder_path, album_name)
                try:
                    os.mkdir(album_path)
                    messagebox.showinfo("Success", "Album created successfully.")
                except FileExistsError:
                    messagebox.showerror("Error", "Album already exists.")
            else:
                messagebox.showerror("Error", "Please enter an album name.")

    def delete_album(self):
        folder_path = filedialog.askdirectory(title="Select Album to Delete")
        if folder_path:
            confirm = messagebox.askquestion("Delete Album", "Are you sure you want to delete this album?")
            if confirm == "yes":
                try:
                    os.rmdir(folder_path)
                    messagebox.showinfo("Success", "Album deleted successfully.")
                except FileNotFoundError:
                    messagebox.showerror("Error", "Album not found.")
                except OSError:
                    messagebox.showerror("Error", "Album is not empty.")               
GalleryApp()